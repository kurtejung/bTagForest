// -*- C++ -*-
//
// Package:    TrackAnalyzer
// Class:      TrackAnalyzer
// 
/**\class TrackAnalyzer TrackAnalyzer.cc MitHig/TrackAnalyzer/src/TrackAnalyzer.cc

Description: <one line class summary>

Implementation:
Prepare the Treack Tree for analysis
 */
//
// Original Author:  Yilmaz Yetkin, Yen-Jie Lee
// Updated: Frank Ma, Matt Nguyen
//         Created:  Tue Sep 30 15:14:28 CEST 2008
// $Id: TrackAnalyzer.cc,v 1.53 2013/02/03 20:00:06 mnguyen Exp $
//
//


// system include files
#include <memory>
#include <iostream>
#include <vector>
#include <string>
#include <map>

// CMSSW user include files
#include "DataFormats/Common/interface/DetSetAlgorithm.h"
#include "DataFormats/GeometryVector/interface/GlobalPoint.h"
#include "DataFormats/SiPixelDetId/interface/PXBDetId.h"
#include "DataFormats/SiPixelDetId/interface/PXFDetId.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/HeavyIonEvent/interface/Centrality.h"
#include "DataFormats/HeavyIonEvent/interface/CentralityProvider.h"
#include "DataFormats/TrackerRecHit2D/interface/SiPixelRecHitCollection.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "Geometry/Records/interface/TrackerDigiGeometryRecord.h"
#include "Geometry/TrackerGeometryBuilder/interface/PixelGeomDetUnit.h"
#include "Geometry/TrackerGeometryBuilder/interface/TrackerGeometry.h"
#include "Geometry/TrackerGeometryBuilder/interface/TrackerLayerIdAccessor.h"
#include "HLTrigger/HLTcore/interface/HLTConfigProvider.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "SimDataFormats/TrackingAnalysis/interface/TrackingVertex.h"
#include "SimDataFormats/TrackingAnalysis/interface/TrackingVertexContainer.h"
#include "SimDataFormats/TrackingAnalysis/interface/TrackingParticle.h"
#include "SimDataFormats/TrackingHit/interface/PSimHit.h"
#include "SimGeneral/HepPDTRecord/interface/ParticleDataTable.h"
#include "SimTracker/TrackerHitAssociation/interface/TrackerHitAssociator.h"
#include "DataFormats/SiPixelDetId/interface/PixelEndcapName.h"

#include "DataFormats/L1GlobalTrigger/interface/L1GlobalTriggerReadoutSetup.h"
#include "DataFormats/L1GlobalTrigger/interface/L1GlobalTriggerReadoutRecord.h"
#include "DataFormats/L1GlobalTrigger/interface/L1GlobalTriggerObjectMapRecord.h"
#include "DataFormats/L1GlobalTrigger/interface/L1GlobalTriggerObjectMap.h"
#include "L1Trigger/GlobalTrigger/interface/L1GlobalTrigger.h"

#include "DataFormats/Math/interface/Point3D.h"
#include "DataFormats/BeamSpot/interface/BeamSpot.h"

#include "SimDataFormats/TrackingAnalysis/interface/TrackingParticle.h"
#include "SimDataFormats/TrackingAnalysis/interface/TrackingParticleFwd.h"
#include "SimTracker/Records/interface/TrackAssociatorRecord.h"
#include "DataFormats/RecoCandidate/interface/TrackAssociation.h"
#include "SimTracker/TrackAssociation/interface/TrackAssociatorByHits.h"
#include "DataFormats/TrackReco/interface/DeDxData.h"

// Heavyion
#include "DataFormats/HeavyIonEvent/interface/Centrality.h"

// Particle Flow
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"
#include "DataFormats/ParticleFlowReco/interface/PFBlock.h"
#include "DataFormats/ParticleFlowReco/interface/PFCluster.h"
#include "DataFormats/ParticleFlowReco/interface/PFClusterFwd.h"

// Vertex significance
#include "RecoBTag/SecondaryVertex/interface/SecondaryVertex.h"

// Root include files
#include "TTree.h"

using namespace std;
using namespace edm;
using namespace reco;

//
// class decleration
//

#define PI 3.14159265358979

#define MAXTRACKS 50000
#define MAXVTX 100
#define MAXQUAL 5

struct TrackEvent{

  // event information
  int nRun;
  int nEv;
  int nLumi;
  int nBX;
  int N; // multiplicity variable 

  // Vertex information
  int nv;
  float vx[MAXVTX];
  float vy[MAXVTX];
  float vz[MAXVTX];
  float vxError[MAXVTX];
  float vyError[MAXVTX];
  float vzError[MAXVTX];
  int nDaugher[MAXVTX];

  // Multiple vtx information
  int nVtx;

  int nTrkVtx[MAXVTX];
  float normChi2Vtx[MAXVTX];
  float sumPtVtx[MAXVTX];
  //int nTrkVtxHard[MAXVTX];
  int maxVtx;
  //int maxVtxHard;

  float xVtx[MAXVTX];
  float yVtx[MAXVTX];
  float zVtx[MAXVTX];
  float xVtxErr[MAXVTX];
  float yVtxErr[MAXVTX];
  float zVtxErr[MAXVTX];

  float vtxDist2D[MAXVTX];
  float vtxDist2DErr[MAXVTX];
  float vtxDist2DSig[MAXVTX];
  float vtxDist3D[MAXVTX];
  float vtxDist3DErr[MAXVTX];
  float vtxDist3DSig[MAXVTX];


  // centrality
  int cbin;

  // -- rec tracks --
  int nTrk;
  float trkEta[MAXTRACKS];
  float trkPhi[MAXTRACKS];
  float trkPt[MAXTRACKS];
  float trkPtError[MAXTRACKS];
  int trkNHit[MAXTRACKS];
  int trkNlayer[MAXTRACKS];
  int trkNlayer3D[MAXTRACKS];
  bool trkQual[MAXQUAL][MAXTRACKS];
  float trkChi2[MAXTRACKS];
  float trkChi2hit1D[MAXTRACKS];
  float trkNdof[MAXTRACKS];
  float trkDz[MAXTRACKS];
  float trkDz1[MAXTRACKS];               // dZ to the first vertex
  float trkDz2[MAXTRACKS];               // dZ to the second vertex
  float trkDzError[MAXTRACKS];
  float trkDzError1[MAXTRACKS];          
  float trkDzError2[MAXTRACKS];          
  float trkDxy[MAXTRACKS];
  float trkDxyBS[MAXTRACKS];
  float trkDxy1[MAXTRACKS];              // d0 to the first vertex
  float trkDxy2[MAXTRACKS];              // d0 to the second vertex
  float trkDxyError[MAXTRACKS];          
  float trkDxyErrorBS[MAXTRACKS];          
  float trkDxyError1[MAXTRACKS];          
  float trkDxyError2[MAXTRACKS];          
  float trkVx[MAXTRACKS];
  float trkVy[MAXTRACKS];
  float trkVz[MAXTRACKS];
  bool  trkFake[MAXTRACKS];
  float trkAlgo[MAXTRACKS];
  float dedx[MAXTRACKS];
  int trkCharge[MAXTRACKS];
  unsigned int trkVtxIndex[MAXTRACKS];

  float trkExpHit1Eta[MAXTRACKS];
  float trkExpHit2Eta[MAXTRACKS];
  float trkExpHit3Eta[MAXTRACKS];
  float trkStatus[MAXTRACKS];

