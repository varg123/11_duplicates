from os import listdir
from os.path import getsize, isfile, isdir, abspath
import argparse

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


def scran_dir(data_files, start_directory):
    all_names_in_dir = listdir(start_directory)
    for name in all_names_in_dir:
        name_full = start_directory+'\\'+name
        if isfile(name_full):
            file_size = getsize(name_full)
            if data_files.get((name, file_size)):
                data_files[(name, file_size)].append(name_full)
            else:
                data_files[(name, file_size)] = []
                data_files[(name, file_size)].append(name_full)
        if isdir(name_full):
            scran_dir(data_files, name_full)
    return data_files


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
    data_files = scran_dir({}, start_directory)
    data_duplicates = list(filter(
        lambda x: len(x[1]) > MAX_COUNT_FILES,
        data_files.items()
    ))
    data_duplicates.sort(key=lambda x: x[0][1], reverse=True)
    print_duplicates_info(data_duplicates)

if __name__ == '__main__':
    main()
