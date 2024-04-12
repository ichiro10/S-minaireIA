import pandas as pd
import numpy as np
import os
from matplotlib import pyplot as plt
def trim(colname):
    return colname.strip()

if __name__ == "__main__":
    typeVid = "confident"
    directory = "data/OpenFace/" + typeVid
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    fig, ax = plt.subplots(ncols=1,nrows=2)
    i = 1
    arr = []
    for file in files:
        file = "data/OpenFace/" + typeVid + "/" + file
        df = pd.read_csv(file)
        df = df.rename(columns=trim)
        df = df[df["confidence"] > 0.2]
        if len(df) > 0:
            unionSet = set(zip(round(df['gaze_angle_x'], 2), 
                            round(df['gaze_angle_y'], 2)))
            unionList = list(zip(round(df['gaze_angle_x'], 2), 
                            round(df['gaze_angle_y'], 2)))
            #print(len(unionSet))
            #print(len(unionSet), " ", file)
            arr.append(len(unionSet)/len(unionList))
            ax[0].boxplot(df['gaze_angle_x'], positions=[i], patch_artist=True)
            ax[1].boxplot(df['gaze_angle_y'], positions=[i], patch_artist=True)
            i += 1
    print(np.mean(arr))
    plt.show()