  //matched PF Candidate Info
  int pfType[MAXTRACKS];
  float pfCandPt[MAXTRACKS];
  float pfSumEcal[MAXTRACKS];
  float pfSumHcal[MAXTRACKS];

  // -- sim tracks --
  int   nParticle;
  float pStatus[MAXTRACKS];
  float pPId[MAXTRACKS];
  float pEta[MAXTRACKS];
  float pPhi[MAXTRACKS];
  float pPt[MAXTRACKS];
  float pAcc[MAXTRACKS];
  float pAccPair[MAXTRACKS];
  int pCharge[MAXTRACKS];

  float pNRec[MAXTRACKS];
  int   pNHit[MAXTRACKS];
  // matched track info (if matched)
  float mtrkPt[MAXTRACKS];
  float mtrkPtError[MAXTRACKS];
  int   mtrkNHit[MAXTRACKS];
  int   mtrkNlayer[MAXTRACKS];
  int   mtrkNlayer3D[MAXTRACKS];
  int   mtrkQual[MAXTRACKS];
  float mtrkChi2[MAXTRACKS];
  float mtrkNdof[MAXTRACKS];
  float mtrkDz1[MAXTRACKS];
  float mtrkDzError1[MAXTRACKS];
  float mtrkDxy1[MAXTRACKS];
  float mtrkDxyError1[MAXTRACKS];          
  float mtrkAlgo[MAXTRACKS];
  // calo compatibility
  int mtrkPfType[MAXTRACKS];
  float mtrkPfCandPt[MAXTRACKS];
  float mtrkPfSumEcal[MAXTRACKS];
  float mtrkPfSumHcal[MAXTRACKS];
};

class TrackAnalyzer : public edm::EDAnalyzer {

  public:
    explicit TrackAnalyzer(const edm::ParameterSet&);
    ~TrackAnalyzer();

  private:
    virtual void beginJob() ;
    virtual void analyze(const edm::Event&, const edm::EventSetup&);
    virtual void endJob() ;

    void fillVertices(const edm::Event& iEvent);
    void fillTracks(const edm::Event& iEvent, const edm::EventSetup& iSetup);
    void fillSimTracks(const edm::Event& iEvent, const edm::EventSetup& iSetup);
    void matchPFCandToTrack(const edm::Event& iEvent, const edm::EventSetup& iSetup, unsigned it, int & cand_type, float & cand_pt, float & mEcalSum, float & mHcalSum);
    std::pair<bool,bool> isAccepted(TrackingParticle & tp);
    int getLayerId(const PSimHit&);
    bool hitDeadPXF(const reco::Track& tr);

    template <typename TYPE>
      void                          getProduct(const std::string name, edm::Handle<TYPE> &prod,
	  const edm::Event &event) const;    
    template <typename TYPE>
      bool                          getProductSafe(const std::string name, edm::Handle<TYPE> &prod,
	  const edm::Event &event) const;

    int associateSimhitToTrackingparticle(unsigned int trid );
    bool checkprimaryparticle(const TrackingParticle* tp);

    // ----------member data ---------------------------

    bool doTrack_;
    bool doTrackExtra_;
    bool doSimTrack_;
    bool doSimVertex_;
    bool fillSimTrack_;
    bool doPFMatching_;
    bool useCentrality_;  
    bool useQuality_;
   bool doDeDx_;
    bool doDebug_;

    double trackPtMin_;
   std::vector<std::string> qualityStrings_;
   std::string qualityString_;
   
    double simTrackPtMin_;
    bool fiducialCut_;
    edm::InputTag trackSrc_;
    edm::InputTag tpFakeSrc_;
    edm::InputTag tpEffSrc_;
    edm::InputTag pfCandSrc_;
   edm::InputTag DeDxSrc_;

    vector<string> vertexSrc_;
    edm::InputTag simVertexSrc_;

    const TrackerGeometry* geo_;
    edm::Service<TFileService> fs;           
    edm::ESHandle < ParticleDataTable > pdt;
    edm::Handle<TrackingParticleCollection> trackingParticles;
    CentralityProvider * centrality_;

    edm::InputTag beamSpotProducer_;

    // Root object
    TTree* trackTree_;

    TrackEvent pev_;

    // Acceptance
    enum { BPix1=0, BPix2=1, BPix3=2,
      FPix1_neg=3, FPix2_neg=4,
      FPix1_pos=5, FPix2_pos=6,
      nLayers=7};

};

//--------------------------------------------------------------------------------------------------
TrackAnalyzer::TrackAnalyzer(const edm::ParameterSet& iConfig)

{

   doTrack_             = iConfig.getUntrackedParameter<bool>  ("doTrack",true);
   doTrackExtra_             = iConfig.getUntrackedParameter<bool>  ("doTrackExtra",false);
   doSimTrack_             = iConfig.getUntrackedParameter<bool>  ("doSimTrack",false);
   fillSimTrack_             = iConfig.getUntrackedParameter<bool>  ("fillSimTrack",false);

   doDeDx_             = iConfig.getUntrackedParameter<bool>  ("doDeDx",false);
   doDebug_             = iConfig.getUntrackedParameter<bool>  ("doDebug",false);

   doPFMatching_             = iConfig.getUntrackedParameter<bool>  ("doPFMatching",false);
   useCentrality_ = iConfig.getUntrackedParameter<bool>("useCentrality",false);
   useQuality_ = iConfig.getUntrackedParameter<bool>("useQuality",false);

   trackPtMin_             = iConfig.getUntrackedParameter<double>  ("trackPtMin",0.4);
   qualityString_ = iConfig.getUntrackedParameter<std::string>("qualityString","highPurity");

   qualityStrings_ = iConfig.getUntrackedParameter<std::vector<std::string> >("qualityStrings",std::vector<std::string>(0));
   if(qualityStrings_.size() == 0) qualityStrings_.push_back(qualityString_);

   simTrackPtMin_             = iConfig.getUntrackedParameter<double>  ("simTrackPtMin",0.4);
   fiducialCut_ = (iConfig.getUntrackedParameter<bool>("fiducialCut",false));
   trackSrc_ = iConfig.getParameter<edm::InputTag>("trackSrc");
   //   tpFakeSrc_ =  iConfig.getUntrackedParameter<edm::InputTag>("tpFakeSrc",edm::InputTag("cutsTPForFak"));
   //   tpEffSrc_ =  iConfig.getUntrackedParameter<edm::InputTag>("tpEffSrc",edm::InputTag("cutsTPForEff"));
   tpFakeSrc_ =  iConfig.getUntrackedParameter<edm::InputTag>("tpFakeSrc",edm::InputTag("mergedtruth","MergedTrackTruth"));
   tpEffSrc_ =  iConfig.getUntrackedParameter<edm::InputTag>("tpEffSrc",edm::InputTag("mergedtruth","MergedTrackTruth"));

   vertexSrc_ = iConfig.getParameter<vector<string> >("vertexSrc");
   simVertexSrc_ =  iConfig.getUntrackedParameter<edm::InputTag>("tpVtxSrc",edm::InputTag("mergedtruth","MergedTrackTruth"));
   beamSpotProducer_  = iConfig.getUntrackedParameter<edm::InputTag>("beamSpotSrc",edm::InputTag("offlineBeamSpot"));   
   pfCandSrc_ = iConfig.getParameter<edm::InputTag>("pfCandSrc");

  doSimVertex_             = iConfig.getUntrackedParameter<bool>  ("doSimVertex",false);

}

