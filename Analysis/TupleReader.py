import ROOT
from array import array

#======================================================================

class TupleReader(object):
    """ This class implements the rules that govern the readout of the ROOT tuples and and provide a caching facility.
    Caching improves the readout by eliminating the need for branch address lookup each time the variable is accessed.
    """

    def __init__(self):
        super(TupleReader, self).__init__()
        self.Tree = None
        
    def initializeTuple(self,tree):
        """The initial setup of the caching is done here. Branches in the TTree may be deactivated using SetBranchStatus to
        increase readout speed. Only necessary branches are activated and their contents are bound to datamembers of the
        tuple reader.
        """
        self.Tree = tree
        self.Tree.SetBranchStatus("*",0)

        #EventInfo 
        self.eventNumber      = self.activate("i", "eventNumber",            1)
        self.runNumber        = self.activate("i", "runNumber" ,             1)
        self.mcWeight         = self.activate("f", "mcWeight",               1)
                                                                             
        self.trigE            = self.activate("b", "trigE",                     1)
        self.trigM            = self.activate("b", "trigM",                     1)
        self.trigP            = self.activate("b", "trigP",                     1)
        self.trigT            = self.activate("b", "trigT",                     1)
        self.trigDT           = self.activate("b", "trigDT",                    1)
        self.SF_Pileup        = self.activate("f", "scaleFactor_PILEUP",        1)
        self.SF_Ele           = self.activate("f", "scaleFactor_ELE",           1)
        self.SF_Mu            = self.activate("f", "scaleFactor_MUON",          1)
        self.SF_Photon        = self.activate("f", "scaleFactor_PHOTON",        1)
        self.SF_Tau           = self.activate("f", "scaleFactor_TAU",           1)
        self.SF_BTag          = self.activate("f", "scaleFactor_BTAG",          1)
        self.SF_LepTrigger    = self.activate("f", "scaleFactor_LepTRIGGER",    1) 
        self.SF_PhotonTrigger = self.activate("f", "scaleFactor_PhotonTRIGGER", 1)
        self.SF_TauTrigger    = self.activate("f", "scaleFactor_TauTRIGGER",    1)
        self.SF_DiTauTrigger  = self.activate("f", "scaleFactor_DiTauTRIGGER",  1)

        self.EventInfo = EventInfo(self)
        

        #LeptonInfo
        max_Lep = self.GetMaximum("lep_n")
        max_Lep = min(abs(max_Lep), 20)
        self.Lep_n         = self.activate("i", "lep_n",                    1)
        self.Lep_pt        = self.activate("f", "lep_pt",                   max_Lep) 
        self.Lep_eta       = self.activate("f", "lep_eta",                  max_Lep) 
        self.Lep_phi       = self.activate("f", "lep_phi",                  max_Lep)
        self.Lep_e         = self.activate("f", "lep_E",                    max_Lep)
        self.Lep_pdgid     = self.activate("i", "lep_type",                 max_Lep)
        self.Lep_charge    = self.activate("i", "lep_charge",               max_Lep)
        self.Lep_ptcone30  = self.activate("f", "lep_ptcone30",             max_Lep)
        self.Lep_etcone20  = self.activate("f", "lep_etcone20",             max_Lep)                    
        self.Lep_d0        = self.activate("f", "lep_trackd0pvunbiased",    max_Lep)
        self.Lep_d0Sig     = self.activate("f", "lep_tracksigd0pvunbiased", max_Lep)
        self.Lep_trigMatch = self.activate("b", "lep_trigMatched",          max_Lep)
        self.Lep_z0        = self.activate("f", "lep_z0",                   max_Lep)
        self.Lep_isTightID = self.activate("b", "lep_isTightID",            max_Lep)
        self.Lep_pt_syst   = self.activate("f", "lep_pt_syst",              max_Lep)

        self.Leptons = [Lepton(i,self) for i in range(0,max_Lep)]

        #PhotonInfo
        max_Photon = self.GetMaximum("photon_n")
        max_Photon = min(abs(max_Photon), 20)
        self.Photon_n         = self.activate("i", "photon_n",         1)
        self.Photon_pt        = self.activate("f", "photon_pt",        max_Photon)
        self.Photon_eta       = self.activate("f", "photon_eta",       max_Photon)
        self.Photon_phi       = self.activate("f", "photon_phi",       max_Photon)
        self.Photon_e         = self.activate("f", "photon_E",         max_Photon)
        self.Photon_ptcone30  = self.activate("f", "photon_ptcone30",  max_Photon)
        self.Photon_etcone20  = self.activate("f", "photon_etcone20",  max_Photon)
        self.Photon_isTightID = self.activate("b", "photon_isTightID", max_Photon)
        self.Photon_pt_syst   = self.activate("f", "photon_pt_syst",   max_Photon)

        self.Photons = [Photon(i,self) for i in range(0,max_Photon)]
         
        #JetInfo
        max_Jet = self.GetMaximum("jet_n")
        max_Jet = min(abs(max_Jet), 20)
        self.Jet_n        = self.activate("i", "jet_n",        1)
        self.Jet_pt       = self.activate("f", "jet_pt",       max_Jet)
        self.Jet_eta      = self.activate("f", "jet_eta",      max_Jet)
        self.Jet_e        = self.activate("f", "jet_E",        max_Jet)
        self.Jet_phi      = self.activate("f", "jet_phi",      max_Jet)
        self.Jet_jvt      = self.activate("f", "jet_jvt",      max_Jet)
        self.Jet_mv2c10   = self.activate("f", "jet_MV2c10",   max_Jet) 
        self.Jet_pt_syst  = self.activate("f", "jet_pt_syst",  max_Jet)
         
        self.Jets = [Jet(i, self) for i in range(0,max_Jet)]

        #FatJetInfo                                                                                 
        max_FatJet = self.GetMaximum("fatjet_n")
        max_FatJet = min(abs(max_FatJet), 20)
        self.FatJet_n       = self.activate("i", "fatjet_n",       1)
        self.FatJet_pt      = self.activate("f", "fatjet_pt",      max_FatJet)
        self.FatJet_eta     = self.activate("f", "fatjet_eta",     max_FatJet)
        self.FatJet_e       = self.activate("f", "fatjet_E",       max_FatJet)
        self.FatJet_phi     = self.activate("f", "fatjet_phi",     max_FatJet)
        self.FatJet_mass    = self.activate("f", "fatjet_m",       max_FatJet)
        self.FatJet_D2      = self.activate("f", "fatjet_D2",      max_FatJet)
        self.FatJet_tau32   = self.activate("f", "fatjet_tau32",   max_FatJet)
        #self.FatJet_pt_syst = self.activate("f", "fatjet_pt_syst", max_FatJet)

        self.FatJets = [FatJet(i, self) for i in range(0,max_FatJet)]

        #TauInfo                                                                                                                                
        max_Tau = self.GetMaximum("tau_n")
        max_Tau = min(abs(max_Tau), 20)
        self.Tau_n         = self.activate("i", "tau_n",         1)
        self.Tau_pt        = self.activate("f", "tau_pt",        max_Tau)
        self.Tau_eta       = self.activate("f", "tau_eta",       max_Tau)
        self.Tau_e         = self.activate("f", "tau_E",         max_Tau)
        self.Tau_phi       = self.activate("f", "tau_phi",       max_Tau)
        self.Tau_isTightID = self.activate("b", "tau_isTightID", max_Tau)
        self.Tau_nTracks   = self.activate("i", "tau_nTracks",   max_Tau)
        self.Tau_BDTid     = self.activate("f", "tau_BDTid",     max_Tau)
        self.Tau_pt_syst   = self.activate("f", "tau_pt_syst",   max_Tau)
        self.DiTau_m       = self.activate("f", "ditau_m",       1)

        self.Taus = [Tau(i, self) for i in range(0,max_Tau)]

        #EtMissInfo
        self.Met_et      = self.activate( "f", "met_et",      1)
        self.Met_phi     = self.activate( "f", "met_phi",     1)
        self.Met_et_syst = self.activate( "f", "met_et_syst", 1)
        
        self.EtMiss = EtMiss(self)
                
                
    def activate(self, vartype,  branchname, maxlength):
        self.Tree.SetBranchStatus(branchname,1)
        if (type(self.Tree.GetBranch(branchname))==ROOT.TBranchElement):
            if vartype=="f": 
                variable = ROOT.vector('float')()
            elif vartype=="i":
                variable = ROOT.vector('int')()
            elif vartype=="b":
                variable = ROOT.vector('bool')()
        else: 
            variable = array(vartype,[0]*maxlength)
        self.Tree.SetBranchAddress( branchname, variable)           
        return variable
    
    # Used for a quick scan to get the largest value encountered in the tuple
    def GetMaximum(self,branchname):
        self.Tree.SetBranchStatus(branchname,1)
        return int(self.Tree.GetMaximum(branchname))
    
    # Functions to retrieve object collections (Tuplereader is called Store in the analysis code)
    def getEtMiss(self):
        return self.EtMiss
        
    def getEventInfo(self):
        return self.EventInfo
        
    def getLeptons(self):
        return self.Leptons[:self.Lep_n[0]]

    def getPhotons(self):
        return self.Photons[:self.Photon_n[0]]
    
    def getJets(self):
        return self.Jets[:self.Jet_n[0]]

    def getFatJets(self):
        return self.FatJets[:self.FatJet_n[0]]

    def getTaus(self):
        return self.Taus[:self.Tau_n[0]]

