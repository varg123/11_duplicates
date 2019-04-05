from os import listdir, walk
from os.path import getsize, isfile, isdir, abspath, join, basename
import argparse
from collections import defaultdict

MAX_COUNT_FILES = 1


def parse_dir_arg():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d',
        '--dirpath',
        required=True,
        help='the scanned start_directory'
    )
    namespace = parser.parse_args()
    return namespace.dirpath


def scan_dir(start_directory):
    mydict = defaultdict(list)
    stuct_of_dir = list(walk(start_directory))
    for root, _, files in stuct_of_dir:
        for f in files:
            if isfile(join(root,f)):
                mydict[(f,getsize(join(root,f)))].append(join(root,f))
    return mydict


def print_duplicates_info(data_duplicates):
    tmpl_about_file = '\nИмя: {}\nРазмер: {}'
    for data_duplicate in data_duplicates:
        info_about_file = tmpl_about_file.format(
            data_duplicate[0][0],
            str(data_duplicate[0][1])
        )
        print(info_about_file)
        print('Расположение дубликатов:')
        for path in data_duplicate[1]:
            print(abspath(path))


def main():
    start_directory = parse_dir_arg()
    if not isdir(start_directory):
        exit('duplicates.py: error: directory not found')
    data_files = scan_dir(start_directory)
    print(data_files)
    data_duplicates = list(filter(
        lambda x: len(x[1]) > MAX_COUNT_FILES,
        data_files.items()
    ))
    data_duplicates.sort(key=lambda x: x[0][1], reverse=True)
    print_duplicates_info(data_duplicates)

if __name__ == '__main__':
    main()
    #scan_dir({},abspath('../'))
    
