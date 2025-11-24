#!/usr/bin/env python3
"""
Star Dust Vehicle Automation System
Prioritizes forging and mobilization of Star Dust-powered vehicles

This system manages the creation, power allocation, and deployment
of vehicles powered by Star Dust energy cores.
"""

import json
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict, field
import uuid


class VehicleType(Enum):
    """Types of Star Dust-powered vehicles"""
    SCOUT = "scout"
    CARRIER = "carrier"
    FORTRESS = "fortress"
    DIMENSIONAL_CRUISER = "dimensional_cruiser"
    QUANTUM_INTERCEPTOR = "quantum_interceptor"


class ForgeStatus(Enum):
    """Status of vehicle in forging pipeline"""
    QUEUED = "queued"
    FORGING = "forging"
    POWER_INFUSION = "power_infusion"
    CALIBRATION = "calibration"
    READY = "ready"
    MOBILIZED = "mobilized"
    MAINTENANCE = "maintenance"


class StarDustGrade(Enum):
    """Quality grades of Star Dust energy"""
    BASIC = "basic"
    ENHANCED = "enhanced"
    PURE = "pure"
    QUANTUM = "quantum"
    TRANSCENDENT = "transcendent"


@dataclass
class StarDustCore:
    """Represents a Star Dust energy core"""
    id: str
    grade: StarDustGrade
    power_level: float  # 0.0 to 100.0
    resonance_frequency: float  # MHz
    dimensional_stability: float  # 0.0 to 1.0
    
    @property
    def effective_power(self) -> float:
        """Calculate effective power output"""
        grade_multipliers = {
            StarDustGrade.BASIC: 1.0,
            StarDustGrade.ENHANCED: 2.0,
            StarDustGrade.PURE: 4.0,
            StarDustGrade.QUANTUM: 8.0,
            StarDustGrade.TRANSCENDENT: 16.0
        }
        return self.power_level * grade_multipliers[self.grade] * self.dimensional_stability
    
    @property
    def priority_score(self) -> int:
        """Calculate priority for resource allocation"""
        return int(self.effective_power * 10)


@dataclass
class Vehicle:
    """Represents a Star Dust-powered vehicle"""
    id: str
    name: str
    vehicle_type: VehicleType
    status: ForgeStatus
    star_dust_core: Optional[StarDustCore]
    forge_priority: int  # 1-100, higher is more urgent
    created_at: str
    forge_started_at: Optional[str] = None
    completed_at: Optional[str] = None
    mobilized_at: Optional[str] = None
    assigned_guardian: Optional[str] = None
    dimensional_coords: Optional[Dict[str, float]] = None
    notes: List[str] = field(default_factory=list)
    
    @property
    def forge_time_required(self) -> int:
        """Estimated forge time in minutes"""
        base_times = {
            VehicleType.SCOUT: 30,
            VehicleType.CARRIER: 60,
            VehicleType.FORTRESS: 120,
            VehicleType.DIMENSIONAL_CRUISER: 180,
            VehicleType.QUANTUM_INTERCEPTOR: 240
        }
        return base_times[self.vehicle_type]
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        data = asdict(self)
        data['vehicle_type'] = self.vehicle_type.value
        data['status'] = self.status.value
        if self.star_dust_core:
            data['star_dust_core']['grade'] = self.star_dust_core.grade.value
        return data


