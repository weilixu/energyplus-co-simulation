from .file_lock import FileLock
import os
import json
from json import JSONDecodeError
import threading
import time

DEBUG_MODE = False

class ReadWrite:
    """ An object that allows many simultaneous read lock but one exclusive write lock"""

    def __init__(self, file_name):
        self.target_file = os.path.join(os.path.dirname(__file__), "%s.jsonl" % file_name)
        self.all_data_file = os.path.join(os.path.dirname(__file__), "%s.jsonl"% "all_data")
        self._readers = 0

    def read(self, time_step, resp={}):
        """Acquire a lock"""
        read_flag = False
        while not read_flag:
            with FileLock(self.target_file, lock_file_contents="Owning thread reader"):
                if DEBUG_MODE: print("Reader acquire a lock at timestep: %s" % time_step)
                if os.path.getsize(self.target_file) != 0:
                    with open(self.target_file, 'r') as data_file:
                        read_info = json.loads(data_file.readline().rstrip('\n|\r'))
                        if read_info["timestep"] == time_step:
                            for key in read_info.keys():
                                resp[key] = read_info[key]
                        data_file.close()
                # has data
                if len(resp.keys()) == 3:
                    # clean up the file
                    with open(self.target_file, 'w') as data_file:
                        pass

                    # write out the new data
                    with open(self.all_data_file, 'a') as all_data:
                        all_data.write("%s\n"%json.dumps(resp))
                        all_data.close()
                    if DEBUG_MODE: print("Reader reading...")
                    read_flag = True
            if DEBUG_MODE: print("Reader release a lock...")
            time.sleep(0.5)


    def write(self, time_step, thread_name, value):
        """
        time_step = the time step of the record
        thread_name = model name
        value = dict contains the values
        """
        write_flag = False

        while not write_flag:
            with FileLock(self.target_file, lock_file_contents="Owning thread %s"%(thread_name)):
                if DEBUG_MODE: print("writer: %s acquire a lock at timestep: %s"% (thread_name, time_step))
                write_info = {}
                if os.path.getsize(self.target_file) == 0:
                    # empty file, the process gain the leader status
                    write_info['timestep'] = time_step
                    write_info[thread_name] = value
                    write_flag = True
                else:
                    with open(self.target_file, 'r') as data_file:
                        write_info = json.loads(data_file.readline().rstrip('\n|\r'))
                        if write_info["timestep"] == time_step:
                            write_info[thread_name] = value
                            write_flag = True

                if write_flag:
                    # write:
                    if DEBUG_MODE: print("Writer %s writing at timestep: %s" %(thread_name, time_step))
                    with open(self.target_file, 'w') as data_file:
                        write_str = json.dumps(write_info)
                        # write back
                        data_file.write("%s" % write_str)

                    if DEBUG_MODE: print("writer: %s release a lock after write "% thread_name)
                else:
                    if DEBUG_MODE: print("writer: %s release a lock "% thread_name)
            time.sleep(0.1)

