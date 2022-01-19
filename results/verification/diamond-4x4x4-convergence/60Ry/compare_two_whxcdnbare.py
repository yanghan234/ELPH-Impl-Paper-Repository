#!/usr/bin/env python3
import click
import numpy as np

#@click.command()
#@click.option("--f1",help="Name of first  real-space PDEP cube file")
#@click.option("--f2",help="Name of second real-space PDEP cube file")
#@click.option("--with-plot",default=True,help="Plot the histogram of difference or not")
def compare_two_whxcdnbare(f1,f2):
    f = open(f1,"r")
    g = open(f2,"r")
    for i in range(11):
        f.readline()
        g.readline()

    diff = []
    count = 0
    line1 = f.readline()
    line2 = g.readline()
    while line1 != "" and line2 != "":
        try:
            norm1 = np.sqrt(float(line1.split(',')[0])**2.0 + float(line1.split(',')[1])**2.0)
            norm2 = np.sqrt(float(line2.split(',')[0])**2.0 + float(line2.split(',')[1])**2.0)
            diff.append(abs(norm1-norm2))
        except ValueError:
            pass
        line1 = f.readline()
        line2 = g.readline()

    diff_mean = np.mean(diff)
    diff_std  = np.std(diff)
    print("Average diff = %15.6e"%(diff_mean))
    print("Std dev diff = %15.6e"%(diff_std))

if __name__ == "__main__":
    folder1 = "./c.welph.save/"
    folder2 = "./c.welph.save.pdep200.backup/"
    for iq in range(1,64+1):
        for imode in range(1,7):
            fname1 = folder1+"whxcdnbare_r_xyz_iq%05d_imode%05d.txt"%(iq,imode)
            fname2 = folder2+"whxcdnbare_r_xyz_iq%05d_imode%05d.txt"%(iq,imode)
            print(fname1,fname2)
            compare_two_whxcdnbare(fname1,fname2)


