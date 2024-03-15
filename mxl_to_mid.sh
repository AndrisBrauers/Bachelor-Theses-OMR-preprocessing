#!/bin/bash

# The directory containing the .mxl files
inputDir="outputs/nonprocessed/positionCorrection/perspective"


# Adjust this command according to how MuseScore is run on your system.
# For example, if you're using an AppImage, replace `musescore` with the path to the AppImage.
# If MuseScore is installed via Flatpak, you might need a command like `flatpak run --command=mscore org.musescore.MuseScore`.
musescoreCommand="/home/andris/.local/bin/MuseScore-4.2.1.240230938-x86_64.AppImage"

# Function to convert a single file
convertFile() {
  local inputFile="$1"
  # Use the same directory as the input file for the output
  local outputFile="${inputFile%.musicxml}.mid"
  echo "Converting $inputFile to $outputFile"
  
  # Run the conversion command
  $musescoreCommand -o "$outputFile" "$inputFile"
}

# Export .mxl to .mid for each file found in the input directory and its subdirectories
find "$inputDir" -type f -name "*.musicxml" | while read file; do
  # Convert the file
  convertFile "$file"
done

echo "Conversion completed."
