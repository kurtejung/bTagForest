import FWCore.ParameterSet.Config as cms

# Pat 
from PhysicsTools.PatAlgos.patHeavyIonSequences_cff import *



# Photons

makeHeavyIonPhotons.remove(interestingTrackEcalDetIds)
photonMatch.matched = cms.InputTag("hiGenParticles")

patPhotons.addPhotonID = cms.bool(False)
makeHeavyIonPhotons *= selectedPatPhotons


# Jets


patJets.jetSource  = cms.InputTag("iterativeConePu5CaloJets")
patJets.addBTagInfo         = True
patJets.addTagInfos         = True
patJets.addDiscriminators   = True
patJets.addAssociatedTracks = True
patJets.addJetCharge        = False
patJets.addJetID            = True
patJets.getJetMCFlavour     = True #true for MC - fills refparton_flavorForB
patJets.addGenPartonMatch   = True #true for MC - fills refparton_flavor
patJets.addGenJetMatch      = True #true for MC
patJets.embedGenJetMatch    = True
patJets.embedGenPartonMatch = True
patJets.embedCaloTowers	    = False

patJetCorrFactors.useNPV = False
# full reco

#icPu5patJets = patJets.clone(
#  jetSource = cms.InputTag("iterativeConePu5CaloJets"),
#  genJetMatch = cms.InputTag("icPu5match"),
#  genPartonMatch = cms.InputTag("icPu5parton"),
#  jetCorrFactorsSource = cms.VInputTag(cms.InputTag("icPu5corr"))
#  )
icPu5corr    = patJetCorrFactors.clone(src      = cms.InputTag("iterativeConePu5CaloJets"),
                                       levels   = cms.vstring('L2Relative','L3Absolute'),
                                       payload  = cms.string('IC5Calo_2760GeV'))

akPu5PFcorr = icPu5corr.clone(
  src = cms.InputTag("akPu5PFJets"),
  #payload = cms.string('AK5PF_hiIterativeTracks')
  )
akPu5PFpatJets = patJets.clone(
  jetSource = cms.InputTag("akPu5PFJets"),
  genJetMatch = cms.InputTag("akPu5PFmatch"),
  genPartonMatch = cms.InputTag("akPu5PFparton"),
  jetCorrFactorsSource = cms.VInputTag(cms.InputTag("akPu5PFcorr"))
  )

akPu3PFcorr = icPu5corr.clone()
akPu3corr = icPu5corr.clone()

#akPu3PFcorr = icPu5corr.clone(
#  src = cms.InputTag("akPu3PFJets"),
#  payload = cms.string('AK3PF_hiIterativeTracks')
#  )

#akPu3PFpatJets = patJets.clone(
#  jetSource = cms.InputTag("akPu3PFJets"),
#  genJetMatch = cms.InputTag("akPu3PFmatch"),
#  genPartonMatch = cms.InputTag("akPu3PFparton"),
#  jetCorrFactorsSource = cms.VInputTag(cms.InputTag("akPu3PFcorr"))
#  )

#akPu5corr = icPu5corr.clone(
#    src = cms.InputTag("akPu5CaloJets"),
#    payload = cms.string('AK5Calo')
#    )

#akPu5patJets = patJets.clone(
#    jetSource = cms.InputTag("akPu5CaloJets"),
#    genJetMatch = cms.InputTag("akPu5match"),
#    genPartonMatch = cms.InputTag("akPu5parton"),
#    jetCorrFactorsSource = cms.VInputTag(cms.InputTag("akPu5corr"))
#    )

#akPu3corr = icPu5corr.clone(
#    src = cms.InputTag("akPu3CaloJets"),
#    payload = cms.string('AK5Calo')
#    )

#akPu3patJets = patJets.clone(
#    jetSource = cms.InputTag("akPu3CaloJets"),
#    genJetMatch = cms.InputTag("akPu3match"),
#    genPartonMatch = cms.InputTag("akPu3parton"),
#    jetCorrFactorsSource = cms.VInputTag(cms.InputTag("akPu3corr"))
#    )



# mc matching
patJetPartonMatch.matched = cms.InputTag("hiPartons")

icPu5clean = heavyIonCleanedGenJets.clone( src = cms.InputTag('iterativeCone5HiGenJets') )
icPu5match = patJetGenJetMatch.clone(
  src = cms.InputTag("iterativeConePu5CaloJets"),
  matched = cms.InputTag("icPu5clean")
  )
icPu5parton = patJetPartonMatch.clone(
  src = cms.InputTag("iterativeConePu5CaloJets")
	)


akPu5PFclean = heavyIonCleanedGenJets.clone( src = cms.InputTag('ak5HiGenJets') ) 
akPu5PFmatch = patJetGenJetMatch.clone(
  src = cms.InputTag("akPu5PFJets"),
  matched = cms.InputTag("akPu5PFclean")
  )
akPu5PFparton = patJetPartonMatch.clone(
  src = cms.InputTag("akPu5PFJets")
	)

akPu3PFclean = heavyIonCleanedGenJets.clone( src = cms.InputTag('ak3HiGenJets') ) 
akPu3PFmatch = patJetGenJetMatch.clone(
  src = cms.InputTag("akPu3PFJets"),
  matched = cms.InputTag("akPu3PFclean")
  )
akPu3PFparton = patJetPartonMatch.clone(
  src = cms.InputTag("akPu3PFJets")
	)

akPu5match = patJetGenJetMatch.clone(
    src = cms.InputTag("akPu5CaloJets"),
    matched = cms.InputTag("akPu5PFclean")
    )
akPu5parton = patJetPartonMatch.clone(
    src = cms.InputTag("akPu5CaloJets")
    )

akPu3match = patJetGenJetMatch.clone(
    src = cms.InputTag("akPu3CaloJets"),
    matched = cms.InputTag("akPu3PFclean")
    )
akPu3parton = patJetPartonMatch.clone(
    src = cms.InputTag("akPu3CaloJets")
    )

from RecoJets.JetAssociationProducers.ak5JTA_cff import *
from RecoBTag.Configuration.RecoBTag_cff import *
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ calo jet
#### b-tagging:
# b-tagging general configuration
# @@@@@@@@@ calo jet
#### b-tagging:
# b-tagging general configuration
icPu5JetTracksAssociatorAtVertex        = ak5JetTracksAssociatorAtVertex.clone()
icPu5JetTracksAssociatorAtVertex.jets   = cms.InputTag("iterativeConePu5CaloJets")
icPu5JetTracksAssociatorAtVertex.tracks = cms.InputTag("generalTracks")

# impact parameter b-tag
icPu5ImpactParameterTagInfos                = impactParameterTagInfos.clone()
icPu5ImpactParameterTagInfos.jetTracks      = cms.InputTag("icPu5JetTracksAssociatorAtVertex")
icPu5ImpactParameterTagInfos.primaryVertex  = cms.InputTag("offlinePrimaryVertices")

icPu5TrackCountingHighEffBJetTags          = trackCountingHighEffBJetTags.clone()
icPu5TrackCountingHighEffBJetTags.tagInfos = cms.VInputTag(cms.InputTag("icPu5ImpactParameterTagInfos"))
icPu5TrackCountingHighPurBJetTags          = trackCountingHighPurBJetTags.clone()
icPu5TrackCountingHighPurBJetTags.tagInfos = cms.VInputTag(cms.InputTag("icPu5ImpactParameterTagInfos"))
icPu5JetProbabilityBJetTags                = jetProbabilityBJetTags.clone()
icPu5JetProbabilityBJetTags.tagInfos       = cms.VInputTag(cms.InputTag("icPu5ImpactParameterTagInfos"))
icPu5JetBProbabilityBJetTags               = jetBProbabilityBJetTags.clone()
icPu5JetBProbabilityBJetTags.tagInfos      = cms.VInputTag(cms.InputTag("icPu5ImpactParameterTagInfos"))

# secondary vertex b-tag
icPu5SecondaryVertexTagInfos                     = secondaryVertexTagInfos.clone()
icPu5SecondaryVertexTagInfos.trackIPTagInfos     = cms.InputTag("icPu5ImpactParameterTagInfos")
icPu5SimpleSecondaryVertexBJetTags               = simpleSecondaryVertexBJetTags.clone()
icPu5SimpleSecondaryVertexBJetTags.tagInfos      = cms.VInputTag(cms.InputTag("icPu5SecondaryVertexTagInfos"))
icPu5CombinedSecondaryVertexBJetTags             = combinedSecondaryVertexBJetTags.clone()
icPu5CombinedSecondaryVertexBJetTags.tagInfos    = cms.VInputTag(cms.InputTag("icPu5ImpactParameterTagInfos"),
                                                                         cms.InputTag("icPu5SecondaryVertexTagInfos"))
icPu5CombinedSecondaryVertexMVABJetTags          = combinedSecondaryVertexMVABJetTags.clone()
icPu5CombinedSecondaryVertexMVABJetTags.tagInfos = cms.VInputTag(cms.InputTag("icPu5ImpactParameterTagInfos"),
                                                                         cms.InputTag("icPu5SecondaryVertexTagInfos"))

# soft muon b-tag
icPu5SoftMuonTagInfos                = softMuonTagInfos.clone()
icPu5SoftMuonTagInfos.jets           = cms.InputTag("iterativeConePu5CaloJets")
icPu5SoftMuonTagInfos.primaryVertex  = cms.InputTag("offlinePrimaryVertices")
icPu5SoftMuonBJetTags                = softMuonBJetTags.clone()
icPu5SoftMuonBJetTags.tagInfos       = cms.VInputTag(cms.InputTag("icPu5SoftMuonTagInfos"))
icPu5SoftMuonByIP3dBJetTags          = softMuonByIP3dBJetTags.clone()
icPu5SoftMuonByIP3dBJetTags.tagInfos = cms.VInputTag(cms.InputTag("icPu5SoftMuonTagInfos"))
icPu5SoftMuonByPtBJetTags            = softMuonByPtBJetTags.clone()
icPu5SoftMuonByPtBJetTags.tagInfos   = cms.VInputTag(cms.InputTag("icPu5SoftMuonTagInfos"))

# ghost tracks
icPu5GhostTrackVertexTagInfos                 = ghostTrackVertexTagInfos.clone()
icPu5GhostTrackVertexTagInfos.trackIPTagInfos = cms.InputTag("icPu5ImpactParameterTagInfos")
icPu5GhostTrackBJetTags                       = ghostTrackBJetTags.clone()
icPu5GhostTrackBJetTags.tagInfos              = cms.VInputTag(cms.InputTag("icPu5ImpactParameterTagInfos"),
                                                                      cms.InputTag("icPu5GhostTrackVertexTagInfos"))
# prepare a path running the new modules
icPu5JetTracksAssociator = cms.Sequence(icPu5JetTracksAssociatorAtVertex)
icPu5JetBtaggingIP       = cms.Sequence(icPu5ImpactParameterTagInfos * (icPu5TrackCountingHighEffBJetTags +
                                                                                        icPu5TrackCountingHighPurBJetTags +
                                                                                        icPu5JetProbabilityBJetTags +
                                                                                        icPu5JetBProbabilityBJetTags
                                                                                        )
                                                )

icPu5JetBtaggingSV = cms.Sequence(icPu5ImpactParameterTagInfos *
                                          icPu5SecondaryVertexTagInfos * (icPu5SimpleSecondaryVertexBJetTags +
                                                                                  icPu5CombinedSecondaryVertexBJetTags +
                                                                                  icPu5CombinedSecondaryVertexMVABJetTags
                                                                                  )
                                          +icPu5GhostTrackVertexTagInfos
                                          *icPu5GhostTrackBJetTags
                                          )


icPu5JetBtaggingMu = cms.Sequence(icPu5SoftMuonTagInfos * (icPu5SoftMuonBJetTags +
                                                                           icPu5SoftMuonByIP3dBJetTags +
                                                                           icPu5SoftMuonByPtBJetTags
                                                                           )
                                          )

icPu5JetBtagging = cms.Sequence(icPu5JetBtaggingIP 
                                        *icPu5JetBtaggingSV 
                                        *icPu5JetBtaggingMu
                                        )
#----------------------


#----------------------

icPu5clean   = heavyIonCleanedGenJets.clone(src = cms.InputTag('iterativeCone5HiGenJets')) # cleans the jets, but NOT the partons
icPu5match   = patJetGenJetMatch.clone(src      = cms.InputTag("iterativeConePu5CaloJets"),
                                                       matched  = cms.InputTag("icPu5clean"))

icPu5parton  = patJetPartonMatch.clone(src      = cms.InputTag("iterativeConePu5CaloJets"))

# ----- flavour bit
icPu5PatJetPartonAssociation       = patJetPartonAssociation.clone(jets    = cms.InputTag("iterativeConePu5CaloJets"),
                                                                                   partons = cms.InputTag("genPartons"),
                                                                                   coneSizeToAssociate = cms.double(0.4))
icPu5PatJetFlavourAssociation      = patJetFlavourAssociation.clone(srcByReference = cms.InputTag("icPu5PatJetPartonAssociation"))

icPu5PatJetFlavourId               = cms.Sequence(icPu5PatJetPartonAssociation*icPu5PatJetFlavourAssociation)

#-------

