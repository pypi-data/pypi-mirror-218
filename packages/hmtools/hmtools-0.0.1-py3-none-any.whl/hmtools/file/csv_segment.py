import pandas as pd



def segment_csv(fname, segment_list):
    data = pd.read_csv(fname)
    assert isinstance(segment_list, list)
    out_list = []
    for segment in segment_list:
        start = segment[0]
        end = segment[1]
        subdata = data[start:end]
        subdata = subdata.reset_index(drop=True)
        out_list.append(subdata)
    return out_list

