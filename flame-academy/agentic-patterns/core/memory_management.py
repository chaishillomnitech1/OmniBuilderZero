"""
Memory Management Pattern for Adaptive Learning

This module implements the memory management design pattern for maintaining
learner context, progress, and preferences across learning sessions.
Enables personalized education by remembering each child's unique journey.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum
import json


class MemoryType(Enum):
    """Types of memory storage"""
    SHORT_TERM = "short_term"      # Current session context
    WORKING = "working"            # Active learning context
    LONG_TERM = "long_term"        # Persistent learner profile
    EPISODIC = "episodic"          # Specific learning experiences


class LearningStyle(Enum):
    """Learning style preferences"""
    VISUAL = "visual"              # Learns best with images, diagrams
    AUDITORY = "auditory"          # Learns best with sounds, explanations
    KINESTHETIC = "kinesthetic"    # Learns best with hands-on activities
    READING = "reading"            # Learns best with text


@dataclass
class LearnerProfile:
    """
    Comprehensive profile of a learner.
    
    Stores demographic and preference information for personalization.
    """
    learner_id: str
    name: str
    age: int
    grade_level: Optional[int] = None
    learning_style: LearningStyle = LearningStyle.VISUAL
    interests: List[str] = field(default_factory=list)
    strengths: List[str] = field(default_factory=list)
    areas_for_growth: List[str] = field(default_factory=list)
    preferred_session_length: int = 15  # minutes
    accessibility_needs: List[str] = field(default_factory=list)
    language: str = "en"
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def update(self, **kwargs):
        """Update profile fields"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.now().isoformat()


@dataclass
class LearningSession:
    """
    Records a single learning session.
    
    Captures what happened during a learning interaction.
    """
    session_id: str
    learner_id: str
    subject: str
    started_at: str
    ended_at: Optional[str] = None
    duration_minutes: int = 0
    concepts_covered: List[str] = field(default_factory=list)
    activities_completed: List[str] = field(default_factory=list)
    scores: Dict[str, float] = field(default_factory=dict)
    engagement_level: float = 0.0  # 0.0 to 1.0
    mood_indicators: List[str] = field(default_factory=list)
    notes: str = ""
    
    def end_session(self):
        """End the current session and calculate duration"""
        self.ended_at = datetime.now().isoformat()
        start = datetime.fromisoformat(self.started_at)
        end = datetime.fromisoformat(self.ended_at)
        self.duration_minutes = int((end - start).total_seconds() / 60)


@dataclass
class ConceptMastery:
    """
    Tracks a learner's mastery of a specific concept.
    """
    concept_id: str
    concept_name: str
    subject: str
    mastery_level: float = 0.0  # 0.0 to 1.0
    attempts: int = 0
    successes: int = 0
    last_practiced: Optional[str] = None
    first_introduced: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def record_attempt(self, success: bool):
        """Record a practice attempt"""
        self.attempts += 1
        if success:
            self.successes += 1
        self.last_practiced = datetime.now().isoformat()
        # Update mastery level based on recent performance
        self.mastery_level = self.successes / self.attempts if self.attempts > 0 else 0.0