#===========================================================

class EtMiss(object):
    """Missing Transverse Momentum Object.
    Missing Transverse Momentum has only two variables, its magnitude (et) and its azimuthal angle (phi).
    It is used as a proxy for all particles that escaped detection (neutrinos and the likes).
    """
    def __init__(self, branches):
        super(EtMiss, self).__init__()
        self.Branches = branches
        self._tlv     = None
    
    def tlv(self):
      if self._tlv == None:
        self._tlv = ROOT.TLorentzVector()
      if self.et() != self._tlv.Pt():
        self._tlv.SetPtEtaPhiE(self.et(), 0, self.phi(), self.et())
      return self._tlv
    
    def et(self):
      return self.Branches.Met_et[0]*0.001

    def et_syst(self):
      return self.Branches.Met_et_syst[0]*0.001

    def phi(self):
      return self.Branches.Met_phi[0]

    def __str__(self):
        return "MET: et: %4.3f  phi: %4.3f" % (self.et(), self.phi())

#===========================================================

class EventInfo(object):
    """EventInfo class holding information about the event
    Information that can be accessed may either be metadata about the event (eventNumber, runNumber),
    information regarding the weight an event has (eventWeight, scalefactor, mcWeight, primaryVertexPosition) or
    information that may be used for selection purposes (passGRL, hasGoodVertex, numberofVertices, triggeredByElectron, 
    triggeredByMuon)
    """
    def __init__(self, branches):
        super(EventInfo, self).__init__()
        self.Branches = branches

    def eventNumber(self):
      return self.Branches.eventNumber[0]

    def runNumber(self):
      return self.Branches.runNumber[0]

    def scalefactorBTAG(self):
      return self.Branches.SF_BTag[0]

    def eventWeight(self):
      return self.Branches.mcWeight[0]*self.Branches.SF_Pileup[0]

    def scalefactor(self):
      return self.Branches.SF_Ele[0]*self.Branches.SF_Mu[0]*self.Branches.SF_LepTrigger[0]*self.Branches.SF_Photon[0]*self.Branches.SF_PhotonTrigger[0]*self.Branches.SF_Tau[0]*self.Branches.SF_TauTrigger[0]*self.Branches.SF_DiTauTrigger[0]

    def mcWeight(self):
      return self.Branches.mcWeight[0]
    
    def triggeredByElectron(self):
      return self.Branches.trigE[0]

    def triggeredByMuon(self):
      return self.Branches.trigM[0]

    def triggeredByPhoton(self):
      return self.Branches.trigP[0]

    def triggeredByTau(self):
      return self.Branches.trigT[0]

    def triggeredByDiTau(self):
      return self.Branches.trigDT[0]

    def __str__(self):
        return "EventInfo: run: %i  event: %i  eventweight: %4.2f" % (self.runNumber(), self.eventNumber(), self.eventWeight())