icPu5patJets = patJets.clone(jetSource            = cms.InputTag("iterativeConePu5CaloJets"),
                                             genJetMatch          = cms.InputTag("icPu5match"),
                                             genPartonMatch       = cms.InputTag("icPu5parton"),
                                             jetCorrFactorsSource = cms.VInputTag(cms.InputTag("icPu5corr")),
                                             JetPartonMapSource   = cms.InputTag("icPu5PatJetFlavourAssociation"),
                                             trackAssociationSource = cms.InputTag("icPu5JetTracksAssociatorAtVertex"),
                                             discriminatorSources = cms.VInputTag(cms.InputTag("icPu5CombinedSecondaryVertexBJetTags"),
                                                                                  cms.InputTag("icPu5CombinedSecondaryVertexMVABJetTags"),
                                                                                  cms.InputTag("icPu5JetBProbabilityBJetTags"),
                                                                                  cms.InputTag("icPu5JetProbabilityBJetTags"),
                                                                                  cms.InputTag("icPu5SoftMuonByPtBJetTags"),                
                                                                                  cms.InputTag("icPu5SoftMuonByIP3dBJetTags"),
                                                                                  cms.InputTag("icPu5TrackCountingHighEffBJetTags"),
                                                                                  cms.InputTag("icPu5TrackCountingHighPurBJetTags"),
                                                                                  ),
                                             )


#### B-tagging for this bit:
# b-tagging general configuration
akPu3PFJetTracksAssociatorAtVertex        = ak5JetTracksAssociatorAtVertex.clone()
akPu3PFJetTracksAssociatorAtVertex.jets   = cms.InputTag("akPu3PFJets")
akPu3PFJetTracksAssociatorAtVertex.tracks = cms.InputTag("generalTracks")
# impact parameter b-tag
akPu3PFImpactParameterTagInfos               = impactParameterTagInfos.clone()
akPu3PFImpactParameterTagInfos.jetTracks     = cms.InputTag("akPu3PFJetTracksAssociatorAtVertex")
akPu3PFImpactParameterTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akPu3PFTrackCountingHighEffBJetTags          = trackCountingHighEffBJetTags.clone()
akPu3PFTrackCountingHighEffBJetTags.tagInfos = cms.VInputTag(cms.InputTag("akPu3PFImpactParameterTagInfos"))
akPu3PFTrackCountingHighPurBJetTags          = trackCountingHighPurBJetTags.clone()
akPu3PFTrackCountingHighPurBJetTags.tagInfos = cms.VInputTag(cms.InputTag("akPu3PFImpactParameterTagInfos"))
akPu3PFJetProbabilityBJetTags                = jetProbabilityBJetTags.clone()
akPu3PFJetProbabilityBJetTags.tagInfos       = cms.VInputTag(cms.InputTag("akPu3PFImpactParameterTagInfos"))
akPu3PFJetBProbabilityBJetTags               = jetBProbabilityBJetTags.clone()
akPu3PFJetBProbabilityBJetTags.tagInfos      = cms.VInputTag(cms.InputTag("akPu3PFImpactParameterTagInfos"))

#negative impact parameter
from RecoBTag.ImpactParameter.positiveOnlyJetProbabilityComputer_cfi import *
from RecoBTag.ImpactParameter.positiveOnlyJetProbabilityJetTags_cfi import *
from RecoBTag.ImpactParameter.negativeOnlyJetProbabilityComputer_cfi import *
from RecoBTag.ImpactParameter.negativeOnlyJetProbabilityJetTags_cfi import *
#from RecoBTag.ImpactParameterLearning.negativeTrackCountingHighPurJetTags_cfi import *
from RecoBTag.ImpactParameter.negativeTrackCountingHighEffJetTags_cfi import *
from RecoBTag.ImpactParameter.negativeTrackCountingHighPur_cfi import *
from RecoBTag.ImpactParameter.positiveOnlyJetBProbabilityComputer_cfi import *
from RecoBTag.ImpactParameter.positiveOnlyJetBProbabilityJetTags_cfi import *
from RecoBTag.ImpactParameter.negativeOnlyJetBProbabilityComputer_cfi import *
from RecoBTag.ImpactParameter.negativeOnlyJetBProbabilityJetTags_cfi import *

akPu3PFPositiveOnlyJetProbabilityJetTags     =       positiveOnlyJetProbabilityJetTags.clone()  
akPu3PFNegativeOnlyJetProbabilityJetTags     =       negativeOnlyJetProbabilityJetTags.clone()    
akPu3PFNegativeTrackCountingHighEffJetTags   =       negativeTrackCountingHighEffJetTags.clone()  
akPu3PFNegativeTrackCountingHighPur          =       negativeTrackCountingHighPur.clone()         
akPu3PFNegativeOnlyJetBProbabilityJetTags    =       negativeOnlyJetBProbabilityJetTags.clone()
akPu3PFPositiveOnlyJetBProbabilityJetTags    =       positiveOnlyJetBProbabilityJetTags.clone()

akPu3PFPositiveOnlyJetProbabilityJetTags.tagInfos   = cms.VInputTag(cms.InputTag("akPu3PFImpactParameterTagInfos"))
akPu3PFNegativeOnlyJetProbabilityJetTags.tagInfos   = cms.VInputTag(cms.InputTag("akPu3PFImpactParameterTagInfos"))
akPu3PFNegativeTrackCountingHighEffJetTags.tagInfos = cms.VInputTag(cms.InputTag("akPu3PFImpactParameterTagInfos"))
akPu3PFNegativeTrackCountingHighPur.tagInfos        = cms.VInputTag(cms.InputTag("akPu3PFImpactParameterTagInfos"))   
akPu3PFNegativeOnlyJetBProbabilityJetTags.tagInfos  = cms.VInputTag(cms.InputTag("akPu3PFImpactParameterTagInfos"))
akPu3PFPositiveOnlyJetBProbabilityJetTags.tagInfos  = cms.VInputTag(cms.InputTag("akPu3PFImpactParameterTagInfos"))



# secondary vertex b-tag
akPu3PFSecondaryVertexTagInfos                     = secondaryVertexTagInfos.clone()
akPu3PFSecondaryVertexTagInfos.trackIPTagInfos     = cms.InputTag("akPu3PFImpactParameterTagInfos")
akPu3PFSimpleSecondaryVertexHighEffBJetTags               = simpleSecondaryVertexHighEffBJetTags.clone()
akPu3PFSimpleSecondaryVertexHighEffBJetTags.tagInfos      = cms.VInputTag(cms.InputTag("akPu3PFSecondaryVertexTagInfos"))
akPu3PFSimpleSecondaryVertexHighPurBJetTags               = simpleSecondaryVertexHighPurBJetTags.clone()
akPu3PFSimpleSecondaryVertexHighPurBJetTags.tagInfos      = cms.VInputTag(cms.InputTag("akPu3PFSecondaryVertexTagInfos"))
akPu3PFCombinedSecondaryVertexBJetTags             = combinedSecondaryVertexBJetTags.clone()
akPu3PFCombinedSecondaryVertexBJetTags.tagInfos    = cms.VInputTag(cms.InputTag("akPu3PFImpactParameterTagInfos"), 
                                                                   cms.InputTag("akPu3PFSecondaryVertexTagInfos"))
akPu3PFCombinedSecondaryVertexMVABJetTags          = combinedSecondaryVertexMVABJetTags.clone()
akPu3PFCombinedSecondaryVertexMVABJetTags.tagInfos = cms.VInputTag(cms.InputTag("akPu3PFImpactParameterTagInfos"), 
                                                                   cms.InputTag("akPu3PFSecondaryVertexTagInfos"))

# secondary vertex negative taggers
from RecoBTag.SecondaryVertex.secondaryVertexNegativeTagInfos_cfi import *
from RecoBTag.SecondaryVertex.simpleSecondaryVertexNegativeHighEffBJetTags_cfi import *
from RecoBTag.SecondaryVertex.simpleSecondaryVertexNegativeHighPurBJetTags_cfi import *
from RecoBTag.SecondaryVertex.combinedSecondaryVertexNegativeES_cfi import *
from RecoBTag.SecondaryVertex.combinedSecondaryVertexNegativeBJetTags_cfi import *
from RecoBTag.SecondaryVertex.combinedSecondaryVertexPositiveES_cfi import *
from RecoBTag.SecondaryVertex.combinedSecondaryVertexPositiveBJetTags_cfi import *

akPu3PFSecondaryVertexNegativeTagInfos                     = secondaryVertexNegativeTagInfos.clone()
akPu3PFSecondaryVertexNegativeTagInfos.trackIPTagInfos     = cms.InputTag("akPu3PFImpactParameterTagInfos")
akPu3PFSimpleSecondaryVertexNegativeHighEffBJetTags               = simpleSecondaryVertexNegativeHighEffBJetTags.clone()
akPu3PFSimpleSecondaryVertexNegativeHighEffBJetTags.tagInfos      = cms.VInputTag(cms.InputTag("akPu3PFSecondaryVertexNegativeTagInfos"))
akPu3PFSimpleSecondaryVertexNegativeHighPurBJetTags               = simpleSecondaryVertexNegativeHighPurBJetTags.clone()
akPu3PFSimpleSecondaryVertexNegativeHighPurBJetTags.tagInfos      = cms.VInputTag(cms.InputTag("akPu3PFSecondaryVertexNegativeTagInfos"))
akPu3PFCombinedSecondaryVertexNegativeBJetTags                    = combinedSecondaryVertexNegativeBJetTags.clone()
akPu3PFCombinedSecondaryVertexNegativeBJetTags.tagInfos    = cms.VInputTag(cms.InputTag("akPu3PFImpactParameterTagInfos"), 
                                                                           cms.InputTag("akPu3PFSecondaryVertexNegativeTagInfos"))
akPu3PFCombinedSecondaryVertexPositiveBJetTags                    = combinedSecondaryVertexPositiveBJetTags.clone()
akPu3PFCombinedSecondaryVertexPositiveBJetTags.tagInfos    = cms.VInputTag(cms.InputTag("akPu3PFImpactParameterTagInfos"), 
                                                                           cms.InputTag("akPu3PFSecondaryVertexTagInfos"))

# soft muon b-tag
akPu3PFSoftMuonTagInfos                = softMuonTagInfos.clone()
akPu3PFSoftMuonTagInfos.jets           = cms.InputTag("akPu3PFJets")
akPu3PFSoftMuonTagInfos.primaryVertex  = cms.InputTag("offlinePrimaryVertices")
akPu3PFSoftMuonBJetTags                = softMuonBJetTags.clone()
akPu3PFSoftMuonBJetTags.tagInfos       = cms.VInputTag(cms.InputTag("akPu3PFSoftMuonTagInfos"))
akPu3PFSoftMuonByIP3dBJetTags          = softMuonByIP3dBJetTags.clone()
akPu3PFSoftMuonByIP3dBJetTags.tagInfos = cms.VInputTag(cms.InputTag("akPu3PFSoftMuonTagInfos"))
akPu3PFSoftMuonByPtBJetTags            = softMuonByPtBJetTags.clone()
akPu3PFSoftMuonByPtBJetTags.tagInfos   = cms.VInputTag(cms.InputTag("akPu3PFSoftMuonTagInfos"))

from RecoBTag.SoftLepton.negativeSoftLeptonByPtES_cfi import *
from RecoBTag.SoftLepton.negativeSoftMuonByPtBJetTags_cfi import *
from RecoBTag.SoftLepton.positiveSoftLeptonByPtES_cfi import *
from RecoBTag.SoftLepton.positiveSoftMuonByPtBJetTags_cfi import *

akPu3PFPositiveSoftMuonByPtBJetTags                = positiveSoftLeptonByPtBJetTags.clone()
akPu3PFPositiveSoftMuonByPtBJetTags.tagInfos       = cms.VInputTag(cms.InputTag("akPu3PFSoftMuonTagInfos"))

# soft muon negative taggers
akPu3PFNegativeSoftMuonByPtBJetTags                = negativeSoftLeptonByPtBJetTags.clone()
akPu3PFNegativeSoftMuonByPtBJetTags.tagInfos       = cms.VInputTag(cms.InputTag("akPu3PFSoftMuonTagInfos"))

# ghost tracks
'''
akPu3PFGhostTrackVertexTagInfos                 = ghostTrackVertexTagInfos.clone()
akPu3PFGhostTrackVertexTagInfos.trackIPTagInfos = cms.InputTag("akPu3PFImpactParameterTagInfos")
akPu3PFGhostTrackBJetTags                       = ghostTrackBJetTags.clone()
akPu3PFGhostTrackBJetTags.tagInfos              = cms.VInputTag(cms.InputTag("akPu3PFImpactParameterTagInfos"),
                                                                cms.InputTag("akPu3PFGhostTrackVertexTagInfos"))
'''

# prepare a path running the new modules
akPu3PFJetTracksAssociator = cms.Sequence(akPu3PFJetTracksAssociatorAtVertex)
akPu3PFJetBtaggingIP       = cms.Sequence(akPu3PFImpactParameterTagInfos * (akPu3PFTrackCountingHighEffBJetTags +
                                                                            akPu3PFTrackCountingHighPurBJetTags +
                                                                            akPu3PFJetProbabilityBJetTags +
                                                                            akPu3PFJetBProbabilityBJetTags +
                                                                            akPu3PFPositiveOnlyJetProbabilityJetTags +
                                                                            akPu3PFNegativeOnlyJetProbabilityJetTags +
                                                                            akPu3PFNegativeTrackCountingHighEffJetTags +
                                                                            akPu3PFNegativeTrackCountingHighPur +
                                                                            akPu3PFNegativeOnlyJetBProbabilityJetTags +
                                                                            akPu3PFPositiveOnlyJetBProbabilityJetTags
                                                                                        )
                                                )

akPu3PFJetBtaggingSV = cms.Sequence(akPu3PFImpactParameterTagInfos *
                                    akPu3PFSecondaryVertexTagInfos * (akPu3PFSimpleSecondaryVertexHighEffBJetTags +
                                                                      akPu3PFSimpleSecondaryVertexHighPurBJetTags +
                                                                      akPu3PFCombinedSecondaryVertexBJetTags +
                                                                      akPu3PFCombinedSecondaryVertexMVABJetTags
                                                                      )
                                    #+akPu3PFGhostTrackVertexTagInfos
                                    #*akPu3PFGhostTrackBJetTags
                                    )