class VehicleForge:
    """Automated Star Dust Vehicle forging and mobilization system"""
    
    def __init__(self, data_file: str = "vehicle_forge_data.json"):
        self.data_file = data_file
        self.vehicles: List[Vehicle] = []
        self.star_dust_inventory: List[StarDustCore] = []
        self.forge_capacity = 3  # Concurrent forging slots
        self.load_data()
    
    def load_data(self):
        """Load existing forge data"""
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                
                # Load vehicles
                for v_data in data.get('vehicles', []):
                    if v_data.get('star_dust_core'):
                        core_data = v_data['star_dust_core']
                        core = StarDustCore(
                            id=core_data['id'],
                            grade=StarDustGrade(core_data['grade']),
                            power_level=core_data['power_level'],
                            resonance_frequency=core_data['resonance_frequency'],
                            dimensional_stability=core_data['dimensional_stability']
                        )
                        v_data['star_dust_core'] = core
                    else:
                        v_data['star_dust_core'] = None
                    
                    v_data['vehicle_type'] = VehicleType(v_data['vehicle_type'])
                    v_data['status'] = ForgeStatus(v_data['status'])
                    self.vehicles.append(Vehicle(**v_data))
                
                # Load star dust inventory
                for core_data in data.get('star_dust_inventory', []):
                    core = StarDustCore(
                        id=core_data['id'],
                        grade=StarDustGrade(core_data['grade']),
                        power_level=core_data['power_level'],
                        resonance_frequency=core_data['resonance_frequency'],
                        dimensional_stability=core_data['dimensional_stability']
                    )
                    self.star_dust_inventory.append(core)
        except FileNotFoundError:
            self.vehicles = []
            self.star_dust_inventory = []
    
    def save_data(self):
        """Save forge data to disk"""
        data = {
            'vehicles': [],
            'star_dust_inventory': []
        }
        
        # Save vehicles
        for vehicle in self.vehicles:
            v_dict = vehicle.to_dict()
            data['vehicles'].append(v_dict)
        
        # Save inventory
        for core in self.star_dust_inventory:
            core_dict = asdict(core)
            core_dict['grade'] = core.grade.value
            data['star_dust_inventory'].append(core_dict)
        
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def add_star_dust_core(self, grade: StarDustGrade, power_level: float, 
                           resonance_frequency: float, dimensional_stability: float) -> StarDustCore:
        """Add a Star Dust core to inventory"""
        core = StarDustCore(
            id=f"core_{uuid.uuid4().hex[:8]}",
            grade=grade,
            power_level=power_level,
            resonance_frequency=resonance_frequency,
            dimensional_stability=dimensional_stability
        )
        self.star_dust_inventory.append(core)
        self.save_data()
        print(f"✨ Added {grade.value} Star Dust core (Power: {core.effective_power:.1f})")
        return core
    
    def queue_vehicle(self, name: str, vehicle_type: VehicleType, 
                     priority: int, assigned_guardian: Optional[str] = None) -> Vehicle:
        """Queue a new vehicle for forging"""
        vehicle = Vehicle(
            id=f"veh_{uuid.uuid4().hex[:8]}",
            name=name,
            vehicle_type=vehicle_type,
            status=ForgeStatus.QUEUED,
            star_dust_core=None,
            forge_priority=priority,
            created_at=datetime.now().isoformat(),
            assigned_guardian=assigned_guardian
        )
        self.vehicles.append(vehicle)
        self.save_data()
        print(f"🔧 Queued {name} for forging (Priority: {priority})")
        return vehicle
    
    def get_best_star_dust_core(self, vehicle_type: VehicleType) -> Optional[StarDustCore]:
        """Select the best available Star Dust core for vehicle type"""
        if not self.star_dust_inventory:
            return None
        
        # Sort by priority score (highest first)
        sorted_cores = sorted(self.star_dust_inventory, 
                            key=lambda c: c.priority_score, reverse=True)
        
        # For now, select the best available core
        # In production, this would match core to vehicle requirements
        return sorted_cores[0] if sorted_cores else None
    
    def start_forge(self, vehicle_id: str) -> bool:
        """Start forging process for a queued vehicle"""
        vehicle = next((v for v in self.vehicles if v.id == vehicle_id), None)
        if not vehicle or vehicle.status != ForgeStatus.QUEUED:
            print(f"❌ Cannot start forge for vehicle {vehicle_id}")
            return False
        
        # Check forge capacity
        active_forges = len([v for v in self.vehicles if v.status == ForgeStatus.FORGING])
        if active_forges >= self.forge_capacity:
            print(f"⚠️  Forge at capacity ({active_forges}/{self.forge_capacity})")
            return False
        
        # Assign Star Dust core
        core = self.get_best_star_dust_core(vehicle.vehicle_type)
        if not core:
            print(f"❌ No Star Dust cores available for {vehicle.name}")
            return False
        
        # Remove core from inventory and assign to vehicle
        self.star_dust_inventory.remove(core)
        vehicle.star_dust_core = core
        vehicle.status = ForgeStatus.FORGING
        vehicle.forge_started_at = datetime.now().isoformat()
        vehicle.notes.append(f"Forging started with {core.grade.value} core")
        self.save_data()
        
        print(f"🔨 Started forging {vehicle.name} with {core.grade.value} Star Dust core")
        return True
    
    def advance_forge_status(self, vehicle_id: str) -> bool:
        """Advance vehicle to next forge stage"""
        vehicle = next((v for v in self.vehicles if v.id == vehicle_id), None)
        if not vehicle:
            return False
        
        status_progression = {
            ForgeStatus.FORGING: ForgeStatus.POWER_INFUSION,
            ForgeStatus.POWER_INFUSION: ForgeStatus.CALIBRATION,
            ForgeStatus.CALIBRATION: ForgeStatus.READY
        }
        
        if vehicle.status in status_progression:
            old_status = vehicle.status
            vehicle.status = status_progression[vehicle.status]
            vehicle.notes.append(f"Advanced: {old_status.value} → {vehicle.status.value}")
            
            if vehicle.status == ForgeStatus.READY:
                vehicle.completed_at = datetime.now().isoformat()
            
            self.save_data()
            print(f"⚡ {vehicle.name}: {old_status.value} → {vehicle.status.value}")
            return True
        
        return False
    
    def mobilize_vehicle(self, vehicle_id: str, dimensional_coords: Optional[Dict[str, float]] = None) -> bool:
        """Mobilize a ready vehicle for deployment"""
        vehicle = next((v for v in self.vehicles if v.id == vehicle_id), None)
        if not vehicle or vehicle.status != ForgeStatus.READY:
            print(f"❌ Vehicle {vehicle_id} not ready for mobilization")
            return False
        
        vehicle.status = ForgeStatus.MOBILIZED
        vehicle.mobilized_at = datetime.now().isoformat()
        vehicle.dimensional_coords = dimensional_coords or {"x": 0.0, "y": 0.0, "z": 0.0, "dimension": 1}
        vehicle.notes.append(f"Mobilized to coordinates: {vehicle.dimensional_coords}")
        self.save_data()
        
        print(f"🚀 Mobilized {vehicle.name} to dimension {vehicle.dimensional_coords.get('dimension', 1)}")
        return True
    
    def get_forge_queue(self) -> List[Vehicle]:
        """Get prioritized queue of vehicles waiting to be forged"""
        queued = [v for v in self.vehicles if v.status == ForgeStatus.QUEUED]
        return sorted(queued, key=lambda v: v.forge_priority, reverse=True)
    
    def get_active_forges(self) -> List[Vehicle]:
        """Get vehicles currently being forged"""
        return [v for v in self.vehicles 
                if v.status in [ForgeStatus.FORGING, ForgeStatus.POWER_INFUSION, ForgeStatus.CALIBRATION]]
    
    def get_ready_vehicles(self) -> List[Vehicle]:
        """Get vehicles ready for mobilization"""
        return [v for v in self.vehicles if v.status == ForgeStatus.READY]
    
    def get_mobilized_vehicles(self) -> List[Vehicle]:
        """Get currently mobilized vehicles"""
        return [v for v in self.vehicles if v.status == ForgeStatus.MOBILIZED]
    
    def auto_process_queue(self) -> Dict[str, int]:
        """Automatically process forge queue based on priority and capacity"""
        results = {
            'started': 0,
            'advanced': 0,
            'mobilized': 0
        }
        
        # Start forging for queued high-priority vehicles
        queue = self.get_forge_queue()
        for vehicle in queue[:self.forge_capacity]:
            if self.start_forge(vehicle.id):
                results['started'] += 1
        
        # Advance vehicles in active forge stages
        active = self.get_active_forges()
        for vehicle in active:
            if self.advance_forge_status(vehicle.id):
                results['advanced'] += 1
        
        # Auto-mobilize vehicles with assigned guardians
        ready = self.get_ready_vehicles()
        for vehicle in ready:
            if vehicle.assigned_guardian:
                default_coords = {"x": 0.0, "y": 0.0, "z": 0.0, "dimension": 1}
                if self.mobilize_vehicle(vehicle.id, default_coords):
                    results['mobilized'] += 1
        
        return results
    
    def generate_forge_report(self) -> Dict:
        """Generate comprehensive forge analytics"""
        report = {
            "total_vehicles": len(self.vehicles),
            "by_status": {},
            "by_type": {},
            "forge_queue_size": len(self.get_forge_queue()),
            "active_forges": len(self.get_active_forges()),
            "ready_for_mobilization": len(self.get_ready_vehicles()),
            "mobilized": len(self.get_mobilized_vehicles()),
            "star_dust_inventory": len(self.star_dust_inventory),
            "average_core_power": sum(c.effective_power for c in self.star_dust_inventory) / len(self.star_dust_inventory) if self.star_dust_inventory else 0
        }
        
        # Count by status
        for status in ForgeStatus:
            count = len([v for v in self.vehicles if v.status == status])
            report["by_status"][status.value] = count
        
        # Count by type
        for vtype in VehicleType:
            count = len([v for v in self.vehicles if v.vehicle_type == vtype])
            report["by_type"][vtype.value] = count
        
        return report


