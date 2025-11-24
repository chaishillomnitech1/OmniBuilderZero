#!/usr/bin/env python3
"""
Guardian NFT Cross-Dimensional Synchronization Framework
Manages Guardian NFTs across multiple dimensions

This system provides synchronization of Guardian NFT states,
attributes, and ownership across dimensional boundaries.
"""

import json
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Set
from dataclasses import dataclass, asdict, field
import uuid


class DimensionType(Enum):
    """Types of dimensions in the multiverse"""
    PRIME = "prime"
    ECHO = "echo"
    QUANTUM = "quantum"
    ASTRAL = "astral"
    ETHEREAL = "ethereal"
    VOID = "void"


class NFTStatus(Enum):
    """Status of Guardian NFT"""
    MINTED = "minted"
    ACTIVE = "active"
    SYNCING = "syncing"
    SYNCHRONIZED = "synchronized"
    DESYNC = "desync"
    LOCKED = "locked"


class SyncOperation(Enum):
    """Types of synchronization operations"""
    FULL_SYNC = "full_sync"
    ATTRIBUTE_SYNC = "attribute_sync"
    OWNERSHIP_SYNC = "ownership_sync"
    STATE_SYNC = "state_sync"
    BRIDGE_SYNC = "bridge_sync"


@dataclass
class DimensionalBridge:
    """Connection between two dimensions"""
    id: str
    source_dimension: DimensionType
    target_dimension: DimensionType
    bandwidth: float  # Data transfer rate (MB/s)
    latency: float  # Milliseconds
    stability: float  # 0.0 to 1.0
    active: bool
    
    @property
    def sync_quality(self) -> float:
        """Calculate sync quality score"""
        if not self.active:
            return 0.0
        # Quality based on bandwidth, latency, and stability
        bandwidth_score = min(self.bandwidth / 100.0, 1.0)
        latency_score = max(1.0 - (self.latency / 1000.0), 0.0)
        return (bandwidth_score + latency_score + self.stability) / 3.0


@dataclass
class GuardianNFT:
    """Represents a Guardian NFT with cross-dimensional capabilities"""
    id: str
    name: str
    token_id: str
    owner_address: str
    home_dimension: DimensionType
    status: NFTStatus
    power_level: int  # 1-100
    resonance_signature: str
    attributes: Dict[str, any]
    synced_dimensions: Set[str] = field(default_factory=set)
    last_sync: Optional[str] = None
    sync_history: List[Dict] = field(default_factory=list)
    
    @property
    def sync_priority(self) -> int:
        """Calculate sync priority based on power level and status"""
        if self.status == NFTStatus.DESYNC:
            return 100
        elif self.status == NFTStatus.SYNCING:
            return 50
        return self.power_level
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        data = asdict(self)
        data['home_dimension'] = self.home_dimension.value
        data['status'] = self.status.value
        data['synced_dimensions'] = list(self.synced_dimensions)
        return data


@dataclass
class SyncJob:
    """Represents a synchronization job"""
    id: str
    nft_id: str
    operation: SyncOperation
    source_dimension: DimensionType
    target_dimensions: List[DimensionType]
    created_at: str
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    progress: float = 0.0  # 0.0 to 100.0
    status: str = "pending"
    error_message: Optional[str] = None
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        data = asdict(self)
        data['operation'] = self.operation.value
        data['source_dimension'] = self.source_dimension.value
        data['target_dimensions'] = [d.value for d in self.target_dimensions]
        return data


