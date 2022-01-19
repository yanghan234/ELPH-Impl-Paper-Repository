#!/bin/sh
EXE=~/project2-yanghan/midway1/qe-6.1-kWest/bin/iotk

folder=./c.welph.save
# for iq in 00001 00002 00003 00006 00007 00008 00011 00028
# do
#   for imode in {00001..00006}
#   do
#     fname=${folder}/dnbare_r_iq${iq}_imode${imode}
#     echo "${fname}.xml --> ${fname}.txt"
#     ${EXE} convert ${fname}.xml ${fname}.txt
#     fname=${folder}/whxcdnbare_r_iq${iq}_imode${imode}
#     echo "${fname}.xml --> ${fname}.txt"
#     ${EXE} convert ${fname}.xml ${fname}.txt
#   done
# done

for iq in {00001..00064}
do
  for imode in {00001..00006}
  do
    fname=${folder}/whxcdnbare_r_xyz_iq${iq}_imode${imode}
    echo "${fname}.xml --> ${fname}.txt"
    ${EXE} convert ${fname}.xml ${fname}.txt
  done
done
