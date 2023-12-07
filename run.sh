#!/bin/bash

#Abort bash script on any error
set -e

#Print some basic debugging info
echo "whoami="`whoami`
echo "pwd="`pwd`
echo "hostname="`hostname`
echo "date="`date`

source /cvmfs/sft.cern.ch/lcg/views/LCG_104c/x86_64-el9-gcc13-opt/setup.sh
python3 /afs/cern.ch/user/n/ntoikka/dijet_automation/src/dijet_analysis.py --inputFiles /eos/cms/store/group/phys_jetmet/JMENanoRun3/v2p1/QCD_Pt-15to7000_TuneCP5_Flat_13p6TeV_pythia8/JMENanoRun3_v2p1_MC22_122/220915_171347/0000/tree_100.root --outputFile /afs/cern.ch/user/n/ntoikka/output/test_output