#===========================================================

class Lepton(object):
    """Leptons may either be electrons or muons (checkable via the pdgId, 11 is for electrons, 13 for muons, 
    negative values signify anti-particles) Accessible information includes the kinematics (pt, eta, phi, e),
    the quality of the reconstruction result (isTightID), and auxillary information
    (pdgId, charge, isolation variables like isoptcone30, d0, z0...).
    """
    def __init__(self, idNr, branches):
        super(Lepton, self).__init__()
        self.Branches = branches
        self.idNr = idNr
        self._tlv = None

    def tlv(self):
      if self._tlv == None:
        self._tlv = ROOT.TLorentzVector()
      if self.pt() != self._tlv.Pt():
        self._tlv.SetPtEtaPhiE(self.pt(), self.eta(), self.phi(), self.e())
      return self._tlv
      
    def pt(self):
      return self.Branches.Lep_pt[self.idNr]*0.001

    def pt_syst(self):
      if self.Branches.SF_Pileup == array('f', [0.0]): return 0
      else: return self.Branches.Lep_pt_syst[self.idNr]*0.001

    def eta(self):
      return self.Branches.Lep_eta[self.idNr]

    def phi(self):
      return self.Branches.Lep_phi[self.idNr]

    def e(self):
      return self.Branches.Lep_e[self.idNr]*0.001

    def isTightID(self):
        return self.Branches.Lep_isTightID[self.idNr]

    def pdgId(self):
      return self.Branches.Lep_pdgid[self.idNr]
 
    def charge(self):
      return self.Branches.Lep_charge[self.idNr]
    
    def isoptcone30(self):
      return self.Branches.Lep_ptcone30[self.idNr]                

    def isoetcone20(self):
      return self.Branches.Lep_etcone20[self.idNr]                

    def isoptconerel30(self):
      return self.Branches.Lep_ptcone30[self.idNr]/self.Branches.Lep_pt[self.idNr]                

    def isoptconerel30_max(self):
      if self.Branches.SF_Pileup == array('f', [0.0]): return self.Branches.Lep_ptcone30[self.idNr]/self.Branches.Lep_pt[self.idNr]
      else: return self.Branches.Lep_ptcone30[self.idNr]/(self.Branches.Lep_pt[self.idNr]-self.Branches.Lep_pt_syst[self.idNr])

    def isoptconerel30_min(self):
      if self.Branches.SF_Pileup == array('f', [0.0]): return self.Branches.Lep_ptcone30[self.idNr]/self.Branches.Lep_pt[self.idNr]
      else: return self.Branches.Lep_ptcone30[self.idNr]/(self.Branches.Lep_pt[self.idNr]+self.Branches.Lep_pt_syst[self.idNr])

    def isoetconerel20(self):
      return self.Branches.Lep_etcone20[self.idNr]/self.Branches.Lep_pt[self.idNr]                

    def isoetconerel20_max(self):
      if self.Branches.SF_Pileup == array('f', [0.0]): return self.Branches.Lep_etcone20[self.idNr]/self.Branches.Lep_pt[self.idNr]
      else: return self.Branches.Lep_etcone20[self.idNr]/(self.Branches.Lep_pt[self.idNr]-self.Branches.Lep_pt_syst[self.idNr])

    def isoetconerel20_min(self):
      if self.Branches.SF_Pileup == array('f', [0.0]): return self.Branches.Lep_etcone20[self.idNr]/self.Branches.Lep_pt[self.idNr]
      else: return self.Branches.Lep_etcone20[self.idNr]/(self.Branches.Lep_pt[self.idNr]+self.Branches.Lep_pt_syst[self.idNr])

    def d0(self):
      return self.Branches.Lep_d0[self.idNr]
    
    def d0Significance(self):
      return self.Branches.Lep_d0Sig[self.idNr]
    
    def isTriggerMatched(self):
      return self.Branches.Lep_trigMatch[self.idNr]

    def z0(self):
      return self.Branches.Lep_z0[self.idNr]
         
    def __str__(self):
        return "Lepton %d: pdgId: %d  pt: %4.3f  eta: %4.3f  phi: %4.3f" % (self.idNr, self.pdgId(), self.pt(), self.eta(), self.phi())
        
