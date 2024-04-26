import pandas as pd
import os
import numpy as np
def trim(colname):
    return colname.strip()

# Extracts a feature from a sequence. We have used the tuples ("gaze_angle_x", 
# "gaze_angle_y") and ("eye_lmk_x_28", "eye_lmk_y_28") for the features. 
# The first tuple analyzes the gaze direction and the other the iris position.
# The method argument can be "meanSum": to do the mean of colX and colY and 
# sum the two, or meanX to only keep the mean of colX, or meanY for colY. If 
# it's anything else, it counts the proportion of different values in the cols.
def extractFeature(df: pd.DataFrame, colX = "gaze_angle_x", 
                   colY = "gaze_angle_y", method:str="gazeValueCount"):
    df = df[df["confidence"] > 0.2]
    if len(df) > 0:
        match method:
            case "meanSum":
                return np.mean(df[colX]) + np.mean(df[colY])
            case "meanX":
                return np.mean(df[colX])
            case "meanY":
                return np.mean(df[colY])
            case _:
                unionSet = set(zip(round(df[colX], 2), 
                                round(df[colY], 2)))
                unionList = list(zip(round(df[colX], 2), 
                                round(df[colY], 2)))
                
                return len(unionSet)/len(unionList)

    else:
        return 0


# Program used to add the a gaze to the extracted_features csv
# In this case, the column added is irisDiffVals which counts the
# number of different values observed for the iris position.
if __name__ == "__main__":
    openFace_folder = os.path.join("data", "OpenFace")
    features_csv_path = os.path.join("src", "Training", "extracted_features.csv")

    features_file = pd.read_csv(features_csv_path)
    gaze_col = "irisDiffVals" # Name of the feature in the csv
    if gaze_col not in features_file.columns:
        features_file[gaze_col] = None

    for index, data in features_file.iterrows():
        file_name = data["File"]
        target = "neurotic" if data["Target"] == "NE" else "confident"
        csvName = os.path.splitext(file_name)[0] + ".csv"
        currentCSV = os.path.join(openFace_folder, target, csvName)
        currentDF = pd.read_csv(currentCSV)
        currentDF = currentDF.rename(columns=trim)
        
        value = extractFeature(currentDF, colX="eye_lmk_x_28", colY="eye_lmk_y_28")
        features_file.at[index, gaze_col] = value
    features_file.to_csv(features_csv_path, index=False)