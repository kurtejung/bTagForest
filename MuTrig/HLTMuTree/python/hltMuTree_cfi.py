import FWCore.ParameterSet.Config as cms

hltMuTree = cms.EDAnalyzer("HLTMuTree",
  muons = cms.InputTag("muons"),
  vertices = cms.InputTag("hiSelectedVertex"),
  doReco = cms.untracked.bool(True),
  doGen = cms.untracked.bool(False),
  doCentrality = cms.untracked.bool(True),
  genparticle = cms.InputTag("hiGenParticles"),
  simtrack = cms.InputTag("mergedtruth","MergedTrackTruth"),
)
