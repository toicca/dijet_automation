import ROOT
import numpy as np
import glob
import sys, argparse

ROOT.EnableImplicitMT(4)

RDataFrame = ROOT.RDataFrame
filepath = '/eos/cms/store/group/phys_jetmet/JMENanoRun3/v2p1/QCD_Pt-15to7000_TuneCP5_Flat_13p6TeV_pythia8/JMENanoRun3_v2p1_MC22_122/220915_171347/0000/'
inputFiles = ['/eos/cms/store/group/phys_jetmet/JMENanoRun3/v2p1/QCD_Pt-15to7000_TuneCP5_Flat_13p6TeV_pythia8/JMENanoRun3_v2p1_MC22_122/220915_171347/0000/tree_100.root']
outputFile = 'output'

    
def getOptions():
    parser = argparse.ArgumentParser(description="Run a simple dijet analysis on nanoAOD with RDataFrames")
    parser.add_argument("-f", "--filepath", type=str, default=filepath, help="Filepath to the files")
    parser.add_argument("-f_in", "--inputFiles", type=str, default=inputFiles, nargs='+', help="Input files separated by a comma")
    parser.add_argument("-o", "--outputFile", type=str, default=outputFile, help="Output file name")
    return parser.parse_args()
    
    
def strTakeN(colName, n):
    result = ""
    
    # Loop over the range of n and add the Take function to the result
    for i in range(n, 1, -1):
        result += f"{colName}.size() > {i-1} ? ROOT::VecOps::Take({colName}, {i}) : ("
        
    # Add the last Take function to the result
    result += f"ROOT::VecOps::Take({colName}, 1)" + ")"*(n-1)
    
    return result
    
def readData(filepath, nFiles=1, prefix=""):
    """
    Read nFiles from filepath and return a list
    """
    print(f'Reading {nFiles} files from', filepath)
    filelist = glob.glob(filepath + "*.root")
    
    # Check if nFiles is smaller than the number of files in the directory, return error otherwise
    if nFiles < len(filelist):
        filelist = filelist[:nFiles]
    else:
        print('nFiles is larger than the number of files in the directory')
        print('Reading all files')
    
    # Add prefix to filelist, required for spark
    filelist = [prefix + file for file in filelist]
    print(filelist)
    return filelist

def makeRDF(inputFiles, printCols=False):
    """Create a RDataFrame from a list of files

    Args:
        filelist (list): List of files to create the RDataFrame from

    Returns:
        RDataFrame: Output RDataFrame 
    """

    # Create a TChain from the filelist
    print("Creating TChain")
    chain = ROOT.TChain("Events")
    for f in inputFiles:
        chain.Add(f)
        
    # Create a RDataFrame
    # Check if spark context is available, if not don't use spark
    print("Creating RDataFrame")
    rdf = RDataFrame(chain)
        
    if printCols:
        # Print column names
        print("Columns in the RDataFrame:")
        for col in rdf.GetColumnNames():
            print(col)
    print("RDataFrame created")
    return rdf


if __name__ == "__main__":
    # Get command line arguments
    args = getOptions()
    # nFiles = args.nFiles
    filepath = args.filepath
    inputFiles = args.inputFiles# .split(",")
    
    # Columns to analyze and use
    cols = ["Jet_pt"]
    
    chain = ROOT.TChain("Events")
    for file in inputFiles:
        chain.Add(file)
    # chain.Add(inputFiles[0])    
    # Create RDataFrame
    rdf = RDataFrame(chain)
    # df = makeRDF(inputFiles)
    print("Filtering events")
    # Filter jets
    rdf = (rdf.Filter("Jet_pt.size() > 2", "Filter events with at least 3 jets")
            .Filter("(Jet_pt[0] + Jet_pt[1]) / 2.0 > Jet_pt[2]", "Choose dijet events")
        )

    # Print the number of events
    print("Number of events:")
    print(rdf.Count().GetValue())
    
    # Plot jet_pt
    h_jet_pt = rdf.Histo1D(("Jet_pt", "Jet_pt", 100, 0, 1000), "Jet_pt")
    
    # Write the histogram to a file
    print("Writing histogram to file")
    f = ROOT.TFile.Open(outputFile+".root", "RECREATE")
    h_jet_pt.Write()
    f.Close()

