import csv
import os
def join_path(filename):
    current_dir = os.getcwd()
    parent_dir = os.path.dirname(current_dir)
    file_path = os.path.join(parent_dir, filename)
    return file_path

def scale_third_column(input_csv_path, output_csv_path, scalar):

    with open(join_path(input_csv_path), mode='r') as infile, open(join_path(output_csv_path), mode='w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        header = next(reader)
        writer.writerow(header)
        for row in reader:
            row[2] = str(float(row[2]) * scalar)
            writer.writerow(row)
    return(output_csv_path)
