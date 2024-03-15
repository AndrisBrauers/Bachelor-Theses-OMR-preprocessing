 #!/bin/bash

# Define the input and output directories
inputDir="inputs"
outputDir="outputs"

# Function to process each file
processFile() {
  local inputFile="$1"
  local outputDir="$2"
  echo "Processing $inputFile -> $outputDir"

  # Run oemer on the inputFile, specify only the output directory
  # oemer determines the filename automatically
  oemer "$inputFile" -o "$outputDir"
}

# Function to traverse the directories recursively
traverse() {
  local currentDir="$1"
  
  for file in "$currentDir"/*; do
    if [ -d "$file" ]; then
      # If it's a directory, create a corresponding directory in outputs and traverse it
      local relPath="${file#$inputDir/}"
      mkdir -p "$outputDir/$relPath"
      traverse "$file"
    else
      # Assuming oemer processes image files (e.g., .jpg, .png, etc.), adjust the condition as necessary
      local fileExtension="${file##*.}"
      local relPath="${file#$inputDir/}"
      local outputPath="$outputDir/${relPath%.*}"
      outputPath="${outputPath%.*}" # Ensuring directory path is correct even if file has multiple dots
      local outputDirForFile=$(dirname "$outputPath")
      if [[ "$fileExtension" == "jpg" || "$fileExtension" == "png" ]]; then
        processFile "$file" "$outputDirForFile"
      fi
    fi
  done
}

# Start processing by traversing the input directory
traverse "$inputDir"
