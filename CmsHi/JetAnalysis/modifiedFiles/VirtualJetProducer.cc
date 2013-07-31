////////////////////////////////////////////////////////////////////////////////
//
// VirtualJetProducer
// ------------------
//
//            04/21/2009 Philipp Schieferdecker <philipp.schieferdecker@cern.ch>
////////////////////////////////////////////////////////////////////////////////

#include "RecoJets/JetProducers/plugins/VirtualJetProducer.h"
#include "RecoJets/JetProducers/interface/JetSpecific.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Utilities/interface/CodedException.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "DataFormats/Common/interface/View.h"
#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/JetReco/interface/CaloJetCollection.h"
#include "DataFormats/JetReco/interface/GenJetCollection.h"
#include "DataFormats/JetReco/interface/PFJetCollection.h"
#include "DataFormats/JetReco/interface/BasicJetCollection.h"
#include "DataFormats/JetReco/interface/TrackJetCollection.h"
#include "DataFormats/Candidate/interface/CandidateFwd.h"
#include "DataFormats/Candidate/interface/LeafCandidate.h"

#include "fastjet/SISConePlugin.hh"
#include "fastjet/CMSIterativeConePlugin.hh"
#include "fastjet/ATLASConePlugin.hh"
#include "fastjet/CDFMidPointPlugin.hh"

#include <iostream>
#include <memory>
#include <algorithm>
#include <limits>
#include <cmath>

using namespace std;


namespace reco {
  namespace helper {
    struct GreaterByPtPseudoJet {
      bool operator()( const fastjet::PseudoJet & t1, const fastjet::PseudoJet & t2 ) const {
	return t1.perp() > t2.perp();
      }
    };

  }
}

//______________________________________________________________________________
const char *VirtualJetProducer::JetType::names[] = {
  "BasicJet","GenJet","CaloJet","PFJet","TrackJet"
};


//______________________________________________________________________________
VirtualJetProducer::JetType::Type
VirtualJetProducer::JetType::byName(const string &name)
{
  const char **pos = std::find(names, names + LastJetType, name);
  if (pos == names + LastJetType) {
    std::string errorMessage="Requested jetType not supported: "+name+"\n"; 
    throw cms::Exception("Configuration",errorMessage);
  }
  return (Type)(pos-names);
}


void VirtualJetProducer::makeProduces( std::string alias, std::string tag ) 
{
  if (makeCaloJet(jetTypeE)) {
    produces<reco::CaloJetCollection>(tag).setBranchAlias(alias);
  }
  else if (makePFJet(jetTypeE)) {
    produces<reco::PFJetCollection>(tag).setBranchAlias(alias);
  }
  else if (makeGenJet(jetTypeE)) {
    produces<reco::GenJetCollection>(tag).setBranchAlias(alias);
  }
  else if (makeTrackJet(jetTypeE)) {
    produces<reco::TrackJetCollection>(tag).setBranchAlias(alias);
  }
  else if (makeBasicJet(jetTypeE)) {
    produces<reco::BasicJetCollection>(tag).setBranchAlias(alias);
  }
}

////////////////////////////////////////////////////////////////////////////////
// construction / destruction
////////////////////////////////////////////////////////////////////////////////