#===========================================================

class Photon(object):
    """Accessible information includes the kinematics (pt, eta, phi, e),                              
    the quality of the reconstruction result (isTightID), and auxillary information                                                          
    (isolation variables like isoptcone30...).                                                                      
    """
    def __init__(self, idNr, branches):
        super(Photon, self).__init__()
        self.Branches = branches
        self.idNr = idNr
        self._tlv = None

    def tlv(self):
      if self._tlv == None:
        self._tlv = ROOT.TLorentzVector()
      if self.pt() != self._tlv.Pt():
        self._tlv.SetPtEtaPhiE(self.pt(), self.eta(), self.phi(), self.e())
      return self._tlv

    def pt(self):
      return self.Branches.Photon_pt[self.idNr]*0.001

    def pt_syst(self):
      if self.Branches.SF_Pileup == array('f', [0.0]): return 0
      else: return self.Branches.Photon_pt_syst[self.idNr]*0.001

    def eta(self):
      return self.Branches.Photon_eta[self.idNr]

    def phi(self):
      return self.Branches.Photon_phi[self.idNr]

    def e(self):
      return self.Branches.Photon_e[self.idNr]*0.001

    def isTightID(self):
      return self.Branches.Photon_isTightID[self.idNr]

    def isoptcone30(self):
      return self.Branches.Photon_ptcone30[self.idNr]

    def isoetcone20(self):
      return self.Branches.Photon_etcone20[self.idNr]

    def isoptconerel30(self):
      return self.Branches.Photon_ptcone30[self.idNr]/self.Branches.Photon_pt[self.idNr]

    def isoptconerel30_max(self):
      if self.Branches.SF_Pileup == array('f', [0.0]): return self.Branches.Photon_ptcone30[self.idNr]/self.Branches.Photon_pt[self.idNr]
      else: return self.Branches.Photon_ptcone30[self.idNr]/(self.Branches.Photon_pt[self.idNr]-self.Branches.Photon_pt_syst[self.idNr])

    def isoptconerel30_min(self):
      if self.Branches.SF_Pileup == array('f', [0.0]): return self.Branches.Photon_ptcone30[self.idNr]/self.Branches.Photon_pt[self.idNr]
      else: return self.Branches.Photon_ptcone30[self.idNr]/(self.Branches.Photon_pt[self.idNr]+self.Branches.Photon_pt_syst[self.idNr])

    def isoetconerel20(self):
      return self.Branches.Photon_etcone20[self.idNr]/self.Branches.Photon_pt[self.idNr]

    def isoetconerel20_max(self):
      if self.Branches.SF_Pileup == array('f', [0.0]): return self.Branches.Photon_etcone20[self.idNr]/self.Branches.Photon_pt[self.idNr]
      else: return self.Branches.Photon_etcone20[self.idNr]/(self.Branches.Photon_pt[self.idNr]-self.Branches.Photon_pt_syst[self.idNr])

    def isoetconerel20_min(self):
      if self.Branches.SF_Pileup == array('f', [0.0]): return self.Branches.Photon_etcone20[self.idNr]/self.Branches.Photon_pt[self.idNr]
      else: return self.Branches.Photon_etcone20[self.idNr]/(self.Branches.Photon_pt[self.idNr]+self.Branches.Photon_pt_syst[self.idNr])

    def __str__(self):
        return "Photon %d: pt: %4.3f  eta: %4.3f  phi: %4.3f" % (self.idNr, self.pt(), self.eta(), self.phi())

