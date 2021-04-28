import pandas as pd

test_set = pd.read_csv("hazid_format_example.csv")
cols = test_set.columns
temp = []
temp2 = pd.DataFrame()
for i in cols:
    test_set.drop(index=0)
    for j in range(20):
        if i != "bowtie_id":
            temp.append(i + str(j))
        else:
            temp.append(1)
    temp2[i] = pd.Series(temp)
    temp = []
temp2.set_index("bowtie_id")
breakpoint()
temp2.to_csv("hazid_test_file.csv")