//--------------------------------------------------------------------------------------------------
TrackAnalyzer::~TrackAnalyzer()
{
}

//--------------------------------------------------------------------------------------------------
  void
TrackAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  // Get tracker geometry
  //  cout <<"StartFill"<<endl;
  
  edm::ESHandle<TrackerGeometry> tGeo;
  iSetup.get<TrackerDigiGeometryRecord>().get(tGeo);
  geo_ = tGeo.product();
  iSetup.getData(pdt);

  //  cout <<"Got data"<<endl;
  pev_.nEv = (int)iEvent.id().event();
  pev_.nRun = (int)iEvent.id().run();
  pev_.nLumi = (int)iEvent.luminosityBlock();
  pev_.nBX = (int)iEvent.bunchCrossing();
  pev_.N = 0;

  pev_.nv = 0;
  pev_.nParticle = 0;
  pev_.nTrk = 0;

  //  cout <<"Fill Vtx"<<endl;
  fillVertices(iEvent);

  if(useCentrality_){
    if(!centrality_) centrality_ = new CentralityProvider(iSetup);      
    centrality_->newEvent(iEvent,iSetup); // make sure you do this first in every event
    pev_.cbin = centrality_->getBin();
  }

  //cout <<"Fill Tracks"<<endl;
  if (doTrack_) fillTracks(iEvent, iSetup);
  //  cout <<"Tracks filled!"<<endl;
  if (doSimTrack_) fillSimTracks(iEvent, iSetup);
  //  cout <<"SimTracks filled!"<<endl;
  trackTree_->Fill();
  //  cout <<"Tree filled!"<<endl;
  memset(&pev_,0,sizeof pev_);

}

//--------------------------------------------------------------------------------------------------
void
TrackAnalyzer::fillVertices(const edm::Event& iEvent){

  // Vertex 0 : pev_vz[0] MC information from TrackingVertexCollection
  // Vertex 1 - n : Reconstructed Vertex from various of algorithms
  pev_.vx[0]=0;
  pev_.vy[0]=0;
  pev_.vz[0]=0;
  pev_.vxError[0]=0;
  pev_.vyError[0]=0;
  pev_.vzError[0]=0;
  pev_.nDaugher[0]=0;

  if(doSimVertex_){
    Handle<TrackingVertexCollection> vertices;
    iEvent.getByLabel(simVertexSrc_, vertices);
    int greatestvtx = -1;
    for (unsigned int i = 0 ; i< vertices->size(); ++i){
      unsigned int daughter = (*vertices)[i].nDaughterTracks();
      if (greatestvtx==-1) {
         greatestvtx = i;
      } else {
         if( daughter >(*vertices)[greatestvtx].nDaughterTracks()&&fabs((*vertices)[i].position().z())<30000) greatestvtx = i;
      }
    }

    if(greatestvtx != -1){
      pev_.vz[pev_.nv] = (*vertices)[greatestvtx].position().z();
    }else{
      pev_.vz[pev_.nv] =  -99; 
    }
  } else {
    pev_.vz[pev_.nv] = -99;
  }

  pev_.nv++;

  // Fill reconstructed vertices.   
  for(unsigned int iv = 0; iv < vertexSrc_.size(); ++iv){
    const reco::VertexCollection * recoVertices;
    edm::Handle<reco::VertexCollection> vertexCollection;
    //cout <<vertexSrc_[iv]<<endl;
    iEvent.getByLabel(vertexSrc_[iv],vertexCollection);
    recoVertices = vertexCollection.product();
    unsigned int daughter = 0;
    int nVertex = 0;
    unsigned int greatestvtx = 0;

    nVertex = recoVertices->size();
    pev_.nVtx = nVertex;
    for (unsigned int i = 0 ; i< recoVertices->size(); ++i){
      daughter = (*recoVertices)[i].tracksSize();
      if( daughter > (*recoVertices)[greatestvtx].tracksSize()) greatestvtx = i;

      pev_.xVtx[i] = (*recoVertices)[i].position().x();
      pev_.yVtx[i] = (*recoVertices)[i].position().y();
      pev_.zVtx[i] = (*recoVertices)[i].position().z();
      pev_.xVtxErr[i] = (*recoVertices)[i].xError();
      pev_.yVtxErr[i] = (*recoVertices)[i].yError();
      pev_.zVtxErr[i] = (*recoVertices)[i].zError();
      pev_.nTrkVtx[i] = (*recoVertices)[i].tracksSize();
      pev_.normChi2Vtx[i] = (*recoVertices)[i].normalizedChi2();

    
      float vtxSumPt=0.;
      for (reco::Vertex::trackRef_iterator it = (*recoVertices)[i].tracks_begin(); it != (*recoVertices)[i].tracks_end(); it++) {
	vtxSumPt += (**it).pt();

	Handle<vector<Track> > etracks;
	iEvent.getByLabel(trackSrc_, etracks);

	for(unsigned itrack=0; itrack<etracks->size(); ++itrack){
	  reco::TrackRef trackRef=reco::TrackRef(etracks,itrack);
	  //cout<<" trackRef.key() "<<trackRef.key()<< " it->key() "<<it->key()<<endl;
	  if(trackRef.key()==it->key()){
	    pev_.trkVtxIndex[itrack] = i+1;  // note that index starts from 1 
	    //cout<< " matching track "<<itrack<<endl;
	  }
	}
      }

      pev_.sumPtVtx[i] = vtxSumPt;
	  
    }

    pev_.maxVtx = greatestvtx;

    //loop over vertices again to get the significance wrt the leading vertex -Matt
    for (unsigned int i = 0 ; i< recoVertices->size(); ++i){
      if(i==greatestvtx) continue;
      GlobalVector direction = GlobalVector(pev_.xVtx[i]-pev_.xVtx[greatestvtx],pev_.xVtx[i]-pev_.xVtx[greatestvtx],pev_.xVtx[i]-pev_.xVtx[greatestvtx]);
      Measurement1D vtxDist2D = reco::SecondaryVertex::computeDist2d((*recoVertices)[greatestvtx], (*recoVertices)[i], direction, true);
      Measurement1D vtxDist3D = reco::SecondaryVertex::computeDist3d((*recoVertices)[greatestvtx], (*recoVertices)[i], direction, true);
      pev_.vtxDist2D[i]=vtxDist2D.value();
      pev_.vtxDist2DErr[i]=vtxDist2D.error();
      pev_.vtxDist2DSig[i]=vtxDist2D.significance();
      pev_.vtxDist3D[i]=vtxDist3D.value();
      pev_.vtxDist3DErr[i]=vtxDist3D.error();
      pev_.vtxDist3DSig[i]=vtxDist3D.significance();
    }

    if(recoVertices->size()>0){
      pev_.vx[pev_.nv] = (*recoVertices)[greatestvtx].position().x();
      pev_.vy[pev_.nv] = (*recoVertices)[greatestvtx].position().y();
      pev_.vz[pev_.nv] = (*recoVertices)[greatestvtx].position().z();
      pev_.vxError[pev_.nv] = (*recoVertices)[greatestvtx].xError();
      pev_.vyError[pev_.nv] = (*recoVertices)[greatestvtx].yError();
      pev_.vzError[pev_.nv] = (*recoVertices)[greatestvtx].zError();
      pev_.nDaugher[pev_.nv] = (*recoVertices)[greatestvtx].tracksSize();
    }else{
      pev_.vx[pev_.nv] =  -99;
      pev_.vy[pev_.nv] =  -99;
      pev_.vz[pev_.nv] =  -99;
      pev_.vxError[pev_.nv] =  -99;
      pev_.vyError[pev_.nv] =  -99;
      pev_.vzError[pev_.nv] =  -99;
      pev_.nDaugher[pev_.nv] = -99;
      
    }
    pev_.nv++;
    //cout <<pev_.nv<<endl;
  }

}



