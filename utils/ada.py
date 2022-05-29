"""вспомогательные общие функции
"""

from __future__ import print_function
import os
import glob
import random
import string
from pathlib import Path
from sys import getsizeof, stderr
from itertools import chain
from collections import deque
from os import listdir
from os.path import isfile, join

try:
    from reprlib import repr
except ImportError:
    pass


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█'):
    """
    Call in a loop to create terminal progress bar
    
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end='\r')
    # Print New Line on Complete
    if iteration == total:
        print()


def size_to_format_view(num, suffix='b'):
    for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Y', suffix)


def get_file_size(_fileobject):
    is_file_name = False
    if type(_fileobject) is str:
        is_file_name = True
        fileobject = open(_fileobject, 'rb')
    else:
        fileobject = _fileobject

    fileobject.seek(0, 2)  # move the cursor to the end of the file
    size = fileobject.tell()

    if is_file_name:
        fileobject.close()

    return size


def clear_directory(_dir):
    """
    Delete all files in the directory
    @params:
        _dir              - Required  : path to folder (Str)
    """

    files = glob.glob(_dir + '/*')

    for f in files:
        os.remove(f)

    return None


def rmfiles(_dir):
    """
    Delete all files in the given directory
    @params:
        _dir              - Required  : path to folder (Str)
    """

    directory = Path(_dir)
    for item in directory.iterdir():
        if item.is_dir():
            rmdir(item)
        else:
            item.unlink()


def rmdir(_dir):
    """
    Delete a directory and all files in the directory
    @params:
        _dir              - Required  : path to folder (Str)
    """

    directory = Path(_dir)
    for item in directory.iterdir():
        if item.is_dir():
            rmdir(item)
        else:
            item.unlink()
    directory.rmdir()


def randomString(_stringLength=8) -> string:
    """
    Get random string
    @params:
        _stringLength              - Optional  : string length (Int)
    """

    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(_stringLength))


def datetime_to_string(_date):
    """
    Convert date to string
    @params:
        _date              - Required  : date in date format (Date)
    """

    if _date == '':
        return ''
    else:
        item = str(_date)
        date = item.split()[0]
        h, m, s = [item.split()[1].split(':')[0],
                item.split()[1].split(':')[1],
                str(round(float(item.split()[1].split(':')[-1])))]
        return date + ' ' + h + ':' + m + ':' + s


def get_disk_free_space(_filename):
    """
    Return free space on the disk where the file located in bytes
    @params:
        _filename          - Required  : path to file (Str)
    """

    statvfs = os.statvfs(_filename)
    free_space = statvfs.f_frsize * statvfs.f_bavail

    return free_space

def get_files_list_recursively(_dir):
    """
    Return a list of all files in the directory recursively
    @params:
        _dir              - Required  : path to folder (Str)
    """

    path_from = _dir

    files_in_dir = [f for f in listdir(path_from) if isfile(join(path_from, f))]

    return files_in_dir

