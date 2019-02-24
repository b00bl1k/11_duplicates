import os
import sys
import hashlib


def get_files_recursive(path):
    files = []
    for file_name in os.listdir(path):
        file_path = os.path.join(path, file_name)
        if os.path.isfile(file_path):
            files.append(file_path)
        elif os.path.isdir(file_path):
            files += get_files_recursive(file_path)
    return files


def get_file_hash(path, fsize):
    file_name = os.path.split(path)[1]
    hash_source = "{}{}".format(file_name, fsize).encode('utf-8')
    return hashlib.sha224(hash_source).hexdigest()


def search_duplicates(path):
    files = get_files_recursive(path)
    unique_dict = {}
    duplicate_list = []

    for file_path in files:
        file_size = os.path.getsize(path)
        file_hash = get_file_hash(file_path, file_size)

        if file_hash not in unique_dict.keys():
            unique_dict[file_hash] = [(file_path, file_size)]
        else:
            unique_dict[file_hash].append((file_path, file_size))
            if file_hash not in duplicate_list:
                duplicate_list.append(file_hash)

    return [unique_dict[file_hash] for file_hash in duplicate_list]


def print_duplicate(dup_files):
    print("Files with the same name and size {} bytes:".format(dup_files[0][1]))
    for dup_file in dup_files:
        print(" {}".format(dup_file[0]))


def main():
    try:
        path = sys.argv[1]
        for dup in search_duplicates(path):
            print_duplicate(dup)
    except IndexError:
        sys.exit("Command line error")


if __name__ == "__main__":
    main()
