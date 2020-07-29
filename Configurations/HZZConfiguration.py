Job = {
    "Batch"           : True,
    "Analysis"        : "HZZAnalysis",
    "Fraction"        : 1,
    "MaxEvents"       : 1234567890,
    "OutputDirectory" : "resultsHZZ/"
}

Processes = {

    # H -> ZZ -> 4lep processes
    "ZH125_ZZ4lep"          : "https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/4lep/MC/mc_341947.ZH125_ZZ4lep.4lep.root",
    "WH125_ZZ4lep"          : "https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/4lep/MC/mc_341964.WH125_ZZ4lep.4lep.root",
    "VBFH125_ZZ4lep"        : "https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/4lep/MC/mc_344235.VBFH125_ZZ4lep.4lep.root",
    "ggH125_ZZ4lep"         : "https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/4lep/MC/mc_345060.ggH125_ZZ4lep.4lep.root",

    # Z + jets processes
    "Zee"                   : "https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/4lep/MC/mc_361106.Zee.4lep.root",
    "Zmumu"                 : "https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/4lep/MC/mc_361107.Zmumu.4lep.root",

    # Diboson processes
    #"ZqqZll"                : "https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/4lep/MC/mc_363356.ZqqZll.4lep.root",
    #"WqqZll"                : "https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/4lep/MC/mc_363358.WqqZll.4lep.root",
    "llll"                  : "https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/4lep/MC/mc_363490.llll.4lep.root",
    #"lllv"                  : "https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/4lep/MC/mc_363491.lllv.4lep.root",
    #"llvv"                  : "https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/4lep/MC/mc_363492.llvv.4lep.root",

    # top pair processes
    "ttbar_lep"             : "https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/4lep/MC/mc_410000.ttbar_lep.4lep.root",

    # Data
    "data_A"                : "https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/4lep/Data/data_A.4lep.root",
    "data_B"                : "https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/4lep/Data/data_B.4lep.root",
    "data_C"                : "https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/4lep/Data/data_C.4lep.root",
    "data_D"                : "https://atlas-opendata.web.cern.ch/atlas-opendata/samples/2020/4lep/Data/data_D.4lep.root",

}