//______________________________________________________________________________
VirtualJetProducer::VirtualJetProducer(const edm::ParameterSet& iConfig)
  : moduleLabel_   (iConfig.getParameter<string>       ("@module_label"))
  , src_           (iConfig.getParameter<edm::InputTag>("src"))
  , srcPVs_        (iConfig.getParameter<edm::InputTag>("srcPVs"))
  , jetType_       (iConfig.getParameter<string>       ("jetType"))
  , jetAlgorithm_  (iConfig.getParameter<string>       ("jetAlgorithm"))
  , rParam_        (iConfig.getParameter<double>       ("rParam"))
  , inputEtMin_    (iConfig.getParameter<double>       ("inputEtMin"))
  , inputEMin_     (iConfig.getParameter<double>       ("inputEMin"))
  , jetPtMin_      (iConfig.getParameter<double>       ("jetPtMin"))
				      //, puPtMin_       (iConfig.getParameter<double>       ("puPtMin"))
  , doPVCorrection_(iConfig.getParameter<bool>         ("doPVCorrection"))
  , restrictInputs_(false)
  , maxInputs_(99999999)
  , doAreaFastjet_ (iConfig.getParameter<bool>         ("doAreaFastjet"))
  , doRhoFastjet_  (iConfig.getParameter<bool>         ("doRhoFastjet"))
  , doPUOffsetCorr_(iConfig.getParameter<bool>         ("doPUOffsetCorr"))
  , maxBadEcalCells_        (iConfig.getParameter<unsigned>("maxBadEcalCells"))
  , maxRecoveredEcalCells_  (iConfig.getParameter<unsigned>("maxRecoveredEcalCells"))
  , maxProblematicEcalCells_(iConfig.getParameter<unsigned>("maxProblematicEcalCells"))
  , maxBadHcalCells_        (iConfig.getParameter<unsigned>("maxBadHcalCells"))
  , maxRecoveredHcalCells_  (iConfig.getParameter<unsigned>("maxRecoveredHcalCells"))
  , maxProblematicHcalCells_(iConfig.getParameter<unsigned>("maxProblematicHcalCells"))
  , jetCollInstanceName_ ("")
{

  //
  // additional parameters to think about:
  // - overlap threshold (set to 0.75 for the time being)
  // - p parameter for generalized kT (set to -2 for the time being)
  // - fastjet PU subtraction parameters (not yet considered)
  //
  if (jetAlgorithm_=="SISCone") {
    fjPlugin_ = PluginPtr( new fastjet::SISConePlugin(rParam_,0.75,0,0.0,false,
						      fastjet::SISConePlugin::SM_pttilde) );
    fjJetDefinition_= JetDefPtr( new fastjet::JetDefinition(&*fjPlugin_) );
  }
  else if (jetAlgorithm_=="IterativeCone") {
    fjPlugin_ = PluginPtr(new fastjet::CMSIterativeConePlugin(rParam_,1.0));
    fjJetDefinition_= JetDefPtr(new fastjet::JetDefinition(&*fjPlugin_));
  }
  else if (jetAlgorithm_=="CDFMidPoint") {
    fjPlugin_ = PluginPtr(new fastjet::CDFMidPointPlugin(rParam_,0.75));
    fjJetDefinition_= JetDefPtr(new fastjet::JetDefinition(&*fjPlugin_));
  }
  else if (jetAlgorithm_=="ATLASCone") {
    fjPlugin_ = PluginPtr(new fastjet::ATLASConePlugin(rParam_));
    fjJetDefinition_= JetDefPtr(new fastjet::JetDefinition(&*fjPlugin_));
  }
  else if (jetAlgorithm_=="Kt")
    fjJetDefinition_= JetDefPtr(new fastjet::JetDefinition(fastjet::kt_algorithm,rParam_));
  else if (jetAlgorithm_=="CambridgeAachen")
    fjJetDefinition_= JetDefPtr(new fastjet::JetDefinition(fastjet::cambridge_algorithm,
							   rParam_) );
  else if (jetAlgorithm_=="AntiKt")
    fjJetDefinition_= JetDefPtr( new fastjet::JetDefinition(fastjet::antikt_algorithm,rParam_) );
  else if (jetAlgorithm_=="GeneralizedKt")
    fjJetDefinition_= JetDefPtr( new fastjet::JetDefinition(fastjet::genkt_algorithm,
							    rParam_,-2) );
  else
    throw cms::Exception("Invalid jetAlgorithm")
      <<"Jet algorithm for VirtualJetProducer is invalid, Abort!\n";
  
  jetTypeE=JetType::byName(jetType_);

  if ( iConfig.exists("jetCollInstanceName") ) {
    jetCollInstanceName_ = iConfig.getParameter<string>("jetCollInstanceName");
  }

  if ( doPUOffsetCorr_ ) {
     if ( jetTypeE != JetType::CaloJet ) {
       //throw cms::Exception("InvalidInput") << "Can only offset correct jets of type CaloJet";
       std::cout<<" Implementing background subtraction using a pseudo calo grid"<<std::endl;
     }
     
     if(iConfig.exists("subtractorName")) puSubtractorName_  =  iConfig.getParameter<string> ("subtractorName");
     else puSubtractorName_ = std::string();
     
     if(puSubtractorName_.empty()){
       edm::LogWarning("VirtualJetProducer") << "Pile Up correction on; however, pile up type is not specified. Using default... \n";
       subtractor_ =  boost::shared_ptr<PileUpSubtractor>(new PileUpSubtractor(iConfig));
     }else{
       subtractor_ =  boost::shared_ptr<PileUpSubtractor>(PileUpSubtractorFactory::get()->create( puSubtractorName_, iConfig));
     }
  }

  // do fasjet area / rho calcluation? => accept corresponding parameters
  if ( doAreaFastjet_ || doRhoFastjet_ ) {
    // Eta range of jets to be considered for Rho calculation
    // Should be at most (jet acceptance - jet radius)
    double rhoEtaMax=iConfig.getParameter<double>("Rho_EtaMax");
    // default Ghost_EtaMax should be 5
    double ghostEtaMax = iConfig.getParameter<double>("Ghost_EtaMax");
    // default Active_Area_Repeats 1
    int    activeAreaRepeats = iConfig.getParameter<int> ("Active_Area_Repeats");
    // default GhostArea 0.01
    double ghostArea = iConfig.getParameter<double> ("GhostArea");
    fjActiveArea_ =  ActiveAreaSpecPtr(new fastjet::ActiveAreaSpec(ghostEtaMax,
								   activeAreaRepeats,
								   ghostArea));
    fjRangeDef_ = RangeDefPtr( new fastjet::RangeDefinition(rhoEtaMax) );
  } 

  // restrict inputs to first "maxInputs" towers?
  if ( iConfig.exists("restrictInputs") ) {
    restrictInputs_ = iConfig.getParameter<bool>("restrictInputs");
    maxInputs_      = iConfig.getParameter<unsigned int>("maxInputs");
  }
 

  string alias=iConfig.getUntrackedParameter<string>("alias",moduleLabel_);

  // make the "produces" statements
  makeProduces( alias, jetCollInstanceName_ );

  doFastJetNonUniform_ = false;
  if(iConfig.exists("doFastJetNonUniform")) doFastJetNonUniform_ = iConfig.getParameter<bool>   ("doFastJetNonUniform");
  if(doFastJetNonUniform_){
    puCenters_ = iConfig.getParameter<std::vector<double> >("puCenters");
    puWidth_ = iConfig.getParameter<double>("puWidth");
  }
  produces<std::vector<double> >("rhos");
  produces<std::vector<double> >("sigmas");
  produces<double>("rho");
  produces<double>("sigma");
  
}