//--------------------------------------------------------------------------------------------------
void
TrackAnalyzer::fillTracks(const edm::Event& iEvent, const edm::EventSetup& iSetup){
  Handle<vector<Track> > etracks;
  iEvent.getByLabel(trackSrc_, etracks);
  reco::BeamSpot beamSpot;
  edm::Handle<reco::BeamSpot> recoBeamSpotHandle;
  iEvent.getByLabel(beamSpotProducer_,recoBeamSpotHandle);
  beamSpot = *recoBeamSpotHandle;

  // do reco-to-sim association
  Handle<TrackingParticleCollection>  TPCollectionHfake;
  Handle<edm::View<reco::Track> >  trackCollection;
  iEvent.getByLabel(trackSrc_, trackCollection);
  ESHandle<TrackAssociatorBase> theAssociator;
  const TrackAssociatorByHits *theAssociatorByHits;
  reco::RecoToSimCollection recSimColl;

  Handle<DeDxDataValueMap> DeDxMap;
  if(doDeDx_){
     iEvent.getByLabel(DeDxSrc_, DeDxMap);
  }

  if(doSimTrack_) {
    iEvent.getByLabel(tpFakeSrc_,TPCollectionHfake);
    iSetup.get<TrackAssociatorRecord>().get("TrackAssociatorByHits",theAssociator);
    theAssociatorByHits = (const TrackAssociatorByHits*) theAssociator.product();

    //       simRecColl= theAssociatorByHits->associateSimToReco(trackCollection,TPCollectionHeff,&iEvent);
    recSimColl= theAssociatorByHits->associateRecoToSim(trackCollection,TPCollectionHfake,&iEvent);
  }

  pev_.nTrk=0;
  pev_.N=0;
  for(unsigned it=0; it<etracks->size(); ++it){
    const reco::Track & etrk = (*etracks)[it];
    reco::TrackRef trackRef=reco::TrackRef(etracks,it);

    if (etrk.pt()<trackPtMin_) continue;
    if(fiducialCut_ && hitDeadPXF(etrk)) continue; // if track hits the dead region, igonore it;


    for(unsigned int iq = 0; iq < qualityStrings_.size(); ++iq){
       pev_.trkQual[iq][pev_.nTrk]=0;
       if(etrk.quality(reco::TrackBase::qualityByName(qualityStrings_[iq].data()))) pev_.trkQual[iq][pev_.nTrk]=1;
    }

    if(useQuality_ && etrk.quality(reco::TrackBase::qualityByName(qualityString_)) != 1) continue;

    if(doDeDx_){
       pev_.dedx[pev_.nTrk]=(*DeDxMap)[trackRef].dEdx();
    }

    trackingRecHit_iterator edh = etrk.recHitsEnd();
    int count1dhits=0;
    for (trackingRecHit_iterator ith = etrk.recHitsBegin(); ith != edh; ++ith) {
      const TrackingRecHit * hit = ith->get();
      //DetId detid = hit->geographicalId();
      if (hit->isValid()) {
	if (typeid(*hit) == typeid(SiStripRecHit1D)) ++count1dhits;
      }
    }
    pev_.trkEta[pev_.nTrk]=etrk.eta();
    pev_.trkPhi[pev_.nTrk]=etrk.phi();
    pev_.trkPt[pev_.nTrk]=etrk.pt();
    pev_.trkPtError[pev_.nTrk]=etrk.ptError();
    pev_.trkCharge[pev_.nTrk]=etrk.charge();
    pev_.trkNHit[pev_.nTrk]=etrk.numberOfValidHits();
    pev_.trkDxy[pev_.nTrk]=etrk.dxy();
    pev_.trkDxyError[pev_.nTrk]=etrk.dxyError();
    pev_.trkDz[pev_.nTrk]=etrk.dz();
    pev_.trkDzError[pev_.nTrk]=etrk.dzError();
    pev_.trkChi2[pev_.nTrk]=etrk.chi2();
    pev_.trkNdof[pev_.nTrk]=etrk.ndof();
    pev_.trkChi2hit1D[pev_.nTrk]=(etrk.chi2()+count1dhits)/double(etrk.ndof()+count1dhits);
    pev_.trkVx[pev_.nTrk]=etrk.vx();
    pev_.trkVy[pev_.nTrk]=etrk.vy();
    pev_.trkVz[pev_.nTrk]=etrk.vz();

    math::XYZPoint v1(pev_.vx[1],pev_.vy[1], pev_.vz[1]);
    pev_.trkDz1[pev_.nTrk]=etrk.dz(v1);
    pev_.trkDzError1[pev_.nTrk]=sqrt(etrk.dzError()*etrk.dzError()+pev_.vzError[1]*pev_.vzError[1]);
    pev_.trkDxy1[pev_.nTrk]=etrk.dxy(v1);
    pev_.trkDxyError1[pev_.nTrk]=sqrt(etrk.dxyError()*etrk.dxyError()+pev_.vxError[1]*pev_.vyError[1]);

    math::XYZPoint v2(pev_.vx[2],pev_.vy[2], pev_.vz[2]);
    pev_.trkDz2[pev_.nTrk]=etrk.dz(v2);
    pev_.trkDzError2[pev_.nTrk]=sqrt(etrk.dzError()*etrk.dzError()+pev_.vzError[2]*pev_.vzError[2]);
    pev_.trkDxy2[pev_.nTrk]=etrk.dxy(v2);
    pev_.trkDxyError2[pev_.nTrk]=sqrt(etrk.dxyError()*etrk.dxyError()+pev_.vxError[2]*pev_.vyError[2]);

    pev_.trkDxyBS[pev_.nTrk]=etrk.dxy(beamSpot.position());
    pev_.trkDxyErrorBS[pev_.nTrk]=sqrt(etrk.dxyError()*etrk.dxyError()+beamSpot.BeamWidthX()*beamSpot.BeamWidthY());

    pev_.trkNlayer[pev_.nTrk] = etrk.hitPattern().trackerLayersWithMeasurement();
    pev_.trkNlayer3D[pev_.nTrk] = etrk.hitPattern().pixelLayersWithMeasurement() + etrk.hitPattern().numberOfValidStripLayersWithMonoAndStereo();

    pev_.trkAlgo[pev_.nTrk] = etrk.algo();

    // multiplicity variable
    if (pev_.trkQual[0][pev_.nTrk]&&
        (fabs(pev_.trkDz1[pev_.nTrk]/pev_.trkDzError1[pev_.nTrk]) < 3)&&
        (fabs(pev_.trkDxy1[pev_.nTrk]/pev_.trkDxyError1[pev_.nTrk]) < 3)&&
        (pev_.trkPtError[pev_.nTrk]/pev_.trkPt[pev_.nTrk]<0.1)&&
        (fabs(pev_.trkEta[pev_.nTrk]) < 2.4)&&
        (pev_.trkPt[pev_.nTrk] > 0.4)
       ) pev_.N++;

    /*
      // done in vertex loop instead
    for(unsigned int iv = 0; iv < vertexSrc_.size(); ++iv){
      const reco::VertexCollection * recoVertices;
      edm::Handle<reco::VertexCollection> vertexCollection;
      iEvent.getByLabel(vertexSrc_[iv],vertexCollection);
      recoVertices = vertexCollection.product();
      
      
      for (unsigned int ivert = 0 ; ivert< recoVertices->size(); ++ivert){

	for (reco::Vertex::trackRef_iterator tr_it = (*recoVertices)[ivert].tracks_begin(); tr_it != (*recoVertices)[ivert].tracks_end(); tr_it++) {
	  
	    cout<<" trackRef.key() "<<trackRef.key()<< " tr_it->key() "<<tr_it->key()<<endl;
	    if(trackRef.key()==tr_it->key()){
	      //pev_.trkVtxIndex[itrack] = i+1;  // note that index starts from 1 
	      pev_.trkVtxIndex[pev_.nTrk] = 1;  // note that index starts from 1 
	      cout<< " matching track "<<pev_.nTrk<<endl;
	    }
	  }
      }
    }
    */

    if (doSimTrack_) {
      pev_.trkFake[pev_.nTrk]=0;
      pev_.trkStatus[pev_.nTrk]=-999;

      reco::RecoToSimCollection::const_iterator matchedSim = recSimColl.find(edm::RefToBase<reco::Track>(trackRef));

      if(matchedSim == recSimColl.end()){
	 pev_.trkFake[pev_.nTrk]=1;
      }else{
	 //  pev_.trkStatus[pev_.nTrk]=matchedSim->status();
      }
    }


    if (doTrackExtra_) {
      // Very rough estimation of the expected position of the Pixel Hit
      double r = 4.4; // averaged first layer rho
      double x = r*cos(etrk.phi())+etrk.vx();
      double y = r*sin(etrk.eta())+etrk.vy();
      double z = r/tan(atan(exp(-etrk.eta()))*2)+etrk.vz();
      ROOT::Math::XYZVector tmpVector(x-pev_.vx[1],y-pev_.vy[1],z-pev_.vz[1]);
      double eta1 = tmpVector.eta();
      //double phi1 = etrk.phi();

      double r2 = 7.29; // averaged 2nd layer rho
      x = r2*cos(etrk.phi())+etrk.vx();
      y = r2*sin(etrk.eta())+etrk.vy();
      z = r2/tan(atan(exp(-etrk.eta()))*2)+etrk.vz();
      ROOT::Math::XYZVector tmpVector2(x-pev_.vx[1],y-pev_.vy[1],z-pev_.vz[1]);
      double eta2 = tmpVector2.eta();


      double r3 = 10.16; // averaged 3rd layer rho
      x = r3*cos(etrk.phi())+etrk.vx();
      y = r3*sin(etrk.eta())+etrk.vy();
      z = r3/tan(atan(exp(-etrk.eta()))*2)+etrk.vz();
      ROOT::Math::XYZVector tmpVector3(x-pev_.vx[1],y-pev_.vy[1],z-pev_.vz[1]);
      double eta3 = tmpVector3.eta();


      pev_.trkExpHit1Eta[pev_.nTrk]=eta1;
      pev_.trkExpHit2Eta[pev_.nTrk]=eta2;
      pev_.trkExpHit3Eta[pev_.nTrk]=eta3;
    }
    //pev_.trkNhit[pev_.nTrk]=tr.numberOfValidHits();
    if(doPFMatching_) matchPFCandToTrack(iEvent, iSetup, it,
	// output to the following vars
	pev_.pfType[pev_.nTrk],
	pev_.pfCandPt[pev_.nTrk],
	pev_.pfSumEcal[pev_.nTrk],
	pev_.pfSumHcal[pev_.nTrk]);	 

    pev_.nTrk++;
  }

}

