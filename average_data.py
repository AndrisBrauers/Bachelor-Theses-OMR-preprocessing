def calculate_directory_averages(input_filepath, output_filepath):
    # Dictionary to hold directory sums and counts
    directory_sums = {}
    directory_counts = {}

    # Read the input file
    with open(input_filepath, 'r') as file:
        for line in file:
            # Split the line into path and value
            path, value = line.strip().split(': ')
            # Extract directory by removing the filename
            directory = '/'.join(path.split('/')[:-1])
            # Convert value to float
            value = float(value)
            # Update the directory sums and counts
            if directory in directory_sums:
                directory_sums[directory] += value
                directory_counts[directory] += 1
            else:
                directory_sums[directory] = value
                directory_counts[directory] = 1

    # Write the averages to the output file
    with open(output_filepath, 'w') as outfile:
        for directory in sorted(directory_sums.keys()):
            average = directory_sums[directory] / directory_counts[directory]
            outfile.write(f'{directory}: {average}\n')

# Define the input and output file paths
input_filepath = ['audiveris/comparison_results_binary.txt', 'audiveris/comparison_results_pitch.txt', 'omere/comparison_results_binary.txt', 'omere/comparison_results_pitch.txt']
output_filepath = ['audiveris/avg_comparison_results_binary.txt', 'audiveris/avg_comparison_results_pitch.txt', 'omere/avg_comparison_results_binary.txt', 'omere/avg_comparison_results_pitch.txt']

# Call the function
for i in range(0, len(input_filepath)):
    calculate_directory_averages(input_filepath[i], output_filepath[i])