class GuardianNFTSyncEngine:
    """Cross-dimensional Guardian NFT synchronization engine"""
    
    def __init__(self, data_file: str = "guardian_nft_sync_data.json"):
        self.data_file = data_file
        self.nfts: List[GuardianNFT] = []
        self.bridges: List[DimensionalBridge] = []
        self.sync_jobs: List[SyncJob] = []
        self.concurrent_sync_limit = 5
        self.load_data()
    
    def load_data(self):
        """Load existing NFT and sync data"""
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                
                # Load NFTs
                for nft_data in data.get('nfts', []):
                    nft_data['home_dimension'] = DimensionType(nft_data['home_dimension'])
                    nft_data['status'] = NFTStatus(nft_data['status'])
                    nft_data['synced_dimensions'] = set(nft_data.get('synced_dimensions', []))
                    self.nfts.append(GuardianNFT(**nft_data))
                
                # Load bridges
                for bridge_data in data.get('bridges', []):
                    bridge_data['source_dimension'] = DimensionType(bridge_data['source_dimension'])
                    bridge_data['target_dimension'] = DimensionType(bridge_data['target_dimension'])
                    self.bridges.append(DimensionalBridge(**bridge_data))
                
                # Load sync jobs
                for job_data in data.get('sync_jobs', []):
                    job_data['operation'] = SyncOperation(job_data['operation'])
                    job_data['source_dimension'] = DimensionType(job_data['source_dimension'])
                    job_data['target_dimensions'] = [DimensionType(d) for d in job_data['target_dimensions']]
                    self.sync_jobs.append(SyncJob(**job_data))
        except FileNotFoundError:
            self.nfts = []
            self.bridges = []
            self.sync_jobs = []
    
    def save_data(self):
        """Save NFT and sync data to disk"""
        data = {
            'nfts': [nft.to_dict() for nft in self.nfts],
            'bridges': [],
            'sync_jobs': [job.to_dict() for job in self.sync_jobs]
        }
        
        # Save bridges
        for bridge in self.bridges:
            bridge_dict = asdict(bridge)
            bridge_dict['source_dimension'] = bridge.source_dimension.value
            bridge_dict['target_dimension'] = bridge.target_dimension.value
            data['bridges'].append(bridge_dict)
        
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def register_nft(self, name: str, token_id: str, owner_address: str,
                    home_dimension: DimensionType, power_level: int,
                    attributes: Optional[Dict] = None) -> GuardianNFT:
        """Register a new Guardian NFT"""
        nft = GuardianNFT(
            id=f"nft_{uuid.uuid4().hex[:8]}",
            name=name,
            token_id=token_id,
            owner_address=owner_address,
            home_dimension=home_dimension,
            status=NFTStatus.MINTED,
            power_level=power_level,
            resonance_signature=f"RES_{uuid.uuid4().hex[:12].upper()}",
            attributes=attributes or {},
            synced_dimensions={home_dimension.value}
        )
        self.nfts.append(nft)
        self.save_data()
        print(f"✨ Registered Guardian NFT: {name} (Token: {token_id})")
        return nft
    
    def create_dimensional_bridge(self, source: DimensionType, target: DimensionType,
                                  bandwidth: float, latency: float, stability: float) -> DimensionalBridge:
        """Create a bridge between two dimensions"""
        bridge = DimensionalBridge(
            id=f"bridge_{uuid.uuid4().hex[:8]}",
            source_dimension=source,
            target_dimension=target,
            bandwidth=bandwidth,
            latency=latency,
            stability=stability,
            active=True
        )
        self.bridges.append(bridge)
        self.save_data()
        print(f"🌉 Created bridge: {source.value} ↔ {target.value} (Quality: {bridge.sync_quality:.2f})")
        return bridge
    
    def get_bridge(self, source: DimensionType, target: DimensionType) -> Optional[DimensionalBridge]:
        """Find an active bridge between two dimensions"""
        # Check direct bridge
        for bridge in self.bridges:
            if bridge.active and bridge.source_dimension == source and bridge.target_dimension == target:
                return bridge
            # Bridges are bidirectional
            if bridge.active and bridge.source_dimension == target and bridge.target_dimension == source:
                return bridge
        return None
    
    def create_sync_job(self, nft_id: str, operation: SyncOperation,
                       target_dimensions: List[DimensionType]) -> Optional[SyncJob]:
        """Create a synchronization job for an NFT"""
        nft = next((n for n in self.nfts if n.id == nft_id), None)
        if not nft:
            print(f"❌ NFT {nft_id} not found")
            return None
        
        # Check if bridges exist for all target dimensions
        for target in target_dimensions:
            if not self.get_bridge(nft.home_dimension, target):
                print(f"⚠️  No bridge available: {nft.home_dimension.value} → {target.value}")
                return None
        
        job = SyncJob(
            id=f"sync_{uuid.uuid4().hex[:8]}",
            nft_id=nft_id,
            operation=operation,
            source_dimension=nft.home_dimension,
            target_dimensions=target_dimensions,
            created_at=datetime.now().isoformat()
        )
        self.sync_jobs.append(job)
        
        # Update NFT status
        nft.status = NFTStatus.SYNCING
        self.save_data()
        
        print(f"🔄 Created sync job for {nft.name}: {operation.value}")
        return job
    
    def execute_sync_job(self, job_id: str) -> bool:
        """Execute a synchronization job"""
        job = next((j for j in self.sync_jobs if j.id == job_id), None)
        if not job or job.status == "completed":
            return False
        
        nft = next((n for n in self.nfts if n.id == job.nft_id), None)
        if not nft:
            return False
        
        # Start job
        job.status = "running"
        job.started_at = datetime.now().isoformat()
        
        # Simulate synchronization process
        total_targets = len(job.target_dimensions)
        for i, target_dim in enumerate(job.target_dimensions):
            bridge = self.get_bridge(job.source_dimension, target_dim)
            if bridge:
                # Sync quality affects success
                if bridge.sync_quality > 0.5:
                    nft.synced_dimensions.add(target_dim.value)
                    job.progress = ((i + 1) / total_targets) * 100.0
                    
                    # Record sync in history
                    sync_record = {
                        "timestamp": datetime.now().isoformat(),
                        "operation": job.operation.value,
                        "dimension": target_dim.value,
                        "success": True
                    }
                    nft.sync_history.append(sync_record)
                else:
                    job.error_message = f"Low quality bridge to {target_dim.value}"
        
        # Complete job
        job.status = "completed"
        job.completed_at = datetime.now().isoformat()
        nft.status = NFTStatus.SYNCHRONIZED
        nft.last_sync = datetime.now().isoformat()
        
        self.save_data()
        print(f"✅ Completed sync job for {nft.name} ({job.progress:.0f}% complete)")
        return True
    
    def auto_sync_all(self) -> Dict[str, int]:
        """Automatically synchronize all NFTs that need syncing"""
        results = {
            'jobs_created': 0,
            'jobs_executed': 0,
            'nfts_synchronized': 0
        }
        
        # Create sync jobs for NFTs that aren't fully synced
        for nft in self.nfts:
            if nft.status in [NFTStatus.MINTED, NFTStatus.ACTIVE, NFTStatus.DESYNC]:
                # Find dimensions we're not synced to
                all_dimensions = set(d.value for d in DimensionType if d != nft.home_dimension)
                unsynced = all_dimensions - nft.synced_dimensions
                
                if unsynced:
                    target_dims = [DimensionType(d) for d in unsynced]
                    # Only create job if we have bridges
                    has_bridges = all(self.get_bridge(nft.home_dimension, td) for td in target_dims)
                    if has_bridges:
                        job = self.create_sync_job(nft.id, SyncOperation.FULL_SYNC, target_dims)
                        if job:
                            results['jobs_created'] += 1
        
        # Execute pending jobs (up to concurrent limit)
        pending_jobs = [j for j in self.sync_jobs if j.status == "pending"][:self.concurrent_sync_limit]
        for job in pending_jobs:
            if self.execute_sync_job(job.id):
                results['jobs_executed'] += 1
        
        # Count fully synchronized NFTs
        results['nfts_synchronized'] = len([n for n in self.nfts if n.status == NFTStatus.SYNCHRONIZED])
        
        return results
    
    def get_nft_sync_status(self, nft_id: str) -> Optional[Dict]:
        """Get detailed sync status for an NFT"""
        nft = next((n for n in self.nfts if n.id == nft_id), None)
        if not nft:
            return None
        
        all_dimensions = set(d.value for d in DimensionType)
        synced_count = len(nft.synced_dimensions)
        total_count = len(all_dimensions)
        
        return {
            "nft_name": nft.name,
            "status": nft.status.value,
            "home_dimension": nft.home_dimension.value,
            "synced_dimensions": list(nft.synced_dimensions),
            "sync_percentage": (synced_count / total_count) * 100,
            "last_sync": nft.last_sync,
            "pending_dimensions": list(all_dimensions - nft.synced_dimensions)
        }
    
    def generate_sync_report(self) -> Dict:
        """Generate comprehensive synchronization analytics"""
        report = {
            "total_nfts": len(self.nfts),
            "total_bridges": len(self.bridges),
            "active_bridges": len([b for b in self.bridges if b.active]),
            "total_sync_jobs": len(self.sync_jobs),
            "completed_jobs": len([j for j in self.sync_jobs if j.status == "completed"]),
            "pending_jobs": len([j for j in self.sync_jobs if j.status == "pending"]),
            "running_jobs": len([j for j in self.sync_jobs if j.status == "running"]),
            "by_status": {},
            "by_dimension": {},
            "average_sync_percentage": 0.0,
            "average_bridge_quality": 0.0
        }
        
        # Count NFTs by status
        for status in NFTStatus:
            count = len([n for n in self.nfts if n.status == status])
            report["by_status"][status.value] = count
        
        # Count NFTs by home dimension
        for dim in DimensionType:
            count = len([n for n in self.nfts if n.home_dimension == dim])
            report["by_dimension"][dim.value] = count
        
        # Calculate averages
        if self.nfts:
            all_dim_count = len(DimensionType)
            avg_sync = sum(len(n.synced_dimensions) / all_dim_count for n in self.nfts) / len(self.nfts)
            report["average_sync_percentage"] = avg_sync * 100
        
        if self.bridges:
            avg_quality = sum(b.sync_quality for b in self.bridges) / len(self.bridges)
            report["average_bridge_quality"] = avg_quality
        
        return report


