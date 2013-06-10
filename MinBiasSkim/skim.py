import FWCore.ParameterSet.Config as cms
process = cms.Process("HIGHPTSKIM")

process.load('Configuration.StandardSequences.Services_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContentHeavyIons_cff')

process.source = cms.Source("PoolSource",
   fileNames = cms.untracked.vstring(
	'/store/hidata/HIRun2013/PAMinBiasUPC/RAW/v1/000/210/614/00000/F6C8DA00-3664-E211-9914-BCAEC518FF63.root'
	)
)

# =============== Other Statements =====================
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))

#Trigger Selection
### Comment out for the timing being assuming running on secondary dataset with trigger bit selected already
import HLTrigger.HLTfilters.hltHighLevel_cfi
process.hltHIZeroBiasSingleTrack = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone()
process.hltHIZeroBiasSingleTrack.HLTPaths = ['HLT_PAZeroBiasPixel_SingleTrack_v*'] # for allphysics
process.hltHIZeroBiasSingleTrack.andOr = cms.bool(True)
process.hltHIZeroBiasSingleTrack.throw = cms.bool(False)

process.eventFilter_step = cms.Path( process.hltHIZeroBiasSingleTrack )

process.output = cms.OutputModule("PoolOutputModule",
    outputCommands = process.FEVTEventContent.outputCommands,
    fileName = cms.untracked.string('hiZeroBiasSingleTrack.root'),
    SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring('eventFilter_step')),
    dataset = cms.untracked.PSet(
      dataTier = cms.untracked.string('RAW'),
      filterName = cms.untracked.string('hiZeroBiasSingleTrack'))
)

process.output_step = cms.EndPath(process.output)

process.schedule = cms.Schedule(
    process.eventFilter_step,
    process.output_step
)
