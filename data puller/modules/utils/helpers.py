from os import path
from pathlib import Path
import __main__ as main


def makeFilePath(outputFileName):
    newFileName = "{}.csv".format(outputFileName)
    curr_path = path.dirname(path.abspath(main.__file__))
    abs_path = path.join(curr_path, '..', "CounterPicker_data")
    Path(abs_path).mkdir(parents=True, exist_ok=True)
    return path.join(abs_path, newFileName)


def printNewestOldest(df):
    min_date = df.date.min()
    max_date = df.date.max()
    print("older match: " + str(min_date)+"   newest match: "+str(max_date))
