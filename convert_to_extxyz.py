import numpy as np


pos_file    = "atom_pos_vecs_N1001.out"
force_file  = "force_N1001.out"
energy_file = "energy_N1001.out"
z_file      = "Z_N1001.out"

out_file = "dataset.extxyz"


# ----------------------------
# position parser
# ----------------------------
def read_positions(fname):

    data = []

    with open(fname) as f:

        for line in f:

            line = line.strip()

            if not line:
                continue

            parts = line.split()

            if len(parts) != 3:
                continue

            try:
                nums = list(map(float, parts))
                data.append(nums)
            except:
                continue

    return np.array(data)


# ----------------------------
# force parser (Atom x: fx fy fz)
# ----------------------------
def read_forces(fname):

    data = []

    with open(fname) as f:

        for line in f:

            line = line.strip()

            if not line.startswith("Atom"):
                continue

            parts = line.split()

            # Atom 1: fx fy fz
            if len(parts) < 5:
                continue

            try:
                fx = float(parts[2])
                fy = float(parts[3])
                fz = float(parts[4])

                data.append([fx, fy, fz])

            except:
                continue

    return np.array(data)


# ----------------------------
# Z
# ----------------------------
def read_Z(fname):

    Z = []

    with open(fname) as f:

        for line in f:

            line = line.strip()

            if not line:
                continue

            try:
                Z.append(int(line))
            except:
                continue

    return np.array(Z)


# ----------------------------
# Energy
# ----------------------------
def read_energy(fname):

    with open(fname) as f:

        txt = f.read()

    return float(txt.strip().split()[-1])


# ----------------------------
# Load
# ----------------------------
positions = read_positions(pos_file)
forces    = read_forces(force_file)
Z         = read_Z(z_file)
energy    = read_energy(energy_file)


# ----------------------------
# Check
# ----------------------------
N = len(Z)

print("Atoms    :", N)
print("Positions:", len(positions))
print("Forces   :", len(forces))
print("Z        :", len(Z))
print("Energy   :", energy)


assert positions.shape == (N, 3)
assert forces.shape == (N, 3)
assert len(Z) == N


# ----------------------------
# Write extxyz
# ----------------------------
with open(out_file, "w") as f:

    f.write(f"{N}\n")

    f.write(
        f'Properties=Z:I:1:pos:R:3:force:R:3 '
        f'energy={energy}\n'
    )


    for i in range(N):

        x, y, zpos = positions[i]
        fx, fy, fz = forces[i]
        z = Z[i]

        f.write(
            f"{z:3d} "
            f"{x:15.8f} {y:15.8f} {zpos:15.8f} "
            f"{fx:15.8f} {fy:15.8f} {fz:15.8f}\n"
        )


print("\n✅ dataset.extxyz 생성 완료")
