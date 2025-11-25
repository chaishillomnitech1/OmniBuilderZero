#!/usr/bin/env python3
"""
Black Batman Concept Art Generator
AI Pipeline for Motion Cartoon Visual Development

This module provides automated AI prompt generation and management
for creating concept art for the Black Batman motion cartoon set in Mays Landing.
"""

import json
import os
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional


class ArtStyle(Enum):
    """Available art style presets for generation"""
    COMIC_BOOK = "comic_book"
    CINEMATIC = "cinematic"
    CONCEPT_ART = "concept_art"
    STORYBOARD = "storyboard"


class AssetCategory(Enum):
    """Categories of concept art assets"""
    CHARACTER = "character"
    ENVIRONMENT = "environment"
    ACTION = "action"
    MOOD_BOARD = "mood_board"
    PROP = "prop"
    VEHICLE = "vehicle"


class TimeOfDay(Enum):
    """Time of day presets for atmospheric generation"""
    NIGHT_PATROL = "night_patrol"
    GOLDEN_HOUR = "golden_hour"
    MIDDAY = "midday"
    STORMY = "stormy"
    DAWN = "dawn"
    DUSK = "dusk"


@dataclass
class GenerationPrompt:
    """Represents a complete AI generation prompt"""
    id: str
    category: AssetCategory
    style: ArtStyle
    subject: str
    location: Optional[str] = None
    time_of_day: Optional[TimeOfDay] = None
    modifiers: List[str] = field(default_factory=list)
    negative_prompts: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def build_prompt(self) -> str:
        """Construct the full generation prompt string"""
        parts = [self.subject]
        
        if self.location:
            parts.append(f"set in {self.location}")
        
        if self.time_of_day:
            time_descriptions = {
                TimeOfDay.NIGHT_PATROL: "moonlit night, dark atmospheric",
                TimeOfDay.GOLDEN_HOUR: "golden hour lighting, warm tones",
                TimeOfDay.MIDDAY: "bright daylight, clear sky",
                TimeOfDay.STORMY: "stormy weather, dramatic clouds",
                TimeOfDay.DAWN: "early dawn light, misty atmosphere",
                TimeOfDay.DUSK: "twilight, fading light"
            }
            parts.append(time_descriptions.get(self.time_of_day, ""))
        
        # Add style-specific modifiers
        style_modifiers = {
            ArtStyle.COMIC_BOOK: ["comic book art", "bold inking", "dynamic composition"],
            ArtStyle.CINEMATIC: ["cinematic lighting", "widescreen composition", "movie quality"],
            ArtStyle.CONCEPT_ART: ["professional concept art", "detailed rendering", "development art"],
            ArtStyle.STORYBOARD: ["clean storyboard style", "sequential art", "clear composition"]
        }
        parts.extend(style_modifiers.get(self.style, []))
        
        # Add custom modifiers
        parts.extend(self.modifiers)
        
        return ", ".join(filter(None, parts))
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization"""
        return {
            "id": self.id,
            "category": self.category.value,
            "style": self.style.value,
            "subject": self.subject,
            "location": self.location,
            "time_of_day": self.time_of_day.value if self.time_of_day else None,
            "modifiers": self.modifiers,
            "negative_prompts": self.negative_prompts,
            "created_at": self.created_at,
            "full_prompt": self.build_prompt()
        }


class ConceptArtGenerator:
    """Main AI pipeline for Black Batman concept art generation"""
    
    def __init__(self, config_path: str = None):
        """Initialize the generator with environment configuration"""
        self.config_path = config_path or self._get_default_config_path()
        self.config = self._load_config()
        self.prompts: List[GenerationPrompt] = []
        self.prompt_history: List[Dict] = []
        
    def _get_default_config_path(self) -> str:
        """Get the default config file path"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(current_dir, "..", "environments", "mays_landing_config.json")
    
    def _load_config(self) -> Dict:
        """Load environment configuration"""
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"⚠️ Config not found at {self.config_path}, using defaults")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict:
        """Return default configuration if file not found"""
        return {
            "project": "Black Batman Motion Cartoon",
            "environment": {
                "name": "Mays Landing",
                "state": "New Jersey"
            },
            "locations": [],
            "hero_integration": {
                "character": "Black Batman",
                "visual_identity": {
                    "primary_colors": ["#0a0a0a", "#1a1a2e", "#ffd700"]
                }
            }
        }
    
    def get_locations(self) -> List[str]:
        """Get list of available location names"""
        return [loc["name"] for loc in self.config.get("locations", [])]
    
    def get_location_by_id(self, location_id: str) -> Optional[Dict]:
        """Get location details by ID"""
        for loc in self.config.get("locations", []):
            if loc.get("id") == location_id:
                return loc
        return None
    
    def generate_character_prompt(
        self,
        pose: str = "heroic stance",
        location: Optional[str] = None,
        time_of_day: TimeOfDay = TimeOfDay.NIGHT_PATROL,
        style: ArtStyle = ArtStyle.CONCEPT_ART,
        additional_modifiers: List[str] = None
    ) -> GenerationPrompt:
        """Generate a prompt for Black Batman character art"""
        hero_config = self.config.get("hero_integration", {})
        character_name = hero_config.get("character", "Black Batman")
        
        subject = f"{character_name} in {pose}, cape flowing dramatically"
        
        modifiers = [
            "heroic essence",
            "dynamic composition",
            "masked vigilante",
            "powerful silhouette"
        ]
        if additional_modifiers:
            modifiers.extend(additional_modifiers)
        
        prompt_id = f"char_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        prompt = GenerationPrompt(
            id=prompt_id,
            category=AssetCategory.CHARACTER,
            style=style,
            subject=subject,
            location=location or "Mays Landing",
            time_of_day=time_of_day,
            modifiers=modifiers,
            negative_prompts=["blurry", "low quality", "deformed", "amateur"]
        )
        
        self.prompts.append(prompt)
        self.prompt_history.append(prompt.to_dict())
        
        return prompt
    
    def generate_environment_prompt(
        self,
        location_id: str,
        time_of_day: TimeOfDay = TimeOfDay.NIGHT_PATROL,
        style: ArtStyle = ArtStyle.CONCEPT_ART,
        additional_modifiers: List[str] = None
    ) -> GenerationPrompt:
        """Generate a prompt for Mays Landing environment art"""
        location = self.get_location_by_id(location_id)
        
        if location:
            subject = f"{location['name']}, {location['description']}"
            visual_themes = location.get("visual_themes", [])
        else:
            subject = "Mays Landing New Jersey suburban landscape"
            visual_themes = []
        
        modifiers = [
            "atmospheric depth",
            "environmental storytelling",
            *visual_themes
        ]
        if additional_modifiers:
            modifiers.extend(additional_modifiers)
        
        prompt_id = f"env_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        prompt = GenerationPrompt(
            id=prompt_id,
            category=AssetCategory.ENVIRONMENT,
            style=style,
            subject=subject,
            location=location["name"] if location else "Mays Landing",
            time_of_day=time_of_day,
            modifiers=modifiers,
            negative_prompts=["people", "crowds", "modern cars", "anachronistic elements"]
        )
        
        self.prompts.append(prompt)
        self.prompt_history.append(prompt.to_dict())
        
        return prompt
    
    def generate_action_sequence_prompt(
        self,
        action: str,
        location: Optional[str] = None,
        time_of_day: TimeOfDay = TimeOfDay.NIGHT_PATROL,
        style: ArtStyle = ArtStyle.CINEMATIC
    ) -> GenerationPrompt:
        """Generate a prompt for action sequence concept art"""
        hero_config = self.config.get("hero_integration", {})
        character_name = hero_config.get("character", "Black Batman")
        
        subject = f"{character_name} {action}, motion blur effect, dynamic perspective"
        
        modifiers = [
            "dramatic action",
            "heroic moment",
            "intense energy",
            "cinematic framing"
        ]
        
        prompt_id = f"action_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        prompt = GenerationPrompt(
            id=prompt_id,
            category=AssetCategory.ACTION,
            style=style,
            subject=subject,
            location=location or "Mays Landing rooftops",
            time_of_day=time_of_day,
            modifiers=modifiers,
            negative_prompts=["static", "stiff", "flat composition"]
        )
        
        self.prompts.append(prompt)
        self.prompt_history.append(prompt.to_dict())
        
        return prompt
    
    def generate_mood_board_prompt(
        self,
        theme: str,
        color_scheme: Optional[str] = None,
        style: ArtStyle = ArtStyle.CONCEPT_ART
    ) -> GenerationPrompt:
        """Generate a prompt for mood board/color palette art"""
        subject = f"Mood board for {theme}, visual development, color studies"
        
        modifiers = [
            "artistic composition",
            "color harmony",
            "visual reference"
        ]
        if color_scheme:
            modifiers.append(f"{color_scheme} color palette")
        
        prompt_id = f"mood_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        prompt = GenerationPrompt(
            id=prompt_id,
            category=AssetCategory.MOOD_BOARD,
            style=style,
            subject=subject,
            modifiers=modifiers,
            negative_prompts=["cluttered", "inconsistent", "chaotic"]
        )
        
        self.prompts.append(prompt)
        self.prompt_history.append(prompt.to_dict())
        
        return prompt
    
    def get_signature_scene_prompts(self) -> List[GenerationPrompt]:
        """Generate prompts for all signature scenes defined in config"""
        signature_scenes = (
            self.config
            .get("hero_integration", {})
            .get("signature_scenes", [])
        )
        
        prompts = []
        for scene in signature_scenes:
            subject = f"Black Batman - {scene['name']}: {scene['description']}"
            modifiers = scene.get("key_elements", [])
            
            prompt = GenerationPrompt(
                id=f"sig_{scene['name'].lower().replace(' ', '_')}",
                category=AssetCategory.CHARACTER,
                style=ArtStyle.CINEMATIC,
                subject=subject,
                location="Mays Landing",
                time_of_day=TimeOfDay.NIGHT_PATROL,
                modifiers=modifiers + ["hero shot", "iconic moment"]
            )
            prompts.append(prompt)
            self.prompts.append(prompt)
            self.prompt_history.append(prompt.to_dict())
        
        return prompts
    
    def export_prompts(self, output_path: str = None) -> str:
        """Export all generated prompts to JSON file"""
        output_path = output_path or os.path.join(
            os.path.dirname(self.config_path),
            "..",
            "assets",
            "prompts_export.json"
        )
        
        export_data = {
            "project": self.config.get("project"),
            "exported_at": datetime.now().isoformat(),
            "prompt_count": len(self.prompt_history),
            "prompts": self.prompt_history
        }
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        return output_path
    
    def generate_batch_prompts(
        self,
        count: int = 5,
        categories: List[AssetCategory] = None
    ) -> List[GenerationPrompt]:
        """Generate a batch of diverse prompts for rapid iteration"""
        if categories is None:
            categories = [
                AssetCategory.CHARACTER,
                AssetCategory.ENVIRONMENT,
                AssetCategory.ACTION
            ]
        
        prompts = []
        locations = self.get_locations()
        times = list(TimeOfDay)
        
        poses = [
            "crouching on rooftop",
            "leaping between buildings",
            "standing vigilant",
            "running at full speed",
            "confronting villain"
        ]
        
        actions = [
            "leaping from rooftop",
            "grappling through the air",
            "landing dramatic pose",
            "fighting in shadows",
            "emerging from darkness"
        ]
        
        for i in range(count):
            category = categories[i % len(categories)]
            time_of_day = times[i % len(times)]
            
            if category == AssetCategory.CHARACTER:
                prompt = self.generate_character_prompt(
                    pose=poses[i % len(poses)],
                    location=locations[i % len(locations)] if locations else None,
                    time_of_day=time_of_day
                )
            elif category == AssetCategory.ENVIRONMENT:
                loc_config = self.config.get("locations", [])
                if loc_config:
                    loc_id = loc_config[i % len(loc_config)]["id"]
                    prompt = self.generate_environment_prompt(
                        location_id=loc_id,
                        time_of_day=time_of_day
                    )
                else:
                    # Fallback to mood board when no locations configured
                    prompt = self.generate_mood_board_prompt(
                        theme=f"Mays Landing Environment {i + 1}"
                    )
            elif category == AssetCategory.ACTION:
                prompt = self.generate_action_sequence_prompt(
                    action=actions[i % len(actions)],
                    time_of_day=time_of_day
                )
            else:
                prompt = self.generate_mood_board_prompt(
                    theme=f"Black Batman Scene {i + 1}"
                )
            
            prompts.append(prompt)
        
        return prompts
    
    def get_prompt_statistics(self) -> Dict:
        """Get statistics about generated prompts"""
        stats = {
            "total_prompts": len(self.prompts),
            "by_category": {},
            "by_style": {},
            "by_time_of_day": {}
        }
        
        for prompt in self.prompts:
            # Count by category
            cat = prompt.category.value
            stats["by_category"][cat] = stats["by_category"].get(cat, 0) + 1
            
            # Count by style
            style = prompt.style.value
            stats["by_style"][style] = stats["by_style"].get(style, 0) + 1
            
            # Count by time of day
            if prompt.time_of_day:
                tod = prompt.time_of_day.value
                stats["by_time_of_day"][tod] = stats["by_time_of_day"].get(tod, 0) + 1
        
        return stats


