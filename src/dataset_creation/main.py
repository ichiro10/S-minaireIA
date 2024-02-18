import pandas as pd 
from video_download import Download
from utils import min2sec
from video_cutting import extraire_sequences

if __name__ == "__main__":
    df = pd.DataFrame(pd.read_excel("data/Dataset_preprocessing.xlsx"))
    for i in df.index:
        if df["Trait"][i] == "NE":
            targetDir = "neurotic"
        else:
            targetDir = "confident"
        link = df["Lien Youtube"][i]
        path = Download(link, targetDir)
        n_seq = df["N_Séquences"][i]
        seqArray = []
        for j in range(int(n_seq)):
            seq = df["Seq" + str(j)][i]
            secStart = min2sec(seq)
            secEnd = secStart + 10
            seqArray.append((secStart, secEnd))
        extraire_sequences(path, "data/video/sequences/" + targetDir + "/", "video_" + str(i), seqArray)