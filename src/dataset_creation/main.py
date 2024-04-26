import pandas as pd 
from video_download import Download
from utils import min2sec
from video_cutting import extraire_sequences

# Program that downloads the videos in the "data/Dataset_preprocessing.xlsx" 
# file and creates the sequences.
if __name__ == "__main__":
    df = pd.DataFrame(pd.read_excel("data/Dataset_preprocessing.xlsx"))
    for i in df.index:
        if df["Trait"][i] == "NE":
            targetDir = "neurotic"
        else:
            targetDir = "confident"
        n_seq = df["N_Séquences"][i]
        if n_seq == 0:
            continue
        link = df["Lien Youtube"][i]
        path = Download(link, targetDir)
        seqArray = []
        for j in range(int(n_seq)):
            seq = df["Seq" + str(j)][i]
            secStart = min2sec(seq)
            secEnd = secStart + 10
            seqArray.append((secStart, secEnd))
        extraire_sequences(path, "data/video/sequences/" + targetDir + "/", "video_" + str(i), seqArray)
