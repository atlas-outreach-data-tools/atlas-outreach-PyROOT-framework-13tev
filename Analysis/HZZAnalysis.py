import ROOT
import itertools 
import math

from Analysis import Analysis
from Analysis import AnalysisHelpers
from Analysis import Constants

#======================================================================
        
class HZZAnalysis(Analysis.Analysis):
  """Analysis searching for the pair production of two Z bosons decaying to leptons."""
  def __init__(self, store):
      super(HZZAnalysis, self).__init__(store)

  
  def initialize(self):
      self.invMassZ1         =  self.addHistogram("invMassZ1",           ROOT.TH1D("invMassZ1",     "Invariant Mass of the Z boson 1;M_{Z1} [GeV]; Events", 30, 50,106))
      self.invMassZ2         =  self.addHistogram("invMassZ2",           ROOT.TH1D("invMassZ2",     "Invariant Mass of the Z boson 2;M_{Z2} [GeV]; Events", 30, 60,120))

      self.mass_four_lep_ext         =  self.addHistogram("mass_four_lep_ext",           ROOT.TH1D("mass_four_lep_ext",     "Invariant Mass of the 4-lepton system;M_{4l} [GeV]; Events",30,80,250))

      self.hist_leptn        =  self.addStandardHistogram("lep_n")
      self.hist_leptpt       =  self.addStandardHistogram("lep_pt")
      self.hist_lepteta      =  self.addStandardHistogram("lep_eta")
      self.hist_leptE        =  self.addStandardHistogram("lep_E")
      self.hist_leptphi      =  self.addStandardHistogram("lep_phi")
      self.hist_leptch       =  self.addStandardHistogram("lep_charge")
      self.hist_leptID       =  self.addStandardHistogram("lep_type")
      self.hist_leptptc      =  self.addStandardHistogram("lep_ptconerel30")
      self.hist_leptetc      =  self.addStandardHistogram("lep_etconerel20")
      self.hist_lepz0        =  self.addStandardHistogram("lep_z0")
      self.hist_lepd0        =  self.addStandardHistogram("lep_d0")

      self.hist_etmiss       = self.addStandardHistogram("etmiss")

    
  def analyze(self):
      # retrieving objects
      eventinfo = self.Store.getEventInfo()
      weight = eventinfo.scalefactor()*eventinfo.eventWeight() if not self.getIsData() else 1

      # retrieve Leptons  
      goodLeptons = AnalysisHelpers.selectAndSortContainer(self.Store.getLeptons(), isGoodLepton, lambda p: p.pt())
      if not len(goodLeptons) == 4: return False
      self.countEvent("4 leptons", weight)

      if not goodLeptons[1].pt() > 15: return False
      self.countEvent("2nd lep_pt > 15 GeV", weight)

      if not goodLeptons[2].pt() > 10: return False
      self.countEvent("3rd lep_pt > 10 GeV", weight)
        
      # find ZZ Candidate
      candidate = self.ZZCandidate(goodLeptons)
      if candidate is None: return False;

 
      # ZZ system histograms
      self.invMassZ1.Fill((candidate[0].tlv() + candidate[1].tlv()).M(), weight)
      self.invMassZ2.Fill((candidate[2].tlv() + candidate[3].tlv()).M(), weight)
      
      self.mass_four_lep_ext.Fill((candidate[0].tlv()+candidate[1].tlv()+candidate[2].tlv()+candidate[3].tlv()).M(),weight)

      # lepton histograms
      self.hist_leptn.Fill(len(goodLeptons), weight)
      [self.hist_leptpt.Fill(lep.pt(), weight) for lep in goodLeptons]
      [self.hist_lepteta.Fill(lep.eta(), weight) for lep in goodLeptons]
      [self.hist_leptE.Fill(lep.e(), weight) for lep in goodLeptons]
      [self.hist_leptphi.Fill(lep.phi(), weight) for lep in goodLeptons]
      [self.hist_leptch.Fill(lep.charge(), weight) for lep in goodLeptons]
      [self.hist_leptID.Fill(lep.pdgId(), weight) for lep in goodLeptons]
      [self.hist_leptptc.Fill(lep.isoptconerel30(), weight) for lep in goodLeptons]
      [self.hist_leptetc.Fill(lep.isoetconerel20(), weight) for lep in goodLeptons]

      return True
  
  def finalize(self):
      pass
    
  def ZWindow(self, lep1, lep2):
      return abs((lep1.tlv()+lep2.tlv()).M() - Constants.Z_Mass)
    
  def DoubleZWindow(self, candidate):
      return self.ZWindow(candidate[0], candidate[1]) + self.ZWindow(candidate[2], candidate[3])

  def ZZCandidate(self, leptons):
      def isValidCandidate(lep1, lep2):
          if lep1.charge()*lep2.charge() > 0: return False
          if abs(lep1.pdgId()) != abs(lep2.pdgId()): return False
          return True
    
      bestCandidate = None
      for p in itertools.permutations(leptons, 4):
         if not isValidCandidate(p[0], p[1]): continue
         if not isValidCandidate(p[2], p[3]): continue 
         if bestCandidate is None:
             bestCandidate = p            
         if self.DoubleZWindow(p) < self.DoubleZWindow(bestCandidate):
             bestCandidate = p
      return bestCandidate

  
def isGoodLepton(Lepton):
    if not Lepton.isoetconerel20() < 0.15: return False
    if not Lepton.isoptconerel30() < 0.15: return False
    return True;
