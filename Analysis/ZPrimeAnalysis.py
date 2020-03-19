import ROOT
import math

import Analysis
import AnalysisHelpers as AH

#======================================================================
        
class ZPrimeAnalysis(Analysis.Analysis):
  """Analysis searching for an exotic Z' particle in a semileptonic top pair topology."""
  def __init__(self, store):
      super(ZPrimeAnalysis, self).__init__(store)
  
  def initialize(self):
      self.hist_leptpt_e    =  self.addHistogram("lep_pt_e", ROOT.TH1D("lep_pt_e",          "Lepton Transverse Momentum;p_{T}^{lep} [GeV];Leptons", 24, 30, 270))
      self.hist_leptpt_mu   =  self.addHistogram("lep_pt_mu", ROOT.TH1D("lep_pt_mu",          "Lepton Transverse Momentum;p_{T}^{lep} [GeV];Leptons", 24, 30, 270))
      self.hist_etmiss_e    =  self.addHistogram("etmiss_e", ROOT.TH1D("etmiss_e",          "Missing Transverse Momentum;p_{T,Miss} [GeV];Events", 22, 20,240))
      self.hist_etmiss_mu   =  self.addHistogram("etmiss_mu", ROOT.TH1D("etmiss_mu",          "Missing Transverse Momentum;p_{T,Miss} [GeV];Events", 22, 20,240))
      self.hist_jetspt_e    =  self.addHistogram("jet_pt_e", ROOT.TH1D("jet_pt_e",          "Jet Transverse Momentum;p_{T}^{jet} [GeV];Jets", 48, 20, 500))
      self.hist_jetspt_mu   =  self.addHistogram("jet_pt_mu", ROOT.TH1D("jet_pt_mu",          "Jet Transverse Momentum;p_{T}^{jet} [GeV];Jets", 48, 20, 500))
      self.TtMass_e         =  self.addHistogram("TtMass_e", ROOT.TH1D("TtMass_e",            "Transverse Mass of the leptonic top Candidate; M_{T,t_{lep}} [GeV]; Events", 24, 110, 230))
      self.TtMass_mu        =  self.addHistogram("TtMass_mu", ROOT.TH1D("TtMass_mu",            "Transverse Mass of the leptonic top Candidate; M_{T,t_{lep}} [GeV]; Events", 24, 110, 230))
      self.TopMass_e        =  self.addHistogram("TopMass_e", ROOT.TH1D("TopMass_e",           "Invariant Mass of the hadronic top Candidate;M_{t_{had}} [GeV];Events", 24, 110, 230))
      self.TopMass_mu       =  self.addHistogram("TopMass_mu", ROOT.TH1D("TopMass_mu",           "Invariant Mass of the hadronic top Candidate;M_{t_{had}} [GeV];Events", 24, 110, 230))

      self.WtMass            = self.addStandardHistogram("WtMass")
      self.hist_WtMass_max  =  self.addHistogram("WtMass_max", ROOT.TH1D("WtMass_max",            "Transverse Mass of the W Candidate Max; M_{T,W} max [GeV]; Events", 40, 0, 200))
      self.hist_WtMass_min  =  self.addHistogram("WtMass_min", ROOT.TH1D("WtMass_min",            "Transverse Mass of the W Candidate Min; M_{T,W} min [GeV]; Events", 40, 0, 200))
      self.TTtMass_e         =  self.addHistogram("TTtMass_e", ROOT.TH1D("TTtMass_e",            "Transverse Mass of the t#bar{t} Candidate; M_{T,t_{lep}} [GeV]; Events", 32, 400, 2000))
      self.TTtMass_mu        =  self.addHistogram("TTtMass_mu", ROOT.TH1D("TTtMass_mu",            "Transverse Mass of the t#bar{t} Candidate; M_{T,t_{lep}} [GeV]; Events", 32, 400, 2000))

      self.hist_leptpt      =  self.addStandardHistogram("lep_pt")
      self.hist_lepteta     =  self.addStandardHistogram("lep_eta")
      self.hist_leptE       =  self.addStandardHistogram("lep_E")
      self.hist_leptphi     =  self.addStandardHistogram("lep_phi")
      self.hist_leptch      =  self.addStandardHistogram("lep_charge")
      self.hist_leptID      =  self.addStandardHistogram("lep_type")
      self.hist_leptptc     =  self.addStandardHistogram("lep_ptconerel30")
      self.hist_leptetc     =  self.addStandardHistogram("lep_etconerel20")
      self.hist_lepz0       =  self.addStandardHistogram("lep_z0")
      self.hist_lepd0       =  self.addStandardHistogram("lep_d0")
      self.hist_leptpt_max  =  self.addHistogram("lep_pt_max", ROOT.TH1D("lep_pt_max", "Lepton Transverse Momentum Max;p_{T}^{lep} max [GeV];Leptons", 40, 0, 200))
      self.hist_leptpt_min  =  self.addHistogram("lep_pt_min", ROOT.TH1D("lep_pt_min", "Lepton Transverse Momentum Min;p_{T}^{lep} min [GeV];Leptons", 40, 0, 200))
      self.hist_leptptc_max  =  self.addHistogram("lep_ptconerel30_max", ROOT.TH1D("lep_ptconerel30_max", "Lepton Relative Transverse Momentum Isolation Max; ptconerel30^{lep} max; Leptons", 40, 0, 0.2))
      self.hist_leptptc_min  =  self.addHistogram("lep_ptconerel30_min", ROOT.TH1D("lep_ptconerel30_min", "Lepton Relative Transverse Momentum Isolation Min; ptconerel30^{lep} min; Leptons", 40, 0, 0.2))
      self.hist_leptetc_max  =  self.addHistogram("lep_etconerel20_max", ROOT.TH1D("lep_etconerel20_max", "Lepton Relative Transverse Energy Isolation Max; etconerel20^{lep} max; Leptons", 40, -0.05, 0.2))
      self.hist_leptetc_min  =  self.addHistogram("lep_etconerel20_min", ROOT.TH1D("lep_etconerel20_min", "Lepton Relative Transverse Energy Isolation Min; etconerel20^{lep} min; Leptons", 40, -0.05, 0.2))

      self.hist_njets       =  self.addStandardHistogram("n_jets")       
      self.hist_jetspt      =  self.addStandardHistogram("jet_pt")       
      self.hist_jetJVT      =  self.addStandardHistogram("jet_jvt")      
      self.hist_jeteta      =  self.addStandardHistogram("jet_eta")      
      self.hist_jetm        =  self.addStandardHistogram("jet_m")
      self.hist_jetmv2c10      =  self.addStandardHistogram("jet_MV2c10")      
      self.hist_jetspt_max      =  self.addHistogram("jet_pt_max", ROOT.TH1D("jet_pt_max", "Jet Transverse Momentum Max;p_{T}^{jet} max [GeV];Jets", 40, 0, 200))
      self.hist_jetspt_min      =  self.addHistogram("jet_pt_min", ROOT.TH1D("jet_pt_min", "Jet Transverse Momentum Min;p_{T}^{jet} min [GeV];Jets", 40, 0, 200))

      self.hist_etmiss      = self.addStandardHistogram("etmiss")
      self.hist_etmiss_max      = self.addHistogram("etmiss_max", ROOT.TH1D("etmiss_max", "Missing Transverse Momentum Max;p_{T,Miss} max [GeV];Events", 20, 0,200))
      self.hist_etmiss_min      = self.addHistogram("etmiss_min", ROOT.TH1D("etmiss_min", "Missing Transverse Momentum Min;p_{T,Miss} min [GeV];Events", 20, 0,200))
  
  def analyze(self):
      # retrieving objects
      eventinfo = self.Store.getEventInfo()
      weight = eventinfo.scalefactor()*eventinfo.eventWeight()*eventinfo.scalefactorBTAG() if not self.getIsData() else 1
      self.countEvent("no cut", weight)
      
      # apply standard event based selection
      if not AH.StandardEventCuts(eventinfo): return False
      self.countEvent("EventCuts", weight)

      # Lepton Requirements
      goodLeptons = AH.selectAndSortContainer(self.Store.getLeptons(), AH.isGoodLepton, lambda p: p.pt())
      if not (len(goodLeptons) == 1): return False
      if not goodLeptons[0].pt() > 30: return False
      self.countEvent("1 high pt Leptons", weight)


      etmiss = self.Store.getEtMiss()
      if not etmiss.et() > 20.: return False
      self.countEvent("etmiss", weight)


      goodJets = AH.selectAndSortContainer(self.Store.getJets(), AH.isGoodJet, lambda p: p.pt())
      if not len(goodJets) >= 4: return False
      self.countEvent("4 jets", weight)

      btags = sum([1 for jet in goodJets if jet.mv2c10() > 0.8244273])
      if not (btags >= 1): return False
      self.countEvent("btag", weight)

      lepton = goodLeptons[0]
      mTW = AH.WTransverseMass(lepton, etmiss)
      if not mTW > 30: return False;
      if not mTW + etmiss.et() > 60: return False
      self.countEvent("masses", weight)

      tlv_jjj = goodJets[0].tlv()+goodJets[1].tlv()+goodJets[2].tlv()
      m_jjj = tlv_jjj.M()
      if lepton.pdgId()==11:
        self.hist_leptpt_e.Fill(lepton.pt(), weight)
        self.hist_etmiss_e.Fill(etmiss.et(), weight)
        [self.hist_jetspt_e.Fill(jet.pt(), weight) for jet in goodJets]
        self.TopMass_e.Fill(m_jjj, weight)
      else:
        self.hist_leptpt_mu.Fill(lepton.pt(), weight)
        self.hist_etmiss_mu.Fill(etmiss.et(), weight)
        [self.hist_jetspt_mu.Fill(jet.pt(), weight) for jet in goodJets]
        self.TopMass_mu.Fill(m_jjj, weight)
      
      # W boson histogram
      self.WtMass.Fill(mTW, weight)
      #self.hist_WtMass_max.Fill(mTW*(1+math.sqrt((lepton.pt_syst()/lepton.pt())*(lepton.pt_syst()/lepton.pt())+(etmiss.et_syst()/etmiss.et())*(etmiss.et_syst()/etmiss.et()))/2), weight)
      #self.hist_WtMass_min.Fill(mTW*(1-math.sqrt((lepton.pt_syst()/lepton.pt())*(lepton.pt_syst()/lepton.pt())+(etmiss.et_syst()/etmiss.et())*(etmiss.et_syst()/etmiss.et()))/2), weight)

      # missing transverse momentum histogram
      self.hist_etmiss.Fill(etmiss.et(), weight)
      #self.hist_etmiss_max.Fill(etmiss.et()+etmiss.et_syst(),weight)
      #self.hist_etmiss_min.Fill(etmiss.et()-etmiss.et_syst(),weight)

      # lepton histograms
      self.hist_leptpt.Fill(lepton.pt(), weight)
      self.hist_lepteta.Fill(lepton.eta(), weight)
      self.hist_leptE.Fill(lepton.e(), weight)
      self.hist_leptphi.Fill(lepton.phi(), weight)
      self.hist_leptch.Fill(lepton.charge(), weight)
      self.hist_leptID.Fill(lepton.pdgId(), weight)
      self.hist_leptptc.Fill(lepton.isoptconerel30(), weight)
      self.hist_leptetc.Fill(lepton.isoetconerel20(), weight)
      self.hist_lepz0.Fill(lepton.z0(), weight)
      self.hist_lepd0.Fill(lepton.d0(), weight)
      #self.hist_leptpt_max.Fill(lepton.pt()+lepton.pt_syst(), weight)
      #self.hist_leptpt_min.Fill(lepton.pt()-lepton.pt_syst(), weight)
      #self.hist_leptptc_max.Fill(lepton.isoptconerel30_max(), weight)
      #self.hist_leptptc_min.Fill(lepton.isoptconerel30_min(), weight)
      #self.hist_leptetc_max.Fill(lepton.isoetconerel20_max(), weight)
      #self.hist_leptetc_min.Fill(lepton.isoetconerel20_min(), weight)

      # jet histograms
      self.hist_njets.Fill(len(goodJets), weight)
      [self.hist_jetspt.Fill(jet.pt(), weight) for jet in goodJets]
      [self.hist_jetJVT.Fill(jet.jvt(), weight) for jet in goodJets]
      [self.hist_jeteta.Fill(jet.eta(), weight) for jet in goodJets]
      [self.hist_jetm.Fill(jet.m(), weight) for jet in goodJets]
      [self.hist_jetmv2c10.Fill(jet.mv2c10(), weight) for jet in goodJets]
      #[self.hist_jetspt_max.Fill(jet.pt()+jet.pt_syst(), weight) for jet in jets]
      #[self.hist_jetspt_min.Fill(jet.pt()-jet.pt_syst(), weight) for jet in jets]
      return True
  
  def finalize(self):
      pass