//______________________________________________________________________________
VirtualJetProducer::~VirtualJetProducer()
{
} 


////////////////////////////////////////////////////////////////////////////////
// implementation of member functions
////////////////////////////////////////////////////////////////////////////////

//______________________________________________________________________________
void VirtualJetProducer::produce(edm::Event& iEvent,const edm::EventSetup& iSetup)
{
  LogDebug("VirtualJetProducer") << "Entered produce\n";
  //determine signal vertex
  vertex_=reco::Jet::Point(0,0,0);
  if (makeCaloJet(jetTypeE)&&doPVCorrection_) {
    LogDebug("VirtualJetProducer") << "Adding PV info\n";
    edm::Handle<reco::VertexCollection> pvCollection;
    iEvent.getByLabel(srcPVs_,pvCollection);
    if (pvCollection->size()>0) vertex_=pvCollection->begin()->position();
  }

  // For Pileup subtraction using offset correction:
  // set up geometry map
  if ( doPUOffsetCorr_ ) {
     subtractor_->setupGeometryMap(iEvent, iSetup);
  }

  // clear data
  LogDebug("VirtualJetProducer") << "Clear data\n";
  fjInputs_.clear();
  fjJets_.clear();
  inputs_.clear();  
  
  // get inputs and convert them to the fastjet format (fastjet::PeudoJet)
  edm::Handle<reco::CandidateView> inputsHandle;
  iEvent.getByLabel(src_,inputsHandle);
  for (size_t i = 0; i < inputsHandle->size(); ++i) {
    inputs_.push_back(inputsHandle->ptrAt(i));
  }
  LogDebug("VirtualJetProducer") << "Got inputs\n";
  
  // Convert candidates to fastjet::PseudoJets.
  // Also correct to Primary Vertex. Will modify fjInputs_
  // and use inputs_
  fjInputs_.reserve(inputs_.size());
  inputTowers();
  LogDebug("VirtualJetProducer") << "Inputted towers\n";

  // For Pileup subtraction using offset correction:
  // Subtract pedestal. 
  if ( doPUOffsetCorr_ ) {
     subtractor_->reset(inputs_,fjInputs_,fjJets_);
     subtractor_->calculatePedestal(fjInputs_); 
     subtractor_->subtractPedestal(fjInputs_);    
     LogDebug("VirtualJetProducer") << "Subtracted pedestal\n";
  }

  // Run algorithm. Will modify fjJets_ and allocate fjClusterSeq_. 
  // This will use fjInputs_
  runAlgorithm( iEvent, iSetup );
  if ( doPUOffsetCorr_ ) {
     subtractor_->setAlgorithm(fjClusterSeq_);
  }

  LogDebug("VirtualJetProducer") << "Ran algorithm\n";

  // For Pileup subtraction using offset correction:
  // Now we find jets and need to recalculate their energy,
  // mark towers participated in jet,
  // remove occupied towers from the list and recalculate mean and sigma
  // put the initial towers collection to the jet,   
  // and subtract from initial towers in jet recalculated mean and sigma of towers 
  if ( doPUOffsetCorr_ ) {
    vector<fastjet::PseudoJet> orphanInput;
    subtractor_->calculateOrphanInput(orphanInput);
    subtractor_->calculatePedestal(orphanInput);
    subtractor_->offsetCorrectJets();
  }

  // Write the output jets.
  // This will (by default) call the member function template
  // "writeJets", but can be overridden. 
  // this will use inputs_
  output( iEvent, iSetup );
  LogDebug("VirtualJetProducer") << "Wrote jets\n";
  
  return;
}

