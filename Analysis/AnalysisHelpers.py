import math

"""These helper functions implement three commonly used functionalities:
The Object Selection Helpers represent standard object selections that serve as a starting point for
self defined object selection strategies.
The selectAndSortContainer function can be used to do selecting and sorting in a one liner.
The StandardEventCuts function implements a standard cut used in essentially all analyses.
"""


# Object Selection Helpers
def isGoodPhoton(Photon):
    if not Photon.isTightID(): return False
    if not Photon.pt() > 25: return False
    if not Photon.isoetconerel20() < 0.15: return False
    if not Photon.isoptconerel30() < 0.15: return False
    return True;

def isGoodLepton(Lepton):
    if (abs(Lepton.pdgId()) == 11 and isGoodElectron(Lepton)): return True;
    if (abs(Lepton.pdgId()) == 13 and isGoodMuon(Lepton)): return True;
    return False;
    
def isGoodElectron(Lepton):
    if not Lepton.isTightID(): return False
    if not Lepton.pt() > 25: return False
    if not Lepton.isoetconerel20() < 0.15: return False
    if not Lepton.isoptconerel30() < 0.15: return False
    return True;
    
def isGoodMuon(Lepton):
    if not Lepton.isTightID(): return False
    if not Lepton.pt() > 25: return False
    if not Lepton.isoetconerel20() < 0.15: return False
    if not Lepton.isoptconerel30() < 0.15: return False
    return True;

def isGoodJet(jet):
    if jet.pt() < 25: return False
    if abs(jet.eta()) > 2.5: return False
    if jet.pt() < 60 and abs(jet.eta()) < 2.4 and jet.jvt() < 0.59: return False
    return True

def isGoodFatJet(FatJet):
    if FatJet.pt() < 250: return False
    if abs(FatJet.eta()) > 2: return False
    if FatJet.m() < 40: return False
    return True

def isGoodTau(Tau):
    if Tau.pt() < 25: return False
    if abs(Tau.eta()) > 2.5: return False
    if not Tau.isTightID(): return False
    return True

# Utility function
def selectAndSortContainer(container, selectingFunction, sortingFunction):
    selectedContainer = [particle for particle in container if selectingFunction(particle)]
    return sorted(selectedContainer, key=sortingFunction, reverse=True)

# Event Selection Helpers
def StandardEventCuts(eventinfo):
    if not (eventinfo.triggeredByElectron() or eventinfo.triggeredByMuon() or eventinfo.triggeredByPhoton() or eventinfo.triggeredByTau() or eventinfo.triggeredByDiTau()): return False
    return True;
    
    
# Variable Definitions:
def WTransverseMass(lepton, etmiss):
    return math.sqrt(2*lepton.pt()*etmiss.et()*(1-math.cos(lepton.tlv().DeltaPhi(etmiss.tlv()))));
