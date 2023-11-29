#!/bin/bash
source /cvmfs/sft.cern.ch/lcg/views/LCG_104a/x86_64-centos7-gcc12-opt/setup.sh
python3 src/dijet_analysis.py --inputFiles /eos/cms/store/group/phys_jetmet/JMENanoRun3/v2p1/QCD_Pt-15to7000_TuneCP5_Flat_13p6TeV_pythia8/JMENanoRun3_v2p1_MC22_122/220915_171347/0000/tree_100.root --outputFile /afs/cern.ch/user/n/ntoikka/output/test_output