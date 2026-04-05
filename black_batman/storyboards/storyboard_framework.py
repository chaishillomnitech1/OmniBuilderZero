#!/usr/bin/env python3
"""
Black Batman Storyboard Framework
Automated Storyboard Generation for Motion Cartoon Development

This module provides a framework for creating, managing, and iterating
on storyboard sequences for the Black Batman motion cartoon.
"""

import json
import os
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional


class ShotType(Enum):
    """Standard camera shot types for storyboarding"""
    EXTREME_WIDE = "extreme_wide"
    WIDE = "wide"
    FULL = "full"
    MEDIUM = "medium"
    MEDIUM_CLOSEUP = "medium_closeup"
    CLOSEUP = "closeup"
    EXTREME_CLOSEUP = "extreme_closeup"
    OVER_SHOULDER = "over_shoulder"
    POV = "pov"
    BIRDS_EYE = "birds_eye"
    WORMS_EYE = "worms_eye"


class CameraMovement(Enum):
    """Camera movement types"""
    STATIC = "static"
    PAN_LEFT = "pan_left"
    PAN_RIGHT = "pan_right"
    TILT_UP = "tilt_up"
    TILT_DOWN = "tilt_down"
    ZOOM_IN = "zoom_in"
    ZOOM_OUT = "zoom_out"
    DOLLY_IN = "dolly_in"
    DOLLY_OUT = "dolly_out"
    TRACK_LEFT = "track_left"
    TRACK_RIGHT = "track_right"
    CRANE_UP = "crane_up"
    CRANE_DOWN = "crane_down"
    HANDHELD = "handheld"
    ORBITAL = "orbital"


class PanelMood(Enum):
    """Emotional mood for panels"""
    TENSE = "tense"
    HEROIC = "heroic"
    MYSTERIOUS = "mysterious"
    ACTION = "action"
    DRAMATIC = "dramatic"
    QUIET = "quiet"
    OMINOUS = "ominous"
    HOPEFUL = "hopeful"
    MELANCHOLIC = "melancholic"


@dataclass
class StoryboardPanel:
    """Represents a single panel in the storyboard"""
    panel_id: str
    sequence_id: str
    panel_number: int
    shot_type: ShotType
    camera_movement: CameraMovement
    mood: PanelMood
    description: str
    action_notes: str
    dialogue: Optional[str] = None
    sound_effects: Optional[str] = None
    duration_seconds: float = 2.0
    characters_in_frame: List[str] = field(default_factory=list)
    location: Optional[str] = None
    time_of_day: str = "night"
    ai_prompt_suggestion: str = ""
    thumbnail_path: Optional[str] = None
    notes: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def generate_ai_prompt(self) -> str:
        """Generate AI art prompt for this panel"""
        parts = [
            f"storyboard panel",
            f"{self.shot_type.value.replace('_', ' ')} shot",
            self.description,
            f"{self.mood.value} atmosphere",
            f"{self.time_of_day} lighting"
        ]
        
        if self.characters_in_frame:
            parts.append(f"featuring {', '.join(self.characters_in_frame)}")
        
        if self.location:
            parts.append(f"set in {self.location}")
        
        if self.camera_movement != CameraMovement.STATIC:
            parts.append(f"suggesting {self.camera_movement.value.replace('_', ' ')} motion")
        
        parts.extend([
            "clean line art",
            "professional storyboard style",
            "animation production quality"
        ])
        
        self.ai_prompt_suggestion = ", ".join(parts)
        return self.ai_prompt_suggestion
    
    def to_dict(self) -> Dict:
        """Convert panel to dictionary for serialization"""
        return {
            "panel_id": self.panel_id,
            "sequence_id": self.sequence_id,
            "panel_number": self.panel_number,
            "shot_type": self.shot_type.value,
            "camera_movement": self.camera_movement.value,
            "mood": self.mood.value,
            "description": self.description,
            "action_notes": self.action_notes,
            "dialogue": self.dialogue,
            "sound_effects": self.sound_effects,
            "duration_seconds": self.duration_seconds,
            "characters_in_frame": self.characters_in_frame,
            "location": self.location,
            "time_of_day": self.time_of_day,
            "ai_prompt_suggestion": self.ai_prompt_suggestion or self.generate_ai_prompt(),
            "thumbnail_path": self.thumbnail_path,
            "notes": self.notes,
            "created_at": self.created_at
        }


