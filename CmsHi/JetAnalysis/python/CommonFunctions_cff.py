import FWCore.ParameterSet.Config as cms

# Turn of MC dependence in pat sequence
def removePatMCMatch(process):
    process.prod.remove(process.genPartons)
    process.prod.remove(process.heavyIonCleanedGenJets)
    process.prod.remove(process.hiPartons)
    process.prod.remove(process.patJetGenJetMatch)
    process.prod.remove(process.patJetPartonMatch)
    
    process.patJets.addGenPartonMatch   = False
    process.patJets.embedGenPartonMatch = False
    process.patJets.genPartonMatch      = ''
    process.patJets.addGenJetMatch      = False
    process.patJets.genJetMatch      = ''
    process.patJets.getJetMCFlavour     = False
    process.patJets.JetPartonMapSource  = ''
    return process

# Top Config to turn off all mc dependence
def disableMC(process):
    process.prod.remove(process.heavyIon)
    removePatMCMatch(process)
    return process

def hltFromREDIGI(process):
    process.hltanalysis.HLTProcessName      = "REDIGI"
    process.hltanalysis.l1GtObjectMapRecord = cms.InputTag("hltL1GtObjectMap::REDIGI")
    process.hltanalysis.l1GtReadoutRecord   = cms.InputTag("hltGtDigis::REDIGI")
    process.hltanalysis.hltresults          = cms.InputTag("TriggerResults::REDIGI")   
    return process

def overrideBeamSpot(process):
    process.GlobalTag.toGet = cms.VPSet(
        cms.PSet(record = cms.string("BeamSpotObjectsRcd"),
                 tag = cms.string("Realistic2.76ATeVCollisions_STARTUP_v0_mc"),
                 connect = cms.untracked.string("frontier://FrontierProd/CMS_COND_31X_BEAMSPOT")
                 ),
        )
    return process


def addRPFlat(process):
    process.GlobalTag.toGet.extend([
        cms.PSet(record = cms.string("HeavyIonRPRcd"),
                 tag = cms.string("RPFlatParams_Test_v0_offline"),
                 connect = cms.untracked.string("frontier://FrontierPrep/CMS_COND_TEMP"),
                 ),
        ])
    return process


