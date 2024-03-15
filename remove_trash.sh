#!/bin/bash

# Specify the path to your outputs directory
outputDir="outputs"

# Find and delete files that do not have the .mid extension
find "$outputDir" -type f ! -name "*.mid" -exec rm -f {} +

echo "Non-.mid files have been removed."
