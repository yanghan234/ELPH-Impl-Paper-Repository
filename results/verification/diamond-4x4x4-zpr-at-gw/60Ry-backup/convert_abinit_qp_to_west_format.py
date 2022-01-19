#!/bin/env python3
from shutil import copyfile
import os

fname = "./diamond_gw_ppm_o_DS3_GW"

def convert_file( fname ):
    nk = 0
    ns = 1
    with open(fname,"r") as f:
        line = f.readline()
        nk = int( line.split()[0] )
        ns = int( line.split()[1] )
        print("nk = %03d, ns = %03d"%(nk,ns))

        for ik in range(nk):
            line = f.readline()
            nbnd = int( f.readline() )
            print("xk(:,%05d) = %s"%(ik+1,line))

            fnames = []
            with open("ibz2bz_%05d.csv"%(ik+1),"r") as fmap:
                line = fmap.readline()
                line = fmap.readline()
                while line != "":
                    ikk = int(float(line.split(',')[1]))
                    dest ="o-eqp_K%05d.tab"%(ikk)
                    fnames.append(dest)
                    line = fmap.readline()

            newfname = fnames[0]
            out = open(newfname,"w")
            out.write("#           band          E0[eV]         EHF[eV]         Eqp[eV]      Eqp-E0[eV]      Sc_Eqp[eV]       Width[eV]       LinEqp[eV]\n")
            for ibn in range(nbnd):
                line = f.readline()
                out.write("%10d"%(ibn+1))
                out.write("%23.10e"%(float(line.split()[1])-float(line.split()[2]))) # E0, not important, won't be used later
                out.write("%23.10e"%(0.0))                    # EHF, not important, won't be used later
                out.write("%23.10e"%(float(line.split()[1]))) # Eqp
                out.write("%23.10e"%(float(line.split()[2]))) # Eqp-E0, not used later
                out.write("%23.10e"%(0.0))                    # Sc_Eqp, not used later
                out.write("%23.10e"%(0.0))                    # Width,  not used later
                out.write("%23.10e"%(0.0))                    # LinEqp, not used later
                out.write("\n")
            out.close()

            if ( len(fnames) == 1 ):
                continue
            else:
                for i in range(1,len(fnames)):
                    dest = fnames[i]
                    copyfile(newfname,dest)


if __name__ == "__main__":
    convert_file( fname )
