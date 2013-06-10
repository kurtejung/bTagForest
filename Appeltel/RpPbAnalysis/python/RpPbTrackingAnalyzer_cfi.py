import FWCore.ParameterSet.Config as cms

trkAna  = cms.EDAnalyzer('RpPbTrackingAnalyzer',
   trackSrc = cms.InputTag("generalTracks"),
   vertexSrc = cms.InputTag("offlinePrimaryVerticesWithBS"),
   etaMin = cms.double(-2.5),
   etaMax = cms.double(2.5),
   ptMin = cms.double(0.0)
)
