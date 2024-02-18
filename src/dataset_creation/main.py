import pandas as pd 
from video_download import Download
from utils import min2sec
from video_cutting import extraire_sequences

if __name__ == "__main__":
    df = pd.DataFrame(pd.read_excel("data/Dataset_preprocessing.xlsx"))
    print(df)
    for i in df.index:
        link = df["Lien Youtube"][i]
        path = Download(link)
        n_seq = df["N_Séquences"][i]
        seqArray = []
        for j in range(n_seq):
            seq = df["Seq" + j][i]
            secStart = min2sec(seq)
            secEnd = secStart + 10
            seqArray.append(secStart, secEnd)
        extraire_sequences("video_" + i, seqArray)