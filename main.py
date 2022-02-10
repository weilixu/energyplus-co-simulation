# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from util.eplus_model_interface import EplusModelIndexedList
import os
import multiprocessing as mp
FILE_DIR = os.path.dirname(__file__)
from pathlib import Path

def run(eplus_wea: str, eplus_file: str):
    """run energyplus"""
    path = Path(eplus_file)
    parent_dir = path.parent.absolute()
    os.chdir(parent_dir)

    os.system("energyplus -w %s -r %s" % (eplus_wea, eplus_file))

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    wea_dir = os.path.join(FILE_DIR, "eplus_files/weather/chicago_tmy3.epw")
    models = [os.path.join(FILE_DIR, "eplus_files/bldg1/PythonPluginCustomSchedule1.idf"),
              os.path.join(FILE_DIR, "eplus_files/bldg2/PythonPluginCustomSchedule2.idf"),
              os.path.join(FILE_DIR, "eplus_files/bldg3/PythonPluginCustomSchedule3.idf")]

    # Setup a list of processes that we want to run
    processes = [mp.Process(target=run, args=(wea_dir, x)) for x in models]

    # Run processes
    for p in processes:
        p.start()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
