import FWCore.ParameterSet.Config as cms


hiGoodTracks = cms.EDProducer("HiHackedAnalyticalTrackSelector",

    src = cms.InputTag("hiSelectedTracks"),
    keepAllTracks = cms.bool(False), ## if set to true tracks failing this filter are kept in the output
    beamspot = cms.InputTag("offlineBeamSpot"),

    vertices = cms.InputTag("hiSelectedVertex"),
    vtxNumber = cms.int32(0),
    vtxTracks = cms.uint32(0), ## at least 3 tracks
    vtxChi2Prob = cms.double(0.0), ## at least 1% chi2nprobability (if it has a chi2)

    copyTrajectories = cms.untracked.bool(True),
    copyExtras = cms.untracked.bool(False), ## set to false on AOD
    qualityBit = cms.string('highPurity'), ## set to '' or comment out if you don't want to set the bit

    # parameters for cutting on pterror/pt and number of valid hits
    min_relpterr = cms.double(0.05),
    min_nhits = cms.uint32(12),                           

    # parameters for adapted optimal cuts on chi2 and primary vertex compatibility
    chi2n_par = cms.double(99999.), # already applied in hiSelectedTracks
    res_par = cms.vdouble(99999., 99999.),
    d0_par1 = cms.vdouble(99999., 0.0),
    dz_par1 = cms.vdouble(99999., 0.0),
    d0_par2 = cms.vdouble(3, 0.0),
    dz_par2 = cms.vdouble(3, 0.0),
    # Boolean indicating if adapted primary vertex compatibility cuts are to be applied.
    applyAdaptedPVCuts = cms.bool(True),

    # Impact parameter absolute cuts.
    max_d0 = cms.double(1000),
    max_z0 = cms.double(1000),

    # Cuts on numbers of layers with hits/3D hits/lost hits. 
    minNumberLayers = cms.uint32(0),
    minNumber3DLayers = cms.uint32(0),
    maxNumberLostLayers = cms.uint32(99999)
)

hiGoodTightTracks = hiGoodTracks.clone(src = cms.InputTag("hiPostGlobalPrimTracks"),
                                       qualityBit = cms.string('highPurity'),
                                       min_nhits = cms.uint32(13),
                                       chi2n_par = cms.double(0.15))

hiGoodLooseTracks = hiGoodTracks.clone(src = cms.InputTag("hiPostGlobalPrimTracks"),
                                       qualityBit = cms.string('loose'),
                                       min_nhits = cms.uint32(12),
                                       chi2n_par = cms.double(0.15),
                                       d0_par2 = cms.vdouble(5.0, 0.0),
                                       dz_par2 = cms.vdouble(5.0, 0.0))

hiHighPtTracks = hiGoodTracks.clone(src = cms.InputTag("hiPostGlobalPrimTracks"),
                                    qualityBit = cms.string('tight'),
                                    min_relpterr = cms.double(0.06),
                                    min_nhits = cms.uint32(13),
                                    chi2n_par = cms.double(0.15),
                                    d0_par2 =cms.vdouble(999.0, 0.0),
                                    dz_par2 = cms.vdouble(999.0, 0.0))

hiLooseTracks = hiGoodTracks.clone(src = cms.InputTag("hiPostGlobalPrimTracks"),
                                   qualityBit = cms.string('loose'),
                                   min_relpterr = cms.double(0.10),
                                   min_nhits = cms.uint32(10),
                                   chi2n_par = cms.double(0.15),
                                   d0_par2 = cms.vdouble(8.0, 0.0),
                                   dz_par2 = cms.vdouble(8.0, 0.0))


## this is hiGoodTightTracks without vtx cut for systematics study
hiPreDTGoodTightTracks = hiGoodTracks.clone(src = cms.InputTag("hiPostGlobalPrimTracks"),
                                            qualityBit = cms.string(''),
                                            min_nhits = cms.uint32(13),
                                            chi2n_par = cms.double(0.15),
                                            d0_par2 =cms.vdouble(999.0, 0.0))

hiPreDZGoodTightTracks = hiGoodTracks.clone(src = cms.InputTag("hiPostGlobalPrimTracks"),
                                            qualityBit = cms.string(''),
                                            min_nhits = cms.uint32(13),
                                            chi2n_par = cms.double(0.15),
                                            dz_par2 =cms.vdouble(999.0, 0.0))

# this is a track collection that PF re-reco judegement (and PF reco)  is based on
hiPostGlobalPrimTracks = hiGoodTracks.clone(src = cms.InputTag("hiGlobalPrimTracks"),
                                            qualityBit = cms.string(''),
                                            min_relpterr = cms.double(0.06),
                                            min_nhits = cms.uint32(12),
                                            chi2n_par = cms.double(0.4),
                                            d0_par2 =cms.vdouble(999.0, 0.0),
                                            dz_par2 = cms.vdouble(999.0, 0.0))

# this is just to avoid duplicate collection produced on the fly for PF
hiPostGlobalPrimDumTracks = hiPostGlobalPrimTracks.clone()

hiGoodTracksSelection = cms.Sequence(hiGoodTracks)
hiGoodLooseTracksSelection = cms.Sequence(hiGoodLooseTracks)
hiGoodTightTracksSelection = cms.Sequence(hiGoodTightTracks)
hiHighPtTrackSelection = cms.Sequence(hiHighPtTracks)

hiPreDTGoodTightTracksSelection = cms.Sequence(hiPreDTGoodTightTracks)
hiPreDZGoodTightTracksSelection = cms.Sequence(hiPreDZGoodTightTracks)

hiPostGlobalPrimTracksSelection = cms.Sequence(hiPostGlobalPrimTracks)
hiPostGlobalPrimDumTracksSelection = cms.Sequence(hiPostGlobalPrimDumTracks)
