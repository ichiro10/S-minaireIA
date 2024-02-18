def min2sec(min : str):
    seqList = min.split(":")
    return seqList[0] * 60 + seqList[1]