@dataclass
class StoryboardSequence:
    """Represents a sequence of storyboard panels"""
    sequence_id: str
    title: str
    episode: Optional[str] = None
    act: int = 1
    scene_number: int = 1
    description: str = ""
    panels: List[StoryboardPanel] = field(default_factory=list)
    total_duration: float = 0.0
    location: str = "Mays Landing"
    time_of_day: str = "night"
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    last_modified: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def add_panel(self, panel: StoryboardPanel):
        """Add a panel to the sequence"""
        panel.sequence_id = self.sequence_id
        panel.panel_number = len(self.panels) + 1
        self.panels.append(panel)
        self.calculate_duration()
        self.last_modified = datetime.now().isoformat()
    
    def calculate_duration(self) -> float:
        """Calculate total sequence duration"""
        self.total_duration = sum(panel.duration_seconds for panel in self.panels)
        return self.total_duration
    
    def reorder_panels(self, new_order: List[int]):
        """Reorder panels based on new order indices"""
        if len(new_order) != len(self.panels):
            raise ValueError("New order must match panel count")
        
        self.panels = [self.panels[i] for i in new_order]
        for idx, panel in enumerate(self.panels):
            panel.panel_number = idx + 1
        
        self.last_modified = datetime.now().isoformat()
    
    def to_dict(self) -> Dict:
        """Convert sequence to dictionary for serialization"""
        return {
            "sequence_id": self.sequence_id,
            "title": self.title,
            "episode": self.episode,
            "act": self.act,
            "scene_number": self.scene_number,
            "description": self.description,
            "panels": [panel.to_dict() for panel in self.panels],
            "panel_count": len(self.panels),
            "total_duration": self.calculate_duration(),
            "location": self.location,
            "time_of_day": self.time_of_day,
            "created_at": self.created_at,
            "last_modified": self.last_modified
        }