@dataclass
class LearnerMemory:
    """
    Complete memory storage for a learner.
    
    Combines short-term, working, and long-term memory patterns
    to provide comprehensive context for adaptive learning.
    """
    profile: LearnerProfile
    sessions: List[LearningSession] = field(default_factory=list)
    concept_mastery: Dict[str, ConceptMastery] = field(default_factory=dict)
    current_context: Dict[str, Any] = field(default_factory=dict)
    achievements: List[str] = field(default_factory=list)
    streak_days: int = 0
    last_active_date: Optional[str] = None
    total_learning_minutes: int = 0
    favorite_subjects: List[str] = field(default_factory=list)
    
    def start_session(self, subject: str) -> LearningSession:
        """Start a new learning session"""
        session = LearningSession(
            session_id=f"session_{len(self.sessions) + 1}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            learner_id=self.profile.learner_id,
            subject=subject,
            started_at=datetime.now().isoformat()
        )
        self.sessions.append(session)
        self._update_streak()
        return session
    
    def end_current_session(self):
        """End the current session"""
        if self.sessions:
            current = self.sessions[-1]
            if not current.ended_at:
                current.end_session()
                self.total_learning_minutes += current.duration_minutes
    
    def _update_streak(self):
        """Update the learning streak"""
        today = datetime.now().date().isoformat()
        if self.last_active_date:
            last_date = datetime.fromisoformat(self.last_active_date).date()
            today_date = datetime.now().date()
            days_diff = (today_date - last_date).days
            if days_diff == 1:
                self.streak_days += 1
            elif days_diff > 1:
                self.streak_days = 1
        else:
            self.streak_days = 1
        self.last_active_date = today
    
    def record_concept_practice(self, concept_id: str, concept_name: str, subject: str, success: bool):
        """Record practice of a concept"""
        if concept_id not in self.concept_mastery:
            self.concept_mastery[concept_id] = ConceptMastery(
                concept_id=concept_id,
                concept_name=concept_name,
                subject=subject
            )
        self.concept_mastery[concept_id].record_attempt(success)
    
    def get_mastery_summary(self, subject: Optional[str] = None) -> Dict[str, Any]:
        """Get a summary of concept mastery"""
        concepts = self.concept_mastery.values()
        if subject:
            concepts = [c for c in concepts if c.subject == subject]
        
        if not concepts:
            return {"average_mastery": 0.0, "concepts_count": 0, "mastered_count": 0}
        
        concepts = list(concepts)
        avg_mastery = sum(c.mastery_level for c in concepts) / len(concepts)
        mastered = sum(1 for c in concepts if c.mastery_level >= 0.8)
        
        return {
            "average_mastery": avg_mastery,
            "concepts_count": len(concepts),
            "mastered_count": mastered
        }
    
    def get_recommended_concepts(self, subject: Optional[str] = None, limit: int = 5) -> List[ConceptMastery]:
        """Get concepts that need more practice"""
        concepts = list(self.concept_mastery.values())
        if subject:
            concepts = [c for c in concepts if c.subject == subject]
        
        # Sort by mastery level (ascending) and last practiced (oldest first)
        concepts.sort(key=lambda c: (c.mastery_level, c.last_practiced or ""))
        return concepts[:limit]
    
    def add_achievement(self, achievement: str):
        """Add an achievement badge"""
        if achievement not in self.achievements:
            self.achievements.append(achievement)
    
    def get_learning_stats(self) -> Dict[str, Any]:
        """Get comprehensive learning statistics"""
        return {
            "learner_name": self.profile.name,
            "total_sessions": len(self.sessions),
            "total_learning_minutes": self.total_learning_minutes,
            "current_streak": self.streak_days,
            "achievements_count": len(self.achievements),
            "mastery_summary": self.get_mastery_summary(),
            "favorite_subjects": self.favorite_subjects,
            "learning_style": self.profile.learning_style.value
        }
    
    def set_context(self, key: str, value: Any):
        """Set a context value for the current interaction"""
        self.current_context[key] = value
    
    def get_context(self, key: str, default: Any = None) -> Any:
        """Get a context value"""
        return self.current_context.get(key, default)
    
    def clear_context(self):
        """Clear the current context (short-term memory)"""
        self.current_context = {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert memory to dictionary for serialization"""
        return {
            "profile": {
                "learner_id": self.profile.learner_id,
                "name": self.profile.name,
                "age": self.profile.age,
                "learning_style": self.profile.learning_style.value,
                "interests": self.profile.interests
            },
            "sessions_count": len(self.sessions),
            "total_learning_minutes": self.total_learning_minutes,
            "streak_days": self.streak_days,
            "achievements": self.achievements,
            "mastery_summary": self.get_mastery_summary()
        }


class MemoryManager:
    """
    Manages memory storage and retrieval for multiple learners.
    
    Provides centralized access to learner memories with persistence
    and retrieval capabilities.
    """
    
    def __init__(self, storage_path: Optional[str] = None):
        """
        Initialize the memory manager.
        
        Args:
            storage_path: Optional path for persisting memories to disk
        """
        self.storage_path = storage_path
        self.learner_memories: Dict[str, LearnerMemory] = {}
    
    def create_learner(self, learner_id: str, name: str, age: int, **kwargs) -> LearnerMemory:
        """
        Create a new learner memory.
        
        Args:
            learner_id: Unique identifier for the learner
            name: Learner's name
            age: Learner's age
            **kwargs: Additional profile attributes
            
        Returns:
            New LearnerMemory instance
        """
        profile = LearnerProfile(
            learner_id=learner_id,
            name=name,
            age=age,
            **kwargs
        )
        memory = LearnerMemory(profile=profile)
        self.learner_memories[learner_id] = memory
        
        if self.storage_path:
            self._save_memory(memory)
        
        return memory
    
    def get_learner(self, learner_id: str) -> Optional[LearnerMemory]:
        """Get a learner's memory by ID"""
        return self.learner_memories.get(learner_id)
    
    def get_or_create_learner(self, learner_id: str, name: str, age: int, **kwargs) -> LearnerMemory:
        """Get existing learner or create new one"""
        if learner_id in self.learner_memories:
            return self.learner_memories[learner_id]
        return self.create_learner(learner_id, name, age, **kwargs)
    
    def get_all_learners(self) -> List[LearnerMemory]:
        """Get all learner memories"""
        return list(self.learner_memories.values())
    
    def update_learner_profile(self, learner_id: str, **kwargs):
        """Update a learner's profile"""
        memory = self.get_learner(learner_id)
        if memory:
            memory.profile.update(**kwargs)
            if self.storage_path:
                self._save_memory(memory)
    
    def get_context_for_agent(self, learner_id: str, subject: str) -> Dict[str, Any]:
        """
        Get comprehensive context for an educational agent.
        
        Returns all relevant information an agent needs to personalize
        the learning experience.
        """
        memory = self.get_learner(learner_id)
        if not memory:
            return {}
        
        return {
            "learner_name": memory.profile.name,
            "learner_age": memory.profile.age,
            "learning_style": memory.profile.learning_style.value,
            "interests": memory.profile.interests,
            "strengths": memory.profile.strengths,
            "areas_for_growth": memory.profile.areas_for_growth,
            "subject_mastery": memory.get_mastery_summary(subject),
            "recommended_concepts": [
                c.concept_name for c in memory.get_recommended_concepts(subject, 3)
            ],
            "current_streak": memory.streak_days,
            "total_learning_time": memory.total_learning_minutes,
            "current_context": memory.current_context
        }
    
    def _save_memory(self, memory: LearnerMemory):
        """Save a learner's memory to disk"""
        if not self.storage_path:
            return
        
        filepath = f"{self.storage_path}/{memory.profile.learner_id}.json"
        try:
            with open(filepath, 'w') as f:
                json.dump(memory.to_dict(), f, indent=2)
        except (IOError, OSError) as e:
            print(f"Warning: Could not save memory: {e}")
    
    def _load_memory(self, learner_id: str) -> Optional[LearnerMemory]:
        """Load a learner's memory from disk"""
        if not self.storage_path:
            return None
        
        filepath = f"{self.storage_path}/{learner_id}.json"
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
                # Reconstruct memory from data
                profile = LearnerProfile(
                    learner_id=data["profile"]["learner_id"],
                    name=data["profile"]["name"],
                    age=data["profile"]["age"],
                    learning_style=LearningStyle(data["profile"]["learning_style"]),
                    interests=data["profile"].get("interests", [])
                )
                memory = LearnerMemory(profile=profile)
                memory.achievements = data.get("achievements", [])
                memory.total_learning_minutes = data.get("total_learning_minutes", 0)
                memory.streak_days = data.get("streak_days", 0)
                return memory
        except (IOError, OSError, json.JSONDecodeError):
            return None


if __name__ == "__main__":
    # Demo the memory management system
    manager = MemoryManager()
    
    # Create a learner
    memory = manager.create_learner(
        learner_id="student_001",
        name="Emma",
        age=8,
        interests=["dinosaurs", "space"],
        learning_style=LearningStyle.VISUAL
    )
    
    # Start a learning session
    session = memory.start_session("math")
    
    # Record some concept practice
    memory.record_concept_practice("add_basic", "Basic Addition", "math", True)
    memory.record_concept_practice("add_basic", "Basic Addition", "math", True)
    memory.record_concept_practice("subtract_basic", "Basic Subtraction", "math", False)
    
    # Add an achievement
    memory.add_achievement("🌟 First Lesson Complete!")
    
    # End the session
    memory.end_current_session()
    
    # Print stats
    print("=== Learner Memory Demo ===\n")
    stats = memory.get_learning_stats()
    print(f"Learner: {stats['learner_name']}")
    print(f"Learning Style: {stats['learning_style']}")
    print(f"Total Sessions: {stats['total_sessions']}")
    print(f"Current Streak: {stats['current_streak']} days")
    print(f"Achievements: {stats['achievements_count']}")
    print(f"\nMastery Summary:")
    print(f"  Average Mastery: {stats['mastery_summary']['average_mastery']:.1%}")
    print(f"  Concepts Practiced: {stats['mastery_summary']['concepts_count']}")
    
    # Get context for an agent
    print("\n=== Agent Context ===")
    context = manager.get_context_for_agent("student_001", "math")
    print(f"Context for math agent: {json.dumps(context, indent=2)}")
