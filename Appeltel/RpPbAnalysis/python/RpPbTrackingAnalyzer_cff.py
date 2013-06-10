import FWCore.ParameterSet.Config as cms

import Appeltel.RpPbAnalysis.RpPbTrackingAnalyzer_cfi

trkAna_etaFull = Appeltel.RpPbAnalysis.RpPbTrackingAnalyzer_cfi.trkAna.clone()

trkAna_etaN2 = trkAna_etaFull.clone(
   etaMin = cms.double(-2.5),
   etaMax = cms.double(-1.5)
)

trkAna_etaN1 = trkAna_etaFull.clone(
   etaMin = cms.double(-1.5),
   etaMax = cms.double(-0.5)
)

trkAna_eta0 = trkAna_etaFull.clone(
   etaMin = cms.double(-0.5),
   etaMax = cms.double(0.5)
)

trkAna_etaP1 = trkAna_etaFull.clone(
   etaMin = cms.double(0.5),
   etaMax = cms.double(1.5)
)

trkAna_etaP2 = trkAna_etaFull.clone(
   etaMin = cms.double(1.5),
   etaMax = cms.double(2.5)
)

trkAna_etaFull_pixel = trkAna_etaFull.clone(
   trackSrc = cms.InputTag("pixelTracks")
)

trkAna_etaFull_noBS = trkAna_etaFull.clone(
   vertexSrc = cms.InputTag("offlinePrimaryVertices")
)

trkAnaMinBias = cms.Sequence( trkAna_etaFull 
                              * trkAna_etaN2
                              * trkAna_etaN1
                              * trkAna_eta0
                              * trkAna_etaP1
                              * trkAna_etaP2
                              * trkAna_etaFull_pixel
                              * trkAna_etaFull_noBS
                            )

trkAna_etaFull_highPt = trkAna_etaFull.clone(
   ptMin = cms.double(6.0)
)

trkAna_etaFull_highPtQuality = trkAna_etaFull.clone(
   ptMin = cms.double(6.0),
   applyCuts = cms.bool(True),
   qualityString = cms.string('highPurity'),
   dxyErrMax = cms.double(3.0),
   dzErrMax = cms.double(3.0),
   ptErrMax = cms.double(0.1)
)
