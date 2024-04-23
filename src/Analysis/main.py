import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import seaborn as sns

def count_outliers_iqr(data):
    Q1 = data.quantile(0.25)
    Q3 = data.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outliers = (data < lower_bound) | (data > upper_bound)
    return outliers.sum()

def boxplotFeature(df, feature_name, title, ax):
    dfNE = df[df["Target"] == "NE"]
    dfES = df[df["Target"] == "ES"]
    ax.boxplot(df[feature_name], positions=[1], patch_artist=True)
    ax.boxplot(dfNE[feature_name], positions=[2], patch_artist=True)
    ax.boxplot(dfES[feature_name], positions=[3], patch_artist=True)
    ax.set_xticklabels(['General boxplot', 'NE repartition', 'ES Repartition'])
    ax.set_title(title)
    ax.legend([f'Average: {np.mean(df[feature_name]):.2f}, Nb outliers: {count_outliers_iqr(df[feature_name])}', 
               f'Average: {np.mean(dfNE[feature_name]):.2f}, Nb outliers: {count_outliers_iqr(dfNE[feature_name])}', 
               f'Average: {np.mean(dfES[feature_name]):.2f}, Nb outliers: {count_outliers_iqr(dfES[feature_name])}'])
if __name__ == "__main__":
    df = pd.read_csv("src/Training/extracted_features.csv")
    fig, ax = plt.subplots(ncols=2,nrows=2)
    boxplotFeature(df, "gaze", "Boxplot for gaze direction (mean position)", 
                   ax[0, 0])
    boxplotFeature(df, "gazeDiffVals", "Boxplot for gaze direction (number of different values)", ax[0, 1])
    boxplotFeature(df, "irisMean", "Boxplot for iris position (mean position)", 
                   ax[1, 0])
    boxplotFeature(df, "irisDiffVals", "Boxplot for iris position (number of different values)", ax[1, 1])
    dfFeatures = df[["Head_nods", "Head_rotations",
                     "Magnitude", "Temporal_dynamic"]]
    covMatrix = dfFeatures.cov()
    plt.show()
    plt.figure(figsize=(10, 8))
    sns.heatmap(covMatrix, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Matrice de covariance')
    plt.show()