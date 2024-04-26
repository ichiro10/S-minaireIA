# Fichier utilisé pour faire l'analyse des résultats obtenu après avoir extrait
# les caractéristiques du visage
import pandas as pd
from matplotlib import pyplot as plt
def trim(colname):
    return colname.strip()

def count_outliers(column):
    q1 = column.quantile(0.25)
    q3 = column.quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    outliers = (column < lower_bound) | (column > upper_bound)
    return outliers.sum()

df1 = pd.read_csv("data/OpenFace/neurotic/sequence_video_0_2.csv")
df1 = df1.rename(columns=trim)
df2 = pd.read_csv("data/OpenFace/neurotic/sequence_video_5_13.csv")
df2 = df2.rename(columns=trim)
df3 = pd.read_csv("data/OpenFace/neurotic/sequence_video_17_10.csv")
df3 = df3.rename(columns=trim)
print(f"Diff max-min df1 : {df1[['gaze_angle_x', 'gaze_angle_y']].max()}")
print(f"Diff max-min df2 : {df2[['gaze_angle_x', 'gaze_angle_y']].max()}")
print(f"Diff max-min df2 : {df3[['gaze_angle_x', 'gaze_angle_y']].max()}")
print(f"Nb outliers x (df1): {count_outliers(df1['gaze_angle_x'])}")
print(f"Nb outliers y (df1): {count_outliers(df1['gaze_angle_y'])}")
print(f"Nb outliers x (df2): {count_outliers(df2['gaze_angle_x'])}")
print(f"Nb outliers y (df2): {count_outliers(df2['gaze_angle_y'])}")
print(f"Nb outliers x (df3): {count_outliers(df3['gaze_angle_x'])}")
print(f"Nb outliers y (df3): {count_outliers(df3['gaze_angle_y'])}")
fig, ax = plt.subplots(ncols=1,nrows=2)
ax[0].boxplot(df1['gaze_angle_x'], positions=[1], patch_artist=True)
ax[0].boxplot(df2['gaze_angle_x'], positions=[2], patch_artist=True)
ax[0].boxplot(df3['gaze_angle_x'], positions=[3], patch_artist=True)
ax[1].boxplot(df1['gaze_angle_y'], positions=[1], patch_artist=True)
ax[1].boxplot(df2['gaze_angle_y'], positions=[2], patch_artist=True)
ax[1].boxplot(df3['gaze_angle_y'], positions=[3], patch_artist=True)
plt.show()
