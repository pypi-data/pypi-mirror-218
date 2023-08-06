import MySQLdb
from dbutils.pooled_db import PooledDB
import hashlib
from typing import Union


from queue import Queue
from threading import Thread, Event
from bounded_pool_executor import BoundedThreadPoolExecutor

import pandas as pd
import time


class Laser:

    instances = 0
    instances_limit = 5

    def __init__(self, db_config: dict, cache_size: int = 30, num_threads: int = 10, columns: str = '*'):
        if Laser.instances >= Laser.instances_limit:
            raise Exception('Too many instances of Laser')
        if db_config is None:
            raise Exception('db_config must be provided')
        Laser.instances += 1

        # Constants
        self.MAIN_TABLE_NAME = 'fs'
        self.CACHED_TABLE_NAME = 'cached'
        self.COLUMNS = columns

        # This is the configuration for the database
        self.db_config = db_config

        # This is the configuration for the cache
        self.cache_size = cache_size
        # This is the configuration for the number of threads for buffering
        self.num_threads = num_threads

        # pool
        self.pool = None
        # pool hash
        self.pool_hash = None

        # is buffering
        self.is_buffering = False

        # request queue (only works with buffering technique)
        self.request_queue = Queue(self.cache_size * 2)
        # Thread that fill the request queue
        self.fill_request_queue_thread = None
        # Signal to kill the fill_request_queue_thread
        self.kill_fill_request_queue_thread = Event()

        # response queue (only works with buffering technique)
        self.response_queue = Queue(self.cache_size)
        # Thread that fill the response queue
        self.fill_response_queue_thread = None
        # Signal to stop the fill_response_queue_thread
        self.kill_fill_response_queue_thread = Event()

        # adding the connection pool
        self.connection_pool = PooledDB(
            creator=MySQLdb,
            mincached=0,  # Minimum number of idle connections to maintain
            maxcached=num_threads,  # Maximum number of idle connections to maintain
            maxconnections=num_threads + 1,  # Maximum number of total connections,
            **self.db_config
        )

    def get_cached_queries(self):
        """
        Get the cached query
        :return: cached query
        """
        cnx = None
        cursor = None
        try:
            # Establish a connection to the database
            cnx = MySQLdb.connect(**self.db_config, )
            cursor = cnx.cursor(cursorclass=MySQLdb.cursors.DictCursor)
            # check if the query is already in the database
            cursor.execute(f"SELECT * FROM {self.CACHED_TABLE_NAME}")
            result = cursor.fetchall()
            if result is None:
                return None
            else:
                return result
        except Exception as e:
            print(e)
            return None
        finally:
            if cursor is not None:
                cursor.close()
            if cnx is not None:
                cnx.close()

    def create_pool(self, query: str = None, force_update: bool = False):
        """
        Create a pool of row_id's from the database
        :param query: The query to be executed and cached to create the pool
        :param force_update: ignore cache and force update
        :return:
            hit is True if the query was already in the database, False otherwise (even in force update is False)
            result: cached result if cannot create pool return None
        """
        hit = True
        cnx = None
        cursor = None
        result = None
        try:
            # pool hash is using MD5
            h = hashlib.md5(query.encode()).hexdigest()
            # Establish a connection to the database
            cnx = MySQLdb.connect(**self.db_config, connect_timeout=1200)
            cursor = cnx.cursor()
            query = query.strip()

            # check if the query is already in the database
            cursor.execute("SELECT * FROM cached WHERE hash = %s", (h,))
            result = cursor.fetchone()

            if result is None or force_update:
                hit = False
                cursor.execute("DROP TABLE IF EXISTS pool_{}".format(h))
                print("Dropped If table Exists pool_{}".format(h))
                # Create a table pool_{hash} with the query
                print("Start creating table pool_{}".format(h))
                cursor.execute("CREATE TABLE pool_{} AS {}".format(h, query))
                print("Commit pool_{}".format(h))
                cnx.commit()
                print("Created table pool_{}".format(h))
                if result is None:
                    # Create a row in the table cached
                    cursor.execute(f"INSERT INTO {self.CACHED_TABLE_NAME} (query, hash) VALUES (%s, %s)", (query, h,))
                    print(f"Inserted query {query} in {self.CACHED_TABLE_NAME}")
                else:
                    # Update the row in the table cached
                    cursor.execute(f"UPDATE {self.CACHED_TABLE_NAME} SET v = %s WHERE hash = %s", ((int(result[-1]) + 1), h,))
                    print(f"Updated query {query} in {self.CACHED_TABLE_NAME}")
                cnx.commit()
                cursor.execute(f"SELECT * FROM {self.CACHED_TABLE_NAME} WHERE hash = %s", (h,))
                result = cursor.fetchone()
        except Exception as e:
            print(e)
        finally:
            # If the query is already in the database, check if it is valid
            if cursor is not None:
                cursor.close()
            if cnx is not None:
                cnx.close()
            return {"hit": hit, "result": result}

    def get_pool(self, query: str = None, hashed: str = None, collate_fn: callable = None, num_parts: int = 1, part: int = 0):
        """
        Get the pool of row_id's from the database
        :param query: the query we want it's pool
        :param hashed: the hashed of the query we want it's pool
        :param collate_fn: how to reach extract data from pool in the database to only row_id's
        :return: pool of row_id's
        """
        # Check if the pool is already exists
        if self.pool is not None:
            raise Exception('Pool already exists')

        # check if the use give us query or hashed of it
        h = None
        if query is not None:
            h = hashlib.md5(query.encode()).hexdigest()
        elif hashed is not None:
            h = hashed
        if h is None:
            raise Exception('You must choose query or hashed of it to get pool')
        pass
        self.pool_hash = h

        cnx = None
        cursor = None
        try:
            # Establish a connection to the database
            cnx = MySQLdb.connect(**self.db_config)
            cursor = cnx.cursor()
            # check if the query is already in the database
            cursor.execute("SELECT * FROM cached WHERE hash = %s", (h,))
            result = cursor.fetchone()
            if result is None:
                raise Exception("Pool does not exist")
            # return SELECT * from pool_{hash}

            pool_q = "SELECT * FROM pool_{}".format(h)
            if num_parts > 1:
                cursor.execute("SELECT count(*) FROM pool_{}".format(h))
                count = cursor.fetchone()[0]
                part_size = count // num_parts
                pool_q += " LIMIT {} OFFSET {}".format(part_size, part * part_size)

            # s = time.perf_counter()
            cursor.execute(pool_q)
            pool = cursor.fetchall()
            # e = time.perf_counter()
            # print("Fetched pool in {} seconds".format(e - s))
            self.pool = pool
        except Exception as e:
            print(e)
        finally:
            if cursor is not None:
                cursor.close()
            if cnx is not None:
                cnx.close()
            if self.pool is None:
                return None
            if collate_fn is not None:
                self.pool = collate_fn(self.pool)
            else:
                self.pool = [t[0] for t in self.pool]
            return self.pool

    def start_buffering(self, sample_number: int, short_nap: int = 2, starting_batch_number: int = 0) -> None:
        """
        Start buffering technique
        :param sample_number: the number of row_id's in each chunk
        :param short_nap: the time to sleep at begging of starting the buffering to let buffer fill
        :param starting_batch_number: the starting batch number in response queue
        :return:
        """


        self.is_buffering = True
        self.fill_request_queue_thread = Thread(target=self.__fill_request_queue, args=(sample_number, starting_batch_number))
        self.fill_request_queue_thread.start()
        self.fill_response_queue_thread = Thread(target=self.__fill_response_queue)
        self.fill_response_queue_thread.start()
        # short nap to let buffer fill
        time.sleep(short_nap)

    def __fill_request_queue(self, sample_number: int, starting_batch_number: int = 0) -> None:
        """
        Fill the request queue
        split the pool into chunks and put them in the request queue
        :param sample_number: the number of row_id's in each chunk
        :param starting_batch_number: the starting batch number
        :return
        """
        # split the pool into chunks
        i = starting_batch_number
        max_i = len(self.pool) // sample_number
        while not self.kill_fill_request_queue_thread.is_set():
            index_list = self.pool[i * sample_number: (i + 1) * sample_number]
            self.request_queue.put(index_list)
            i = (i + 1) % max_i
        return

    def __fill_response_queue(self) -> None:
        """
        Fill the response queue
        Make the pool of threads with the threads number
        :return:
        """
        with BoundedThreadPoolExecutor(max_workers=self.num_threads) as executor:
            while not self.kill_fill_response_queue_thread.is_set():
                executor.submit(self.__put_response_to_queue)
            try:
                while not self.response_queue.empty():
                    self.response_queue.get()
            except Exception as e:
                print(e)
                pass
            executor.shutdown(wait=True)

    def __put_response_to_queue(self, retry: int = 0) -> None:
        """
        First get the index list from the request queue
        Then put the result in the response queue
        :return:
        """
        index_list = self.request_queue.get()
        df = self.get_batch_by_pointer_list(index_list)
        if df is not None:
            self.response_queue.put(df)
        else:
            # put the index list back to the request queue so ensure that we will get it again
            self.request_queue.put(index_list)
            # this part is for control retrying in case of error in getting batch by pointer list
            # It will raise an exception if the retry is more than 10
            if retry > 10:
                raise Exception("Error in getting batch by pointer list")
            print("Error in getting batch by pointer list")
            retry += 1
            print("Retrying in {} seconds".format(10 * retry))
            time.sleep(10 * retry)
            self.__put_response_to_queue(retry)

    def get_batch_by_pointer_list(self, index_list: list) -> Union[pd.DataFrame, None]:
        """
        Get batch by index list
        Then make a connection to the database
        Then execute the query
        Then convert the result to pandas dataframe
        :param index_list:
        :return:
        """
        cnx = None
        cursor = None
        result = None
        try:
            # cnx = MySQLdb.connect(**self.db_config)
            cnx = self.connection_pool.connection()
            cursor = cnx.cursor(cursorclass=MySQLdb.cursors.DictCursor)
            query = "SELECT {} FROM {} WHERE row_id IN ({})".format(self.COLUMNS, self.MAIN_TABLE_NAME, ','.join(map(str, index_list)))
            cursor.execute(query)
            result = cursor.fetchall()
        except Exception as e:
            result = None
            print(e)
        finally:
            if cursor is not None:
                cursor.close()
            if cnx is not None:
                cnx.close()
            if result is None:
                return None
            return pd.DataFrame(result)

    def get_batch(self):
        """
        Get batch from the response queue
        :return:
        """
        return self.response_queue.get()

    def stop_buffering(self) -> None:
        """
        Stop buffering technique
        :return:
        """
        self.kill_fill_request_queue_thread.set()
        self.kill_fill_response_queue_thread.set()

        if self.fill_request_queue_thread is not None:
            if not self.request_queue.empty():
                self.request_queue.get()
            self.fill_request_queue_thread.join(10)
            if self.fill_request_queue_thread.is_alive():
                self.fill_request_queue_thread.terminate()

        if self.fill_response_queue_thread is not None:
            if not self.response_queue.empty():
                self.response_queue.get()
            self.fill_response_queue_thread.join(10)
            if self.fill_response_queue_thread.is_alive():
                self.fill_response_queue_thread.terminate()

        self.kill_fill_request_queue_thread.clear()
        self.kill_fill_response_queue_thread.clear()

        self.is_buffering = False

    def __del__(self):
        if self.is_buffering:
            self.stop_buffering()
        Laser.instances -= 1
        self.connection_pool.close()