akPu3PFJetBtaggingNegSV = cms.Sequence(akPu3PFImpactParameterTagInfos *
                                       akPu3PFSecondaryVertexNegativeTagInfos * (akPu3PFSimpleSecondaryVertexNegativeHighEffBJetTags +
                                                                                 akPu3PFSimpleSecondaryVertexNegativeHighPurBJetTags +
                                                                                 akPu3PFCombinedSecondaryVertexNegativeBJetTags +
                                                                                 akPu3PFCombinedSecondaryVertexPositiveBJetTags 
                                                                                 )
                                       )


akPu3PFJetBtaggingMu = cms.Sequence(akPu3PFSoftMuonTagInfos * (akPu3PFSoftMuonBJetTags +
                                                               akPu3PFSoftMuonByIP3dBJetTags +
                                                               akPu3PFSoftMuonByPtBJetTags +
                                                               akPu3PFNegativeSoftMuonByPtBJetTags +
                                                               akPu3PFPositiveSoftMuonByPtBJetTags
                                                               )
                                          )

akPu3PFJetBtagging = cms.Sequence(akPu3PFJetBtaggingIP 
                                  *akPu3PFJetBtaggingSV 
                                  *akPu3PFJetBtaggingNegSV
                                  *akPu3PFJetBtaggingMu
                                  )

#__________________________________________________________
# ----- flavour bit
akPu3PFPatJetPartonAssociation       = patJetPartonAssociation.clone(jets    = cms.InputTag("akPu3PFJets"),
                                                                                     partons = cms.InputTag("genPartons"),
                                                                                     coneSizeToAssociate = cms.double(0.4))
akPu3PFPatJetFlavourAssociation      = patJetFlavourAssociation.clone(srcByReference = cms.InputTag("akPu3PFPatJetPartonAssociation"))

akPu3PFPatJetFlavourId               = cms.Sequence(akPu3PFPatJetPartonAssociation*akPu3PFPatJetFlavourAssociation)
#
#-------
#akPu3PFcorr = patJetCorrFactors.clone(src     = cms.InputTag("akPu3PFJets"),
#                                      levels  = cms.vstring('L2Relative','L3Absolute'),
#                                      payload = cms.string('AK3PFTowers_hiGoodTightTracks')
#                                                      )
akPu3PFclean   = heavyIonCleanedGenJets.clone(src = cms.InputTag('ak3HiGenJets'))
akPu3PFmatch   = patJetGenJetMatch.clone(src      = cms.InputTag("akPu3PFJets"),
                                                         matched  = cms.InputTag("akPu3PFclean"))
akPu3PFparton  = patJetPartonMatch.clone(src      = cms.InputTag("akPu3PFJets"))
akPu3PFpatJets = patJets.clone(jetSource            = cms.InputTag("akPu3PFJets"),
                                               genJetMatch          = cms.InputTag("akPu3PFmatch"),
                                               genPartonMatch       = cms.InputTag("akPu3PFparton"),
                                               jetCorrFactorsSource = cms.VInputTag(cms.InputTag("akPu3PFcorr")),
                                               JetPartonMapSource   = cms.InputTag("akPu3PFPatJetFlavourAssociation"),
                                               trackAssociationSource = cms.InputTag("akPu3PFJetTracksAssociatorAtVertex"),
                                               discriminatorSources = cms.VInputTag(cms.InputTag("akPu3PFSimpleSecondaryVertexHighEffBJetTags"),
                                                                                    cms.InputTag("akPu3PFSimpleSecondaryVertexHighPurBJetTags"),
                                                                                    cms.InputTag("akPu3PFCombinedSecondaryVertexBJetTags"),
                                                                                    cms.InputTag("akPu3PFCombinedSecondaryVertexMVABJetTags"),
                                                                                    cms.InputTag("akPu3PFJetBProbabilityBJetTags"),
                                                                                    cms.InputTag("akPu3PFJetProbabilityBJetTags"),
                                                                                    cms.InputTag("akPu3PFSoftMuonByPtBJetTags"),                
                                                                                    cms.InputTag("akPu3PFSoftMuonByIP3dBJetTags"),
                                                                                    cms.InputTag("akPu3PFTrackCountingHighEffBJetTags"),
                                                                                    cms.InputTag("akPu3PFTrackCountingHighPurBJetTags"),
                                                                                    ),
                                               )


#### B-tagging for this bit:
# b-tagging general configuration
akPu5PFJetTracksAssociatorAtVertex        = ak5JetTracksAssociatorAtVertex.clone()
akPu5PFJetTracksAssociatorAtVertex.jets   = cms.InputTag("akPu5PFJets")
akPu5PFJetTracksAssociatorAtVertex.tracks = cms.InputTag("generalTracks")
# impact parameter b-tag
akPu5PFImpactParameterTagInfos               = impactParameterTagInfos.clone()
akPu5PFImpactParameterTagInfos.jetTracks     = cms.InputTag("akPu5PFJetTracksAssociatorAtVertex")
akPu5PFImpactParameterTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
akPu5PFTrackCountingHighEffBJetTags          = trackCountingHighEffBJetTags.clone()
akPu5PFTrackCountingHighEffBJetTags.tagInfos = cms.VInputTag(cms.InputTag("akPu5PFImpactParameterTagInfos"))
akPu5PFTrackCountingHighPurBJetTags          = trackCountingHighPurBJetTags.clone()
akPu5PFTrackCountingHighPurBJetTags.tagInfos = cms.VInputTag(cms.InputTag("akPu5PFImpactParameterTagInfos"))
akPu5PFJetProbabilityBJetTags                = jetProbabilityBJetTags.clone()
akPu5PFJetProbabilityBJetTags.tagInfos       = cms.VInputTag(cms.InputTag("akPu5PFImpactParameterTagInfos"))
akPu5PFJetBProbabilityBJetTags               = jetBProbabilityBJetTags.clone()
akPu5PFJetBProbabilityBJetTags.tagInfos      = cms.VInputTag(cms.InputTag("akPu5PFImpactParameterTagInfos"))

#negative impact parameter
#from RecoBTag.ImpactParameter.positiveOnlyJetProbabilityJetTags_cfi import *
#from RecoBTag.ImpactParameter.negativeOnlyJetProbabilityJetTags_cfi import *
#from RecoBTag.ImpactParameter.negativeTrackCountingHighEffJetTags_cfi import *
#from RecoBTag.ImpactParameter.negativeTrackCountingHighPur_cfi import *
#from RecoBTag.ImpactParameter.negativeOnlyJetBProbabilityJetTags_cfi import *

akPu5PFPositiveOnlyJetProbabilityJetTags     =       positiveOnlyJetProbabilityJetTags.clone()  
akPu5PFNegativeOnlyJetProbabilityJetTags     =       negativeOnlyJetProbabilityJetTags.clone()    
akPu5PFNegativeTrackCountingHighEffJetTags   =       negativeTrackCountingHighEffJetTags.clone()  
akPu5PFNegativeTrackCountingHighPur          =       negativeTrackCountingHighPur.clone()         
akPu5PFNegativeOnlyJetBProbabilityJetTags    =       negativeOnlyJetBProbabilityJetTags.clone()
akPu5PFPositiveOnlyJetBProbabilityJetTags    =       positiveOnlyJetBProbabilityJetTags.clone()

akPu5PFPositiveOnlyJetProbabilityJetTags.tagInfos   = cms.VInputTag(cms.InputTag("akPu5PFImpactParameterTagInfos"))
akPu5PFNegativeOnlyJetProbabilityJetTags.tagInfos   = cms.VInputTag(cms.InputTag("akPu5PFImpactParameterTagInfos"))
akPu5PFNegativeTrackCountingHighEffJetTags.tagInfos = cms.VInputTag(cms.InputTag("akPu5PFImpactParameterTagInfos"))
akPu5PFNegativeTrackCountingHighPur.tagInfos        = cms.VInputTag(cms.InputTag("akPu5PFImpactParameterTagInfos"))   
akPu5PFNegativeOnlyJetBProbabilityJetTags.tagInfos  = cms.VInputTag(cms.InputTag("akPu5PFImpactParameterTagInfos"))
akPu5PFPositiveOnlyJetBProbabilityJetTags.tagInfos  = cms.VInputTag(cms.InputTag("akPu5PFImpactParameterTagInfos"))



# secondary vertex b-tag
akPu5PFSecondaryVertexTagInfos                     = secondaryVertexTagInfos.clone()
akPu5PFSecondaryVertexTagInfos.trackIPTagInfos     = cms.InputTag("akPu5PFImpactParameterTagInfos")
akPu5PFSimpleSecondaryVertexHighEffBJetTags               = simpleSecondaryVertexHighEffBJetTags.clone()
akPu5PFSimpleSecondaryVertexHighEffBJetTags.tagInfos      = cms.VInputTag(cms.InputTag("akPu5PFSecondaryVertexTagInfos"))
akPu5PFSimpleSecondaryVertexHighPurBJetTags               = simpleSecondaryVertexHighPurBJetTags.clone()
akPu5PFSimpleSecondaryVertexHighPurBJetTags.tagInfos      = cms.VInputTag(cms.InputTag("akPu5PFSecondaryVertexTagInfos"))
akPu5PFCombinedSecondaryVertexBJetTags             = combinedSecondaryVertexBJetTags.clone()
akPu5PFCombinedSecondaryVertexBJetTags.tagInfos    = cms.VInputTag(cms.InputTag("akPu5PFImpactParameterTagInfos"), 
                                                                   cms.InputTag("akPu5PFSecondaryVertexTagInfos"))
akPu5PFCombinedSecondaryVertexMVABJetTags          = combinedSecondaryVertexMVABJetTags.clone()
akPu5PFCombinedSecondaryVertexMVABJetTags.tagInfos = cms.VInputTag(cms.InputTag("akPu5PFImpactParameterTagInfos"), 
                                                                   cms.InputTag("akPu5PFSecondaryVertexTagInfos"))

# secondary vertex negative taggers
#from RecoBTag.SecondaryVertex.secondaryVertexNegativeTagInfos_cfi import *
#from RecoBTag.ImpactParameterLearning.simpleSecondaryVertexNegativeHighEffBJetTags_cfi import *
#from RecoBTag.ImpactParameterLearning.simpleSecondaryVertexNegativeHighPurBJetTags_cfi import *
#from RecoBTag.SecondaryVertex.combinedSecondaryVertexNegativeBJetTags_cfi import *
#from RecoBTag.SecondaryVertex.combinedSecondaryVertexPositiveBJetTags_cfi import *

akPu5PFSecondaryVertexNegativeTagInfos                     = secondaryVertexNegativeTagInfos.clone()
akPu5PFSecondaryVertexNegativeTagInfos.trackIPTagInfos     = cms.InputTag("akPu5PFImpactParameterTagInfos")
akPu5PFSimpleSecondaryVertexNegativeHighEffBJetTags               = simpleSecondaryVertexNegativeHighEffBJetTags.clone()
akPu5PFSimpleSecondaryVertexNegativeHighEffBJetTags.tagInfos      = cms.VInputTag(cms.InputTag("akPu5PFSecondaryVertexNegativeTagInfos"))
akPu5PFSimpleSecondaryVertexNegativeHighPurBJetTags               = simpleSecondaryVertexNegativeHighPurBJetTags.clone()
akPu5PFSimpleSecondaryVertexNegativeHighPurBJetTags.tagInfos      = cms.VInputTag(cms.InputTag("akPu5PFSecondaryVertexNegativeTagInfos"))
akPu5PFCombinedSecondaryVertexNegativeBJetTags                    = combinedSecondaryVertexNegativeBJetTags.clone()
akPu5PFCombinedSecondaryVertexNegativeBJetTags.tagInfos    = cms.VInputTag(cms.InputTag("akPu5PFImpactParameterTagInfos"), 
                                                                           cms.InputTag("akPu5PFSecondaryVertexNegativeTagInfos"))
akPu5PFCombinedSecondaryVertexPositiveBJetTags                    = combinedSecondaryVertexPositiveBJetTags.clone()
akPu5PFCombinedSecondaryVertexPositiveBJetTags.tagInfos    = cms.VInputTag(cms.InputTag("akPu5PFImpactParameterTagInfos"), 
                                                                           cms.InputTag("akPu5PFSecondaryVertexTagInfos"))

# soft muon b-tag
akPu5PFSoftMuonTagInfos                = softMuonTagInfos.clone()
akPu5PFSoftMuonTagInfos.jets           = cms.InputTag("akPu5PFJets")
akPu5PFSoftMuonTagInfos.primaryVertex  = cms.InputTag("offlinePrimaryVertices")
akPu5PFSoftMuonBJetTags                = softMuonBJetTags.clone()
akPu5PFSoftMuonBJetTags.tagInfos       = cms.VInputTag(cms.InputTag("akPu5PFSoftMuonTagInfos"))
akPu5PFSoftMuonByIP3dBJetTags          = softMuonByIP3dBJetTags.clone()
akPu5PFSoftMuonByIP3dBJetTags.tagInfos = cms.VInputTag(cms.InputTag("akPu5PFSoftMuonTagInfos"))
akPu5PFSoftMuonByPtBJetTags            = softMuonByPtBJetTags.clone()
akPu5PFSoftMuonByPtBJetTags.tagInfos   = cms.VInputTag(cms.InputTag("akPu5PFSoftMuonTagInfos"))

#from RecoBTag.SoftLepton.negativeSoftMuonByPtBJetTags_cfi import *
#from RecoBTag.SoftLepton.positiveSoftMuonByPtBJetTags_cfi import *

akPu5PFPositiveSoftMuonByPtBJetTags                = positiveSoftLeptonByPtBJetTags.clone()
akPu5PFPositiveSoftMuonByPtBJetTags.tagInfos       = cms.VInputTag(cms.InputTag("akPu5PFSoftMuonTagInfos"))

