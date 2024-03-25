# %% GET LIBRARIES
import os
import matplotlib
import matplotlib.pyplot as plt
import re
import numpy as np

from alg_tarvainen import find_art_tarvainen

# %%
path = "E:/Mgr_new_data/prepared_data/"
exam_ids = list(range(1, 111))
for addition in range(int(110/5)):
    prefixes = [f"{id}_" for id in exam_ids]

    # Convert exam IDs to strings and create a list of subfolder names
    files_in_subfolder = sorted([file for file in os.listdir(path) if any(file.startswith(prefix) for prefix in prefixes)],
                                key=lambda x: prefixes.index(x.split("_")[0] + "_"))
    # Get a list of all files in the specified path
    all_files = []

    # Loop through subfolders and get files with the specified suffix
    for subfolder in files_in_subfolder:
        subfolder_path = os.path.join(path, subfolder)
        files_in_subsubfolder = [file for file in os.listdir(subfolder_path) if file.endswith('yoyo.txt')]
        all_files.extend([os.path.join(subfolder, file) for file in files_in_subsubfolder])
    

# Plot the data from each file
for j in range(int(len(all_files)/5)):
    fig, axs = plt.subplots(5, 1, figsize=(10, 5 * 5))
    for i, file_path in enumerate(all_files[j*5:(j*5)+5]):
        intervals = []
        
        with open(os.path.join(path, file_path), 'r') as file:
            for line in file:
                # Extract numerical data after 'Time' and 'Beat-to-beat intervals' headers, skipping the date
                line = line.strip()
                if line.isdigit():
                    intervals.append(int(line))
        arts = find_art_tarvainen(intervals)  # Assuming you have defined this function
        # Plot the extracted data
        axs[i].plot(range(len(intervals)), intervals, label="original signal")
        axs[i].set_title(f"{prefixes[j*5+i][:-1]} - number of artifacts detected: {len(arts)}")
        axs[i].scatter(arts, [intervals[idx] for idx in arts], color='red', label='Artifacts')
        axs[i].legend()

    plt.savefig(f"C:/Users/mlado/Desktop/params_travainen/exams_{j}.png")
# %%
