import os
import sys


def get_files_list(path):
    file_paths = {}
    for root_path, _, file_names in os.walk(path):
        for file_name in file_names:
            file_path = os.path.join(root_path, file_name)
            file_size = os.path.getsize(file_path)
            file_paths.setdefault((file_name, file_size), []).append(file_path)
    return file_paths


def search_duplicates(path):
    files_list = get_files_list(path)
    return {info: paths for info, paths in files_list.items() if len(paths) > 1}


def print_duplicates(duplicates):
    for info, paths in duplicates.items():
        print("Duplicate file '{}' with size {}:".format(*info))
        print("\n".join([" {}".format(path) for path in paths]))

    if not duplicates:
        print("Duplicate files is not found")


def main():
    try:
        path = sys.argv[1]
    except IndexError:
        sys.exit("Command line error")

    if not os.path.isdir(path):
        sys.exit("'{}' is not a directory".format(path))

    duplicates = search_duplicates(path)
    print_duplicates(duplicates)


if __name__ == "__main__":
    main()
