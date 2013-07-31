import FWCore.ParameterSet.Config as cms

from Configuration.Generator.PythiaUEZ2Settings_cfi import *

# copied it from Configuration/GenProduction/python/WToENu_TuneZ2_7TeV_pythia6_cff.py

hiSignal =  cms.EDFilter("Pythia6GeneratorFilter",
                         pythiaHepMCVerbosity = cms.untracked.bool(False),
                         maxEventsToPrint = cms.untracked.int32(0),
                         pythiaPylistVerbosity = cms.untracked.int32(1),
                         filterEfficiency = cms.untracked.double(0.742),
                         crossSection = cms.untracked.double(7899.),
                         comEnergy = cms.double(2760.0),
                         PythiaParameters = cms.PSet(
    pythiaUESettingsBlock,
    processParameters = cms.vstring('MSEL        = 0    !User defined processes',
                                    'MSUB(2)     = 1    !W production',
                                    'MDME(190,1) = 0    !W decay into dbar u',
                                    'MDME(191,1) = 0    !W decay into dbar c',
                                    'MDME(192,1) = 0    !W decay into dbar t',
                                    'MDME(194,1) = 0    !W decay into sbar u',
                                    'MDME(195,1) = 0    !W decay into sbar c',
                                    'MDME(196,1) = 0    !W decay into sbar t',
                                    'MDME(198,1) = 0    !W decay into bbar u',
                                    'MDME(199,1) = 0    !W decay into bbar c',
                                    'MDME(200,1) = 0    !W decay into bbar t',
                                    'MDME(205,1) = 0    !W decay into bbar tp',
                                    'MDME(206,1) = 1    !W decay into e+ nu_e',
                                    'MDME(207,1) = 0    !W decay into mu+ nu_mu',
                                    'MDME(208,1) = 0    !W decay into tau+ nu_tau'),
    # This is a vector of ParameterSet names to be read, in this order
    parameterSets = cms.vstring('pythiaUESettings',
                                'processParameters')
    )
                         )


configurationMetadata = cms.untracked.PSet(
    version = cms.untracked.string('$Revision: 1.1 $'),
    name = cms.untracked.string('$Source: /local/reps/CMSSW/UserCode/CmsHi/PhotonAnalysis/python/hiSignal_2760GeV_Wev_PYTHIA6_cfi.py,v $'),
    annotation = cms.untracked.string('PYTHIA6-Wenu Tune Z2 at 7TeV')
    )