class StoryboardTemplate:
    """Pre-built storyboard templates for common sequences"""
    
    @staticmethod
    def create_rooftop_reveal() -> List[StoryboardPanel]:
        """Template: Hero revealed on rooftop overlooking city"""
        panels = []
        
        panels.append(StoryboardPanel(
            panel_id="reveal_001",
            sequence_id="",
            panel_number=1,
            shot_type=ShotType.EXTREME_WIDE,
            camera_movement=CameraMovement.STATIC,
            mood=PanelMood.MYSTERIOUS,
            description="Mays Landing skyline at night, courthouse silhouette visible",
            action_notes="Establishing shot, set the scene",
            characters_in_frame=[],
            location="Mays Landing overview",
            time_of_day="night"
        ))
        
        panels.append(StoryboardPanel(
            panel_id="reveal_002",
            sequence_id="",
            panel_number=2,
            shot_type=ShotType.WIDE,
            camera_movement=CameraMovement.TILT_UP,
            mood=PanelMood.OMINOUS,
            description="Camera tilts up courthouse building, mysterious shadow at top",
            action_notes="Building tension, hint at presence",
            characters_in_frame=["Black Batman (silhouette)"],
            location="Courthouse exterior",
            time_of_day="night"
        ))
        
        panels.append(StoryboardPanel(
            panel_id="reveal_003",
            sequence_id="",
            panel_number=3,
            shot_type=ShotType.MEDIUM,
            camera_movement=CameraMovement.STATIC,
            mood=PanelMood.HEROIC,
            description="Black Batman's cape billows in wind, back to camera",
            action_notes="Iconic hero shot, cape motion",
            sound_effects="WIND HOWLING",
            characters_in_frame=["Black Batman"],
            location="Courthouse rooftop",
            time_of_day="night",
            duration_seconds=3.0
        ))
        
        panels.append(StoryboardPanel(
            panel_id="reveal_004",
            sequence_id="",
            panel_number=4,
            shot_type=ShotType.CLOSEUP,
            camera_movement=CameraMovement.DOLLY_IN,
            mood=PanelMood.DRAMATIC,
            description="Black Batman's masked face, eyes narrowing",
            action_notes="Character reveal, establish presence",
            characters_in_frame=["Black Batman"],
            location="Courthouse rooftop",
            time_of_day="night",
            duration_seconds=2.5
        ))
        
        panels.append(StoryboardPanel(
            panel_id="reveal_005",
            sequence_id="",
            panel_number=5,
            shot_type=ShotType.EXTREME_WIDE,
            camera_movement=CameraMovement.CRANE_UP,
            mood=PanelMood.HEROIC,
            description="Full hero reveal, Black Batman standing powerful against moon",
            action_notes="Iconic pose, moonlight silhouette",
            sound_effects="DRAMATIC MUSIC STING",
            characters_in_frame=["Black Batman"],
            location="Courthouse rooftop",
            time_of_day="night",
            duration_seconds=4.0
        ))
        
        return panels
    
    @staticmethod
    def create_action_pursuit() -> List[StoryboardPanel]:
        """Template: High-energy chase/pursuit sequence"""
        panels = []
        
        panels.append(StoryboardPanel(
            panel_id="pursuit_001",
            sequence_id="",
            panel_number=1,
            shot_type=ShotType.WIDE,
            camera_movement=CameraMovement.TRACK_RIGHT,
            mood=PanelMood.ACTION,
            description="Criminal vehicle speeding through Mays Landing streets",
            action_notes="Establish the chase, show speed",
            sound_effects="TIRES SCREECHING, ENGINE ROARING",
            characters_in_frame=["Villain vehicle"],
            location="Downtown Mays Landing",
            time_of_day="night"
        ))
        
        panels.append(StoryboardPanel(
            panel_id="pursuit_002",
            sequence_id="",
            panel_number=2,
            shot_type=ShotType.BIRDS_EYE,
            camera_movement=CameraMovement.TRACK_LEFT,
            mood=PanelMood.TENSE,
            description="Black Batman leaping across rooftops, tracking the vehicle",
            action_notes="Parallel pursuit from above",
            characters_in_frame=["Black Batman"],
            location="Rooftops",
            time_of_day="night",
            duration_seconds=1.5
        ))
        
        panels.append(StoryboardPanel(
            panel_id="pursuit_003",
            sequence_id="",
            panel_number=3,
            shot_type=ShotType.POV,
            camera_movement=CameraMovement.HANDHELD,
            mood=PanelMood.ACTION,
            description="Black Batman's POV, targeting vehicle below",
            action_notes="Build tension, show hero's focus",
            characters_in_frame=["Black Batman (implied)"],
            location="Air",
            time_of_day="night",
            duration_seconds=1.0
        ))
        
        panels.append(StoryboardPanel(
            panel_id="pursuit_004",
            sequence_id="",
            panel_number=4,
            shot_type=ShotType.WIDE,
            camera_movement=CameraMovement.STATIC,
            mood=PanelMood.DRAMATIC,
            description="Black Batman diving from rooftop toward street",
            action_notes="The leap - freeze moment before action",
            sound_effects="CAPE SNAP",
            characters_in_frame=["Black Batman"],
            location="Between buildings",
            time_of_day="night",
            duration_seconds=2.0
        ))
        
        panels.append(StoryboardPanel(
            panel_id="pursuit_005",
            sequence_id="",
            panel_number=5,
            shot_type=ShotType.MEDIUM,
            camera_movement=CameraMovement.DOLLY_IN,
            mood=PanelMood.HEROIC,
            description="Black Batman lands on vehicle roof, cape settling",
            action_notes="Impact moment, hero takes control",
            sound_effects="METAL THUD",
            characters_in_frame=["Black Batman"],
            location="Vehicle roof",
            time_of_day="night",
            duration_seconds=1.5
        ))
        
        return panels
    
    @staticmethod
    def create_confrontation() -> List[StoryboardPanel]:
        """Template: Hero confronts villain scene"""
        panels = []
        
        panels.append(StoryboardPanel(
            panel_id="confront_001",
            sequence_id="",
            panel_number=1,
            shot_type=ShotType.WIDE,
            camera_movement=CameraMovement.STATIC,
            mood=PanelMood.TENSE,
            description="Dark warehouse interior, villain silhouette visible",
            action_notes="Establish confrontation location",
            location="Abandoned warehouse",
            time_of_day="night"
        ))
        
        panels.append(StoryboardPanel(
            panel_id="confront_002",
            sequence_id="",
            panel_number=2,
            shot_type=ShotType.MEDIUM,
            camera_movement=CameraMovement.STATIC,
            mood=PanelMood.OMINOUS,
            description="Villain turns, aware of presence",
            action_notes="Villain awareness",
            dialogue="Who's there?",
            characters_in_frame=["Villain"],
            location="Warehouse interior",
            time_of_day="night"
        ))
        
        panels.append(StoryboardPanel(
            panel_id="confront_003",
            sequence_id="",
            panel_number=3,
            shot_type=ShotType.WORMS_EYE,
            camera_movement=CameraMovement.STATIC,
            mood=PanelMood.HEROIC,
            description="Black Batman emerges from shadows, imposing angle",
            action_notes="Hero reveal, power pose",
            characters_in_frame=["Black Batman"],
            location="Warehouse interior",
            time_of_day="night",
            duration_seconds=3.0
        ))
        
        panels.append(StoryboardPanel(
            panel_id="confront_004",
            sequence_id="",
            panel_number=4,
            shot_type=ShotType.OVER_SHOULDER,
            camera_movement=CameraMovement.STATIC,
            mood=PanelMood.DRAMATIC,
            description="Over Black Batman's shoulder, villain in distance",
            action_notes="Face-off composition",
            characters_in_frame=["Black Batman", "Villain"],
            location="Warehouse interior",
            time_of_day="night"
        ))
        
        panels.append(StoryboardPanel(
            panel_id="confront_005",
            sequence_id="",
            panel_number=5,
            shot_type=ShotType.CLOSEUP,
            camera_movement=CameraMovement.ZOOM_IN,
            mood=PanelMood.TENSE,
            description="Black Batman's eyes, intense focus",
            action_notes="Build to action, tension peak",
            dialogue="It's over.",
            characters_in_frame=["Black Batman"],
            location="Warehouse interior",
            time_of_day="night"
        ))
        
        return panels