# soft muon negative taggers
akPu5PFNegativeSoftMuonByPtBJetTags                = negativeSoftLeptonByPtBJetTags.clone()
akPu5PFNegativeSoftMuonByPtBJetTags.tagInfos       = cms.VInputTag(cms.InputTag("akPu5PFSoftMuonTagInfos"))

# ghost tracks
'''
akPu5PFGhostTrackVertexTagInfos                 = ghostTrackVertexTagInfos.clone()
akPu5PFGhostTrackVertexTagInfos.trackIPTagInfos = cms.InputTag("akPu5PFImpactParameterTagInfos")
akPu5PFGhostTrackBJetTags                       = ghostTrackBJetTags.clone()
akPu5PFGhostTrackBJetTags.tagInfos              = cms.VInputTag(cms.InputTag("akPu5PFImpactParameterTagInfos"),
                                                                cms.InputTag("akPu5PFGhostTrackVertexTagInfos"))
'''

# prepare a path running the new modules
akPu5PFJetTracksAssociator = cms.Sequence(akPu5PFJetTracksAssociatorAtVertex)
akPu5PFJetBtaggingIP       = cms.Sequence(akPu5PFImpactParameterTagInfos * (akPu5PFTrackCountingHighEffBJetTags +
                                                                            akPu5PFTrackCountingHighPurBJetTags +
                                                                            akPu5PFJetProbabilityBJetTags +
                                                                            akPu5PFJetBProbabilityBJetTags +
                                                                            akPu5PFPositiveOnlyJetProbabilityJetTags +
                                                                            akPu5PFNegativeOnlyJetProbabilityJetTags +
                                                                            akPu5PFNegativeTrackCountingHighEffJetTags +
                                                                            akPu5PFNegativeTrackCountingHighPur +
                                                                            akPu5PFNegativeOnlyJetBProbabilityJetTags +
                                                                            akPu5PFPositiveOnlyJetBProbabilityJetTags
                                                                                        )
                                                )

akPu5PFJetBtaggingSV = cms.Sequence(akPu5PFImpactParameterTagInfos *
                                    akPu5PFSecondaryVertexTagInfos * (akPu5PFSimpleSecondaryVertexHighEffBJetTags +
                                                                      akPu5PFSimpleSecondaryVertexHighPurBJetTags +
                                                                      akPu5PFCombinedSecondaryVertexBJetTags +
                                                                      akPu5PFCombinedSecondaryVertexMVABJetTags
                                                                      )
                                    #+akPu5PFGhostTrackVertexTagInfos
                                    #*akPu5PFGhostTrackBJetTags
                                    )

akPu5PFJetBtaggingNegSV = cms.Sequence(akPu5PFImpactParameterTagInfos *
                                       akPu5PFSecondaryVertexNegativeTagInfos * (akPu5PFSimpleSecondaryVertexNegativeHighEffBJetTags +
                                                                                 akPu5PFSimpleSecondaryVertexNegativeHighPurBJetTags +
                                                                                 akPu5PFCombinedSecondaryVertexNegativeBJetTags +
                                                                                 akPu5PFCombinedSecondaryVertexPositiveBJetTags 
                                                                                 )
                                       )


akPu5PFJetBtaggingMu = cms.Sequence(akPu5PFSoftMuonTagInfos * (akPu5PFSoftMuonBJetTags +
                                                               akPu5PFSoftMuonByIP3dBJetTags +
                                                               akPu5PFSoftMuonByPtBJetTags +
                                                               akPu5PFNegativeSoftMuonByPtBJetTags +
                                                               akPu5PFPositiveSoftMuonByPtBJetTags
                                                               )
                                          )

akPu5PFJetBtagging = cms.Sequence(akPu5PFJetBtaggingIP 
                                  *akPu5PFJetBtaggingSV 
                                  *akPu5PFJetBtaggingNegSV
                                  *akPu5PFJetBtaggingMu
                                  )

#__________________________________________________________
# ----- flavour bit
akPu5PFPatJetPartonAssociation       = patJetPartonAssociation.clone(jets    = cms.InputTag("akPu5PFJets"),
                                                                                     partons = cms.InputTag("genPartons"),
                                                                                     coneSizeToAssociate = cms.double(0.4))
akPu5PFPatJetFlavourAssociation      = patJetFlavourAssociation.clone(srcByReference = cms.InputTag("akPu5PFPatJetPartonAssociation"))

akPu5PFPatJetFlavourId               = cms.Sequence(akPu5PFPatJetPartonAssociation*akPu5PFPatJetFlavourAssociation)
#
#-------
#akPu5PFcorr = patJetCorrFactors.clone(src     = cms.InputTag("akPu5PFJets"),
#                                      levels  = cms.vstring('L2Relative','L3Absolute'),
#                                      payload = cms.string('AK3PFTowers_hiGoodTightTracks')
#                                                      )
akPu5PFclean   = heavyIonCleanedGenJets.clone(src = cms.InputTag('ak3HiGenJets'))
akPu5PFmatch   = patJetGenJetMatch.clone(src      = cms.InputTag("akPu5PFJets"),
                                                         matched  = cms.InputTag("akPu5PFclean"))
akPu5PFparton  = patJetPartonMatch.clone(src      = cms.InputTag("akPu5PFJets"))
akPu5PFpatJets = patJets.clone(jetSource            = cms.InputTag("akPu5PFJets"),
                                               genJetMatch          = cms.InputTag("akPu5PFmatch"),
                                               genPartonMatch       = cms.InputTag("akPu5PFparton"),
                                               jetCorrFactorsSource = cms.VInputTag(cms.InputTag("akPu5PFcorr")),
                                               JetPartonMapSource   = cms.InputTag("akPu5PFPatJetFlavourAssociation"),
                                               trackAssociationSource = cms.InputTag("akPu5PFJetTracksAssociatorAtVertex"),
                                               discriminatorSources = cms.VInputTag(cms.InputTag("akPu5PFSimpleSecondaryVertexHighEffBJetTags"),
                                                                                    cms.InputTag("akPu5PFSimpleSecondaryVertexHighPurBJetTags"),
                                                                                    cms.InputTag("akPu5PFCombinedSecondaryVertexBJetTags"),
                                                                                    cms.InputTag("akPu5PFCombinedSecondaryVertexMVABJetTags"),
                                                                                    cms.InputTag("akPu5PFJetBProbabilityBJetTags"),
                                                                                    cms.InputTag("akPu5PFJetProbabilityBJetTags"),
                                                                                    cms.InputTag("akPu5PFSoftMuonByPtBJetTags"),                
                                                                                    cms.InputTag("akPu5PFSoftMuonByIP3dBJetTags"),
                                                                                    cms.InputTag("akPu5PFTrackCountingHighEffBJetTags"),
                                                                                    cms.InputTag("akPu5PFTrackCountingHighPurBJetTags"),
                                                                                    ),
                                               )

  ####################################################################################

#### B-tagging for this bit:
# b-tagging general configuration
ak5PFJetTracksAssociatorAtVertex        = ak5JetTracksAssociatorAtVertex.clone()
ak5PFJetTracksAssociatorAtVertex.jets   = cms.InputTag("ak5PFJets")
ak5PFJetTracksAssociatorAtVertex.tracks = cms.InputTag("generalTracks")
# impact parameter b-tag
ak5PFImpactParameterTagInfos               = impactParameterTagInfos.clone()
ak5PFImpactParameterTagInfos.jetTracks     = cms.InputTag("ak5PFJetTracksAssociatorAtVertex")
ak5PFImpactParameterTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
ak5PFTrackCountingHighEffBJetTags          = trackCountingHighEffBJetTags.clone()
ak5PFTrackCountingHighEffBJetTags.tagInfos = cms.VInputTag(cms.InputTag("ak5PFImpactParameterTagInfos"))
ak5PFTrackCountingHighPurBJetTags          = trackCountingHighPurBJetTags.clone()
ak5PFTrackCountingHighPurBJetTags.tagInfos = cms.VInputTag(cms.InputTag("ak5PFImpactParameterTagInfos"))
ak5PFJetProbabilityBJetTags                = jetProbabilityBJetTags.clone()
ak5PFJetProbabilityBJetTags.tagInfos       = cms.VInputTag(cms.InputTag("ak5PFImpactParameterTagInfos"))
ak5PFJetBProbabilityBJetTags               = jetBProbabilityBJetTags.clone()
ak5PFJetBProbabilityBJetTags.tagInfos      = cms.VInputTag(cms.InputTag("ak5PFImpactParameterTagInfos"))

#negative impact parameter
#from RecoBTag.ImpactParameter.positiveOnlyJetProbabilityJetTags_cfi import *
#from RecoBTag.ImpactParameter.negativeOnlyJetProbabilityJetTags_cfi import *
#from RecoBTag.ImpactParameter.negativeTrackCountingHighEffJetTags_cfi import *
#from RecoBTag.ImpactParameter.negativeTrackCountingHighPur_cfi import *
#from RecoBTag.ImpactParameter.negativeOnlyJetBProbabilityJetTags_cfi import *

ak5PFPositiveOnlyJetProbabilityJetTags     =       positiveOnlyJetProbabilityJetTags.clone()  
ak5PFNegativeOnlyJetProbabilityJetTags     =       negativeOnlyJetProbabilityJetTags.clone()    
ak5PFNegativeTrackCountingHighEffJetTags   =       negativeTrackCountingHighEffJetTags.clone()  
ak5PFNegativeTrackCountingHighPur          =       negativeTrackCountingHighPur.clone()         
ak5PFNegativeOnlyJetBProbabilityJetTags    =       negativeOnlyJetBProbabilityJetTags.clone()
ak5PFPositiveOnlyJetBProbabilityJetTags    =       positiveOnlyJetBProbabilityJetTags.clone()

ak5PFPositiveOnlyJetProbabilityJetTags.tagInfos   = cms.VInputTag(cms.InputTag("ak5PFImpactParameterTagInfos"))
ak5PFNegativeOnlyJetProbabilityJetTags.tagInfos   = cms.VInputTag(cms.InputTag("ak5PFImpactParameterTagInfos"))
ak5PFNegativeTrackCountingHighEffJetTags.tagInfos = cms.VInputTag(cms.InputTag("ak5PFImpactParameterTagInfos"))
ak5PFNegativeTrackCountingHighPur.tagInfos        = cms.VInputTag(cms.InputTag("ak5PFImpactParameterTagInfos"))   
ak5PFNegativeOnlyJetBProbabilityJetTags.tagInfos  = cms.VInputTag(cms.InputTag("ak5PFImpactParameterTagInfos"))
ak5PFPositiveOnlyJetBProbabilityJetTags.tagInfos  = cms.VInputTag(cms.InputTag("ak5PFImpactParameterTagInfos"))



# secondary vertex b-tag
ak5PFSecondaryVertexTagInfos                     = secondaryVertexTagInfos.clone()
ak5PFSecondaryVertexTagInfos.trackIPTagInfos     = cms.InputTag("ak5PFImpactParameterTagInfos")
ak5PFSimpleSecondaryVertexHighEffBJetTags               = simpleSecondaryVertexHighEffBJetTags.clone()
ak5PFSimpleSecondaryVertexHighEffBJetTags.tagInfos      = cms.VInputTag(cms.InputTag("ak5PFSecondaryVertexTagInfos"))
ak5PFSimpleSecondaryVertexHighPurBJetTags               = simpleSecondaryVertexHighPurBJetTags.clone()
ak5PFSimpleSecondaryVertexHighPurBJetTags.tagInfos      = cms.VInputTag(cms.InputTag("ak5PFSecondaryVertexTagInfos"))
ak5PFCombinedSecondaryVertexBJetTags             = combinedSecondaryVertexBJetTags.clone()
ak5PFCombinedSecondaryVertexBJetTags.tagInfos    = cms.VInputTag(cms.InputTag("ak5PFImpactParameterTagInfos"), 
                                                                   cms.InputTag("ak5PFSecondaryVertexTagInfos"))
ak5PFCombinedSecondaryVertexMVABJetTags          = combinedSecondaryVertexMVABJetTags.clone()
ak5PFCombinedSecondaryVertexMVABJetTags.tagInfos = cms.VInputTag(cms.InputTag("ak5PFImpactParameterTagInfos"), 
                                                                   cms.InputTag("ak5PFSecondaryVertexTagInfos"))

# secondary vertex negative taggers
#from RecoBTag.SecondaryVertex.secondaryVertexNegativeTagInfos_cfi import *
#from RecoBTag.ImpactParameterLearning.simpleSecondaryVertexNegativeHighEffBJetTags_cfi import *
#from RecoBTag.ImpactParameterLearning.simpleSecondaryVertexNegativeHighPurBJetTags_cfi import *
#from RecoBTag.SecondaryVertex.combinedSecondaryVertexNegativeBJetTags_cfi import *
#from RecoBTag.SecondaryVertex.combinedSecondaryVertexPositiveBJetTags_cfi import *

ak5PFSecondaryVertexNegativeTagInfos                     = secondaryVertexNegativeTagInfos.clone()
ak5PFSecondaryVertexNegativeTagInfos.trackIPTagInfos     = cms.InputTag("ak5PFImpactParameterTagInfos")
ak5PFSimpleSecondaryVertexNegativeHighEffBJetTags               = simpleSecondaryVertexNegativeHighEffBJetTags.clone()
ak5PFSimpleSecondaryVertexNegativeHighEffBJetTags.tagInfos      = cms.VInputTag(cms.InputTag("ak5PFSecondaryVertexNegativeTagInfos"))
ak5PFSimpleSecondaryVertexNegativeHighPurBJetTags               = simpleSecondaryVertexNegativeHighPurBJetTags.clone()
ak5PFSimpleSecondaryVertexNegativeHighPurBJetTags.tagInfos      = cms.VInputTag(cms.InputTag("ak5PFSecondaryVertexNegativeTagInfos"))
ak5PFCombinedSecondaryVertexNegativeBJetTags                    = combinedSecondaryVertexNegativeBJetTags.clone()
ak5PFCombinedSecondaryVertexNegativeBJetTags.tagInfos    = cms.VInputTag(cms.InputTag("ak5PFImpactParameterTagInfos"), 
                                                                           cms.InputTag("ak5PFSecondaryVertexNegativeTagInfos"))
