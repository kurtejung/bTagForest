
# Auto generated configuration file
# using: 
# Revision: 1.341 
# Source: /cvs_server/repositories/CMSSW/CMSSW/Configuration/PyReleaseValidation/python/ConfigBuilder.py,v 
# with command line options: Configuration/GenProduction/python/QCD_Pt_15to3000_TuneZ2_Flat_7TeV_pythia6_cff.py -s GEN --datatier=GEN-SIM-RAW --conditions 
#auto:mc --eventcontent RAWSIM --no_exec -n 10000 --python_filename=rivet_cfg.py --customise=Configuration/GenProduction/rivet_customize.py
import FWCore.ParameterSet.Config as cms

process = cms.Process('GEN')

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.Generator_cff')
process.load('IOMC.EventVertexGenerators.VtxSmearedRealistic7TeV2011Collision_cfi')
process.load('GeneratorInterface.Core.genFilterSummary_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(500)
)
process.MessageLogger.cerr.FwkReport.reportEvery = 100

# Input source
process.source = cms.Source("EmptySource")

# Production Info
process.configurationMetadata = cms.untracked.PSet(
	version = cms.untracked.string('$Revision: 1.1 $'),
	name = cms.untracked.string('$Source: /afs/cern.ch/project/cvs/reps/CMSSW/CMSSW/GeneratorInterface/ReggeGribovPartonMCInterface/python/ReggeGribovPartonMC_EposLHC_8TeV_pp_cfi.py,v $'),
	annotation = cms.untracked.string('ReggeGribovMC generator')
	)

# Output definition

process.GENoutput = cms.OutputModule("PoolOutputModule",
    splitLevel = cms.untracked.int32(0),
    eventAutoFlushCompressedSize = cms.untracked.int32(5242880),
    outputCommands = process.RAWSIMEventContent.outputCommands,
    fileName = cms.untracked.string('EPOS_GEN.root'),
    dataset = cms.untracked.PSet(
        filterName = cms.untracked.string(''),
        dataTier = cms.untracked.string('GEN')
    ),
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('generation_step')
    )
)

# Additional output definition

# Other statements
process.GlobalTag.globaltag = 'MC_53_V14::All'

process.generator = cms.EDFilter("ReggeGribovPartonMCGeneratorFilter",
			                     beammomentum = cms.double(450),
			                     targetmomentum = cms.double(-450),
			                     beamid = cms.int32(1),
			                     targetid = cms.int32(1),
			                     model = cms.int32(0),
			                     skipNuclFrag = cms.bool(True),
                                             bmin = cms.double(0),
			                     bmax = cms.double(10000),
                                             paramFileName = cms.untracked.string("Configuration/Generator/data/ReggeGribovPartonMC.param")
			                     )


# Path and EndPath definitions
process.generation_step = cms.Path(process.pgen)
process.genfiltersummary_step = cms.EndPath(process.genFilterSummary)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.GENoutput_step = cms.EndPath(process.GENoutput)

# Schedule definition
process.schedule = cms.Schedule(process.generation_step,process.genfiltersummary_step,process.endjob_step,process.GENoutput_step)
# filter all path with the production filter sequence
for path in process.paths:
	getattr(process,path)._seq = process.generator * getattr(process,path)._seq 

# customisation of the process.

# Automatic addition of the customisation function from Configuration.GenProduction.rivet_customize
# from Configuration.GenProduction.rivet_customize import customise 
def customise(process):
        process.load('GeneratorInterface.RivetInterface.rivetAnalyzer_cfi')
        process.rivetAnalyzer.AnalysisNames = cms.vstring('ATLAS_2010_S8894728')#CMS_2010_S8547297')
        process.rivetAnalyzer.OutputFile= cms.string('EPOS.aida')
        process.generation_step+=process.rivetAnalyzer
        process.schedule.remove(process.GENoutput_step)
        return(process)

#call to customisation function customise imported from Configuration.GenProduction.rivet_customize
process = customise(process)

# End of customisation functions

