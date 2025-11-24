#!/usr/bin/env python3
"""
Integrated Automation Controller
Orchestrates Star Dust Vehicle Forge, Guardian NFT Sync, and Quantum Manufacturing

This unified controller integrates all Phase 3 automation systems
and provides a single interface for managing the entire pipeline.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from automation.stardust_vehicle_forge import (
    VehicleForge, VehicleType, StarDustGrade, ForgeStatus
)
from nft_sync.guardian_nft_sync import (
    GuardianNFTSyncEngine, DimensionType, SyncOperation, NFTStatus
)
from quantum_manufacturing.quantum_consciousness_models import (
    QuantumManufacturingSystem, ManufacturingPhase, ConsciousnessLevel, 
    ConsciousnessIntegration
)
from datetime import datetime
from typing import Dict, List


class IntegratedAutomationController:
    """Master controller for all Phase 3 automation systems"""
    
    def __init__(self, data_prefix: str = "integrated"):
        self.vehicle_forge = VehicleForge(f"{data_prefix}_vehicle_forge.json")
        self.nft_sync = GuardianNFTSyncEngine(f"{data_prefix}_nft_sync.json")
        self.manufacturing = QuantumManufacturingSystem(f"{data_prefix}_manufacturing.json")
        
    def initialize_infrastructure(self):
        """Set up initial infrastructure across all systems"""
        print("\n" + "="*80)
        print("PHASE 3 INTEGRATED AUTOMATION SYSTEM - INITIALIZATION")
        print("="*80)
        
        # Initialize dimensional bridges for NFT sync
        print("\n🌉 Establishing Dimensional Bridge Network...")
        self.nft_sync.create_dimensional_bridge(DimensionType.PRIME, DimensionType.ECHO, 150.0, 25.0, 0.95)
        self.nft_sync.create_dimensional_bridge(DimensionType.PRIME, DimensionType.QUANTUM, 200.0, 15.0, 0.98)
        self.nft_sync.create_dimensional_bridge(DimensionType.ECHO, DimensionType.ASTRAL, 100.0, 50.0, 0.88)
        self.nft_sync.create_dimensional_bridge(DimensionType.QUANTUM, DimensionType.ETHEREAL, 180.0, 20.0, 0.93)
        self.nft_sync.create_dimensional_bridge(DimensionType.ASTRAL, DimensionType.VOID, 75.0, 100.0, 0.80)
        self.nft_sync.create_dimensional_bridge(DimensionType.ETHEREAL, DimensionType.VOID, 120.0, 40.0, 0.85)
        
        # Initialize Star Dust inventory
        print("\n✨ Initializing Star Dust Core Inventory...")
        self.vehicle_forge.add_star_dust_core(StarDustGrade.TRANSCENDENT, 99.0, 777.7, 0.99)
        self.vehicle_forge.add_star_dust_core(StarDustGrade.QUANTUM, 95.0, 666.6, 0.98)
        self.vehicle_forge.add_star_dust_core(StarDustGrade.PURE, 88.0, 528.3, 0.92)
        self.vehicle_forge.add_star_dust_core(StarDustGrade.ENHANCED, 75.0, 432.1, 0.85)
        
        print("\n✅ Infrastructure Initialization Complete")
    
    def deploy_guardian_vehicle_pair(self, guardian_name: str, vehicle_name: str,
                                    vehicle_type: VehicleType, priority: int) -> Dict:
        """Deploy a Guardian NFT with its paired vehicle"""
        print(f"\n🚀 Deploying Guardian-Vehicle Pair: {guardian_name} + {vehicle_name}")
        
        # Register Guardian NFT
        nft = self.nft_sync.register_nft(
            name=guardian_name,
            token_id=f"GN-{len(self.nft_sync.nfts):03d}",
            owner_address=f"0x{os.urandom(20).hex()}",
            home_dimension=DimensionType.PRIME,
            power_level=85 + (priority // 10),
            attributes={
                "class": "Guardian",
                "vehicle_paired": vehicle_name,
                "deployment_priority": priority
            }
        )
        
        # Queue vehicle for forging
        vehicle = self.vehicle_forge.queue_vehicle(
            name=vehicle_name,
            vehicle_type=vehicle_type,
            priority=priority,
            assigned_guardian=nft.token_id
        )
        
        # Create manufacturing blueprint for vehicle components
        quantum_params = self.manufacturing.optimize_quantum_parameters("star_dust_vehicle")
        consciousness_params = ConsciousnessIntegration(
            level=ConsciousnessLevel.TRANSCENDENT,
            resonance_frequency=777.0,
            awareness_depth=0.95,
            intention_clarity=0.98
        )
        blueprint = self.manufacturing.create_blueprint(
            name=f"{vehicle_name} Core Components",
            product_type="star_dust_vehicle",
            quantum_params=quantum_params,
            consciousness_params=consciousness_params,
            material_requirements=["Pure Star Dust", "Quantum Crystals", "Consciousness Matrix"],
            estimated_duration=180
        )
        
        return {
            "guardian": nft.id,
            "vehicle": vehicle.id,
            "blueprint": blueprint.id,
            "deployment_ready": False
        }
    
    def auto_process_all_systems(self) -> Dict[str, Dict]:
        """Run automated processing across all systems"""
        print("\n⚙️  AUTO-PROCESSING ALL SYSTEMS...")
        
        results = {
            "vehicle_forge": {},
            "nft_sync": {},
            "manufacturing": {}
        }
        
        # Process manufacturing first (produces components)
        print("\n  📐 Manufacturing System...")
        mfg_results = self.manufacturing.auto_advance_all()
        results["manufacturing"] = mfg_results
        print(f"     Advanced: {mfg_results['advanced']} | Completed: {mfg_results['completed']}")
        
        # Process vehicle forge (uses manufactured components)
        print("\n  🔨 Vehicle Forge System...")
        forge_results = self.vehicle_forge.auto_process_queue()
        results["vehicle_forge"] = forge_results
        print(f"     Started: {forge_results['started']} | Advanced: {forge_results['advanced']} | Mobilized: {forge_results['mobilized']}")
        
        # Process NFT synchronization
        print("\n  🔄 NFT Synchronization System...")
        sync_results = self.nft_sync.auto_sync_all()
        results["nft_sync"] = sync_results
        print(f"     Jobs Created: {sync_results['jobs_created']} | Executed: {sync_results['jobs_executed']} | Synced: {sync_results['nfts_synchronized']}")
        
        return results
    
    def generate_unified_report(self) -> Dict:
        """Generate comprehensive report across all systems"""
        print("\n" + "="*80)
        print("INTEGRATED AUTOMATION SYSTEM - ANALYTICS REPORT")
        print("="*80)
        
        # Gather reports from each system
        vehicle_report = self.vehicle_forge.generate_forge_report()
        nft_report = self.nft_sync.generate_sync_report()
        mfg_report = self.manufacturing.generate_manufacturing_report()
        
        # Vehicle Forge Summary
        print("\n🔨 STAR DUST VEHICLE FORGE")
        print(f"   Total Vehicles: {vehicle_report['total_vehicles']}")
        print(f"   Forge Queue: {vehicle_report['forge_queue_size']}")
        print(f"   Active Forges: {vehicle_report['active_forges']}")
        print(f"   Ready for Mobilization: {vehicle_report['ready_for_mobilization']}")
        print(f"   Mobilized: {vehicle_report['mobilized']}")
        print(f"   Star Dust Cores: {vehicle_report['star_dust_inventory']}")
        
        # NFT Sync Summary
        print("\n🔄 GUARDIAN NFT SYNCHRONIZATION")
        print(f"   Total Guardian NFTs: {nft_report['total_nfts']}")
        print(f"   Dimensional Bridges: {nft_report['active_bridges']}/{nft_report['total_bridges']}")
        print(f"   Sync Jobs: {nft_report['completed_jobs']} completed, {nft_report['pending_jobs']} pending")
        print(f"   Average Sync Coverage: {nft_report['average_sync_percentage']:.1f}%")
        print(f"   Bridge Quality: {nft_report['average_bridge_quality']:.2f}")
        
        # Manufacturing Summary
        print("\n📐 QUANTUM-CONSCIOUS MANUFACTURING")
        print(f"   Total Blueprints: {mfg_report['total_blueprints']}")
        print(f"   Completed Products: {mfg_report['completed_products']}")
        print(f"   Active Processes: {mfg_report['active_processes']}")
        print(f"   High Resonance: {mfg_report['high_resonance_count']}")
        print(f"   Average Resonance: {mfg_report['average_resonance']:.2f}")
        
        # Integration Metrics
        print("\n🔗 INTEGRATION METRICS")
        paired_vehicles = len([v for v in self.vehicle_forge.vehicles if v.assigned_guardian])
        print(f"   Guardian-Vehicle Pairs: {paired_vehicles}")
        print(f"   Total Automation Tasks: {vehicle_report['total_vehicles'] + nft_report['total_nfts'] + mfg_report['total_blueprints']}")
        
        # System Health
        forge_health = min(vehicle_report['active_forges'] / 3.0, 1.0) if vehicle_report['active_forges'] else 0.5
        sync_health = nft_report['average_bridge_quality']
        mfg_health = mfg_report['average_resonance']
        overall_health = (forge_health + sync_health + mfg_health) / 3.0
        
        print(f"\n💚 SYSTEM HEALTH: {overall_health:.2f} (Optimal: >0.80)")
        
        return {
            "vehicle_forge": vehicle_report,
            "nft_sync": nft_report,
            "manufacturing": mfg_report,
            "integration": {
                "paired_vehicles": paired_vehicles,
                "overall_health": overall_health
            }
        }
    
    def deployment_status(self) -> List[Dict]:
        """Get deployment status of all Guardian-Vehicle pairs"""
        deployments = []
        
        for vehicle in self.vehicle_forge.vehicles:
            if vehicle.assigned_guardian:
                nft = next((n for n in self.nft_sync.nfts 
                           if n.token_id == vehicle.assigned_guardian), None)
                
                if nft:
                    deployment = {
                        "guardian_name": nft.name,
                        "guardian_token": nft.token_id,
                        "guardian_status": nft.status.value,
                        "vehicle_name": vehicle.name,
                        "vehicle_type": vehicle.vehicle_type.value,
                        "vehicle_status": vehicle.status.value,
                        "forge_priority": vehicle.forge_priority,
                        "synced_dimensions": len(nft.synced_dimensions),
                        "deployment_ready": (
                            vehicle.status == ForgeStatus.READY and 
                            nft.status == NFTStatus.SYNCHRONIZED
                        )
                    }
                    deployments.append(deployment)
        
        return deployments


def demo_integrated_system():
    """Comprehensive demonstration of integrated automation system"""
    controller = IntegratedAutomationController("demo_integrated")
    
    # Initialize infrastructure
    controller.initialize_infrastructure()
    
    # Deploy Guardian-Vehicle pairs
    print("\n" + "="*80)
    print("DEPLOYING GUARDIAN-VEHICLE PAIRS")
    print("="*80)
    
    controller.deploy_guardian_vehicle_pair(
        "Celestial Warden Alpha",
        "Guardian's Wings Alpha",
        VehicleType.SCOUT,
        priority=95
    )
    
    controller.deploy_guardian_vehicle_pair(
        "Dimensional Keeper Beta",
        "Dimensional Ark Beta",
        VehicleType.DIMENSIONAL_CRUISER,
        priority=90
    )
    
    controller.deploy_guardian_vehicle_pair(
        "Quantum Sentinel Gamma",
        "Quantum Phoenix Gamma",
        VehicleType.QUANTUM_INTERCEPTOR,
        priority=85
    )
    
    # Auto-process all systems multiple times
    print("\n" + "="*80)
    print("AUTO-PROCESSING CYCLES")
    print("="*80)
    
    for cycle in range(5):
        print(f"\n📊 Cycle {cycle + 1}/5")
        controller.auto_process_all_systems()
    
    # Generate unified report
    report = controller.generate_unified_report()
    
    # Show deployment status
    print("\n" + "="*80)
    print("GUARDIAN-VEHICLE DEPLOYMENT STATUS")
    print("="*80)
    
    deployments = controller.deployment_status()
    for deployment in deployments:
        status_icon = "✅" if deployment['deployment_ready'] else "🔄"
        print(f"\n{status_icon} {deployment['guardian_name']} + {deployment['vehicle_name']}")
        print(f"   Guardian: {deployment['guardian_status']} | Synced to {deployment['synced_dimensions']} dimensions")
        print(f"   Vehicle: {deployment['vehicle_status']} | Type: {deployment['vehicle_type']}")
        print(f"   Priority: {deployment['forge_priority']} | Ready: {deployment['deployment_ready']}")
    
    print("\n" + "="*80)
    print("🎉 PHASE 3 AUTOMATION SYSTEM DEMONSTRATION COMPLETE")
    print("="*80)


if __name__ == "__main__":
    demo_integrated_system()