ak5PFCombinedSecondaryVertexPositiveBJetTags                    = combinedSecondaryVertexPositiveBJetTags.clone()
ak5PFCombinedSecondaryVertexPositiveBJetTags.tagInfos    = cms.VInputTag(cms.InputTag("ak5PFImpactParameterTagInfos"), 
                                                                           cms.InputTag("ak5PFSecondaryVertexTagInfos"))

# soft muon b-tag
ak5PFSoftMuonTagInfos                = softMuonTagInfos.clone()
ak5PFSoftMuonTagInfos.jets           = cms.InputTag("ak5PFJets")
ak5PFSoftMuonTagInfos.primaryVertex  = cms.InputTag("offlinePrimaryVertices")
ak5PFSoftMuonBJetTags                = softMuonBJetTags.clone()
ak5PFSoftMuonBJetTags.tagInfos       = cms.VInputTag(cms.InputTag("ak5PFSoftMuonTagInfos"))
ak5PFSoftMuonByIP3dBJetTags          = softMuonByIP3dBJetTags.clone()
ak5PFSoftMuonByIP3dBJetTags.tagInfos = cms.VInputTag(cms.InputTag("ak5PFSoftMuonTagInfos"))
ak5PFSoftMuonByPtBJetTags            = softMuonByPtBJetTags.clone()
ak5PFSoftMuonByPtBJetTags.tagInfos   = cms.VInputTag(cms.InputTag("ak5PFSoftMuonTagInfos"))

#from RecoBTag.SoftLepton.negativeSoftMuonByPtBJetTags_cfi import *
#from RecoBTag.SoftLepton.positiveSoftMuonByPtBJetTags_cfi import *

ak5PFPositiveSoftMuonByPtBJetTags                = positiveSoftLeptonByPtBJetTags.clone()
ak5PFPositiveSoftMuonByPtBJetTags.tagInfos       = cms.VInputTag(cms.InputTag("ak5PFSoftMuonTagInfos"))

# soft muon negative taggers
ak5PFNegativeSoftMuonByPtBJetTags                = negativeSoftLeptonByPtBJetTags.clone()
ak5PFNegativeSoftMuonByPtBJetTags.tagInfos       = cms.VInputTag(cms.InputTag("ak5PFSoftMuonTagInfos"))

# ghost tracks
'''
ak5PFGhostTrackVertexTagInfos                 = ghostTrackVertexTagInfos.clone()
ak5PFGhostTrackVertexTagInfos.trackIPTagInfos = cms.InputTag("ak5PFImpactParameterTagInfos")
ak5PFGhostTrackBJetTags                       = ghostTrackBJetTags.clone()
ak5PFGhostTrackBJetTags.tagInfos              = cms.VInputTag(cms.InputTag("ak5PFImpactParameterTagInfos"),
                                                                cms.InputTag("ak5PFGhostTrackVertexTagInfos"))
'''

# prepare a path running the new modules
ak5PFJetTracksAssociator = cms.Sequence(ak5PFJetTracksAssociatorAtVertex)
ak5PFJetBtaggingIP       = cms.Sequence(ak5PFImpactParameterTagInfos * (ak5PFTrackCountingHighEffBJetTags +
                                                                            ak5PFTrackCountingHighPurBJetTags +
                                                                            ak5PFJetProbabilityBJetTags +
                                                                            ak5PFJetBProbabilityBJetTags +
                                                                            ak5PFPositiveOnlyJetProbabilityJetTags +
                                                                            ak5PFNegativeOnlyJetProbabilityJetTags +
                                                                            ak5PFNegativeTrackCountingHighEffJetTags +
                                                                            ak5PFNegativeTrackCountingHighPur +
                                                                            ak5PFNegativeOnlyJetBProbabilityJetTags +
                                                                            ak5PFPositiveOnlyJetBProbabilityJetTags
                                                                                        )
                                                )

ak5PFJetBtaggingSV = cms.Sequence(ak5PFImpactParameterTagInfos *
                                    ak5PFSecondaryVertexTagInfos * (ak5PFSimpleSecondaryVertexHighEffBJetTags +
                                                                      ak5PFSimpleSecondaryVertexHighPurBJetTags +
                                                                      ak5PFCombinedSecondaryVertexBJetTags +
                                                                      ak5PFCombinedSecondaryVertexMVABJetTags
                                                                      )
                                    #+ak5PFGhostTrackVertexTagInfos
                                    #*ak5PFGhostTrackBJetTags
                                    )

ak5PFJetBtaggingNegSV = cms.Sequence(ak5PFImpactParameterTagInfos *
                                       ak5PFSecondaryVertexNegativeTagInfos * (ak5PFSimpleSecondaryVertexNegativeHighEffBJetTags +
                                                                                 ak5PFSimpleSecondaryVertexNegativeHighPurBJetTags +
                                                                                 ak5PFCombinedSecondaryVertexNegativeBJetTags +
                                                                                 ak5PFCombinedSecondaryVertexPositiveBJetTags 
                                                                                 )
                                       )


ak5PFJetBtaggingMu = cms.Sequence(ak5PFSoftMuonTagInfos * (ak5PFSoftMuonBJetTags +
                                                               ak5PFSoftMuonByIP3dBJetTags +
                                                               ak5PFSoftMuonByPtBJetTags +
                                                               ak5PFNegativeSoftMuonByPtBJetTags +
                                                               ak5PFPositiveSoftMuonByPtBJetTags
                                                               )
                                          )

ak5PFJetBtagging = cms.Sequence(ak5PFJetBtaggingIP 
                                  *ak5PFJetBtaggingSV 
                                  *ak5PFJetBtaggingNegSV
                                  *ak5PFJetBtaggingMu
                                  )

#__________________________________________________________
# ----- flavour bit
ak5PFPatJetPartonAssociation       = patJetPartonAssociation.clone(jets    = cms.InputTag("ak5PFJets"),
                                                                                     partons = cms.InputTag("genPartons"),
                                                                                     coneSizeToAssociate = cms.double(0.4))
ak5PFPatJetFlavourAssociation      = patJetFlavourAssociation.clone(srcByReference = cms.InputTag("ak5PFPatJetPartonAssociation"))

ak5PFPatJetFlavourId               = cms.Sequence(ak5PFPatJetPartonAssociation*ak5PFPatJetFlavourAssociation)
#
#-------
#ak5PFcorr = patJetCorrFactors.clone(src     = cms.InputTag("ak5PFJets"),
#                                      levels  = cms.vstring('L2Relative','L3Absolute'),
#                                      payload = cms.string('AK3PFTowers_hiGoodTightTracks')
#                                                      )
ak5PFclean   = heavyIonCleanedGenJets.clone(src = cms.InputTag('ak3HiGenJets'))
ak5PFmatch   = patJetGenJetMatch.clone(src      = cms.InputTag("ak5PFJets"),
                                                         matched  = cms.InputTag("ak5PFclean"))
ak5PFparton  = patJetPartonMatch.clone(src      = cms.InputTag("ak5PFJets"))
ak5PFpatJets = patJets.clone(jetSource            = cms.InputTag("ak5PFJets"),
                                               genJetMatch          = cms.InputTag("ak5PFmatch"),
                                               genPartonMatch       = cms.InputTag("ak5PFparton"),
                                               jetCorrFactorsSource = cms.VInputTag(cms.InputTag("ak5PFcorr")),
                                               JetPartonMapSource   = cms.InputTag("ak5PFPatJetFlavourAssociation"),
                                               trackAssociationSource = cms.InputTag("ak5PFJetTracksAssociatorAtVertex"),
                                               discriminatorSources = cms.VInputTag(cms.InputTag("ak5PFSimpleSecondaryVertexHighEffBJetTags"),
                                                                                    cms.InputTag("ak5PFSimpleSecondaryVertexHighPurBJetTags"),
                                                                                    cms.InputTag("ak5PFCombinedSecondaryVertexBJetTags"),
                                                                                    cms.InputTag("ak5PFCombinedSecondaryVertexMVABJetTags"),
                                                                                    cms.InputTag("ak5PFJetBProbabilityBJetTags"),
                                                                                    cms.InputTag("ak5PFJetProbabilityBJetTags"),
                                                                                    cms.InputTag("ak5PFSoftMuonByPtBJetTags"),                
                                                                                    cms.InputTag("ak5PFSoftMuonByIP3dBJetTags"),
                                                                                    cms.InputTag("ak5PFTrackCountingHighEffBJetTags"),
                                                                                    cms.InputTag("ak5PFTrackCountingHighPurBJetTags"),
                                                                                    ),
                                               )
  
  
  #################################################################################

#### B-tagging for this bit:
# b-tagging general configuration
ak3PFJetTracksAssociatorAtVertex        = ak5JetTracksAssociatorAtVertex.clone()
ak3PFJetTracksAssociatorAtVertex.jets   = cms.InputTag("ak3PFJets")
ak3PFJetTracksAssociatorAtVertex.tracks = cms.InputTag("generalTracks")
# impact parameter b-tag
ak3PFImpactParameterTagInfos               = impactParameterTagInfos.clone()
ak3PFImpactParameterTagInfos.jetTracks     = cms.InputTag("ak3PFJetTracksAssociatorAtVertex")
ak3PFImpactParameterTagInfos.primaryVertex = cms.InputTag("offlinePrimaryVertices")
ak3PFTrackCountingHighEffBJetTags          = trackCountingHighEffBJetTags.clone()
ak3PFTrackCountingHighEffBJetTags.tagInfos = cms.VInputTag(cms.InputTag("ak3PFImpactParameterTagInfos"))
ak3PFTrackCountingHighPurBJetTags          = trackCountingHighPurBJetTags.clone()
ak3PFTrackCountingHighPurBJetTags.tagInfos = cms.VInputTag(cms.InputTag("ak3PFImpactParameterTagInfos"))
ak3PFJetProbabilityBJetTags                = jetProbabilityBJetTags.clone()
ak3PFJetProbabilityBJetTags.tagInfos       = cms.VInputTag(cms.InputTag("ak3PFImpactParameterTagInfos"))
ak3PFJetBProbabilityBJetTags               = jetBProbabilityBJetTags.clone()
ak3PFJetBProbabilityBJetTags.tagInfos      = cms.VInputTag(cms.InputTag("ak3PFImpactParameterTagInfos"))

#negative impact parameter
#from RecoBTag.ImpactParameter.positiveOnlyJetProbabilityJetTags_cfi import *
#from RecoBTag.ImpactParameter.negativeOnlyJetProbabilityJetTags_cfi import *
#from RecoBTag.ImpactParameter.negativeTrackCountingHighEffJetTags_cfi import *
#from RecoBTag.ImpactParameter.negativeTrackCountingHighPur_cfi import *
#from RecoBTag.ImpactParameter.negativeOnlyJetBProbabilityJetTags_cfi import *

ak3PFPositiveOnlyJetProbabilityJetTags     =       positiveOnlyJetProbabilityJetTags.clone()  
ak3PFNegativeOnlyJetProbabilityJetTags     =       negativeOnlyJetProbabilityJetTags.clone()    
ak3PFNegativeTrackCountingHighEffJetTags   =       negativeTrackCountingHighEffJetTags.clone()  
ak3PFNegativeTrackCountingHighPur          =       negativeTrackCountingHighPur.clone()         
ak3PFNegativeOnlyJetBProbabilityJetTags    =       negativeOnlyJetBProbabilityJetTags.clone()
ak3PFPositiveOnlyJetBProbabilityJetTags    =       positiveOnlyJetBProbabilityJetTags.clone()

ak3PFPositiveOnlyJetProbabilityJetTags.tagInfos   = cms.VInputTag(cms.InputTag("ak3PFImpactParameterTagInfos"))
ak3PFNegativeOnlyJetProbabilityJetTags.tagInfos   = cms.VInputTag(cms.InputTag("ak3PFImpactParameterTagInfos"))
ak3PFNegativeTrackCountingHighEffJetTags.tagInfos = cms.VInputTag(cms.InputTag("ak3PFImpactParameterTagInfos"))
ak3PFNegativeTrackCountingHighPur.tagInfos        = cms.VInputTag(cms.InputTag("ak3PFImpactParameterTagInfos"))   
ak3PFNegativeOnlyJetBProbabilityJetTags.tagInfos  = cms.VInputTag(cms.InputTag("ak3PFImpactParameterTagInfos"))
ak3PFPositiveOnlyJetBProbabilityJetTags.tagInfos  = cms.VInputTag(cms.InputTag("ak3PFImpactParameterTagInfos"))



# secondary vertex b-tag
ak3PFSecondaryVertexTagInfos                     = secondaryVertexTagInfos.clone()
ak3PFSecondaryVertexTagInfos.trackIPTagInfos     = cms.InputTag("ak3PFImpactParameterTagInfos")
ak3PFSimpleSecondaryVertexHighEffBJetTags               = simpleSecondaryVertexHighEffBJetTags.clone()
ak3PFSimpleSecondaryVertexHighEffBJetTags.tagInfos      = cms.VInputTag(cms.InputTag("ak3PFSecondaryVertexTagInfos"))
ak3PFSimpleSecondaryVertexHighPurBJetTags               = simpleSecondaryVertexHighPurBJetTags.clone()
ak3PFSimpleSecondaryVertexHighPurBJetTags.tagInfos      = cms.VInputTag(cms.InputTag("ak3PFSecondaryVertexTagInfos"))
ak3PFCombinedSecondaryVertexBJetTags             = combinedSecondaryVertexBJetTags.clone()
ak3PFCombinedSecondaryVertexBJetTags.tagInfos    = cms.VInputTag(cms.InputTag("ak3PFImpactParameterTagInfos"), 
                                                                   cms.InputTag("ak3PFSecondaryVertexTagInfos"))
