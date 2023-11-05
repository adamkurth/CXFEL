from Bio.PDB import PDBParser, PDBIO
import os
import sys
# Dictionary of atomic weights (in Da (Dalton))) 
# 1 Dalton is approximately equal to the mass of one hydrogen atom, which is about 1.00784 atomic mass units (u).
# Script is close by not exact...
# Protein Weight (Da) = Protein Weight (kDa) * 1000
atomic_weights = {
    'H': 1.00784,
    'He': 4.0026,
    'Li': 6.94,
    'Be': 9.0122,
    'B': 10.81,
    'C': 12.011,
    'N': 14.007,
    'O': 15.999,
    'F': 18.998,
    'Ne': 20.180,
    'Na': 22.990,
    'Mg': 24.305,
    'Al': 26.982,
    'Si': 28.085,
    'P': 30.974,
    'S': 32.06,
    'Cl': 35.45,
    'K': 39.098,
    'Ar': 39.95,
    'Ca': 40.08,
    'Sc': 44.956,
    'Ti': 47.87,
    'V': 50.942,
    'Cr': 51.996,
    'Mn': 54.938,
    'Fe': 55.845,
    'Ni': 58.693,
    'Co': 58.933,
    'Cu': 63.546,
    'Zn': 65.38,
    'Ga': 69.723,
    'Ge': 72.630,
    'As': 74.922,
    'Se': 78.971,
    'Br': 79.904,
    'Kr': 83.798,
    'Rb': 85.468,
    'Sr': 87.62,
    'Y': 88.906,
    'Zr': 91.224,
    'Nb': 92.906,
    'Mo': 95.95,
    'Tc': 98,
    'Ru': 101.1,
    'Rh': 102.9,
    'Pd': 106.4,
    'Ag': 107.9,
    'Cd': 112.4,
    'In': 114.8,
    'Sn': 118.7,
    'Sb': 121.8,
    'I': 126.9,
    'Te': 127.6,
    'Xe': 131.3,
    'Cs': 132.9,
    'Ba': 137.3,
    'La': 138.9,
    'Ce': 140.1,
    'Pr': 140.9,
    'Nd': 144.2,
    'Pm': 145,
    'Sm': 150.4,
    'Eu': 152.0,
    'Gd': 157.3,
    'Tb': 158.9,
    'Dy': 162.5,
    'Ho': 164.9,
    'Er': 167.3,
    'Tm': 168.9,
    'Yb': 173.0,
    'Lu': 175.0,
    'Hf': 178.5,
    'Ta': 180.9,
    'W': 183.8,
    'Re': 186.2,
    'Os': 190.2,
    'Ir': 192.2,
    'Pt': 195.1,
    'Au': 197.0,
    'Hg': 200.6,
    'Tl': 204.4,
    'Pb': 207.2,
    'Bi': 208.9,
    'Th': 232.0,
    'Pa': 231.0,
    'U': 238.0,
    'Np': 237.0,
    'Pu': 244.0,
    'Am': 243.0,
    'Cm': 247.0,
    'Bk': 247.0,
    'Cf': 251.0,
    'Es': 252.0,
    'Fm': 257.0,
    'Md': 258.0,
    'No': 259.0,
    'Lr': 262.0,
}

def calculate_structure_weight(structure):
    weight = 0.0
    for model in structure:
        for chain in model:
            for residue in chain:
                for atom in residue:
                    element = atom.element
                    if element in atomic_weights:
                        weight += atomic_weights[element]
    return weight

def main(pdb_file):
    # Create a PDB parser
    parser = PDBParser(QUIET=True)

    # Load the PDB structure from the file
    structure = parser.get_structure("protein", pdb_file)

    # Add hydrogen atoms to the structure
    io = PDBIO()
    io.set_structure(structure)
    io.save(pdb_file)

    # Recreate the structure after adding hydrogen atoms
    structure = parser.get_structure("protein", pdb_file)

    # Calculate the structure weight
    weight = calculate_structure_weight(structure)

    print(f"Total structure weight: {weight/1000:.4f} kDa")

if __name__ == "__main__":
    pdb_files = []
    for root, dirs, files in os.walk(os.path.join(os.getcwd(), "formatted_data/pdb_files")):
        for file in files:
            if file.endswith(".pdb"):
                pdb_files.append(file)

    if len(sys.argv) < 2:
        print("Please provide a PDB file name as an argument.")
    else:
        pdb_file = sys.argv[1]
        if pdb_file not in pdb_files:
            print(f"{pdb_file} not found in directory.")
        else:
            pdb_path = os.path.join(os.getcwd(), "formatted_data/pdb_files", pdb_file)
            main(pdb_path)