def demo_pipeline():
    """Demonstration of the concept art generation pipeline"""
    print("\n" + "=" * 70)
    print("BLACK BATMAN CONCEPT ART GENERATOR")
    print("AI Pipeline for Motion Cartoon Visual Development")
    print("=" * 70)
    
    # Initialize generator
    generator = ConceptArtGenerator()
    
    print(f"\n✨ Project: {generator.config.get('project')}")
    print(f"📍 Setting: {generator.config.get('environment', {}).get('name')}")
    
    # List available locations
    locations = generator.get_locations()
    print(f"\n🗺️ Available Locations ({len(locations)}):")
    for loc in locations:
        print(f"   • {loc}")
    
    # Generate character prompt
    print("\n" + "-" * 70)
    print("GENERATING CHARACTER PROMPT")
    print("-" * 70)
    
    char_prompt = generator.generate_character_prompt(
        pose="perched on courthouse rooftop",
        location="Mays Landing Historic Courthouse",
        time_of_day=TimeOfDay.NIGHT_PATROL,
        style=ArtStyle.CINEMATIC,
        additional_modifiers=["rain effects", "lightning in background"]
    )
    
    print(f"\n📸 Prompt ID: {char_prompt.id}")
    print(f"📝 Full Prompt:\n   {char_prompt.build_prompt()}")
    
    # Generate environment prompt
    print("\n" + "-" * 70)
    print("GENERATING ENVIRONMENT PROMPT")
    print("-" * 70)
    
    env_prompt = generator.generate_environment_prompt(
        location_id="loc_002",
        time_of_day=TimeOfDay.DAWN,
        style=ArtStyle.CONCEPT_ART
    )
    
    print(f"\n🏞️ Prompt ID: {env_prompt.id}")
    print(f"📝 Full Prompt:\n   {env_prompt.build_prompt()}")
    
    # Generate action sequence prompt
    print("\n" + "-" * 70)
    print("GENERATING ACTION SEQUENCE PROMPT")
    print("-" * 70)
    
    action_prompt = generator.generate_action_sequence_prompt(
        action="diving from rooftop toward fleeing vehicle",
        location="Great Egg Harbor River Bridge",
        time_of_day=TimeOfDay.STORMY
    )
    
    print(f"\n⚡ Prompt ID: {action_prompt.id}")
    print(f"📝 Full Prompt:\n   {action_prompt.build_prompt()}")
    
    # Generate signature scene prompts
    print("\n" + "-" * 70)
    print("GENERATING SIGNATURE SCENE PROMPTS")
    print("-" * 70)
    
    sig_prompts = generator.get_signature_scene_prompts()
    for prompt in sig_prompts:
        print(f"\n🌟 {prompt.id}")
        print(f"   {prompt.build_prompt()[:100]}...")
    
    # Generate batch prompts
    print("\n" + "-" * 70)
    print("GENERATING BATCH PROMPTS FOR RAPID ITERATION")
    print("-" * 70)
    
    batch = generator.generate_batch_prompts(count=5)
    print(f"\n✅ Generated {len(batch)} prompts for rapid iteration")
    
    # Show statistics
    print("\n" + "=" * 70)
    print("PIPELINE STATISTICS")
    print("=" * 70)
    
    stats = generator.get_prompt_statistics()
    print(f"\n📊 Total Prompts Generated: {stats['total_prompts']}")
    
    print("\n   By Category:")
    for cat, count in stats['by_category'].items():
        print(f"      {cat}: {count}")
    
    print("\n   By Style:")
    for style, count in stats['by_style'].items():
        print(f"      {style}: {count}")
    
    print("\n   By Time of Day:")
    for tod, count in stats['by_time_of_day'].items():
        print(f"      {tod}: {count}")
    
    print("\n" + "=" * 70)
    print("✨ Pipeline demonstration complete!")
    print("=" * 70)


if __name__ == "__main__":
    demo_pipeline()
