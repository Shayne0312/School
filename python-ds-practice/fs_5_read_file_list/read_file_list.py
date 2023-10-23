def read_file_list(filename):
    """Read file and print out each line separately with a "-" before it.

    For example, if we have a file, `dogs`, containing:
        Fido
        Whiskey
        Dr. Sniffle
    
    This should work:

    >>> read_file_list("dogs")
    - Fido
    - Whiskey 
    - Dr. Sniffle

    It will raise an error if the file cannot be found.
    """

    try:
        with open(filename) as f:
            for line in f:
                print("- " + line.rstrip()) 
    except FileNotFoundError:
        print(f"Error: could not find file {filename}")

read_file_list("fs_5_read_file_list\dogs")
read_file_list("fs_5_read_file_list\cats")