import FWCore.ParameterSet.Config as cms

pileupVertexFilter  = cms.EDFilter('PAPileUpVertexFilter',
    vtxSrc = cms.InputTag("offlinePrimaryVertices"),
    doDzNtrkCut = cms.bool(True),
    doDxyDzCut = cms.bool(False),
    dxyVeto = cms.double(999.),
    dzVeto = cms.double(-999.),
    dxyDzCutPar0 = cms.double(0.6),
    dxyDzCutPar1 = cms.double(13.333),
    dzCutByNtrk = cms.vdouble(
        999., 3.0, 2.4, 2.0, 1.2, 1.2, 0.9, 0.6
    )
)
