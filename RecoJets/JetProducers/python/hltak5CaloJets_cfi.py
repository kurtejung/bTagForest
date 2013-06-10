import FWCore.ParameterSet.Config as cms

hltak5CaloJets = cms.EDProducer( "FastjetJetProducer", 
    Active_Area_Repeats = cms.int32(1),
    doOutputJets = cms.bool(True),
    useDeterministicSeed = cms.bool(True),
    doPVCorrection = cms.bool(False),
    minSeed = cms.uint32(14327),
    Ghost_EtaMax = cms.double(5.0),
    voronoiRfact = cms.double(0.9),
    doRhoFastjet = cms.bool(False),
    srcPVs = cms.InputTag("offlinePrimaryVertices"),
    inputEtMin = cms.double(0.3),
    doAreaFastjet = cms.bool(False),
    nSigmaPU = cms.double(1.0),
    GhostArea = cms.double(0.01),
    Rho_EtaMax = cms.double(4.4),
    jetPtMin = cms.double(3.0),
    jetType = cms.string('CaloJet'),
    doPUOffsetCorr = cms.bool(False),
    radiusPU = cms.double(0.5),
    doAreaDiskApprox = cms.bool(True),
    inputEMin = cms.double(0.0),
    maxRecoveredHcalCells = cms.uint32(9999999),
    maxRecoveredEcalCells = cms.uint32(9999999),
    maxProblematicEcalCells = cms.uint32(9999999),
    maxBadHcalCells = cms.uint32(9999999),
    maxBadEcalCells = cms.uint32(9999999),
    maxProblematicHcalCells = cms.uint32(9999999),
    jetAlgorithm = cms.string('AntiKt'),
    rParam = cms.double(0.5),
    UseOnlyVertexTracks = cms.bool(False),
    UseOnlyOnePV = cms.bool(False),
    DzTrVtxMax = cms.double(0.0),
    DxyTrVtxMax = cms.double(0.0),
    MinVtxNdof = cms.int32(5),
    MaxVtxZ = cms.double(15.0),
    src = cms.InputTag("hltTowerMakerForAll"),
    subtractorName = cms.string(""),
    sumRecHits = cms.bool(False)
)