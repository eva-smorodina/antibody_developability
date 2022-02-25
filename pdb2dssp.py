import os

from Bio import BiopythonWarning
import warnings
with warnings.catch_warnings():
    warnings.simplefilter('ignore', BiopythonWarning)

from Bio.PDB import PDBParser
from Bio.PDB.DSSP import DSSP
from Bio.PDB.DSSP import ss_to_index

import functools
from collections import Counter
import pandas as pd
import numpy as np

from multiprocessing import Pool


cpus = 20

structure_path = '/storage/evagsm/nobackup/sensitivity_h/'
structures = os.listdir(structure_path)

def dssp_to_dict(structure, path = structure_path):

    try:
        print(structure[:-4])
        p = PDBParser(QUIET=True)
        model = p.get_structure("", path + structure)[0]
        dssp = DSSP(model, path + structure)

        data = np.array(list(dict(dssp).values()))

        init_c = Counter({
            'H': 0,
            'B': 0,
            'E': 0,
            'G': 0,
            'I': 0,
            'T': 0,
            'S': 0,
            '-': 0
        })

        get_c = Counter(data[..., 2])

        ss_c = dict(functools.reduce(lambda a, b: a.update(b) or a, [init_c, get_c], Counter()))

        values = np.mean(data[..., 3:].astype(np.float32), axis=0)

        ss_d = {}
        keys = ['relative_ASA', 'phi', 'psi', 'NH_O_1_relidx', 
                'NH_O_1_energy', 'O_NH_1_relidx', 'O_NH_1_energy',
                'NH_O_2_relidx', 'NH_O_2_energy', 'O_NH_2_relidx', 
                'O_NH_2_energy']

        ss_d.update(ss_c)

        for n, key in enumerate(keys):
            ss_d.update({key: values[n]})
        
        return ss_d

    except Exception:
        print('Error:', structure[:-4])
        
pool = Pool(processes = cpus)
results = pool.map(dssp_to_dict, structures)
pool.close()
pool.join()

print(len(results))

df = pd.DataFrame(results)
df.insert(0, 'ID', [s[:-4] for s in structures])
df.to_csv('./sens_dssp.csv', index=None)