ak3PFCombinedSecondaryVertexMVABJetTags          = combinedSecondaryVertexMVABJetTags.clone()
ak3PFCombinedSecondaryVertexMVABJetTags.tagInfos = cms.VInputTag(cms.InputTag("ak3PFImpactParameterTagInfos"), 
                                                                   cms.InputTag("ak3PFSecondaryVertexTagInfos"))

# secondary vertex negative taggers
#from RecoBTag.SecondaryVertex.secondaryVertexNegativeTagInfos_cfi import *
#from RecoBTag.ImpactParameterLearning.simpleSecondaryVertexNegativeHighEffBJetTags_cfi import *
#from RecoBTag.ImpactParameterLearning.simpleSecondaryVertexNegativeHighPurBJetTags_cfi import *
#from RecoBTag.SecondaryVertex.combinedSecondaryVertexNegativeBJetTags_cfi import *
#from RecoBTag.SecondaryVertex.combinedSecondaryVertexPositiveBJetTags_cfi import *

ak3PFSecondaryVertexNegativeTagInfos                     = secondaryVertexNegativeTagInfos.clone()
ak3PFSecondaryVertexNegativeTagInfos.trackIPTagInfos     = cms.InputTag("ak3PFImpactParameterTagInfos")
ak3PFSimpleSecondaryVertexNegativeHighEffBJetTags               = simpleSecondaryVertexNegativeHighEffBJetTags.clone()
ak3PFSimpleSecondaryVertexNegativeHighEffBJetTags.tagInfos      = cms.VInputTag(cms.InputTag("ak3PFSecondaryVertexNegativeTagInfos"))
ak3PFSimpleSecondaryVertexNegativeHighPurBJetTags               = simpleSecondaryVertexNegativeHighPurBJetTags.clone()
ak3PFSimpleSecondaryVertexNegativeHighPurBJetTags.tagInfos      = cms.VInputTag(cms.InputTag("ak3PFSecondaryVertexNegativeTagInfos"))
ak3PFCombinedSecondaryVertexNegativeBJetTags                    = combinedSecondaryVertexNegativeBJetTags.clone()
ak3PFCombinedSecondaryVertexNegativeBJetTags.tagInfos    = cms.VInputTag(cms.InputTag("ak3PFImpactParameterTagInfos"), 
                                                                           cms.InputTag("ak3PFSecondaryVertexNegativeTagInfos"))
ak3PFCombinedSecondaryVertexPositiveBJetTags                    = combinedSecondaryVertexPositiveBJetTags.clone()
ak3PFCombinedSecondaryVertexPositiveBJetTags.tagInfos    = cms.VInputTag(cms.InputTag("ak3PFImpactParameterTagInfos"), 
                                                                           cms.InputTag("ak3PFSecondaryVertexTagInfos"))

# soft muon b-tag
ak3PFSoftMuonTagInfos                = softMuonTagInfos.clone()
ak3PFSoftMuonTagInfos.jets           = cms.InputTag("ak3PFJets")
ak3PFSoftMuonTagInfos.primaryVertex  = cms.InputTag("offlinePrimaryVertices")
ak3PFSoftMuonBJetTags                = softMuonBJetTags.clone()
ak3PFSoftMuonBJetTags.tagInfos       = cms.VInputTag(cms.InputTag("ak3PFSoftMuonTagInfos"))
ak3PFSoftMuonByIP3dBJetTags          = softMuonByIP3dBJetTags.clone()
ak3PFSoftMuonByIP3dBJetTags.tagInfos = cms.VInputTag(cms.InputTag("ak3PFSoftMuonTagInfos"))
ak3PFSoftMuonByPtBJetTags            = softMuonByPtBJetTags.clone()
ak3PFSoftMuonByPtBJetTags.tagInfos   = cms.VInputTag(cms.InputTag("ak3PFSoftMuonTagInfos"))

#from RecoBTag.SoftLepton.negativeSoftMuonByPtBJetTags_cfi import *
#from RecoBTag.SoftLepton.positiveSoftMuonByPtBJetTags_cfi import *

ak3PFPositiveSoftMuonByPtBJetTags                = positiveSoftLeptonByPtBJetTags.clone()
ak3PFPositiveSoftMuonByPtBJetTags.tagInfos       = cms.VInputTag(cms.InputTag("ak3PFSoftMuonTagInfos"))

# soft muon negative taggers
ak3PFNegativeSoftMuonByPtBJetTags                = negativeSoftLeptonByPtBJetTags.clone()
ak3PFNegativeSoftMuonByPtBJetTags.tagInfos       = cms.VInputTag(cms.InputTag("ak3PFSoftMuonTagInfos"))

# ghost tracks
'''
ak3PFGhostTrackVertexTagInfos                 = ghostTrackVertexTagInfos.clone()
ak3PFGhostTrackVertexTagInfos.trackIPTagInfos = cms.InputTag("ak3PFImpactParameterTagInfos")
ak3PFGhostTrackBJetTags                       = ghostTrackBJetTags.clone()
ak3PFGhostTrackBJetTags.tagInfos              = cms.VInputTag(cms.InputTag("ak3PFImpactParameterTagInfos"),
                                                                cms.InputTag("ak3PFGhostTrackVertexTagInfos"))
'''

# prepare a path running the new modules
ak3PFJetTracksAssociator = cms.Sequence(ak3PFJetTracksAssociatorAtVertex)
ak3PFJetBtaggingIP       = cms.Sequence(ak3PFImpactParameterTagInfos * (ak3PFTrackCountingHighEffBJetTags +
                                                                            ak3PFTrackCountingHighPurBJetTags +
                                                                            ak3PFJetProbabilityBJetTags +
                                                                            ak3PFJetBProbabilityBJetTags +
                                                                            ak3PFPositiveOnlyJetProbabilityJetTags +
                                                                            ak3PFNegativeOnlyJetProbabilityJetTags +
                                                                            ak3PFNegativeTrackCountingHighEffJetTags +
                                                                            ak3PFNegativeTrackCountingHighPur +
                                                                            ak3PFNegativeOnlyJetBProbabilityJetTags +
                                                                            ak3PFPositiveOnlyJetBProbabilityJetTags
                                                                                        )
                                                )

ak3PFJetBtaggingSV = cms.Sequence(ak3PFImpactParameterTagInfos *
                                    ak3PFSecondaryVertexTagInfos * (ak3PFSimpleSecondaryVertexHighEffBJetTags +
                                                                      ak3PFSimpleSecondaryVertexHighPurBJetTags +
                                                                      ak3PFCombinedSecondaryVertexBJetTags +
                                                                      ak3PFCombinedSecondaryVertexMVABJetTags
                                                                      )
                                    #+ak3PFGhostTrackVertexTagInfos
                                    #*ak3PFGhostTrackBJetTags
                                    )

ak3PFJetBtaggingNegSV = cms.Sequence(ak3PFImpactParameterTagInfos *
                                       ak3PFSecondaryVertexNegativeTagInfos * (ak3PFSimpleSecondaryVertexNegativeHighEffBJetTags +
                                                                                 ak3PFSimpleSecondaryVertexNegativeHighPurBJetTags +
                                                                                 ak3PFCombinedSecondaryVertexNegativeBJetTags +
                                                                                 ak3PFCombinedSecondaryVertexPositiveBJetTags 
                                                                                 )
                                       )


ak3PFJetBtaggingMu = cms.Sequence(ak3PFSoftMuonTagInfos * (ak3PFSoftMuonBJetTags +
                                                               ak3PFSoftMuonByIP3dBJetTags +
                                                               ak3PFSoftMuonByPtBJetTags +
                                                               ak3PFNegativeSoftMuonByPtBJetTags +
                                                               ak3PFPositiveSoftMuonByPtBJetTags
                                                               )
                                          )

ak3PFJetBtagging = cms.Sequence(ak3PFJetBtaggingIP 
                                  *ak3PFJetBtaggingSV 
                                  *ak3PFJetBtaggingNegSV
                                  *ak3PFJetBtaggingMu
                                  )

#__________________________________________________________
# ----- flavour bit
ak3PFPatJetPartonAssociation       = patJetPartonAssociation.clone(jets    = cms.InputTag("ak3PFJets"),
                                                                                     partons = cms.InputTag("genPartons"),
                                                                                     coneSizeToAssociate = cms.double(0.4))
ak3PFPatJetFlavourAssociation      = patJetFlavourAssociation.clone(srcByReference = cms.InputTag("ak3PFPatJetPartonAssociation"))

ak3PFPatJetFlavourId               = cms.Sequence(ak3PFPatJetPartonAssociation*ak3PFPatJetFlavourAssociation)
#
#-------
#ak3PFcorr = patJetCorrFactors.clone(src     = cms.InputTag("ak3PFJets"),
#                                      levels  = cms.vstring('L2Relative','L3Absolute'),
#                                      payload = cms.string('AK3PFTowers_hiGoodTightTracks')
#                                                      )
ak3PFclean   = heavyIonCleanedGenJets.clone(src = cms.InputTag('ak3HiGenJets'))
ak3PFmatch   = patJetGenJetMatch.clone(src      = cms.InputTag("ak3PFJets"),
                                                         matched  = cms.InputTag("ak3PFclean"))
ak3PFparton  = patJetPartonMatch.clone(src      = cms.InputTag("ak3PFJets"))
ak3PFpatJets = patJets.clone(jetSource            = cms.InputTag("ak3PFJets"),
                                               genJetMatch          = cms.InputTag("ak3PFmatch"),
                                               genPartonMatch       = cms.InputTag("ak3PFparton"),
                                               jetCorrFactorsSource = cms.VInputTag(cms.InputTag("ak3PFcorr")),
                                               JetPartonMapSource   = cms.InputTag("ak3PFPatJetFlavourAssociation"),
                                               trackAssociationSource = cms.InputTag("ak3PFJetTracksAssociatorAtVertex"),
                                               discriminatorSources = cms.VInputTag(cms.InputTag("ak3PFSimpleSecondaryVertexHighEffBJetTags"),
                                                                                    cms.InputTag("ak3PFSimpleSecondaryVertexHighPurBJetTags"),
                                                                                    cms.InputTag("ak3PFCombinedSecondaryVertexBJetTags"),
                                                                                    cms.InputTag("ak3PFCombinedSecondaryVertexMVABJetTags"),
                                                                                    cms.InputTag("ak3PFJetBProbabilityBJetTags"),
                                                                                    cms.InputTag("ak3PFJetProbabilityBJetTags"),
                                                                                    cms.InputTag("ak3PFSoftMuonByPtBJetTags"),                
                                                                                    cms.InputTag("ak3PFSoftMuonByIP3dBJetTags"),
                                                                                    cms.InputTag("ak3PFTrackCountingHighEffBJetTags"),
                                                                                    cms.InputTag("ak3PFTrackCountingHighPurBJetTags"),
                                                                                    ),
                                               )

  ###############################################################################

  #
  #
  # === data sequences ===
# Note still need to use enableData function in cfg to remove mc dep of patjet

# All corrections

#akPu1PFcorr = akPu3PFcorr.clone(src = cms.InputTag("akPu1PFJets"),payload = cms.string('AK1PF_hiIterativeTracks'))
#akPu2PFcorr = akPu3PFcorr.clone(src = cms.InputTag("akPu2PFJets"),payload = cms.string('AK2PF_hiIterativeTracks'))
#akPu3PFcorr = akPu3PFcorr.clone(src = cms.InputTag("akPu3PFJets"),payload = cms.string('AK3PF_hiIterativeTracks'))
#akPu4PFcorr = akPu3PFcorr.clone(src = cms.InputTag("akPu4PFJets"),payload = cms.string('AK4PF_hiIterativeTracks'))
#akPu5PFcorr = akPu3PFcorr.clone(src = cms.InputTag("akPu5PFJets"),payload = cms.string('AK5PF_hiIterativeTracks'))
#akPu6PFcorr = akPu3PFcorr.clone(src = cms.InputTag("akPu6PFJets"),payload = cms.string('AK6PF_hiIterativeTracks'))

#ak1PFcorr = akPu3PFcorr.clone(src = cms.InputTag("ak1PFJets"),payload = cms.string('AK1PF_hiIterativeTracks'))
#ak2PFcorr = akPu3PFcorr.clone(src = cms.InputTag("ak2PFJets"),payload = cms.string('AK2PF_hiIterativeTracks'))
#ak3PFcorr = akPu3PFcorr.clone(src = cms.InputTag("ak3PFJets"),payload = cms.string('AK3PF_hiIterativeTracks'))
#ak4PFcorr = akPu3PFcorr.clone(src = cms.InputTag("ak4PFJets"),payload = cms.string('AK4PF_hiIterativeTracks'))
#ak5PFcorr = akPu3PFcorr.clone(src = cms.InputTag("ak5PFJets"),payload = cms.string('AK5PF_hiIterativeTracks'))
#ak6PFcorr = akPu3PFcorr.clone(src = cms.InputTag("ak6PFJets"),payload = cms.string('AK6PF_hiIterativeTracks'))

akPu1PFcorr = akPu3PFcorr.clone(src = cms.InputTag("akPu1PFJets"),payload = cms.string('AKPu1PF_generalTracks'))
akPu2PFcorr = akPu3PFcorr.clone(src = cms.InputTag("akPu2PFJets"),payload = cms.string('AKPu2PF_generalTracks'))
akPu3PFcorr = akPu3PFcorr.clone(src = cms.InputTag("akPu3PFJets"),payload = cms.string('AKPu3PF_generalTracks'))
akPu4PFcorr = akPu3PFcorr.clone(src = cms.InputTag("akPu4PFJets"),payload = cms.string('AKPu4PF_generalTracks'))
akPu5PFcorr = akPu3PFcorr.clone(src = cms.InputTag("akPu5PFJets"),payload = cms.string('AKPu5PF_generalTracks'))
akPu6PFcorr = akPu3PFcorr.clone(src = cms.InputTag("akPu6PFJets"),payload = cms.string('AKPu6PF_generalTracks'))