//--------------------------------------------------------------------------------------------------
  void
TrackAnalyzer::fillSimTracks(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  edm::ESHandle<TrackAssociatorBase> theAssociator;
  edm::Handle<reco::SimToRecoCollection > simtorecoCollectionH;
  edm::Handle<TrackingParticleCollection>  TPCollectionHeff;
  edm::Handle<edm::View<reco::Track> >  trackCollection;

  iEvent.getByLabel(tpEffSrc_,TPCollectionHeff);
  iEvent.getByLabel(trackSrc_,trackCollection);

  // Make simtrk-to-rectrk association
  iSetup.get<TrackAssociatorRecord>().get("TrackAssociatorByHits",theAssociator);
  const TrackAssociatorByHits * theAssociatorByHits = (const TrackAssociatorByHits*) theAssociator.product();
  reco::SimToRecoCollection simRecColl = theAssociatorByHits->associateSimToReco(trackCollection,TPCollectionHeff,&iEvent);

  // Loop through sim tracks
  pev_.nParticle = 0;
  for(TrackingParticleCollection::size_type i=0; i<TPCollectionHeff->size(); i++) {
    TrackingParticleRef tpr(TPCollectionHeff, i);
    TrackingParticle* tp=const_cast<TrackingParticle*>(tpr.get());

    if (tp->pt() < simTrackPtMin_) continue;
    if (tp->status() < 0 || tp->charge()==0) continue; //only charged primaries

    // Fill sim track info
    pev_.pStatus[pev_.nParticle] = tp->status();
    pev_.pPId[pev_.nParticle] = tp->pdgId();
    pev_.pEta[pev_.nParticle] = tp->eta();
    pev_.pPhi[pev_.nParticle] = tp->phi();
    pev_.pPt[pev_.nParticle] = tp->pt();
    std::pair<bool,bool> acc = isAccepted(*tp);
    pev_.pAcc[pev_.nParticle] = acc.first; // triplets
    pev_.pAccPair[pev_.nParticle] = acc.second; // pairs

    // Look up association map
    std::vector<std::pair<edm::RefToBase<reco::Track>, double> > rt;
    const reco::Track* mtrk=0;
    size_t nrec=0;
    if(simRecColl.find(tpr) != simRecColl.end()){
      rt = (std::vector<std::pair<edm::RefToBase<reco::Track>, double> >) simRecColl[tpr];
      nrec=rt.size();   
      if(nrec) mtrk = rt.begin()->first.get();      
    }
    // remove the association if the track hits the bed region in FPIX
    // nrec>0 since we don't need it for nrec=0 case 
    if(fiducialCut_ && nrec>0 && hitDeadPXF(*mtrk)) nrec=0;
    //cout << "simtrk: " << tp->pdgId() << " pt: " << tp->pt() << " nrec: " << nrec << endl;

    // Fill matched rec track info
    pev_.pNRec[pev_.nParticle] = nrec;
    pev_.mtrkQual[pev_.nParticle] = 0;
    if (nrec>0) {
      pev_.mtrkPt[pev_.nParticle] = mtrk->pt();
      pev_.mtrkPtError[pev_.nParticle] = mtrk->ptError();
      pev_.mtrkNHit[pev_.nParticle] = mtrk->numberOfValidHits();
      pev_.mtrkNlayer[pev_.nParticle] = mtrk->hitPattern().trackerLayersWithMeasurement();
      pev_.mtrkNlayer3D[pev_.nParticle] = mtrk->hitPattern().pixelLayersWithMeasurement() + mtrk->hitPattern().numberOfValidStripLayersWithMonoAndStereo();
      if (mtrk->quality(reco::TrackBase::qualityByName(qualityString_))) pev_.mtrkQual[pev_.nParticle] = 1;
      pev_.mtrkChi2[pev_.nParticle]=mtrk->chi2();
      pev_.mtrkNdof[pev_.nParticle]=mtrk->ndof();
      math::XYZPoint v1(pev_.vx[1],pev_.vy[1], pev_.vz[1]);
      pev_.mtrkDz1[pev_.nParticle] = mtrk->dz(v1);
      pev_.mtrkDzError1[pev_.nParticle] = sqrt(mtrk->dzError()*mtrk->dzError()+pev_.vzError[1]*pev_.vzError[1]);
      pev_.mtrkDxy1[pev_.nParticle] = mtrk->dxy(v1);
      pev_.mtrkDxyError1[pev_.nParticle] = sqrt(mtrk->dxyError()*mtrk->dxyError()+pev_.vxError[1]*pev_.vyError[1]);
      pev_.mtrkAlgo[pev_.nParticle] = mtrk->algo();
      // calo matching info for the matched track
      if(doPFMatching_) {
	size_t mtrkkey = rt.begin()->first.key();
	matchPFCandToTrack(iEvent, iSetup, mtrkkey,
	    // output to the following vars
	    pev_.mtrkPfType[pev_.nParticle],
	    pev_.mtrkPfCandPt[pev_.nParticle],
	    pev_.mtrkPfSumEcal[pev_.nParticle],
	    pev_.mtrkPfSumHcal[pev_.nParticle]);
      }
    }

    ++pev_.nParticle;
  }

}


