import os

data_folder = r'C:\Users\prashant\Desktop\project 1\data'
files_to_keep_in_data = [
    'liverpool_clean.csv',
    'london_clean.csv',
    'liverpool_cost_living.db'
]

print("Checking /data/ for files to delete:")
for fname in os.listdir(data_folder):
    fpath = os.path.join(data_folder, fname)
    if os.path.isfile(fpath):
        if fname not in files_to_keep_in_data:
            print(f"Will DELETE: {fname}")
            os.remove(fpath)
        else:
            print(f"Will KEEP:   {fname}")
print("Data folder duplicate cleanup complete!")