ak1PFcorr = akPu3PFcorr.clone(src = cms.InputTag("ak1PFJets"),payload = cms.string('AK1PF_generalTracks'))
ak2PFcorr = akPu3PFcorr.clone(src = cms.InputTag("ak2PFJets"),payload = cms.string('AK2PF_generalTracks'))
ak3PFcorr = akPu3PFcorr.clone(src = cms.InputTag("ak3PFJets"),payload = cms.string('AK3PF_generalTracks'))
ak4PFcorr = akPu3PFcorr.clone(src = cms.InputTag("ak4PFJets"),payload = cms.string('AK4PF_generalTracks'))
ak5PFcorr = akPu3PFcorr.clone(src = cms.InputTag("ak5PFJets"),payload = cms.string('AK5PF_generalTracks'))
ak6PFcorr = akPu3PFcorr.clone(src = cms.InputTag("ak6PFJets"),payload = cms.string('AK6PF_generalTracks'))

akPu1Calocorr = akPu3PFcorr.clone(src = cms.InputTag("akPu1CaloJets"),payload = cms.string('AKPu1Calo_HI'))
akPu2Calocorr = akPu3PFcorr.clone(src = cms.InputTag("akPu2CaloJets"),payload = cms.string('AKPu2Calo_HI'))
akPu3Calocorr = akPu3PFcorr.clone(src = cms.InputTag("akPu3CaloJets"),payload = cms.string('AKPu3Calo_HI'))
akPu4Calocorr = akPu3PFcorr.clone(src = cms.InputTag("akPu4CaloJets"),payload = cms.string('AKPu4Calo_HI'))
akPu5Calocorr = akPu3PFcorr.clone(src = cms.InputTag("akPu5CaloJets"),payload = cms.string('AKPu5Calo_HI'))
# We don't have corrections for ak6calo. This algorithm will be kept for debugging
akPu6Calocorr = akPu3PFcorr.clone(src = cms.InputTag("akPu6CaloJets"),payload = cms.string('AKPu5Calo_HI'))

ak1Calocorr = akPu3PFcorr.clone(src = cms.InputTag("ak1CaloJets"),payload = cms.string('AK1Calo_HI'))
ak2Calocorr = akPu3PFcorr.clone(src = cms.InputTag("ak2CaloJets"),payload = cms.string('AK2Calo_HI'))
ak3Calocorr = akPu3PFcorr.clone(src = cms.InputTag("ak3CaloJets"),payload = cms.string('AK3Calo_HI'))
ak4Calocorr = akPu3PFcorr.clone(src = cms.InputTag("ak4CaloJets"),payload = cms.string('AK4Calo_HI'))
ak5Calocorr = akPu3PFcorr.clone(src = cms.InputTag("ak5CaloJets"),payload = cms.string('AK5Calo_HI'))
# We don't have corrections for ak6calo. This algorithm will be kept for debugging
ak6Calocorr = akPu3PFcorr.clone(src = cms.InputTag("ak6CaloJets"),payload = cms.string('AK5Calo_HI'))

# Gen stuff

ak1clean = akPu3PFclean.clone(src = cms.InputTag("ak1HiGenJets"))
ak2clean = akPu3PFclean.clone(src = cms.InputTag("ak2HiGenJets"))
ak3clean = akPu3PFclean.clone(src = cms.InputTag("ak3HiGenJets"))
ak4clean = akPu3PFclean.clone(src = cms.InputTag("ak4HiGenJets"))
ak5clean = akPu3PFclean.clone(src = cms.InputTag("ak5HiGenJets"))
ak6clean = akPu3PFclean.clone(src = cms.InputTag("ak6HiGenJets"))


akPu1PFmatch = akPu3PFmatch.clone(src = cms.InputTag("akPu1PFJets"), matched = cms.InputTag("ak1clean"))
akPu2PFmatch = akPu3PFmatch.clone(src = cms.InputTag("akPu2PFJets"), matched = cms.InputTag("ak2clean"))
akPu3PFmatch = akPu3PFmatch.clone(src = cms.InputTag("akPu3PFJets"), matched = cms.InputTag("ak3clean"))
akPu4PFmatch = akPu3PFmatch.clone(src = cms.InputTag("akPu4PFJets"), matched = cms.InputTag("ak4clean"))
akPu5PFmatch = akPu3PFmatch.clone(src = cms.InputTag("akPu5PFJets"), matched = cms.InputTag("ak5clean"))
akPu6PFmatch = akPu3PFmatch.clone(src = cms.InputTag("akPu6PFJets"), matched = cms.InputTag("ak6clean"))
akPu1Calomatch = akPu3PFmatch.clone(src = cms.InputTag("akPu1CaloJets"), matched = cms.InputTag("ak1clean"))
akPu2Calomatch = akPu3PFmatch.clone(src = cms.InputTag("akPu2CaloJets"), matched = cms.InputTag("ak2clean"))
akPu3Calomatch = akPu3PFmatch.clone(src = cms.InputTag("akPu3CaloJets"), matched = cms.InputTag("ak3clean"))
akPu4Calomatch = akPu3PFmatch.clone(src = cms.InputTag("akPu4CaloJets"), matched = cms.InputTag("ak4clean"))
akPu5Calomatch = akPu3PFmatch.clone(src = cms.InputTag("akPu5CaloJets"), matched = cms.InputTag("ak5clean"))
akPu6Calomatch = akPu3PFmatch.clone(src = cms.InputTag("akPu6CaloJets"), matched = cms.InputTag("ak6clean"))
ak1PFmatch = akPu3PFmatch.clone(src = cms.InputTag("ak1PFJets"), matched = cms.InputTag("ak1clean"))
ak2PFmatch = akPu3PFmatch.clone(src = cms.InputTag("ak2PFJets"), matched = cms.InputTag("ak2clean"))
ak3PFmatch = akPu3PFmatch.clone(src = cms.InputTag("ak3PFJets"), matched = cms.InputTag("ak3clean"))
ak4PFmatch = akPu3PFmatch.clone(src = cms.InputTag("ak4PFJets"), matched = cms.InputTag("ak4clean"))
ak5PFmatch = akPu3PFmatch.clone(src = cms.InputTag("ak5PFJets"), matched = cms.InputTag("ak5clean"))
ak6PFmatch = akPu3PFmatch.clone(src = cms.InputTag("ak6PFJets"), matched = cms.InputTag("ak6clean"))
ak1Calomatch = akPu3PFmatch.clone(src = cms.InputTag("ak1CaloJets"), matched = cms.InputTag("ak1clean"))
ak2Calomatch = akPu3PFmatch.clone(src = cms.InputTag("ak2CaloJets"), matched = cms.InputTag("ak2clean"))
ak3Calomatch = akPu3PFmatch.clone(src = cms.InputTag("ak3CaloJets"), matched = cms.InputTag("ak3clean"))
ak4Calomatch = akPu3PFmatch.clone(src = cms.InputTag("ak4CaloJets"), matched = cms.InputTag("ak4clean"))
ak5Calomatch = akPu3PFmatch.clone(src = cms.InputTag("ak5CaloJets"), matched = cms.InputTag("ak5clean"))
ak6Calomatch = akPu3PFmatch.clone(src = cms.InputTag("ak6CaloJets"), matched = cms.InputTag("ak6clean"))
akPu1PFparton = akPu3PFparton.clone(src = cms.InputTag("akPu1PFJets"))
akPu2PFparton = akPu3PFparton.clone(src = cms.InputTag("akPu2PFJets"))
akPu3PFparton = akPu3PFparton.clone(src = cms.InputTag("akPu3PFJets"))
akPu4PFparton = akPu3PFparton.clone(src = cms.InputTag("akPu4PFJets"))
akPu5PFparton = akPu3PFparton.clone(src = cms.InputTag("akPu5PFJets"))
akPu6PFparton = akPu3PFparton.clone(src = cms.InputTag("akPu6PFJets"))
akPu1Caloparton = akPu3PFparton.clone(src = cms.InputTag("akPu1CaloJets"))
akPu2Caloparton = akPu3PFparton.clone(src = cms.InputTag("akPu2CaloJets"))
akPu3Caloparton = akPu3PFparton.clone(src = cms.InputTag("akPu3CaloJets"))
akPu4Caloparton = akPu3PFparton.clone(src = cms.InputTag("akPu4CaloJets"))
akPu5Caloparton = akPu3PFparton.clone(src = cms.InputTag("akPu5CaloJets"))
akPu6Caloparton = akPu3PFparton.clone(src = cms.InputTag("akPu6CaloJets"))
ak1PFparton = akPu3PFparton.clone(src = cms.InputTag("ak1PFJets"))
ak2PFparton = akPu3PFparton.clone(src = cms.InputTag("ak2PFJets"))
ak3PFparton = akPu3PFparton.clone(src = cms.InputTag("ak3PFJets"))
ak4PFparton = akPu3PFparton.clone(src = cms.InputTag("ak4PFJets"))
ak5PFparton = akPu3PFparton.clone(src = cms.InputTag("ak5PFJets"))
ak6PFparton = akPu3PFparton.clone(src = cms.InputTag("ak6PFJets"))
ak1Caloparton = akPu3PFparton.clone(src = cms.InputTag("ak1CaloJets"))
ak2Caloparton = akPu3PFparton.clone(src = cms.InputTag("ak2CaloJets"))
ak3Caloparton = akPu3PFparton.clone(src = cms.InputTag("ak3CaloJets"))
ak4Caloparton = akPu3PFparton.clone(src = cms.InputTag("ak4CaloJets"))
ak5Caloparton = akPu3PFparton.clone(src = cms.InputTag("ak5CaloJets"))
ak6Caloparton = akPu3PFparton.clone(src = cms.InputTag("ak6CaloJets"))


# PAT Maker