//______________________________________________________________________________
  
void VirtualJetProducer::inputTowers( )
{
  std::vector<edm::Ptr<reco::Candidate> >::const_iterator inBegin = inputs_.begin(),
    inEnd = inputs_.end(), i = inBegin;
  for (; i != inEnd; ++i ) {
    reco::CandidatePtr input = *i;
    if (isnan(input->pt()))           continue;
    if (input->et()    <inputEtMin_)  continue;
    if (input->energy()<inputEMin_)   continue;
    if (isAnomalousTower(input))      continue;
    if (makeCaloJet(jetTypeE)&&doPVCorrection_) {
      const CaloTower* tower=dynamic_cast<const CaloTower*>(input.get());
      math::PtEtaPhiMLorentzVector ct(tower->p4(vertex_));
      fjInputs_.push_back(fastjet::PseudoJet(ct.px(),ct.py(),ct.pz(),ct.energy()));
    }
    else {
      fjInputs_.push_back(fastjet::PseudoJet(input->px(),input->py(),input->pz(),
					    input->energy()));
    }
    fjInputs_.back().set_user_index(i - inBegin);
  }

  if ( restrictInputs_ && fjInputs_.size() > maxInputs_ ) {
    reco::helper::GreaterByPtPseudoJet   pTComparator;
    std::sort(fjInputs_.begin(), fjInputs_.end(), pTComparator);
    fjInputs_.resize(maxInputs_);
    edm::LogWarning("JetRecoTooManyEntries") << "Too many inputs in the event, limiting to first " << maxInputs_ << ". Output is suspect.";
  }
}

//______________________________________________________________________________
bool VirtualJetProducer::isAnomalousTower(reco::CandidatePtr input)
{
  if (!makeCaloJet(jetTypeE)) return false;
  const CaloTower* tower=dynamic_cast<const CaloTower*>(input.get());
  if (0==tower) return false;
  if (tower->numBadEcalCells()        >maxBadEcalCells_        ||
      tower->numRecoveredEcalCells()  >maxRecoveredEcalCells_  ||
      tower->numProblematicEcalCells()>maxProblematicEcalCells_||
      tower->numBadHcalCells()        >maxBadHcalCells_        ||
      tower->numRecoveredHcalCells()  >maxRecoveredHcalCells_  ||
      tower->numProblematicHcalCells()>maxProblematicHcalCells_) return true;
  return false;
}


//------------------------------------------------------------------------------
// This is pure virtual. 
//______________________________________________________________________________
// void VirtualJetProducer::runAlgorithm( edm::Event & iEvent, edm::EventSetup const& iSetup,
// 				       std::vector<edm::Ptr<reco::Candidate> > const & inputs_);

//______________________________________________________________________________
void VirtualJetProducer::copyConstituents(const vector<fastjet::PseudoJet>& fjConstituents,
					  reco::Jet* jet)
{
  for (unsigned int i=0;i<fjConstituents.size();++i)
    jet->addDaughter(inputs_[fjConstituents[i].user_index()]);
}


//______________________________________________________________________________
vector<reco::CandidatePtr>
VirtualJetProducer::getConstituents(const vector<fastjet::PseudoJet>&fjConstituents)
{
  vector<reco::CandidatePtr> result;
  for (unsigned int i=0;i<fjConstituents.size();i++) {
    int index = fjConstituents[i].user_index();
    reco::CandidatePtr candidate = inputs_[index];
    result.push_back(candidate);
  }
  return result;
}

