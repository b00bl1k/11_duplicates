import os
import sys
import hashlib


def get_files_list(path):
    file_paths = []
    for root_path, _, file_names in os.walk(path):
        for file_name in file_names:
            file_path = os.path.join(root_path, file_name)
            file_paths.append(file_path)
    return file_paths


def get_file_hash(path, fsize):
    file_name = os.path.split(path)[1]
    hash_source = "{}{}".format(file_name, fsize).encode('utf-8')
    return hashlib.sha224(hash_source).hexdigest()


def search_duplicates(path):
    files = get_files_list(path)
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
    except IndexError:
        sys.exit("Command line error")

    if not os.path.isdir(path):
        sys.exit("'{}' is not a directory".format(path))

    duplicates = search_duplicates(path)

    if not duplicates:
        sys.exit("Duplicate files is not found")

    for dup in duplicates:
        print_duplicate(dup)


if __name__ == "__main__":
    main()
