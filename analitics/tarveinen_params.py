# %% GET LIBRARIES
import os
import matplotlib
import matplotlib.pyplot as plt
import re
import numpy as np

from alg_tarvainen import find_art_tarvainen

# %%
path = "E:/Mgr_new_data/prepared_data/"
exam_ids = [1, 2, 3, 4, 5]
for addition in range(int(110/5)):
    prefixes = [f"{id+addition*5}_" for id in exam_ids]

    # Convert exam IDs to strings and create a list of subfolder names
    subfolders_beggining = [f"{id}_" for id in exam_ids]
    files_in_subfolder = [file for file in os.listdir(path) if any(file.startswith(prefix) for prefix in prefixes)]

    # Get a list of all files in the specified path
    all_files = []

    # Loop through subfolders and get files with the specified suffix
    for subfolder in files_in_subfolder:
        subfolder_path = os.path.join(path, subfolder)
        files_in_subsubfolder = [file for file in os.listdir(subfolder_path) if file.endswith('yoyo.txt')]
        all_files.extend([os.path.join(subfolder, file) for file in files_in_subsubfolder])

    # Create a subplot
    fig, axs = plt.subplots(len(all_files), 1, figsize=(10, 5 * len(all_files)))

    # Plot the data from each file
    for i, file_path in enumerate(all_files):
        intervals = []
        
        with open(f"{path}/{file_path}", 'r') as file:
            for line in file:
                # Extract numerical data after 'Time' and 'Beat-to-beat intervals' headers, skipping the date
                line = line.strip()
                if line.isdigit():
                    intervals.append(int(line))
        arts = find_art_tarvainen(intervals)
        # Plot the extracted data
        axs[i].plot(range(len(intervals)), intervals, label="original signal")
        axs[i].set_title(f"{prefixes[i][:-1]} - number of artifacts detected: {len(arts)}")
        axs[i].scatter(arts, [intervals[idx] for idx in arts], color='red', label='Artifacts')
        axs[i].legend()

    plt.savefig(f"C:/Users/mlado/Desktop/params_travainen/exams_{addition}.png")
    #plt.show()
# %%
#%matplotlib notebook 
exam_ids = [2, 3, 4, 5, 9, 13,
            23, 25, 26, 39, 42, 61]

prefixes = [f"{id}_" for id in exam_ids]
subfolders_beggining = [f"{id}_" for id in exam_ids]
files_in_subfolder = [file for file in os.listdir(path) if any(file.startswith(prefix) for prefix in prefixes)]

# Get a list of all files in the specified path
all_files = []

# Loop through subfolders and get files with the specified suffix
for subfolder in files_in_subfolder:
    subfolder_path = os.path.join(path, subfolder)
    files_in_subsubfolder = [file for file in os.listdir(subfolder_path) if file.endswith('yoyo.txt')]
    all_files.extend([os.path.join(subfolder, file) for file in files_in_subsubfolder])

for i, file_path in enumerate(all_files):
    intervals = []
    with open(f"{path}/{file_path}", 'r') as file:
                for line in file:
                    # Extract numerical data after 'Time' and 'Beat-to-beat intervals' headers, skipping the date
                    line = line.strip()
                    if line.isdigit():
                        intervals.append(int(line))

    arts = find_art_tarvainen(intervals)
    plt.plot(range(len(intervals)), intervals, label="original signal")
    plt.title(f"{prefixes[i][:-1]} - number of artifacts detected: {len(arts)}")
    plt.scatter(arts, [intervals[idx] for idx in arts], color='red', label='Artifacts')
    plt.legend()
    #plt.show()
# %%
