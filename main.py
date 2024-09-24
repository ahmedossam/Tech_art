import os
import json
import xml.etree.ElementTree as ET

# Working with the os module
file_path = "example.txt"

# Check if a file exists
if os.path.exists(file_path):
    print(f"The file {file_path} exists.")
else:
    print(f"The file {file_path} does not exist.")

# List all files in the directory
files_in_directory = os.listdir(os.getcwd())
print("Files in Current Directory:", files_in_directory)

# Reading and writing to a file
# Writing to a file
with open("example.txt", "w") as file:
    file.write("Hello, this is a sample text file.")

# Reading from a file
with open("example.txt", "r") as file:
    content = file.read()
    print("File Content:", content)

# Parsing JSON
json_data =
