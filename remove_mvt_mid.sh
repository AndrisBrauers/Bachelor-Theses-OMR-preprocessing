#!/bin/bash

# Define the directory to search in, default to current directory if not specified
directory="outputs"

# Find and remove .mvt*.mid files
find "$directory" -type f -name '*.mid' -exec rm -v {} \;

echo "All .mvt*.mid files have been removed from $directory and its subdirectories."
