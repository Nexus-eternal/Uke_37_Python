# Import block
import os
import re

# Variables block
my_name = "Ivanchenko"


# Define function to find specific word
def find_word_in_file(file_to_search, word_to_search):
    
    # Work with file block
    file_dir = os.path.dirname(os.path.realpath('__file__'))                    # Locate current directory
    file_name = os.path.join(file_dir, f'text_file//{file_to_search}')          # Locate file
    file_name = os.path.abspath(os.path.realpath(file_name))                    # Locate absolute path to file
    text_file = open(file_name, encoding="utf-16")                              # Open file
    text_file = text_file.read()                                                # Read file and save it


    word = re.compile(rf'\b{word_to_search}\b', re.IGNORECASE)                  # Configure word to look for
    matches = word.findall(text_file)                                           # Look for word
    
    print(word)
    print(matches)

#find_word_in_file("EleverVG2IT.txt", my_name)
find_word_in_file("EleverVG2IT.txt", my_name)