#=========================================================== 

class Jet(object):
    """Jet objects have accessors regarding their kinematic information (pt, eta, phi, e), their properties (m), and
    auxillary information (mv2c10, jvt). Truth information regarding the flavour of the quark they com from (truepdgid)
    and whether they were matched to a true jet (isTrueJet) is available.
    """
    def __init__(self, idNr, branches):
        super(Jet, self).__init__()
        self.idNr = idNr
        self.Branches = branches
        self._tlv = None

    def tlv(self):
      if self._tlv == None:
        self._tlv = ROOT.TLorentzVector()
      if self.pt() != self._tlv.Pt():
        self._tlv.SetPtEtaPhiE(self.pt(), self.eta(), self.phi(), self.e())
      return self._tlv
    
    def pt(self):
      return self.Branches.Jet_pt[self.idNr]*0.001

    def n(self):
        return self.Branches.Jet_n[self.idNr]

    def pt_syst(self):
      if self.Branches.SF_Pileup == array('f', [0.0]): return 0
      else: return self.Branches.Jet_pt_syst[self.idNr]*0.001
    
    def eta(self):
      return self.Branches.Jet_eta[self.idNr]
    
    def phi(self):
      return self.Branches.Jet_phi[self.idNr]
    
    def e(self):
      return self.Branches.Jet_e[self.idNr]*0.001
    
    def m(self):
      return self.tlv().M() 

    def mv2c10(self):
      return self.Branches.Jet_mv2c10[self.idNr] 
      
    def jvt(self):
      return self.Branches.Jet_jvt[self.idNr]

    def truepdgid(self):
      return self.Branches.Jet_trueflav[self.idNr]

    def isTrueJet(self):
      return bool(self.Branches.Jet_truthMatched[self.idNr])
         
    def __str__(self):
        return "Jet %d: pt: %4.3f  eta: %4.3f  phi: %4.3f" % (self.idNr, self.pt(), self.eta(), self.phi())


