#!/usr/bin/env python3
import numpy as np

def build_supercell(atoms,nx,ny,nz,random_disp=False):
    scatoms = []
    for i in range(nx):
        for j in range(ny):
            for k in range(nz):
                for atom in atoms:
                  if ( random_disp ):
                      disp = ( np.random.random((3,))*10.0-5.0 ) / 1000;
                  else:
                      disp = [0.0,0.0,0.0]
                  scatoms.append({"symbol":atom["symbol"],
                                  "coord": [(atom["coord"][0]+i)/nx+disp[0],
                                            (atom["coord"][1]+j)/ny+disp[1],
                                            (atom["coord"][2]+k)/nz+disp[2]]})
    return np.array(scatoms)

if __name__ == "__main__":
    ## diamond primitive cell
    atoms = [ {"symbol": "C", "coord": [0.00,0.00,0.00] },
              {"symbol": "C", "coord": [0.25,0.25,0.25] } ]

    ## diamond conventional unit cell
    ## atoms = [ {"symbol": "C", "coord": [0.00,0.00,0.00] },
    ##           {"symbol": "C", "coord": [0.25,0.25,0.25] },
    ##           {"symbol": "C", "coord": [0.50,0.50,0.00] },
    ##           {"symbol": "C", "coord": [0.75,0.75,0.25] },
    ##           {"symbol": "C", "coord": [0.50,0.00,0.50] },
    ##           {"symbol": "C", "coord": [0.75,0.25,0.75] },
    ##           {"symbol": "C", "coord": [0.00,0.50,0.50] },
    ##           {"symbol": "C", "coord": [0.25,0.75,0.75] } ]

    ## a pair of boron atoms in diamond 2x2x2 supercell based on primitive cell
    atoms = [ {"symbol": "B", "coord": [ -0.020374508,  -0.020374602,  -0.020374582] },
              {"symbol": "B", "coord": [  0.145376853,   0.145376924,   0.145376927] },
              {"symbol": "C", "coord": [ -0.006695046,  -0.006695018,   0.504763145] },
              {"symbol": "C", "coord": [  0.131691306,   0.131691281,   0.620227134] },
              {"symbol": "C", "coord": [ -0.006695068,   0.504763181,  -0.006695027] },
              {"symbol": "C", "coord": [  0.131691331,   0.620227098,   0.131691288] },
              {"symbol": "C", "coord": [  0.001685519,   0.498910707,   0.498910707] },
              {"symbol": "C", "coord": [  0.123329138,   0.626082464,   0.626082479] },
              {"symbol": "C", "coord": [  0.504763061,  -0.006694983,  -0.006694996] },
              {"symbol": "C", "coord": [  0.620227224,   0.131691248,   0.131691250] },
              {"symbol": "C", "coord": [  0.498910742,   0.001685516,   0.498910694] },
              {"symbol": "C", "coord": [  0.626082429,   0.123329150,   0.626082487] },
              {"symbol": "C", "coord": [  0.498910761,   0.498910692,   0.001685495] },
              {"symbol": "C", "coord": [  0.626082418,   0.626082490,   0.123329162] },
              {"symbol": "C", "coord": [  0.500167460,   0.500167484,   0.500167487] },
              {"symbol": "C", "coord": [  0.624846381,   0.624846368,   0.624846352] } ]


    # scatoms = build_supercell(atoms,2,2,2,True)
    # scatoms = build_supercell(atoms,1,1,1)
    scatoms = build_supercell(atoms,2,2,2)
    # scatoms = build_supercell(atoms,3,3,3)
    # scatoms = build_supercell(atoms,4,4,4)
    # scatoms = build_supercell(atoms,4,4,4,True)
    # scatoms = build_supercell(atoms,5,5,5)
    # scatoms = build_supercell(atoms,6,6,6)

    # print( scatoms )

    for atom in scatoms:
        print("%3s  %15.10f  %15.10f  %15.10f"%(atom["symbol"],atom["coord"][0],atom["coord"][1],atom["coord"][2]))

    # print( len( scatoms ) )

