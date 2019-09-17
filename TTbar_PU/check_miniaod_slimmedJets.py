# import ROOT in batch mode
import sys
oldargv = sys.argv[:]
sys.argv = [ '-b-' ]
import ROOT
ROOT.gROOT.SetBatch(True)
sys.argv = oldargv

from ctypes import c_uint8

# load FWLite C++ libraries
ROOT.gSystem.Load("libFWCoreFWLite.so")
ROOT.gSystem.Load("libDataFormatsFWLite.so")
ROOT.AutoLibraryLoader.enable()

# load FWlite python libraries
from DataFormats.FWLite import Handle, Events

muons, muonLabel = Handle("std::vector<pat::Muon>"), "slimmedMuons"
electrons, electronLabel = Handle("std::vector<pat::Electron>"), "slimmedElectrons"
photons, photonLabel = Handle("std::vector<pat::Photon>"), "slimmedPhotons"
taus, tauLabel = Handle("std::vector<pat::Tau>"), "slimmedTaus"
jets, jetLabel = Handle("std::vector<pat::Jet>"), "slimmedJets"
fatjets, fatjetLabel = Handle("std::vector<pat::Jet>"), "slimmedJetsAK8"
mets, metLabel = Handle("std::vector<pat::MET>"), "slimmedMETs"
vertices, vertexLabel = Handle("std::vector<reco::Vertex>"), "offlineSlimmedPrimaryVertices"
pfcands, pfcandLabel = Handle("std::vector<pat::PackedCandidate>"), "packedPFCandidates"
pfcandHcalDepthLabel = ("packedPFCandidates","hcalDepthEnergyFractions")

pfcandPtScore = Handle("edm::ValueMap<float>")
hcalDepthScore = Handle("edm::ValueMap<pat::HcalDepthEnergyFractions>")
verticesScore = Handle("edm::ValueMap<float>")

# open file (you can use 'edmFileUtil -d /store/whatever.root' to get the physical file name)
events = Events('file:step3_inMINIAODSIM.root')

for iev,event in enumerate(events):
    if iev >= 10: break 
    event.getByLabel(muonLabel, muons)
    event.getByLabel(electronLabel, electrons)
    event.getByLabel(photonLabel, photons)
    event.getByLabel(tauLabel, taus)
    event.getByLabel(jetLabel, jets)
    event.getByLabel(metLabel, mets)
    event.getByLabel(vertexLabel, vertices)
    event.getByLabel(vertexLabel, verticesScore)
    event.getByLabel(pfcandLabel,pfcands)
    event.getByLabel(pfcandHcalDepthLabel,hcalDepthScore)
    print "\nEvent %d: run %6d, lumi %4d, event %12d" % (iev,event.eventAuxiliary().run(), event.eventAuxiliary().luminosityBlock(),event.eventAuxiliary().event())

    # Vertices 
    if len(vertices.product()) == 0 or vertices.product()[0].ndof() < 4:
        print "Event has no good primary vertex."
        continue
    else:
        PV = vertices.product()[0]
        print "PV at x,y,z = %+5.3f, %+5.3f, %+6.3f, ndof: %.1f, score: (pt2 of clustered objects) %.1f" % (PV.x(), PV.y(), PV.z(), PV.ndof(),verticesScore.product().get(0))

    # Jets (standard AK4)
    for i,j in enumerate(jets.product()):
        if j.pt() < 20: continue
        print "jet %3d: pt %5.1f (raw pt %5.1f, matched-calojet pt %5.1f), eta %+4.2f, btag run1(CSV) ) %.3f, run2(pfCSVIVFV2) %.3f, pileup mva disc %+.2f" % (
            i, j.pt(), j.pt()*j.jecFactor('Uncorrected'), j.userFloat("caloJetMap:pt"), j.eta(), max(0,j.bDiscriminator("combinedSecondaryVertexBJetTags")), max(0,j.bDiscriminator("pfCombinedInclusiveSecondaryVertexV2BJetTags")), j.userFloat("pileupJetId:fullDiscriminant"))

    # pfcands
    # for i,j in enumerate(pfcands.product()):
    #     if j.pt() < 0: continue
    #     print "pfcands %3d: pt %5.1f eta %5.2f pdgId %5d %5.3f %5.3f " % ( i, j.pt(), j.eta(), j.pdgId(), j.rawCaloFraction(), j.hcalFraction())
