#!/bin/bash

# Define the input and output directories
inputDir="inputs"
outputDir="outputs"

# Function to process each file
processFile() {
  local inputFile="$1"
  local outputFile="$2"
  echo "Processing $inputFile -> $outputFile"
  
  # Use the full Flatpak command to run Audiveris on the inputFile
  flatpak run org.audiveris.audiveris -batch -export -output "$(dirname "$outputFile")" "$inputFile"
  
  # Note: No need to manually rename the output file if Audiveris automatically saves it with an .mxl extension
}

# Function to traverse the directories recursively
traverse() {
  local currentDir="$1"
  
  for file in "$currentDir"/*; do
    if [ -d "$file" ]; then
      # Create a corresponding directory in outputs and traverse it
      local relPath="${file#$inputDir/}"
      mkdir -p "$outputDir/$relPath"
      traverse "$file"
    elif [[ $file == *.jpg ]]; then
      # Process files with .jpg extension
      local relPath="${file#$inputDir/}"
      local outputPath="$outputDir/${relPath%.jpg}.mxl"
      processFile "$file" "$outputPath"
    fi
  done
}

# Start processing by traversing the input directory
traverse "$inputDir"