def overrideGlobalTag(process):
    process.GlobalTag.toGet.extend([

        #==================== MC Tables ====================
        cms.PSet(record = cms.string("HeavyIonRcd"),
                 tag = cms.string("CentralityTable_HFhits40_AMPTOrgan_v0_offline"),
                 connect = cms.untracked.string("frontier://FrontierProd/CMS_COND_31X_PHYSICSTOOLS"),
                 label = cms.untracked.string("HFhitsAMPT_Organ")
                 ),
        cms.PSet(record = cms.string("HeavyIonRcd"),
                 tag = cms.string("CentralityTable_PixelHits40_AMPTOrgan_v0_offline"),
                 connect = cms.untracked.string("frontier://FrontierProd/CMS_COND_31X_PHYSICSTOOLS"),
                 label = cms.untracked.string("PixelHitsAMPT_Organ")
                 ),
        
        cms.PSet(record = cms.string("HeavyIonRcd"),
                 tag = cms.string("CentralityTable_HFhits40_HydjetBass_vv44x04_mc"),
                 connect = cms.untracked.string("frontier://FrontierProd/CMS_COND_31X_PHYSICSTOOLS"),
                 label = cms.untracked.string("HFhitsHydjet_Bass")
                                    ),
        cms.PSet(record = cms.string("HeavyIonRcd"),
                 tag = cms.string("CentralityTable_PixelHits40_HydjetBass_vv44x04_mc"),
                 connect = cms.untracked.string("frontier://FrontierProd/CMS_COND_31X_PHYSICSTOOLS"),
                 label = cms.untracked.string("PixelHitsHydjet_Bass")
                 ),               
        cms.PSet(record = cms.string("HeavyIonRcd"),
                 tag = cms.string("CentralityTable_Tracks40_HydjetBass_vv44x04_mc"),
                 connect = cms.untracked.string("frontier://FrontierProd/CMS_COND_31X_PHYSICSTOOLS"),
                 label = cms.untracked.string("TracksHydjet_Bass")
                 ),
        cms.PSet(record = cms.string("HeavyIonRcd"),
                 tag = cms.string("CentralityTable_PixelTracks40_HydjetBass_vv44x04_mc"),
                 connect = cms.untracked.string("frontier://FrontierProd/CMS_COND_31X_PHYSICSTOOLS"),
                 label = cms.untracked.string("PixelTracksHydjet_Bass")
                 ),

        cms.PSet(record = cms.string("HeavyIonRcd"),
                 tag = cms.string("CentralityTable_HFtowers40_HydjetBass_vv44x04_mc"),
                 connect = cms.untracked.string("frontier://FrontierProd/CMS_COND_31X_PHYSICSTOOLS"),
                 label = cms.untracked.string("HFtowersHydjet_Bass")   
                 ),        


    cms.PSet(record = cms.string("HeavyIonRcd"),
                              tag = cms.string("CentralityTable_HFhits40_HydjetDrum_vv44x05_mc"),
                              connect = cms.untracked.string("frontier://FrontierProd/CMS_COND_31X_PHYSICSTOOLS"),
                              label = cms.untracked.string("HFhitsHydjet_Drum")
                                                 ),
                cms.PSet(record = cms.string("HeavyIonRcd"),
                                          tag = cms.string("CentralityTable_PixelHits40_HydjetDrum_vv44x05_mc"),
                                          connect = cms.untracked.string("frontier://FrontierProd/CMS_COND_31X_PHYSICSTOOLS"),
                                          label = cms.untracked.string("PixelHitsHydjet_Drum")
                                          ),
                cms.PSet(record = cms.string("HeavyIonRcd"),
                                          tag = cms.string("CentralityTable_Tracks40_HydjetDrum_vv44x05_mc"),
                                          connect = cms.untracked.string("frontier://FrontierProd/CMS_COND_31X_PHYSICSTOOLS"),
                                          label = cms.untracked.string("TracksHydjet_Drum")
                                          ),
                cms.PSet(record = cms.string("HeavyIonRcd"),
                                          tag = cms.string("CentralityTable_PixelTracks40_HydjetDrum_vv44x05_mc"),
                                          connect = cms.untracked.string("frontier://FrontierProd/CMS_COND_31X_PHYSICSTOOLS"),
                                          label = cms.untracked.string("PixelTracksHydjet_Drum")
                                          ),

                cms.PSet(record = cms.string("HeavyIonRcd"),
                                          tag = cms.string("CentralityTable_HFtowers40_HydjetDrum_vv44x05_mc"),
                                          connect = cms.untracked.string("frontier://FrontierProd/CMS_COND_31X_PHYSICSTOOLS"),
                                          label = cms.untracked.string("HFtowersHydjet_Drum")
                                          ),

        #==================== JET CORRECTIONS

        cms.PSet(record = cms.string("JetCorrectionsRecord"),
#                 tag = cms.string("JetCorrectorParametersCollection_HI_PFTowers_hiGoodTightTracks_PythiaZ2_442p5_AK1PF"),
#                 connect = cms.untracked.string("sqlite_file:JEC_HI2760_CMSSW442pa9_2012.db"),
#                 connect = cms.untracked.string("sqlite_file:JEC_HI2760_CMSSW501_2012.db"),
                 
                 tag = cms.string("JetCorrectorParametersCollection_AK1PFTowers_hiIterativeTracks_HI_2760GeV_v3_offline"), 
                 connect = cms.untracked.string("frontier://FrontierProd/CMS_COND_31X_PHYSICSTOOLS"),


                              label = cms.untracked.string("AK1PF_hiIterativeTracks")
                 ),
        cms.PSet(record = cms.string("JetCorrectionsRecord"),
                 tag = cms.string("JetCorrectorParametersCollection_AK2PFTowers_hiIterativeTracks_HI_2760GeV_v3_offline"),
                 connect = cms.untracked.string("frontier://FrontierProd/CMS_COND_31X_PHYSICSTOOLS"),
                 label = cms.untracked.string("AK2PF_hiIterativeTracks")
                 ),
          cms.PSet(record = cms.string("JetCorrectionsRecord"),
                   tag = cms.string("JetCorrectorParametersCollection_AK3PFTowers_hiIterativeTracks_HI_2760GeV_v3_offline"),
                   connect = cms.untracked.string("frontier://FrontierProd/CMS_COND_31X_PHYSICSTOOLS"),
                   label = cms.untracked.string("AK3PF_hiIterativeTracks")
                   ),
        cms.PSet(record = cms.string("JetCorrectionsRecord"),
                 tag = cms.string("JetCorrectorParametersCollection_AK4PFTowers_hiIterativeTracks_HI_2760GeV_v3_offline"),
                 connect = cms.untracked.string("frontier://FrontierProd/CMS_COND_31X_PHYSICSTOOLS"),
                 label = cms.untracked.string("AK4PF_hiIterativeTracks")
                 ),
        cms.PSet(record = cms.string("JetCorrectionsRecord"),
                 tag = cms.string("JetCorrectorParametersCollection_AK5PFTowers_hiIterativeTracks_HI_2760GeV_v3_offline"),
                 connect = cms.untracked.string("frontier://FrontierProd/CMS_COND_31X_PHYSICSTOOLS"),
                 label = cms.untracked.string("AK5PF_hiIterativeTracks")
                 ),
        cms.PSet(record = cms.string("JetCorrectionsRecord"),
                 tag = cms.string("JetCorrectorParametersCollection_AK6PFTowers_hiIterativeTracks_HI_2760GeV_v3_offline"),
                 connect = cms.untracked.string("frontier://FrontierProd/CMS_COND_31X_PHYSICSTOOLS"),
                 label = cms.untracked.string("AK6PF_hiIterativeTracks")
                 ),

          cms.PSet(record = cms.string("JetCorrectionsRecord"),
                                    tag = cms.string("JetCorrectorParametersCollection_AK1Calo_HI_2760GeV_v3_offline"),
                                    connect = cms.untracked.string("frontier://FrontierProd/CMS_COND_31X_PHYSICSTOOLS"),
                                                 label = cms.untracked.string("AK1Calo_HI")
                                    ),
                cms.PSet(record = cms.string("JetCorrectionsRecord"),
                                          tag = cms.string("JetCorrectorParametersCollection_AK2Calo_HI_2760GeV_v3_offline"),
                                          connect = cms.untracked.string("frontier://FrontierProd/CMS_COND_31X_PHYSICSTOOLS"),
                                          label = cms.untracked.string("AK2Calo_HI")
                                          ),
                  cms.PSet(record = cms.string("JetCorrectionsRecord"),
                                              tag = cms.string("JetCorrectorParametersCollection_AK3Calo_HI_2760GeV_v3_offline"),
                                              connect = cms.untracked.string("frontier://FrontierProd/CMS_COND_31X_PHYSICSTOOLS"),
                                              label = cms.untracked.string("AK3Calo_HI")
                                              ),
                cms.PSet(record = cms.string("JetCorrectionsRecord"),
                                          tag = cms.string("JetCorrectorParametersCollection_AK4Calo_HI_2760GeV_v3_offline"),
                                          connect = cms.untracked.string("frontier://FrontierProd/CMS_COND_31X_PHYSICSTOOLS"),
                                          label = cms.untracked.string("AK4Calo_HI")
                                          ),
                cms.PSet(record = cms.string("JetCorrectionsRecord"),
                                          tag = cms.string("JetCorrectorParametersCollection_AK5Calo_HI_2760GeV_v3_offline"),
                                          connect = cms.untracked.string("frontier://FrontierProd/CMS_COND_31X_PHYSICSTOOLS"),
                                          label = cms.untracked.string("AK5Calo_HI")
                                          ),
                cms.PSet(record = cms.string("JetCorrectionsRecord"),
                                          tag = cms.string("JetCorrectorParametersCollection_AK6Calo_HI_2760GeV_v3_offline"),
                                          connect = cms.untracked.string("frontier://FrontierProd/CMS_COND_31X_PHYSICSTOOLS"),
                                          label = cms.untracked.string("AK6Calo_HI")
                                          ),
        
        cms.PSet(record = cms.string("JetCorrectionsRecord"),
                 tag = cms.string("JetCorrectorParametersCollection_IC5Calo_2760GeV_v0_offline"),
                 connect = cms.untracked.string("frontier://FrontierProd/CMS_COND_31X_PHYSICSTOOLS"),
                 label = cms.untracked.string("IC5Calo_2760GeV")
                 ),
        
#==================== DATA ONLY, FIXED RUN TAGS =====================================
# NOTHING
        ])
    
    return process


def overrideCentrality(process):    
    overrideGlobalTag(process)
    return process

                              