//--------------------------------------------------------------------------------------------------
  void
TrackAnalyzer::matchPFCandToTrack(const edm::Event& iEvent, const edm::EventSetup& iSetup, unsigned it, int & cand_type, float & cand_pt, float & mEcalSum, float & mHcalSum)
{

  // get PF candidates
  Handle<PFCandidateCollection> pfCandidates;
  bool isPFThere = iEvent.getByLabel(pfCandSrc_, pfCandidates);

  if (!isPFThere){
    //cout<<" NO PF Candidates Found"<<endl;
    return;  // if no PFCand in an event, skip it 
  }

  double sum_ecal=0.0, sum_hcal=0.0;


  // loop over pfCandidates to find track

  int cand_index = -999;
  cand_pt = -999.0;
  cand_type =-1;

  for( unsigned ic=0; ic<pfCandidates->size(); ic++ ) {

    const reco::PFCandidate& cand = (*pfCandidates)[ic];

    int type = cand.particleId();

    // only charged hadrons and leptons can be asscociated with a track
    if(!(type == PFCandidate::h ||     //type1
	  type == PFCandidate::e ||     //type2
	  type == PFCandidate::mu      //type3
	)
      ) continue;


    reco::TrackRef trackRef = cand.trackRef();      

    if(it==trackRef.key()) {
      cand_index = ic;
      cand_type = type;
      cand_pt = cand.pt();
      break;

    }
  }

  if(cand_index>=0){

    const reco::PFCandidate& cand = (*pfCandidates)[cand_index];

    for(unsigned ib=0; ib<cand.elementsInBlocks().size(); ib++) {

      PFBlockRef blockRef = cand.elementsInBlocks()[ib].first;


      unsigned indexInBlock = cand.elementsInBlocks()[ib].second;
      const edm::OwnVector<  reco::PFBlockElement>&  elements = (*blockRef).elements();

      //This tells you what type of element it is:
      //cout<<" block type"<<elements[indexInBlock].type()<<endl;

      switch (elements[indexInBlock].type()) {

	case PFBlockElement::ECAL: {
				     reco::PFClusterRef clusterRef = elements[indexInBlock].clusterRef();
				     double eet = clusterRef->energy()/cosh(clusterRef->eta());
				     sum_ecal+=eet;
				     break;
				   }

	case PFBlockElement::HCAL: {
				     reco::PFClusterRef clusterRef = elements[indexInBlock].clusterRef();
				     double eet = clusterRef->energy()/cosh(clusterRef->eta());
				     sum_hcal+=eet;
				     break; 
				   }       
	case PFBlockElement::TRACK: {
				      //Do nothing since track are not normally linked to other tracks
				      break; 
				    }       
	default:
				    break;
      }

    } // end of elementsInBlocks()
  }  // end of if(cand_index >= 0)	



  cand_type=cand_type;
  cand_pt=cand_pt;
  mEcalSum=sum_ecal;
  mHcalSum=sum_hcal;

  return;

}


// ------------
  std::pair<bool,bool> 
TrackAnalyzer::isAccepted(TrackingParticle & tp)
{
  std::vector<bool> f(nLayers, false);

  const std::vector<PSimHit> & simHits = tp.trackPSimHit(DetId::Tracker);

  for(std::vector<PSimHit>::const_iterator simHit = simHits.begin();
      simHit!= simHits.end(); simHit++)
  {
    int id = getLayerId(*simHit);

    if(id != -1)
      f[id] = true;
  }

  bool canBeTriplet =
    ( (f[BPix1] && f[BPix2]     && f[BPix3]) ||
      (f[BPix1] && f[BPix2]     && f[FPix1_pos]) ||
      (f[BPix1] && f[BPix2]     && f[FPix1_neg]) ||
      (f[BPix1] && f[FPix1_pos] && f[FPix2_pos]) ||
      (f[BPix1] && f[FPix1_neg] && f[FPix2_neg]) );

  bool canBePair =
    ( (f[BPix1] && f[BPix2]) ||
      (f[BPix1] && f[BPix3]) ||
      (f[BPix2] && f[BPix3]) ||
      (f[BPix1] && f[FPix1_pos]) ||
      (f[BPix1] && f[FPix1_neg]) ||
      (f[BPix1] && f[FPix2_pos]) ||
      (f[BPix1] && f[FPix2_neg]) ||
      (f[BPix2] && f[FPix1_pos]) ||
      (f[BPix2] && f[FPix1_neg]) ||
      (f[BPix2] && f[FPix2_pos]) ||
      (f[BPix2] && f[FPix2_neg]) ||
      (f[FPix2_neg] && f[FPix2_neg]) ||
      (f[FPix2_pos] && f[FPix2_pos]) );

  return std::pair<bool,bool>(canBeTriplet, canBePair);
}

// ------------
  int 
TrackAnalyzer::getLayerId(const PSimHit & simHit)
{
  unsigned int id = simHit.detUnitId();

  if(geo_->idToDetUnit(id)->subDetector() ==
      GeomDetEnumerators::PixelBarrel)
  {
    PXBDetId pid(id);
    return pid.layer() - 1; // 0, 1, 2
  }

  if(geo_->idToDetUnit(id)->subDetector() ==
      GeomDetEnumerators::PixelEndcap)
  {
    PXFDetId pid(id);
    return BPix3 + ((pid.side()-1) << 1) + pid.disk(); // 3 -
  }

  // strip
  return -1;
}

