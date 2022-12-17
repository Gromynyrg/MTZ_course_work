import pandas as pd
import numpy as np


def convert_ex(file_p):

    file_d = pd.read_excel(file_p)
    r = [len(file_d.iloc[0]), len(file_d.iloc[1])]
    r.extend([np.nan for i in range(len(file_d.columns)-2)])

    file_new = pd.DataFrame(r, index=list(file_d.columns)).transpose()
    file_new = pd.concat([file_new, file_d])

    new_file_name = file_p.split('/')[-1].split('.')[0]

    output_file_p = f"{new_file_name}.txt"

    file_new.to_csv(output_file_p, sep=" ", header=False, index=False, float_format="%.0f")

    return output_file_p
