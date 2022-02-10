from .file_lock import FileLock
import os
import json
from json import JSONDecodeError

class ReadWrite:
    """ An object that allows many simultaneous read lock but one exclusive write lock"""

    def __init__(self, file_name):
        self.target_file = os.path.join(os.path.dirname(__file__), "%s.jsonl" % file_name)
        self._readers = 0

    def read(self, time_step):
        """Acquire a read lock, Block only if a thread has acquired the write lock"""
        with FileLock(self.target_file, lock_file_contents="Owning thread reader"):
            with open(self.target_file, 'r') as data_file:
                for line in data_file:
                    try:
                        data = json.loads(line.rstrip('\n|\r'))
                        if data["timestep"] == time_step:
                            return data
                    except JSONDecodeError:
                        pass
                data_file.close()
            return None

    def write(self, time_step, thread_name, value):
        """
        time_step = the time step of the record
        thread_name = model name
        value = dict contains the values
        """
        with FileLock(self.target_file, lock_file_contents="Owning thread %s"%(thread_name)):
            write_flag = False
            data_list = []
            with open(self.target_file, 'r') as data_file:
                for line in data_file:
                    try:
                        data = json.loads(line.rstrip('\n|\r'))
                        # found existing timestep
                        if data["timestep"] == time_step:
                            # Write over the thread_name
                            data[thread_name] = value
                            write_flag = True
                            # dump back the updated line of data
                            line = json.dumps(data)
                        data_list.append(line)
                    except JSONDecodeError:
                        pass
                    
            with open(self.target_file, 'w') as data_file:
                # it's a new timestep
                if not write_flag:
                    new_data = {"timestep": time_step, thread_name: value}
                    data_list.append(json.dumps(new_data))

                # write back
                for data_str in data_list:
                    data_file.write("%s\r" % data_str)
                data_file.flush()