// ---------------
bool
TrackAnalyzer::hitDeadPXF(const reco::Track& tr){

  //-----------------------------------------------
  // For a given track, check whether this contains 
  // hits on the dead region in the forward pixel 
  //-----------------------------------------------

  bool hitDeadRegion = false;

  for(trackingRecHit_iterator recHit = tr.recHitsBegin();recHit!= tr.recHitsEnd(); recHit++){

    if((*recHit)->isValid()){

      DetId detId = (*recHit)->geographicalId();
      if(!geo_->idToDet(detId)) continue;

      Int_t diskLayerNum=0, bladeLayerNum=0, hcylLayerNum=0;

      unsigned int subdetId = static_cast<unsigned int>(detId.subdetId());

      if (subdetId == PixelSubdetector::PixelEndcap){

	PixelEndcapName pxfname(detId.rawId());
	diskLayerNum = pxfname.diskName();
	bladeLayerNum = pxfname.bladeName();
	hcylLayerNum = pxfname.halfCylinder();

	// hard-coded now based on /UserCode/Appeltel/PixelFiducialRemover/pixelfiducialremover_cfg.py
	if((bladeLayerNum==4 || bladeLayerNum==5 || bladeLayerNum==6) &&
	    (diskLayerNum==2) && (hcylLayerNum==4)) hitDeadRegion = true;
      }

    }// end of isValid
  }

  return hitDeadRegion;
}

// ------------ method called once each job just before starting event loop  ------------
  void 
TrackAnalyzer::beginJob()
{

  trackTree_ = fs->make<TTree>("trackTree","v1");

  // event
  trackTree_->Branch("nEv",&pev_.nEv,"nEv/I");
  trackTree_->Branch("nLumi",&pev_.nLumi,"nLumi/I");
  trackTree_->Branch("nBX",&pev_.nBX,"nBX/I");
  trackTree_->Branch("nRun",&pev_.nRun,"nRun/I");
  trackTree_->Branch("N",&pev_.N,"N/I");

  // vertex
  trackTree_->Branch("nv",&pev_.nv,"nv/I");
  trackTree_->Branch("vx",pev_.vx,"vx[nv]/F");
  trackTree_->Branch("vy",pev_.vy,"vy[nv]/F");
  trackTree_->Branch("vz",pev_.vz,"vz[nv]/F");
  trackTree_->Branch("vxErr",pev_.vxError,"vxErr[nv]/F"); 
  trackTree_->Branch("vyErr",pev_.vyError,"vyErr[nv]/F"); 
  trackTree_->Branch("vzErr",pev_.vzError,"vzErr[nv]/F");
  trackTree_->Branch("nDaugher",pev_.nDaugher,"nDaugher[nv]/I");

  trackTree_->Branch("nVtx",&pev_.nVtx,"nVtx/I");
  trackTree_->Branch("maxVtx",&pev_.maxVtx,"maxVtx/I");
  //  trackTree_->Branch("maxVtxHard",&pev_.maxVtxHard,"maxVtxHard/I");

  trackTree_->Branch("nTrkVtx",pev_.nTrkVtx,"nTrkVtx[nVtx]/I");
  trackTree_->Branch("normChi2Vtx",pev_.normChi2Vtx,"normChi2Vtx[nVtx]/F");
  trackTree_->Branch("sumPtVtx",pev_.sumPtVtx,"sumPtVtx[nVtx]/F");
  //  trackTree_->Branch("nTrkVtxHard",pev_.nTrkVtxHard,"nTrkVtxHard[nVtx]/I");

  trackTree_->Branch("xVtx",pev_.xVtx,"xVtx[nVtx]/F");
  trackTree_->Branch("yVtx",pev_.yVtx,"yVtx[nVtx]/F");
  trackTree_->Branch("zVtx",pev_.zVtx,"zVtx[nVtx]/F");
  trackTree_->Branch("xVtxErr",pev_.xVtxErr,"xVtxErr[nVtx]/F");
  trackTree_->Branch("yVtxErr",pev_.yVtxErr,"yVtxErr[nVtx]/F");
  trackTree_->Branch("zVtxErr",pev_.zVtxErr,"zVtxErr[nVtx]/F");

  trackTree_->Branch("vtxDist2D",pev_.vtxDist2D,"vtxDist2D[nVtx]/F");
  trackTree_->Branch("vtxDist2DErr",pev_.vtxDist2DErr,"vtxDist2DErr[nVtx]/F");
  trackTree_->Branch("vtxDist2DSig",pev_.vtxDist2DSig,"vtxDist2DSig[nVtx]/F");
  trackTree_->Branch("vtxDist2D",pev_.vtxDist3D,"vtxDist3D[nVtx]/F");
  trackTree_->Branch("vtxDist3DErr",pev_.vtxDist3DErr,"vtxDist3DErr[nVtx]/F");
  trackTree_->Branch("vtxDist3DSig",pev_.vtxDist3DSig,"vtxDist3DSig[nVtx]/F");

  // centrality
  if (useCentrality_) trackTree_->Branch("cbin",&pev_.cbin,"cbin/I");

  // Tracks
  trackTree_->Branch("nTrk",&pev_.nTrk,"nTrk/I");
  trackTree_->Branch("trkPt",&pev_.trkPt,"trkPt[nTrk]/F");
  trackTree_->Branch("trkPtError",&pev_.trkPtError,"trkPtError[nTrk]/F");
  trackTree_->Branch("trkNHit",&pev_.trkNHit,"trkNHit[nTrk]/I");
  trackTree_->Branch("trkNlayer",&pev_.trkNlayer,"trkNlayer[nTrk]/I");
  trackTree_->Branch("trkEta",&pev_.trkEta,"trkEta[nTrk]/F");
  trackTree_->Branch("trkPhi",&pev_.trkPhi,"trkPhi[nTrk]/F");
  trackTree_->Branch("trkCharge",&pev_.trkCharge,"trkCharge[nTrk]/I");
  trackTree_->Branch("trkVtxIndex",&pev_.trkVtxIndex,"trkVtxIndex[nTrk]/I");

  if (doDeDx_) {
    trackTree_->Branch("dedx",&pev_.dedx,"dedx[nTrk]/F");
  }

  //  trackTree_->Branch("trkQual",&pev_.trkQual,"trkQual[nTrk]/I");

  for(unsigned int i  = 0; i < qualityStrings_.size(); ++i){
     trackTree_->Branch(qualityStrings_[i].data(),&pev_.trkQual[i],(qualityStrings_[i]+"[nTrk]/O").data());
  }


  trackTree_->Branch("trkChi2",&pev_.trkChi2,"trkChi2[nTrk]/F");
  trackTree_->Branch("trkNdof",&pev_.trkNdof,"trkNdof[nTrk]/F");
  trackTree_->Branch("trkDxy1",&pev_.trkDxy1,"trkDxy1[nTrk]/F");
  trackTree_->Branch("trkDxyError1",&pev_.trkDxyError1,"trkDxyError1[nTrk]/F");
  trackTree_->Branch("trkDz1",&pev_.trkDz1,"trkDz1[nTrk]/F");
  trackTree_->Branch("trkDzError1",&pev_.trkDzError1,"trkDzError1[nTrk]/F");
  trackTree_->Branch("trkFake",&pev_.trkFake,"trkFake[nTrk]/O");
  trackTree_->Branch("trkAlgo",&pev_.trkAlgo,"trkAlgo[nTrk]/F");

  if (doDebug_) {
     trackTree_->Branch("trkNlayer3D",&pev_.trkNlayer3D,"trkNlayer3D[nTrk]/I");
     trackTree_->Branch("trkDxyBS",&pev_.trkDxyBS,"trkDxyBS[nTrk]/F");
     trackTree_->Branch("trkDxyErrorBS",&pev_.trkDxyErrorBS,"trkDxyErrorBS[nTrk]/F");
     trackTree_->Branch("trkDxy",&pev_.trkDxy,"trkDxy[nTrk]/F");
     trackTree_->Branch("trkDz",&pev_.trkDz,"trkDz[nTrk]/F");
     trackTree_->Branch("trkDxyError",&pev_.trkDxyError,"trkDxyError[nTrk]/F");
     trackTree_->Branch("trkDzError",&pev_.trkDzError,"trkDzError[nTrk]/F");
     trackTree_->Branch("trkChi2hit1D",&pev_.trkChi2hit1D,"trkChi2hit1D[nTrk]/F");
     trackTree_->Branch("trkDzError2",&pev_.trkDzError2,"trkDzError2[nTrk]/F");
     trackTree_->Branch("trkDxy2",&pev_.trkDxy2,"trkDxy2[nTrk]/F");
     trackTree_->Branch("trkDz2",&pev_.trkDz2,"trkDz2[nTrk]/F");
     trackTree_->Branch("trkDxyError2",&pev_.trkDxyError2,"trkDxyError2[nTrk]/F");
     trackTree_->Branch("trkVx",&pev_.trkVx,"trkVx[nTrk]/F");
     trackTree_->Branch("trkVy",&pev_.trkVy,"trkVy[nTrk]/F");
     trackTree_->Branch("trkVz",&pev_.trkVz,"trkVz[nTrk]/F");
  }

  if (doPFMatching_) {
    trackTree_->Branch("pfType",&pev_.pfType,"pfType[nTrk]/I");
    trackTree_->Branch("pfCandPt",&pev_.pfCandPt,"pfCandPt[nTrk]/F");
    trackTree_->Branch("pfSumEcal",&pev_.pfSumEcal,"pfSumEcal[nTrk]/F");
    trackTree_->Branch("pfSumHcal",&pev_.pfSumHcal,"pfSumHcal[nTrk]/F");
  }

  // Track Extra
  if (doTrackExtra_) {
    trackTree_->Branch("trkExpHit1Eta",&pev_.trkExpHit1Eta,"trkExpHit1Eta[nTrk]/F");
    trackTree_->Branch("trkExpHit2Eta",&pev_.trkExpHit2Eta,"trkExpHit2Eta[nTrk]/F");
    trackTree_->Branch("trkExpHit3Eta",&pev_.trkExpHit3Eta,"trkExpHit3Eta[nTrk]/F");
  }

  // Sim Tracks
  if (doSimTrack_) {
     trackTree_->Branch("trkStatus",&pev_.trkStatus,"trkStatus[nTrk]/F");

     if(fillSimTrack_){

	trackTree_->Branch("nParticle",&pev_.nParticle,"nParticle/I");
	trackTree_->Branch("pStatus",&pev_.pStatus,"pStatus[nParticle]/F");
	trackTree_->Branch("pPId",&pev_.pPId,"pPId[nParticle]/F");
	trackTree_->Branch("pEta",&pev_.pEta,"pEta[nParticle]/F");
	trackTree_->Branch("pPhi",&pev_.pPhi,"pPhi[nParticle]/F");
	trackTree_->Branch("pPt",&pev_.pPt,"pPt[nParticle]/F");
	trackTree_->Branch("pAcc",&pev_.pAcc,"pAcc[nParticle]/F");
        trackTree_->Branch("pAccPair",&pev_.pAccPair,"pAccPair[nParticle]/F");
	trackTree_->Branch("pNRec",&pev_.pNRec,"pNRec[nParticle]/F");
	trackTree_->Branch("pNHit",&pev_.pNHit,"pNHit[nParticle]/I");
	trackTree_->Branch("mtrkPt",&pev_.mtrkPt,"mtrkPt[nParticle]/F");
	trackTree_->Branch("mtrkPtError",&pev_.mtrkPtError,"mtrkPtError[nParticle]/F");
	trackTree_->Branch("mtrkNHit",&pev_.mtrkNHit,"mtrkNHit[nParticle]/I");
	trackTree_->Branch("mtrkNlayer",&pev_.mtrkNlayer,"mtrkNlayer[nParticle]/I");
	trackTree_->Branch("mtrkNlayer3D",&pev_.mtrkNlayer3D,"mtrkNlayer3D[nParticle]/I");
	trackTree_->Branch("mtrkQual",&pev_.mtrkQual,"mtrkQual[nParticle]/I");
	trackTree_->Branch("mtrkChi2",&pev_.mtrkChi2,"mtrkChi2[nParticle]/F");
	trackTree_->Branch("mtrkNdof",&pev_.mtrkNdof,"mtrkNdof[nParticle]/F");
	trackTree_->Branch("mtrkDz1",&pev_.mtrkDz1,"mtrkDz1[nParticle]/F");
	trackTree_->Branch("mtrkDzError1",&pev_.mtrkDzError1,"mtrkDzError1[nParticle]/F");
	trackTree_->Branch("mtrkDxy1",&pev_.mtrkDxy1,"mtrkDxy1[nParticle]/F");
	trackTree_->Branch("mtrkDxyError1",&pev_.mtrkDxyError1,"mtrkDxyError1[nParticle]/F");
	trackTree_->Branch("mtrkAlgo",&pev_.mtrkAlgo,"mtrkAlgo[nParticle]/F");

	if (doPFMatching_) {
	   trackTree_->Branch("mtrkPfType",&pev_.mtrkPfType,"mtrkPfType[nParticle]/I");
	   trackTree_->Branch("mtrkPfCandPt",&pev_.mtrkPfCandPt,"mtrkPfCandPt[nParticle]/F");
	   trackTree_->Branch("mtrkPfSumEcal",&pev_.mtrkPfSumEcal,"mtrkPfSumEcal[nParticle]/F");
	   trackTree_->Branch("mtrkPfSumHcal",&pev_.mtrkPfSumHcal,"mtrkPfSumHcal[nParticle]/F");
	}
     }
  }


}