void VirtualJetProducer::output(edm::Event & iEvent, edm::EventSetup const& iSetup)
{
  // Write jets and constitutents. Will use fjJets_, inputs_
  // and fjClusterSeq_
  switch( jetTypeE ) {
  case JetType::CaloJet :
    writeJets<reco::CaloJet>( iEvent, iSetup);
    break;
  case JetType::PFJet :
    writeJets<reco::PFJet>( iEvent, iSetup);
    break;
  case JetType::GenJet :
    writeJets<reco::GenJet>( iEvent, iSetup);
    break;
  case JetType::TrackJet :
    writeJets<reco::TrackJet>( iEvent, iSetup);
    break;
  case JetType::BasicJet :
    writeJets<reco::BasicJet>( iEvent, iSetup);
    break;
  default:
    throw cms::Exception("InvalidInput") << "invalid jet type in VirtualJetProducer\n";
    break;
  };
  
}

template< typename T >
void VirtualJetProducer::writeJets( edm::Event & iEvent, edm::EventSetup const& iSetup )
{
  // produce output jet collection

  using namespace reco;

  std::auto_ptr<std::vector<T> > jets(new std::vector<T>() );
  jets->reserve(fjJets_.size());
      
  for (unsigned int ijet=0;ijet<fjJets_.size();++ijet) {
    // allocate this jet
    T jet;
    // get the fastjet jet
    const fastjet::PseudoJet& fjJet = fjJets_[ijet];
    // get the constituents from fastjet
    std::vector<fastjet::PseudoJet> fjConstituents =
      sorted_by_pt(fjClusterSeq_->constituents(fjJet));
    // convert them to CandidatePtr vector
    std::vector<CandidatePtr> constituents =
      getConstituents(fjConstituents);

    // calcuate the jet area
    double jetArea=0.0;
    if ( doAreaFastjet_ ) {
      fastjet::ClusterSequenceArea const * clusterSequenceWithArea =
	dynamic_cast<fastjet::ClusterSequenceArea const *>(&*fjClusterSeq_);
      jetArea = clusterSequenceWithArea->area(fjJet);
    }
    
    // write the specifics to the jet (simultaneously sets 4-vector, vertex).
    // These are overridden functions that will call the appropriate
    // specific allocator. 
    writeSpecific(jet,
		  Particle::LorentzVector(fjJet.px(),
					  fjJet.py(),
					  fjJet.pz(),
					  fjJet.E()),
		  vertex_, 
		  constituents, iSetup);
    
    jet.setJetArea (jetArea);

    if(doPUOffsetCorr_){
       jet.setPileup(subtractor_->getPileUpEnergy(ijet));
   }else{
       jet.setPileup (0.0);
    }

    // add to the list
    jets->push_back(jet);	
  }
  
  // put the jets in the collection
  iEvent.put(jets);
  
  if (doRhoFastjet_) {
    if(doFastJetNonUniform_){
      std::auto_ptr<std::vector<double> > rhos(new std::vector<double>);
      std::auto_ptr<std::vector<double> > sigmas(new std::vector<double>);
      int nEta = puCenters_.size();
      rhos->reserve(nEta);
      sigmas->reserve(nEta);
      fastjet::ClusterSequenceArea const * clusterSequenceWithArea =
	dynamic_cast<fastjet::ClusterSequenceArea const *> ( &*fjClusterSeq_ );

      for(int ie = 0; ie < nEta; ++ie){
	double eta = puCenters_[ie];
	double rho = 0;
	double sigma = 0;
	double etamin=eta-puWidth_;
	double etamax=eta+puWidth_;
	fastjet::RangeDefinition range_rho(etamin,etamax);
	clusterSequenceWithArea->get_median_rho_and_sigma(range_rho, true, rho, sigma);
	rhos->push_back(rho);
	sigmas->push_back(sigma);
      }
      iEvent.put(rhos,"rhos");
      iEvent.put(sigmas,"sigmas");
    }else{
      std::auto_ptr<double> rho(new double(0.0));
      std::auto_ptr<double> sigma(new double(0.0));
      double mean_area = 0;
      
      fastjet::ClusterSequenceArea const * clusterSequenceWithArea =
	dynamic_cast<fastjet::ClusterSequenceArea const *> ( &*fjClusterSeq_ );
      clusterSequenceWithArea->get_median_rho_and_sigma(*fjRangeDef_,false,*rho,*sigma,mean_area);
      iEvent.put(rho,"rho");
      iEvent.put(sigma,"sigma");
    }
    
  }
}



