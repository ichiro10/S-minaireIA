import pandas as pd
import os
import numpy as np
def trim(colname):
    return colname.strip()

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



if __name__ == "__main__":
    openFace_folder = os.path.join("data", "OpenFace")
    features_csv_path = os.path.join("src", "Training", "extracted_features.csv")

    features_file = pd.read_csv(features_csv_path)
    gaze_col = "irisDiffVals"
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