//--------------------------------------------------------------------------------------------------
template <typename TYPE>
inline void TrackAnalyzer::getProduct(const std::string name, edm::Handle<TYPE> &prod,
    const edm::Event &event) const
{
  // Try to access data collection from EDM file. We check if we really get just one
  // product with the given name. If not we throw an exception.

  event.getByLabel(edm::InputTag(name),prod);
  if (!prod.isValid()) 
    throw edm::Exception(edm::errors::Configuration, "TrackAnalyzer::GetProduct()\n")
      << "Collection with label '" << name << "' is not valid" <<  std::endl;
}

//--------------------------------------------------------------------------------------------------
template <typename TYPE>
inline bool TrackAnalyzer::getProductSafe(const std::string name, edm::Handle<TYPE> &prod,
    const edm::Event &event) const
{
  // Try to safely access data collection from EDM file. We check if we really get just one
  // product with the given name. If not, we return false.

  if (name.size()==0)
    return false;

  try {
    event.getByLabel(edm::InputTag(name),prod);
    if (!prod.isValid()) 
      return false;
  } catch (...) {
    return false;
  }
  return true;
}

// ------------ method called once each job just after ending the event loop  ------------
void 
TrackAnalyzer::endJob() {
}

//define this as a plug-in
DEFINE_FWK_MODULE(TrackAnalyzer);
