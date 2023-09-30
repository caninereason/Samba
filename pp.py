import os

def list_directories(path='.', depth=0):
    """
    List the names of directories in the specified path, including child directories.
    Default path is the current directory.
    Excludes directories beginning with a '.'.
    """
    directories = []  # Initialize an empty list to store the directory names

    with os.scandir(path) as entries:
        for entry in entries:
            if entry.is_dir() and not entry.name.startswith('.'):  # Check if the entry is a directory and does not start with a '.'
                if depth >= 1:  # Only add to list if depth is 2 or more
                    directories.append(entry.path)
                # Recursively add child directories, incrementing depth
                directories.extend(list_directories(entry.path, depth+1))  

    return directories

# Call the function and print the list of directories
directories = list_directories()
print(directories)
