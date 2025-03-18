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

def find_differences_in_demand(inputpath1, inputpath2, output_path):
    input1 = csv_to_dict_list(inputpath1, has_headers=0)
    input2 = csv_to_dict_list(inputpath2, has_headers=0)
    
    demand_diff = []
    
    for t_row in input1:
        for nt_row in input2:
            if t_row[0] == nt_row[0]:
                diff = float(t_row[2]) - float(nt_row[2])
                demand_diff.append([t_row[0], t_row[1], diff])
                break
    
    with open(output_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['ID', 'County', 'Demand Difference'])
        for row in demand_diff:
            writer.writerow(row)

def find_demand_fill(inputpath1, inputpath2, output_path):
    input1 = csv_to_dict_list(inputpath1, has_headers=0)
    input2 = csv_to_dict_list(inputpath2, has_headers=0)
    
    demand_diff = []
    
    for t_row in input1:
        for nt_row in input2:
            if t_row[0] == nt_row[0]:
                diff = round((-1*(float(nt_row[2]))+float(t_row[2])) / float(t_row[2]), 3)
                demand_diff.append([t_row[0], t_row[1], diff])
                break
    
    with open(output_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['ID', 'County', 'Demand Difference'])
        for row in demand_diff:
            writer.writerow(row)

# Example usage
def find_difference_and_ratio(file1path, file2path, outputpath1, outputpath2):
    countydatapath = join_path(file1path)
    datapath = join_path(file2path)

   #
   #  find_differences_in_demand(countydatapath, datapath, join_path(outputpath1))
    find_demand_fill(countydatapath, datapath, join_path(outputpath2))