#===========================================================                                                                                      

class FatJet(object):
    """Jet objects have accessors regarding their kinematic information (pt, eta, phi, e), their properties (m), and                             
    auxillary information (mv2c10, jvt). Truth information regarding the flavour of the quark they com from (truepdgid)                          
    and whether they were matched to a true jet (isTrueJet) is available.                                                                        
    """
    def __init__(self, idNr, branches):
        super(FatJet, self).__init__()
        self.idNr = idNr
        self.Branches = branches
        self._tlv = None

    def tlv(self):
      if self._tlv == None:
        self._tlv = ROOT.TLorentzVector()
      if self.pt() != self._tlv.Pt():
        self._tlv.SetPtEtaPhiE(self.pt(), self.eta(), self.phi(), self.e())
      return self._tlv

    def pt(self):
      return self.Branches.FatJet_pt[self.idNr]*0.001

    def pt_syst(self):
      if self.Branches.SF_Pileup == array('f', [0.0]): return 0
      else: return self.Branches.FatJet_pt_syst[self.idNr]*0.001

    def eta(self):
      return self.Branches.FatJet_eta[self.idNr]

    def phi(self):
      return self.Branches.FatJet_phi[self.idNr]

    def e(self):
      return self.Branches.FatJet_e[self.idNr]*0.001

    def m(self):
      return self.Branches.FatJet_mass[self.idNr]*0.001

    def isTrueJet(self):
      return self.Branches.FatJet_truthMatched[self.idNr]

    def D2(self):
      return self.Branches.FatJet_D2[self.idNr]

    def tau32(self):
      return self.Branches.FatJet_tau32[self.idNr]

    def __str__(self):
        return "FatJet %d: pt: %4.3f  eta: %4.3f  phi: %4.3f" % (self.idNr, self.pt(), self.eta(), self.phi())


#===========================================================                                                                                      

class Tau(object):
    """Jet objects have accessors regarding their kinematic information (pt, eta, phi, e), their properties (m), and                             
    auxillary information (mv2c10, jvt). Truth information regarding the flavour of the quark they com from (truepdgid)                          
    and whether they were matched to a true jet (isTrueJet) is available.                                                                        
    """
    def __init__(self, idNr, branches):
        super(Tau, self).__init__()
        self.idNr = idNr
        self.Branches = branches
        self._tlv = None

    def tlv(self):
      if self._tlv == None:
        self._tlv = ROOT.TLorentzVector()
      if self.pt() != self._tlv.Pt():
        self._tlv.SetPtEtaPhiE(self.pt(), self.eta(), self.phi(), self.e())
      return self._tlv

    def pt(self):
      return self.Branches.Tau_pt[self.idNr]*0.001

    def pt_syst(self):
      if self.Branches.SF_Pileup == array('f', [0.0]): return 0
      else: return self.Branches.Tau_pt_syst[self.idNr]*0.001

    def eta(self):
      return self.Branches.Tau_eta[self.idNr]

    def phi(self):
      return self.Branches.Tau_phi[self.idNr]

    def e(self):
      return self.Branches.Tau_e[self.idNr]*0.001

    def isTightID(self):
      return self.Branches.Tau_isTightID[self.idNr]

    def nTracks(self):
      return self.Branches.Tau_nTracks[self.idNr]

    def BDTid(self):
      return self.Branches.Tau_BDTid[self.idNr]

    def DiTau_m(self):
      return self.Branches.DiTau_m[0]

    def __str__(self):
        return "Tau %d: pt: %4.3f  eta: %4.3f  phi: %4.3f" % (self.idNr, self.pt(), self.eta(), self.phi())


#===========================================================

