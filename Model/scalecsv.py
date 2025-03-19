import csv
import os
def join_path(filename):
    current_dir = os.getcwd()
    parent_dir = os.path.dirname(current_dir)
    file_path = os.path.join(parent_dir, filename)
    return file_path

def scale_third_column(input_csv_path, output_csv_path, scalar):
    """
    Scale the third column of a CSV file by a scalar value and save to a new CSV file.
    
    :param input_csv_path: Path to the input CSV file
    :param output_csv_path: Path to the output CSV file
    :param scalar: Scalar value to multiply the third column by
    """
    with open(join_path(input_csv_path), mode='r') as infile, open(join_path(output_csv_path), mode='w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        header = next(reader)
        writer.writerow(header)
        for row in reader:
            row[2] = str(float(row[2]) * scalar)
            writer.writerow(row)
    return(output_csv_path)