class StoryboardFramework:
    """Main framework for managing Black Batman storyboards"""
    
    def __init__(self, project_dir: str = None):
        """Initialize the storyboard framework"""
        self.project_dir = project_dir or self._get_default_dir()
        self.sequences: Dict[str, StoryboardSequence] = {}
        self.templates = StoryboardTemplate()
        
    def _get_default_dir(self) -> str:
        """Get the default storyboards directory"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        return current_dir
    
    def create_sequence(
        self,
        title: str,
        description: str = "",
        episode: Optional[str] = None,
        act: int = 1,
        scene_number: int = 1,
        location: str = "Mays Landing",
        time_of_day: str = "night"
    ) -> StoryboardSequence:
        """Create a new storyboard sequence"""
        sequence_id = f"seq_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        sequence = StoryboardSequence(
            sequence_id=sequence_id,
            title=title,
            episode=episode,
            act=act,
            scene_number=scene_number,
            description=description,
            location=location,
            time_of_day=time_of_day
        )
        
        self.sequences[sequence_id] = sequence
        return sequence
    
    def create_sequence_from_template(
        self,
        template_name: str,
        title: str,
        episode: Optional[str] = None
    ) -> StoryboardSequence:
        """Create a sequence using a pre-built template"""
        template_methods = {
            "rooftop_reveal": self.templates.create_rooftop_reveal,
            "action_pursuit": self.templates.create_action_pursuit,
            "confrontation": self.templates.create_confrontation
        }
        
        if template_name not in template_methods:
            raise ValueError(f"Unknown template: {template_name}")
        
        sequence = self.create_sequence(
            title=title,
            episode=episode,
            description=f"Generated from {template_name} template"
        )
        
        panels = template_methods[template_name]()
        for panel in panels:
            sequence.add_panel(panel)
        
        return sequence
    
    def get_available_templates(self) -> List[str]:
        """Get list of available storyboard templates"""
        return ["rooftop_reveal", "action_pursuit", "confrontation"]
    
    def create_panel(
        self,
        sequence_id: str,
        shot_type: ShotType,
        camera_movement: CameraMovement,
        mood: PanelMood,
        description: str,
        action_notes: str,
        **kwargs
    ) -> StoryboardPanel:
        """Create and add a new panel to a sequence"""
        if sequence_id not in self.sequences:
            raise ValueError(f"Sequence {sequence_id} not found")
        
        sequence = self.sequences[sequence_id]
        panel_num = len(sequence.panels) + 1
        
        panel = StoryboardPanel(
            panel_id=f"{sequence_id}_panel_{panel_num:03d}",
            sequence_id=sequence_id,
            panel_number=panel_num,
            shot_type=shot_type,
            camera_movement=camera_movement,
            mood=mood,
            description=description,
            action_notes=action_notes,
            **kwargs
        )
        
        # Generate AI prompt
        panel.generate_ai_prompt()
        
        sequence.add_panel(panel)
        return panel
    
    def export_sequence(self, sequence_id: str, output_path: str = None) -> str:
        """Export a sequence to JSON file"""
        if sequence_id not in self.sequences:
            raise ValueError(f"Sequence {sequence_id} not found")
        
        sequence = self.sequences[sequence_id]
        
        if output_path is None:
            safe_title = sequence.title.lower().replace(" ", "_")
            output_path = os.path.join(self.project_dir, f"{safe_title}_storyboard.json")
        
        with open(output_path, 'w') as f:
            json.dump(sequence.to_dict(), f, indent=2)
        
        return output_path
    
    def export_all_sequences(self, output_dir: str = None) -> List[str]:
        """Export all sequences to JSON files"""
        output_dir = output_dir or self.project_dir
        os.makedirs(output_dir, exist_ok=True)
        
        exported_files = []
        for sequence_id in self.sequences:
            output_path = self.export_sequence(
                sequence_id,
                os.path.join(output_dir, f"{sequence_id}.json")
            )
            exported_files.append(output_path)
        
        return exported_files
    
    def generate_ai_prompts_for_sequence(self, sequence_id: str) -> List[str]:
        """Generate AI prompts for all panels in a sequence"""
        if sequence_id not in self.sequences:
            raise ValueError(f"Sequence {sequence_id} not found")
        
        sequence = self.sequences[sequence_id]
        prompts = []
        
        for panel in sequence.panels:
            prompt = panel.generate_ai_prompt()
            prompts.append(prompt)
        
        return prompts
    
    def get_sequence_statistics(self, sequence_id: str) -> Dict:
        """Get statistics for a storyboard sequence"""
        if sequence_id not in self.sequences:
            raise ValueError(f"Sequence {sequence_id} not found")
        
        sequence = self.sequences[sequence_id]
        
        shot_counts = {}
        mood_counts = {}
        movement_counts = {}
        
        for panel in sequence.panels:
            shot_counts[panel.shot_type.value] = shot_counts.get(panel.shot_type.value, 0) + 1
            mood_counts[panel.mood.value] = mood_counts.get(panel.mood.value, 0) + 1
            movement_counts[panel.camera_movement.value] = movement_counts.get(panel.camera_movement.value, 0) + 1
        
        return {
            "sequence_id": sequence_id,
            "title": sequence.title,
            "panel_count": len(sequence.panels),
            "total_duration": sequence.calculate_duration(),
            "shot_type_distribution": shot_counts,
            "mood_distribution": mood_counts,
            "camera_movement_distribution": movement_counts
        }
    
    def get_global_statistics(self) -> Dict:
        """Get statistics across all sequences"""
        total_panels = sum(len(seq.panels) for seq in self.sequences.values())
        total_duration = sum(seq.calculate_duration() for seq in self.sequences.values())
        
        return {
            "total_sequences": len(self.sequences),
            "total_panels": total_panels,
            "total_duration_seconds": total_duration,
            "total_duration_formatted": f"{int(total_duration // 60)}:{int(total_duration % 60):02d}"
        }


def demo_storyboard_framework():
    """Demonstration of the storyboard framework"""
    print("\n" + "=" * 70)
    print("BLACK BATMAN STORYBOARD FRAMEWORK")
    print("Automated Storyboard Generation for Motion Cartoon")
    print("=" * 70)
    
    # Initialize framework
    framework = StoryboardFramework()
    
    # Show available templates
    templates = framework.get_available_templates()
    print(f"\n📋 Available Templates: {', '.join(templates)}")
    
    # Create sequence from template
    print("\n" + "-" * 70)
    print("CREATING ROOFTOP REVEAL SEQUENCE")
    print("-" * 70)
    
    reveal_seq = framework.create_sequence_from_template(
        template_name="rooftop_reveal",
        title="Episode 1 - Hero Reveal",
        episode="E01"
    )
    
    print(f"\n✨ Created sequence: {reveal_seq.title}")
    print(f"   ID: {reveal_seq.sequence_id}")
    print(f"   Panels: {len(reveal_seq.panels)}")
    print(f"   Duration: {reveal_seq.calculate_duration():.1f}s")
    
    print("\n   Panels:")
    for panel in reveal_seq.panels:
        print(f"   {panel.panel_number}. [{panel.shot_type.value}] {panel.description[:50]}...")
    
    # Create pursuit sequence
    print("\n" + "-" * 70)
    print("CREATING ACTION PURSUIT SEQUENCE")
    print("-" * 70)
    
    pursuit_seq = framework.create_sequence_from_template(
        template_name="action_pursuit",
        title="Episode 1 - Chase Sequence",
        episode="E01"
    )
    
    print(f"\n⚡ Created sequence: {pursuit_seq.title}")
    print(f"   Panels: {len(pursuit_seq.panels)}")
    print(f"   Duration: {pursuit_seq.calculate_duration():.1f}s")
    
    # Create custom sequence with panels
    print("\n" + "-" * 70)
    print("CREATING CUSTOM SEQUENCE")
    print("-" * 70)
    
    custom_seq = framework.create_sequence(
        title="Lake Lenape Reflection Scene",
        description="Contemplative moment at the lake",
        episode="E01",
        act=2,
        scene_number=5,
        location="Lake Lenape",
        time_of_day="dawn"
    )
    
    # Add custom panels
    framework.create_panel(
        sequence_id=custom_seq.sequence_id,
        shot_type=ShotType.EXTREME_WIDE,
        camera_movement=CameraMovement.STATIC,
        mood=PanelMood.QUIET,
        description="Lake Lenape at dawn, mist rising from water",
        action_notes="Peaceful establishing shot",
        location="Lake Lenape",
        duration_seconds=4.0
    )
    
    framework.create_panel(
        sequence_id=custom_seq.sequence_id,
        shot_type=ShotType.MEDIUM,
        camera_movement=CameraMovement.DOLLY_IN,
        mood=PanelMood.MELANCHOLIC,
        description="Black Batman standing at water's edge, cape still",
        action_notes="Contemplative moment, rare vulnerability",
        characters_in_frame=["Black Batman"],
        location="Lake Lenape shore",
        duration_seconds=3.0
    )
    
    framework.create_panel(
        sequence_id=custom_seq.sequence_id,
        shot_type=ShotType.CLOSEUP,
        camera_movement=CameraMovement.STATIC,
        mood=PanelMood.DRAMATIC,
        description="Black Batman's reflection in the still water",
        action_notes="Symbolic reflection, dual identity theme",
        characters_in_frame=["Black Batman (reflection)"],
        location="Lake Lenape",
        duration_seconds=2.5
    )
    
    print(f"\n🌊 Created custom sequence: {custom_seq.title}")
    print(f"   Panels: {len(custom_seq.panels)}")
    
    # Generate AI prompts
    print("\n" + "-" * 70)
    print("GENERATING AI PROMPTS FOR PANELS")
    print("-" * 70)
    
    prompts = framework.generate_ai_prompts_for_sequence(custom_seq.sequence_id)
    print(f"\n🎨 Generated {len(prompts)} AI prompts:")
    for i, prompt in enumerate(prompts, 1):
        print(f"\n   Panel {i}:")
        print(f"   {prompt[:100]}...")
    
    # Show statistics
    print("\n" + "=" * 70)
    print("FRAMEWORK STATISTICS")
    print("=" * 70)
    
    global_stats = framework.get_global_statistics()
    print(f"\n📊 Global Statistics:")
    print(f"   Total Sequences: {global_stats['total_sequences']}")
    print(f"   Total Panels: {global_stats['total_panels']}")
    print(f"   Total Duration: {global_stats['total_duration_formatted']}")
    
    # Sequence-specific stats
    for seq_id in list(framework.sequences.keys())[:2]:
        stats = framework.get_sequence_statistics(seq_id)
        print(f"\n   📽️ {stats['title']}:")
        print(f"      Panels: {stats['panel_count']}")
        print(f"      Duration: {stats['total_duration']:.1f}s")
        print(f"      Shot Types: {list(stats['shot_type_distribution'].keys())}")
    
    print("\n" + "=" * 70)
    print("✨ Storyboard framework demonstration complete!")
    print("=" * 70)


if __name__ == "__main__":
    demo_storyboard_framework()
