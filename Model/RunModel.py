from CompareModel import Model
import pandas as pd
import os

def join_path(filename):
    current_dir = os.getcwd()
    parent_dir = os.path.dirname(current_dir)
    file_path = os.path.join(parent_dir, filename)
    return file_path

# Create an empty DataFrame with appropriate column names
results_df = pd.DataFrame(columns=['ratio', 'cost', 'transparentequity', 'cost', 'nontransparentequity'])

for i in range(5):
    scalar = 1/(i+1)
    results = Model(scalar)
    # Append the results to the DataFrame
    results_df.loc[i] = results

pd.to_csv(join_path('Model/CSVResults/Results.csv'))