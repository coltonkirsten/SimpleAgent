# file_manager.py
# UNUSED??
import os

def read_file(file_path):
    """Reads the contents of a file."""
    with open(file_path, 'r') as file:
        return file.read()

def write_file(file_path, content):
    """Appends content to a file."""
    with open(file_path, 'a') as file:
        file.write(content)

def append_to_file(file_path, content):
    """Appends content to a file."""
    with open(file_path, 'a') as file:
        file.write(content)

def append_files(file_list, output_file):
    """Appends a list of files into one file."""
    with open(output_file, 'w') as outfile:
        for file_path in file_list:
            with open(file_path, 'r') as infile:
                outfile.write(infile.read())
                outfile.write("\n")  # Ensure separation between files

def delete_file(file_path):
    """Deletes a file."""
    if os.path.exists(file_path):
        os.remove(file_path)
    else:
        print(f"The file {file_path} does not exist")

# # Example usage:
# if __name__ == "__main__":
#     # Create files
#     create_file('example.txt', 'This is an example text file.')
#     create_file('example.py', 'print("This is an example Python file.")')

#     # Read files
#     print(read_file('example.txt'))
#     print(read_file('example.py'))

#     # Write to files
#     write_file('example.txt', 'Updated content for example text file.')
#     write_file('example.py', 'print("Updated content for example Python file.")')

#     # Append to files
#     append_to_file('example.txt', '\nAppending new content to the text file.')
#     append_to_file('example.py', '\nprint("Appending new content to the Python file.")')

#     # Append multiple files into one
#     append_files(['example.txt', 'example.py'], 'combined_output.txt')

#     # Delete files
#     delete_file('example.txt')
#     delete_file('example.py')
#     delete_file('combined_output.txt')