akPu1PFpatJets = akPu3PFpatJets.clone(jetSource = cms.InputTag("akPu1PFJets"), jetCorrFactorsSource = cms.VInputTag(cms.InputTag("akPu1PFcorr")), genJetMatch = cms.InputTag("akPu1PFmatch"), genPartonMatch = cms.InputTag("akPu1PFparton"),jetIDMap = cms.InputTag("akPu1PFJetID"))
akPu2PFpatJets = akPu3PFpatJets.clone(jetSource = cms.InputTag("akPu2PFJets"), jetCorrFactorsSource = cms.VInputTag(cms.InputTag("akPu2PFcorr")), genJetMatch = cms.InputTag("akPu2PFmatch"), genPartonMatch = cms.InputTag("akPu2PFparton"),jetIDMap = cms.InputTag("akPu2PFJetID"))
akPu3PFpatJets = akPu3PFpatJets.clone(jetSource = cms.InputTag("akPu3PFJets"), jetCorrFactorsSource = cms.VInputTag(cms.InputTag("akPu3PFcorr")), genJetMatch = cms.InputTag("akPu3PFmatch"), genPartonMatch = cms.InputTag("akPu3PFparton"),jetIDMap = cms.InputTag("akPu3PFJetID"))
akPu4PFpatJets = akPu3PFpatJets.clone(jetSource = cms.InputTag("akPu4PFJets"), jetCorrFactorsSource = cms.VInputTag(cms.InputTag("akPu4PFcorr")), genJetMatch = cms.InputTag("akPu4PFmatch"), genPartonMatch = cms.InputTag("akPu4PFparton"),jetIDMap = cms.InputTag("akPu4PFJetID"))
#akPu5PFpatJets = akPu3PFpatJets.clone(jetSource = cms.InputTag("akPu5PFJets"), jetCorrFactorsSource = cms.VInputTag(cms.InputTag("akPu5PFcorr")), genJetMatch = cms.InputTag("akPu5PFmatch"), genPartonMatch = cms.InputTag("akPu5PFparton"),jetIDMap = cms.InputTag("akPu5PFJetID"))
akPu6PFpatJets = akPu3PFpatJets.clone(jetSource = cms.InputTag("akPu6PFJets"), jetCorrFactorsSource = cms.VInputTag(cms.InputTag("akPu6PFcorr")), genJetMatch = cms.InputTag("akPu6PFmatch"), genPartonMatch = cms.InputTag("akPu6PFparton"),jetIDMap = cms.InputTag("akPu6PFJetID"))
akPu1CalopatJets = akPu3PFpatJets.clone(jetSource = cms.InputTag("akPu1CaloJets"), jetCorrFactorsSource = cms.VInputTag(cms.InputTag("akPu1Calocorr")), genJetMatch = cms.InputTag("akPu1Calomatch"), genPartonMatch = cms.InputTag("akPu1Caloparton"),jetIDMap = cms.InputTag("akPu1CaloJetID"))
akPu2CalopatJets = akPu3PFpatJets.clone(jetSource = cms.InputTag("akPu2CaloJets"), jetCorrFactorsSource = cms.VInputTag(cms.InputTag("akPu2Calocorr")), genJetMatch = cms.InputTag("akPu2Calomatch"), genPartonMatch = cms.InputTag("akPu2Caloparton"),jetIDMap = cms.InputTag("akPu2CaloJetID"))
akPu3CalopatJets = akPu3PFpatJets.clone(jetSource = cms.InputTag("akPu3CaloJets"), jetCorrFactorsSource = cms.VInputTag(cms.InputTag("akPu3Calocorr")), genJetMatch = cms.InputTag("akPu3Calomatch"), genPartonMatch = cms.InputTag("akPu3Caloparton"),jetIDMap = cms.InputTag("akPu3CaloJetID"))
akPu4CalopatJets = akPu3PFpatJets.clone(jetSource = cms.InputTag("akPu4CaloJets"), jetCorrFactorsSource = cms.VInputTag(cms.InputTag("akPu4Calocorr")), genJetMatch = cms.InputTag("akPu4Calomatch"), genPartonMatch = cms.InputTag("akPu4Caloparton"),jetIDMap = cms.InputTag("akPu4CaloJetID"))
akPu5CalopatJets = akPu3PFpatJets.clone(jetSource = cms.InputTag("akPu5CaloJets"), jetCorrFactorsSource = cms.VInputTag(cms.InputTag("akPu5Calocorr")), genJetMatch = cms.InputTag("akPu5Calomatch"), genPartonMatch = cms.InputTag("akPu5Caloparton"),jetIDMap = cms.InputTag("akPu5CaloJetID"))
akPu6CalopatJets = akPu3PFpatJets.clone(jetSource = cms.InputTag("akPu6CaloJets"), jetCorrFactorsSource = cms.VInputTag(cms.InputTag("akPu6Calocorr")), genJetMatch = cms.InputTag("akPu6Calomatch"), genPartonMatch = cms.InputTag("akPu6Caloparton"),jetIDMap = cms.InputTag("akPu6CaloJetID"))
ak1PFpatJets = akPu3PFpatJets.clone(jetSource = cms.InputTag("ak1PFJets"), jetCorrFactorsSource = cms.VInputTag(cms.InputTag("ak1PFcorr")), genJetMatch = cms.InputTag("ak1PFmatch"), genPartonMatch = cms.InputTag("ak1PFparton"),jetIDMap = cms.InputTag("ak1PFJetID"))
ak2PFpatJets = akPu3PFpatJets.clone(jetSource = cms.InputTag("ak2PFJets"), jetCorrFactorsSource = cms.VInputTag(cms.InputTag("ak2PFcorr")), genJetMatch = cms.InputTag("ak2PFmatch"), genPartonMatch = cms.InputTag("ak2PFparton"),jetIDMap = cms.InputTag("ak2PFJetID"))
#ak3PFpatJets = akPu3PFpatJets.clone(jetSource = cms.InputTag("ak3PFJets"), jetCorrFactorsSource = cms.VInputTag(cms.InputTag("ak3PFcorr")), genJetMatch = cms.InputTag("ak3PFmatch"), genPartonMatch = cms.InputTag("ak3PFparton"),jetIDMap = cms.InputTag("ak3PFJetID"))
ak4PFpatJets = akPu3PFpatJets.clone(jetSource = cms.InputTag("ak4PFJets"), jetCorrFactorsSource = cms.VInputTag(cms.InputTag("ak4PFcorr")), genJetMatch = cms.InputTag("ak4PFmatch"), genPartonMatch = cms.InputTag("ak4PFparton"),jetIDMap = cms.InputTag("ak4PFJetID"))
#ak5PFpatJets = akPu3PFpatJets.clone(jetSource = cms.InputTag("ak5PFJets"), jetCorrFactorsSource = cms.VInputTag(cms.InputTag("ak5PFcorr")), genJetMatch = cms.InputTag("ak5PFmatch"), genPartonMatch = cms.InputTag("ak5PFparton"),jetIDMap = cms.InputTag("ak5PFJetID"))
ak6PFpatJets = akPu3PFpatJets.clone(jetSource = cms.InputTag("ak6PFJets"), jetCorrFactorsSource = cms.VInputTag(cms.InputTag("ak6PFcorr")), genJetMatch = cms.InputTag("ak6PFmatch"), genPartonMatch = cms.InputTag("ak6PFparton"),jetIDMap = cms.InputTag("ak6PFJetID"))
ak1CalopatJets = akPu3PFpatJets.clone(jetSource = cms.InputTag("ak1CaloJets"), jetCorrFactorsSource = cms.VInputTag(cms.InputTag("ak1Calocorr")), genJetMatch = cms.InputTag("ak1Calomatch"), genPartonMatch = cms.InputTag("ak1Caloparton"),jetIDMap = cms.InputTag("ak1CaloJetID"))
ak2CalopatJets = akPu3PFpatJets.clone(jetSource = cms.InputTag("ak2CaloJets"), jetCorrFactorsSource = cms.VInputTag(cms.InputTag("ak2Calocorr")), genJetMatch = cms.InputTag("ak2Calomatch"), genPartonMatch = cms.InputTag("ak2Caloparton"),jetIDMap = cms.InputTag("ak2CaloJetID"))
ak3CalopatJets = akPu3PFpatJets.clone(jetSource = cms.InputTag("ak3CaloJets"), jetCorrFactorsSource = cms.VInputTag(cms.InputTag("ak3Calocorr")), genJetMatch = cms.InputTag("ak3Calomatch"), genPartonMatch = cms.InputTag("ak3Caloparton"),jetIDMap = cms.InputTag("ak3CaloJetID"))
ak4CalopatJets = akPu3PFpatJets.clone(jetSource = cms.InputTag("ak4CaloJets"), jetCorrFactorsSource = cms.VInputTag(cms.InputTag("ak4Calocorr")), genJetMatch = cms.InputTag("ak4Calomatch"), genPartonMatch = cms.InputTag("ak4Caloparton"),jetIDMap = cms.InputTag("ak4CaloJetID"))
ak5CalopatJets = akPu3PFpatJets.clone(jetSource = cms.InputTag("ak5CaloJets"), jetCorrFactorsSource = cms.VInputTag(cms.InputTag("ak5Calocorr")), genJetMatch = cms.InputTag("ak5Calomatch"), genPartonMatch = cms.InputTag("ak5Caloparton"),jetIDMap = cms.InputTag("ak5CaloJetID"))
ak6CalopatJets = akPu3PFpatJets.clone(jetSource = cms.InputTag("ak6CaloJets"), jetCorrFactorsSource = cms.VInputTag(cms.InputTag("ak6Calocorr")), genJetMatch = cms.InputTag("ak6Calomatch"), genPartonMatch = cms.InputTag("ak6Caloparton"),jetIDMap = cms.InputTag("ak6CaloJetID"))

icPu5patSequence = cms.Sequence(icPu5corr * icPu5clean * icPu5match * icPu5parton  *  icPu5patJets)

akPu1PFpatSequence = cms.Sequence(akPu1PFcorr+ak1clean+akPu1PFmatch+akPu1PFparton+akPu1PFpatJets)
akPu2PFpatSequence = cms.Sequence(akPu2PFcorr+ak2clean+akPu2PFmatch+akPu2PFparton+akPu2PFpatJets)
akPu3PFpatSequence = cms.Sequence(akPu3PFcorr+ak3clean+akPu3PFmatch+akPu3PFparton+akPu3PFpatJets)
akPu4PFpatSequence = cms.Sequence(akPu4PFcorr+ak4clean+akPu4PFmatch+akPu4PFparton+akPu4PFpatJets)
akPu5PFpatSequence = cms.Sequence(akPu5PFcorr+ak5clean+akPu5PFmatch+akPu5PFparton+akPu5PFpatJets)
akPu6PFpatSequence = cms.Sequence(akPu6PFcorr+ak6clean+akPu6PFmatch+akPu6PFparton+akPu6PFpatJets)

akPu1CalopatSequence = cms.Sequence(akPu1Calocorr+ak1clean+akPu1Calomatch+akPu1Caloparton+akPu1CalopatJets)
akPu2CalopatSequence = cms.Sequence(akPu2Calocorr+ak2clean+akPu2Calomatch+akPu2Caloparton+akPu2CalopatJets)
akPu3CalopatSequence = cms.Sequence(akPu3Calocorr+ak3clean+akPu3Calomatch+akPu3Caloparton+akPu3CalopatJets)
akPu4CalopatSequence = cms.Sequence(akPu4Calocorr+ak4clean+akPu4Calomatch+akPu4Caloparton+akPu4CalopatJets)
akPu5CalopatSequence = cms.Sequence(akPu5Calocorr+ak5clean+akPu5Calomatch+akPu5Caloparton+akPu5CalopatJets)
akPu6CalopatSequence = cms.Sequence(akPu6Calocorr+ak6clean+akPu6Calomatch+akPu6Caloparton+akPu6CalopatJets)

ak1PFpatSequence = cms.Sequence(ak1PFcorr+ak1clean+ak1PFmatch+ak1PFparton+ak1PFpatJets)
ak2PFpatSequence = cms.Sequence(ak2PFcorr+ak2clean+ak2PFmatch+ak2PFparton+ak2PFpatJets)
ak3PFpatSequence = cms.Sequence(ak3PFcorr+ak3clean+ak3PFmatch+ak3PFparton+ak3PFpatJets)
ak4PFpatSequence = cms.Sequence(ak4PFcorr+ak4clean+ak4PFmatch+ak4PFparton+ak4PFpatJets)
ak5PFpatSequence = cms.Sequence(ak5PFcorr+ak5clean+ak5PFmatch+ak5PFparton+ak5PFpatJets)
ak6PFpatSequence = cms.Sequence(ak6PFcorr+ak6clean+ak6PFmatch+ak6PFparton+ak6PFpatJets)

ak1CalopatSequence = cms.Sequence(ak1Calocorr+ak1clean+ak1Calomatch+ak1Caloparton+ak1CalopatJets)
ak2CalopatSequence = cms.Sequence(ak2Calocorr+ak2clean+ak2Calomatch+ak2Caloparton+ak2CalopatJets)
ak3CalopatSequence = cms.Sequence(ak3Calocorr+ak3clean+ak3Calomatch+ak3Caloparton+ak3CalopatJets)
ak4CalopatSequence = cms.Sequence(ak4Calocorr+ak4clean+ak4Calomatch+ak4Caloparton+ak4CalopatJets)
ak5CalopatSequence = cms.Sequence(ak5Calocorr+ak5clean+ak5Calomatch+ak5Caloparton+ak5CalopatJets)
ak6CalopatSequence = cms.Sequence(ak6Calocorr+ak6clean+ak6Calomatch+ak6Caloparton+ak6CalopatJets)

#<<<<<<< PatAna_MC_cff.py
akPu3PFpatSequence_withBtagging = cms.Sequence(akPu3PFcorr * ak3clean * akPu3PFmatch * akPu3PFparton * akPu3PFPatJetFlavourId * akPu3PFJetTracksAssociator * akPu3PFJetBtagging * akPu3PFpatJets)

icPu5patSequence_withBtagging = cms.Sequence(icPu5corr * icPu5clean * icPu5match * icPu5parton * icPu5PatJetFlavourId * icPu5JetTracksAssociator * icPu5JetBtagging * icPu5patJets)

akPu5PFpatSequence_withBtagging = cms.Sequence(akPu5PFcorr * ak5clean * akPu5PFmatch * akPu5PFparton * akPu5PFPatJetFlavourId * akPu5PFJetTracksAssociator * akPu5PFJetBtagging * akPu5PFpatJets)
ak5PFpatSequence_withBtagging = cms.Sequence(ak5PFcorr * ak5clean * ak5PFmatch * ak5PFparton * ak5PFPatJetFlavourId * ak5PFJetTracksAssociator * ak5PFJetBtagging * ak5PFpatJets)
ak3PFpatSequence_withBtagging = cms.Sequence(ak3PFcorr * ak3clean * ak3PFmatch * ak3PFparton * ak3PFPatJetFlavourId * ak3PFJetTracksAssociator * ak3PFJetBtagging * ak3PFpatJets)

#makeHeavyIonJets = cms.Sequence(icPu5patSequence_withBtagging +
                                
                                #akPu1PFpatSequence +
                                #akPu2PFpatSequence +
 #                               akPu3PFpatSequence_withBtagging +
                                #akPu4PFpatSequence +
  #                              akPu5PFpatSequence_withBtagging
                                #akPu6PFpatSequence +

                                #akPu1CalopatSequence +
                                #akPu2CalopatSequence +
                                #akPu3CalopatSequence +
                                #akPu4CalopatSequence +
                                #akPu5CalopatSequence +
                                #akPu6CalopatSequence +
#=======
makeHeavyIonJets = cms.Sequence(
#                                akPu1PFpatSequence +
#                                akPu2PFpatSequence +
                                akPu3PFpatSequence_withBtagging +
#                                akPu4PFpatSequence +
                                akPu5PFpatSequence_withBtagging +
#                                akPu6PFpatSequence +

#                                akPu1CalopatSequence +
#                                akPu2CalopatSequence +
#                                akPu3CalopatSequence +
#                                akPu4CalopatSequence +
#                                akPu5CalopatSequence +
#                                akPu6CalopatSequence +
#>>>>>>> 1.11
                                
                                #ak1PFpatSequence +
                                #ak2PFpatSequence +
                                ak3PFpatSequence +
                                #ak4PFpatSequence +
                                ak5PFpatSequence 
                                #ak6PFpatSequence +
                                
                                #ak1CalopatSequence +
                                #ak2CalopatSequence +
                                #ak3CalopatSequence +
                                #ak4CalopatSequence +
                                #ak5CalopatSequence +
                                #ak6CalopatSequence
                                
                                )

makeHeavyIonJets2to5 = cms.Sequence(
#                                akPu2PFpatSequence +
                                akPu3PFpatSequence_withBtagging +
#                                akPu4PFpatSequence +
                                akPu5PFpatSequence_withBtagging + 

 #                               akPu2CalopatSequence +
                                #akPu3CalopatSequence +
 #                               akPu4CalopatSequence +
                                #akPu5CalopatSequence 
                                
 #                               ak2PFpatSequence +
                                ak3PFpatSequence_withBtagging +
 #                               ak4PFpatSequence +
                                ak5PFpatSequence_withBtagging 
                                
 #                               ak2CalopatSequence +
                                #ak3CalopatSequence +
 #                               ak4CalopatSequence +
                                #ak5CalopatSequence 
                                
                                )
                               