def demo_nft_sync_system():
    """Demonstration of Guardian NFT Synchronization system"""
    print("\n" + "="*70)
    print("GUARDIAN NFT CROSS-DIMENSIONAL SYNCHRONIZATION SYSTEM")
    print("="*70)
    
    sync_engine = GuardianNFTSyncEngine("demo_guardian_nft_sync_data.json")
    
    # Create dimensional bridges
    print("\n🌉 Establishing Dimensional Bridges...")
    sync_engine.create_dimensional_bridge(DimensionType.PRIME, DimensionType.ECHO, 150.0, 25.0, 0.95)
    sync_engine.create_dimensional_bridge(DimensionType.PRIME, DimensionType.QUANTUM, 200.0, 15.0, 0.98)
    sync_engine.create_dimensional_bridge(DimensionType.ECHO, DimensionType.ASTRAL, 100.0, 50.0, 0.88)
    sync_engine.create_dimensional_bridge(DimensionType.QUANTUM, DimensionType.ETHEREAL, 180.0, 20.0, 0.93)
    sync_engine.create_dimensional_bridge(DimensionType.ASTRAL, DimensionType.VOID, 75.0, 100.0, 0.80)
    
    # Register Guardian NFTs
    print("\n✨ Registering Guardian NFTs...")
    sync_engine.register_nft(
        "Celestial Warden #001",
        "GN-001",
        "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb1",
        DimensionType.PRIME,
        95,
        {"class": "Warden", "element": "Light", "rarity": "Legendary"}
    )
    
    sync_engine.register_nft(
        "Void Walker #007",
        "GN-007",
        "0x8ba1f109551bD432803012645Ac136ddd64DBA72",
        DimensionType.ECHO,
        88,
        {"class": "Walker", "element": "Void", "rarity": "Epic"}
    )
    
    sync_engine.register_nft(
        "Quantum Sage #013",
        "GN-013",
        "0xDD2FD4581271e230360230F9337D5c0430Bf44C0",
        DimensionType.QUANTUM,
        92,
        {"class": "Sage", "element": "Quantum", "rarity": "Legendary"}
    )
    
    # Auto-sync all NFTs
    print("\n🔄 Auto-Syncing Guardian NFTs Across Dimensions...")
    results = sync_engine.auto_sync_all()
    print(f"   Jobs Created: {results['jobs_created']} | Executed: {results['jobs_executed']} | Synchronized: {results['nfts_synchronized']}")
    
    # Generate report
    print("\n" + "="*70)
    print("SYNCHRONIZATION ANALYTICS REPORT")
    print("="*70)
    report = sync_engine.generate_sync_report()
    print(f"\nTotal Guardian NFTs: {report['total_nfts']}")
    print(f"Dimensional Bridges: {report['active_bridges']}/{report['total_bridges']} active")
    print(f"Sync Jobs: {report['completed_jobs']} completed, {report['pending_jobs']} pending, {report['running_jobs']} running")
    print(f"Average Sync Coverage: {report['average_sync_percentage']:.1f}%")
    print(f"Average Bridge Quality: {report['average_bridge_quality']:.2f}")
    
    print("\n📊 NFTs by Status:")
    for status, count in report['by_status'].items():
        if count > 0:
            print(f"   {status}: {count}")
    
    print("\n🌌 NFTs by Home Dimension:")
    for dim, count in report['by_dimension'].items():
        if count > 0:
            print(f"   {dim}: {count}")
    
    print("\n" + "="*70)
    print("INDIVIDUAL NFT SYNC STATUS")
    print("="*70)
    for nft in sync_engine.nfts:
        status_info = sync_engine.get_nft_sync_status(nft.id)
        if status_info:
            print(f"\n{status_info['nft_name']}")
            print(f"   Home: {status_info['home_dimension']} | Status: {status_info['status']}")
            print(f"   Sync Coverage: {status_info['sync_percentage']:.1f}%")
            print(f"   Synced To: {', '.join(status_info['synced_dimensions'])}")
            if status_info['pending_dimensions']:
                print(f"   Pending: {', '.join(status_info['pending_dimensions'])}")
    
    print("\n" + "="*70)


if __name__ == "__main__":
    demo_nft_sync_system()