def demo_forge_system():
    """Demonstration of Star Dust Vehicle Forge system"""
    print("\n" + "="*70)
    print("STAR DUST VEHICLE FORGE SYSTEM - INITIALIZATION")
    print("="*70)
    
    forge = VehicleForge("demo_vehicle_forge_data.json")
    
    # Add Star Dust cores to inventory
    print("\n📦 Adding Star Dust Cores to Inventory...")
    forge.add_star_dust_core(StarDustGrade.QUANTUM, 95.0, 432.5, 0.98)
    forge.add_star_dust_core(StarDustGrade.PURE, 88.0, 528.3, 0.92)
    forge.add_star_dust_core(StarDustGrade.ENHANCED, 75.0, 384.7, 0.85)
    forge.add_star_dust_core(StarDustGrade.TRANSCENDENT, 99.0, 777.7, 0.99)
    
    # Queue vehicles for forging
    print("\n🔧 Queuing Vehicles for Forging...")
    forge.queue_vehicle("Guardian's Wings", VehicleType.SCOUT, priority=85, assigned_guardian="NFT_001")
    forge.queue_vehicle("Dimensional Ark", VehicleType.DIMENSIONAL_CRUISER, priority=95, assigned_guardian="NFT_007")
    forge.queue_vehicle("Quantum Phoenix", VehicleType.QUANTUM_INTERCEPTOR, priority=90, assigned_guardian="NFT_013")
    forge.queue_vehicle("Star Fortress Alpha", VehicleType.FORTRESS, priority=80)
    forge.queue_vehicle("Swift Carrier Beta", VehicleType.CARRIER, priority=70)
    
    # Auto-process the queue
    print("\n⚙️  Auto-Processing Forge Queue...")
    results = forge.auto_process_queue()
    print(f"   Started: {results['started']} | Advanced: {results['advanced']} | Mobilized: {results['mobilized']}")
    
    # Generate report
    print("\n" + "="*70)
    print("FORGE ANALYTICS REPORT")
    print("="*70)
    report = forge.generate_forge_report()
    print(f"\nTotal Vehicles: {report['total_vehicles']}")
    print(f"Forge Queue: {report['forge_queue_size']}")
    print(f"Active Forges: {report['active_forges']}")
    print(f"Ready for Mobilization: {report['ready_for_mobilization']}")
    print(f"Mobilized: {report['mobilized']}")
    print(f"Star Dust Cores Available: {report['star_dust_inventory']}")
    print(f"Average Core Power: {report['average_core_power']:.1f}")
    
    print("\n📊 Vehicles by Status:")
    for status, count in report['by_status'].items():
        if count > 0:
            print(f"   {status}: {count}")
    
    print("\n🚀 Vehicles by Type:")
    for vtype, count in report['by_type'].items():
        if count > 0:
            print(f"   {vtype}: {count}")
    
    print("\n" + "="*70)
    print("HIGH PRIORITY FORGE QUEUE")
    print("="*70)
    for vehicle in forge.get_forge_queue()[:5]:
        guardian_info = f" (Guardian: {vehicle.assigned_guardian})" if vehicle.assigned_guardian else ""
        print(f"\n{vehicle.name} - {vehicle.vehicle_type.value.upper()}")
        print(f"   Priority: {vehicle.forge_priority}/100{guardian_info}")
        print(f"   Est. Forge Time: {vehicle.forge_time_required} minutes")
    
    print("\n" + "="*70)


if __name__ == "__main__":
    demo_forge_system()
