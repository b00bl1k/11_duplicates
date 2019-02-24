import os
import sys
import hashlib


def get_files_recursive(path):
    files = []
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isfile(item_path):
            files.append(item_path)
        elif os.path.isdir(item_path):
            files += get_files_recursive(item_path)
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


def print_duplicate(dup):
    print("Files with the same name and size {} bytes:".format(dup[0][1]))
    for item in dup:
        print(" {}".format(item[0]))


def main():
    try:
        path = sys.argv[1]
        for dup in search_duplicates(path):
            print_duplicate(dup)
    except IndexError:
        sys.exit("Command line error")


if __name__ == "__main__":
    main()
