import os
from Bio.PDB import PDBParser, MMCIFIO

structure_path = '/storage/evagsm/nobackup/sensitivity/'
output_path = '/storage/evagsm/nobackup/cif_sensitivity/'

structures = os.listdir(structure_path)

errors = []

for n, pdb in enumerate(structures):
    try:
        parser = PDBParser(QUIET=True)
        structure = parser.get_structure('', structure_path + pdb) 
        io = MMCIFIO()
        io.set_structure(structure)
        io.save("{}.cif".format(output_path + pdb))
        print('{} done'.format(n))
    except Exception:
        errors.append(pdb)
        print('{} failed'.format(n))
        
_ = [print(e) for e in errors]
