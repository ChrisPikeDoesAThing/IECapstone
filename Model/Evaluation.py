import csv
import os
def join_path(filename):
    current_dir = os.getcwd()
    parent_dir = os.path.dirname(current_dir)
    file_path = os.path.join(parent_dir, filename)
    return file_path
def csv_to_dict_list(csv_file_path, has_headers=0):
    dict_list = []
    with open(csv_file_path, mode='r') as file:
        csv_reader = csv.reader(file)
        if has_headers:
            headers = next(csv_reader)
        else:
            headers = [str(i) for i in range(len(next(csv_reader)))]
            file.seek(0)
        for row in csv_reader:
            row_dict = {i: row[i] for i in range(len(headers))}
            dict_list.append(row_dict)
    return dict_list

def read_csv_to_list(file_path,has_headers=0):
    data = []
    with open(file_path, mode='r') as file:
        if has_headers:
            headers = next(file)
        csv_reader = csv.reader(file)
        for row in csv_reader:
            data.append(row)
    return data


def add_supply_amount_to_county_data(transparent_distribution_path, county_data_path, output_path):
    transparent_distribution = read_csv_to_list(transparent_distribution_path)
    county_data = read_csv_to_list(county_data_path,has_headers=1)

    for row in county_data:
        for dist in transparent_distribution:
            if dist[1] == row[0]:
                row[2] = round(float(row[2])) - round(float(dist[2]))
    with open(output_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['ID', 'County', 'Updated Demand'])
        for row in county_data:
            writer.writerow([row[0], row[1], row[2]])

# Example usage
def Evaluate(inputpath, outputpath):
    county_data_path = join_path('Model/CSVLib/CountyData.csv')
    add_supply_amount_to_county_data(join_path(inputpath), county_data_path, join_path(outputpath))
