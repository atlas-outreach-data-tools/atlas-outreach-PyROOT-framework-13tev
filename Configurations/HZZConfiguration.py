Job = {
    "Batch"           : True,
    "Analysis"        : "HZZAnalysis",
    "Fraction"        : 1,
    "MaxEvents"       : 1234567890,
    "OutputDirectory" : "resultsHZZ/"
}

prefix = "https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/4lep/" # online
#prefix = "Input/4lep/" # local if you've downloaded the data

Processes = {

    # H -> ZZ -> 4lep processes
    "ZH125_ZZ4lep"          : prefix+"MC/mc_341947.ZH125_ZZ4lep.4lep.root",
    "WH125_ZZ4lep"          : prefix+"MC/mc_341964.WH125_ZZ4lep.4lep.root",
    "VBFH125_ZZ4lep"        : prefix+"MC/mc_344235.VBFH125_ZZ4lep.4lep.root",
    "ggH125_ZZ4lep"         : prefix+"MC/mc_345060.ggH125_ZZ4lep.4lep.root",

    # Z + jets processes
    "Zee"                   : prefix+"MC/mc_361106.Zee.4lep.root",
    "Zmumu"                 : prefix+"MC/mc_361107.Zmumu.4lep.root",

    # Diboson processes
    #"ZqqZll"                : prefix+"MC/mc_363356.ZqqZll.4lep.root",
    #"WqqZll"                : prefix+"MC/mc_363358.WqqZll.4lep.root",
    "llll"                  : prefix+"MC/mc_363490.llll.4lep.root",
    #"lllv"                  : prefix+"MC/mc_363491.lllv.4lep.root",
    #"llvv"                  : prefix+"MC/mc_363492.llvv.4lep.root",

    # top pair processes
    "ttbar_lep"             : prefix+"MC/mc_410000.ttbar_lep.4lep.root",

    # Data
    "data_A"                : prefix+"Data/data_A.4lep.root",
    "data_B"                : prefix+"Data/data_B.4lep.root",
    "data_C"                : prefix+"Data/data_C.4lep.root",
    "data_D"                : prefix+"Data/data_D.4lep.root",

}
