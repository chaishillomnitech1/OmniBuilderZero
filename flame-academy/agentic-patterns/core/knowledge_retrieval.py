"""
Knowledge Retrieval Pattern for Educational Content

This module implements the knowledge retrieval design pattern for
context-aware retrieval of educational content based on learner needs,
current curriculum position, and learning objectives.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Callable
from datetime import datetime
from enum import Enum
import json
import re


class ContentType(Enum):
    """Types of educational content"""
    LESSON = "lesson"
    EXERCISE = "exercise"
    QUIZ = "quiz"
    VIDEO = "video"
    GAME = "game"
    STORY = "story"
    ACTIVITY = "activity"
    EXAMPLE = "example"
    REFERENCE = "reference"


class DifficultyLevel(Enum):
    """Content difficulty levels"""
    BEGINNER = "beginner"
    ELEMENTARY = "elementary"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class LearningModality(Enum):
    """Learning modalities for content"""
    VISUAL = "visual"
    AUDITORY = "auditory"
    KINESTHETIC = "kinesthetic"
    READING = "reading"
    MULTIMODAL = "multimodal"


@dataclass
class KnowledgeItem:
    """
    A single piece of educational content.
    
    Represents any retrievable learning material with metadata
    for intelligent matching to learner needs.
    """
    id: str
    title: str
    content: str
    content_type: ContentType
    subject: str
    topics: List[str]
    difficulty: DifficultyLevel
    age_range: tuple = (6, 12)
    modalities: List[LearningModality] = field(default_factory=lambda: [LearningModality.READING])
    prerequisites: List[str] = field(default_factory=list)
    related_items: List[str] = field(default_factory=list)
    keywords: List[str] = field(default_factory=list)
    estimated_duration_minutes: int = 10
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def matches_query(self, query: str) -> float:
        """
        Calculate relevance score for a search query.
        
        Args:
            query: Search query string
            
        Returns:
            Relevance score from 0.0 to 1.0
        """
        query_lower = query.lower()
        query_words = set(query_lower.split())
        
        score = 0.0
        
        # Check title match
        if query_lower in self.title.lower():
            score += 0.4
        
        # Check topic match
        for topic in self.topics:
            if query_lower in topic.lower() or topic.lower() in query_lower:
                score += 0.3
                break
        
        # Check keyword match
        keyword_matches = sum(1 for kw in self.keywords if kw.lower() in query_lower or query_lower in kw.lower())
        if self.keywords:
            score += (keyword_matches / len(self.keywords)) * 0.2
        
        # Check content match
        content_lower = self.content.lower()
        word_matches = sum(1 for word in query_words if word in content_lower)
        if query_words:
            score += (word_matches / len(query_words)) * 0.1
        
        return min(1.0, score)
    
    def is_appropriate_for(self, age: int, current_level: DifficultyLevel) -> bool:
        """
        Check if content is appropriate for learner.
        
        Args:
            age: Learner's age
            current_level: Learner's current difficulty level
            
        Returns:
            True if content is appropriate
        """
        # Check age range
        min_age, max_age = self.age_range
        if not (min_age <= age <= max_age):
            return False
        
        # Check difficulty - allow current level and one below
        difficulty_order = list(DifficultyLevel)
        current_index = difficulty_order.index(current_level)
        content_index = difficulty_order.index(self.difficulty)
        
        return content_index <= current_index + 1
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "title": self.title,
            "content_type": self.content_type.value,
            "subject": self.subject,
            "topics": self.topics,
            "difficulty": self.difficulty.value,
            "age_range": self.age_range,
            "estimated_duration": self.estimated_duration_minutes,
            "keywords": self.keywords
        }


@dataclass
class RetrievalContext:
    """
    Context for knowledge retrieval.
    
    Captures all relevant information for intelligent content selection.
    """
    learner_id: str
    learner_age: int
    current_subject: str
    current_topic: Optional[str] = None
    difficulty_level: DifficultyLevel = DifficultyLevel.BEGINNER
    preferred_modalities: List[LearningModality] = field(default_factory=lambda: [LearningModality.VISUAL])
    completed_items: List[str] = field(default_factory=list)
    struggling_topics: List[str] = field(default_factory=list)
    interests: List[str] = field(default_factory=list)
    session_duration_remaining: int = 15  # minutes
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "learner_id": self.learner_id,
            "learner_age": self.learner_age,
            "subject": self.current_subject,
            "topic": self.current_topic,
            "difficulty": self.difficulty_level.value,
            "modalities": [m.value for m in self.preferred_modalities],
            "interests": self.interests
        }


class KnowledgeRetriever:
    """
    Retrieves educational content based on learner context.
    
    Implements intelligent retrieval with filtering, ranking,
    and personalization for adaptive learning.
    """
    
    def __init__(self):
        """Initialize the knowledge retriever"""
        self.knowledge_base: Dict[str, KnowledgeItem] = {}
        self.subject_indices: Dict[str, List[str]] = {}  # subject -> item_ids
        self.topic_indices: Dict[str, List[str]] = {}    # topic -> item_ids
        self._init_sample_content()
    
    def _init_sample_content(self):
        """Initialize with sample educational content"""
        sample_items = [
            # Math Content
            KnowledgeItem(
                id="math_addition_intro",
                title="Introduction to Addition",
                content="""
                Addition is putting numbers together to get a bigger number!
                
                When we add, we use the plus sign (+).
                
                Example: 2 + 3 = 5
                
                We can use objects to help us:
                🍎🍎 + 🍎🍎🍎 = 🍎🍎🍎🍎🍎 (5 apples!)
                """,
                content_type=ContentType.LESSON,
                subject="math",
                topics=["addition", "basics", "numbers"],
                difficulty=DifficultyLevel.BEGINNER,
                age_range=(5, 8),
                keywords=["add", "plus", "sum", "total", "together"],
                estimated_duration_minutes=10
            ),
            KnowledgeItem(
                id="math_addition_practice",
                title="Addition Practice: Counting Objects",
                content="""
                Let's practice adding with pictures!
                
                1. Count the stars: ⭐⭐ + ⭐⭐⭐ = ?
                2. Count the hearts: ❤️❤️❤️ + ❤️❤️ = ?
                3. Count the suns: ☀️ + ☀️☀️☀️☀️ = ?
                
                Remember: Count all the objects together!
                """,
                content_type=ContentType.EXERCISE,
                subject="math",
                topics=["addition", "counting", "practice"],
                difficulty=DifficultyLevel.BEGINNER,
                age_range=(5, 8),
                prerequisites=["math_addition_intro"],
                keywords=["add", "count", "practice", "objects"],
                estimated_duration_minutes=15
            ),
            KnowledgeItem(
                id="math_subtraction_intro",
                title="Introduction to Subtraction",
                content="""
                Subtraction is taking away to find what's left!
                
                When we subtract, we use the minus sign (-).
                
                Example: 5 - 2 = 3
                
                Imagine you have 5 cookies 🍪🍪🍪🍪🍪
                You eat 2 of them 🍪🍪
                How many are left? 🍪🍪🍪 (3 cookies!)
                """,
                content_type=ContentType.LESSON,
                subject="math",
                topics=["subtraction", "basics", "numbers"],
                difficulty=DifficultyLevel.BEGINNER,
                age_range=(5, 8),
                keywords=["subtract", "minus", "take away", "left", "difference"],
                estimated_duration_minutes=10
            ),
            
            # Science Content
            KnowledgeItem(
                id="science_planets_intro",
                title="Our Solar System: Meet the Planets!",
                content="""
                Our Solar System has 8 amazing planets that go around the Sun!
                
                🌍 Here they are in order from the Sun:
                1. Mercury - The smallest and fastest planet
                2. Venus - The hottest planet (even hotter than Mercury!)
                3. Earth - Our home! The only planet with life we know of
                4. Mars - The red planet
                5. Jupiter - The biggest planet
                6. Saturn - Famous for its beautiful rings
                7. Uranus - A tilted, icy giant
                8. Neptune - The windiest planet
                
                Can you remember all 8?
                """,
                content_type=ContentType.LESSON,
                subject="science",
                topics=["space", "planets", "solar system"],
                difficulty=DifficultyLevel.ELEMENTARY,
                age_range=(6, 10),
                modalities=[LearningModality.VISUAL, LearningModality.READING],
                keywords=["planets", "space", "solar system", "sun", "earth", "mars"],
                estimated_duration_minutes=12
            ),
            KnowledgeItem(
                id="science_animals_classify",
                title="Animal Classification: How Scientists Group Animals",
                content="""
                Scientists group animals to understand them better!
                
                🐾 Main Animal Groups:
                
                1. MAMMALS 🐕
                   - Have fur or hair
                   - Feed babies milk
                   - Examples: dogs, cats, elephants, humans!
                
                2. BIRDS 🐦
                   - Have feathers
                   - Lay eggs
                   - Most can fly
                   - Examples: eagles, penguins, owls
                
                3. FISH 🐠
                   - Live in water
                   - Have scales
                   - Breathe through gills
                   - Examples: goldfish, sharks, clownfish
                
                4. REPTILES 🐊
                   - Have scales
                   - Cold-blooded
                   - Examples: snakes, lizards, turtles
                
                5. AMPHIBIANS 🐸
                   - Live in water AND on land
                   - Examples: frogs, salamanders
                """,
                content_type=ContentType.LESSON,
                subject="science",
                topics=["animals", "classification", "biology"],
                difficulty=DifficultyLevel.ELEMENTARY,
                age_range=(6, 10),
                keywords=["animals", "mammals", "birds", "fish", "reptiles", "classify"],
                estimated_duration_minutes=15
            ),
            
            # Reading/Storytelling Content
            KnowledgeItem(
                id="story_dragon_friend",
                title="The Friendly Dragon",
                content="""
                🐉 THE FRIENDLY DRAGON
                
                Once upon a time, in a cozy village, lived a little dragon named Spark.
                
                Spark was different from other dragons. He didn't like scaring people.
                He liked to help!
                
                One day, a farmer's barn caught fire from lightning.
                "Oh no!" cried the villagers. "We can't put it out!"
                
                Spark flew over quickly. Instead of breathing fire like other dragons,
                Spark could breathe WATER! 💧
                
                SPLASH! SPLASH! The fire went out.
                
                "Thank you, Spark!" cheered everyone.
                
                From that day on, Spark became the village's best friend.
                He helped warm houses in winter and put out fires in summer.
                
                The End. 🌟
                
                What did you learn from Spark's story?
                """,
                content_type=ContentType.STORY,
                subject="reading",
                topics=["stories", "friendship", "helping others"],
                difficulty=DifficultyLevel.BEGINNER,
                age_range=(5, 8),
                modalities=[LearningModality.READING, LearningModality.AUDITORY],
                keywords=["dragon", "story", "friend", "help", "village"],
                estimated_duration_minutes=8
            ),
            KnowledgeItem(
                id="reading_comprehension_basics",
                title="Understanding Stories: Who, What, Where",
                content="""
                📖 HOW TO UNDERSTAND STORIES
                
                When you read a story, ask yourself these questions:
                
                👤 WHO is in the story?
                   - Who are the characters?
                   - Who is the main character?
                
                ❓ WHAT happens?
                   - What is the problem?
                   - What do the characters do?
                   - What happens at the end?
                
                📍 WHERE does it happen?
                   - Where are the characters?
                   - Does the place change?
                
                ⏰ WHEN does it happen?
                   - Is it day or night?
                   - Is it long ago or now?
                
                Practice: Read "The Friendly Dragon" and answer these questions!
                """,
                content_type=ContentType.LESSON,
                subject="reading",
                topics=["comprehension", "stories", "analysis"],
                difficulty=DifficultyLevel.ELEMENTARY,
                age_range=(6, 9),
                keywords=["story", "understand", "who", "what", "where", "when"],
                estimated_duration_minutes=10
            )
        ]
        
        # Add items to knowledge base
        for item in sample_items:
            self.add_item(item)
    
    def add_item(self, item: KnowledgeItem):
        """
        Add an item to the knowledge base.
        
        Args:
            item: KnowledgeItem to add
        """
        self.knowledge_base[item.id] = item
        
        # Update subject index
        if item.subject not in self.subject_indices:
            self.subject_indices[item.subject] = []
        self.subject_indices[item.subject].append(item.id)
        
        # Update topic indices
        for topic in item.topics:
            if topic not in self.topic_indices:
                self.topic_indices[topic] = []
            self.topic_indices[topic].append(item.id)
    
    def get_item(self, item_id: str) -> Optional[KnowledgeItem]:
        """Get an item by ID"""
        return self.knowledge_base.get(item_id)
    
    def search(self, query: str, limit: int = 5) -> List[KnowledgeItem]:
        """
        Search the knowledge base.
        
        Args:
            query: Search query
            limit: Maximum results to return
            
        Returns:
            List of matching items sorted by relevance
        """
        results = []
        for item in self.knowledge_base.values():
            score = item.matches_query(query)
            if score > 0.1:
                results.append((score, item))
        
        # Sort by score descending
        results.sort(key=lambda x: x[0], reverse=True)
        return [item for _, item in results[:limit]]
    
    def retrieve_for_context(self, context: RetrievalContext, limit: int = 5) -> List[KnowledgeItem]:
        """
        Retrieve content appropriate for the given context.
        
        Args:
            context: Retrieval context with learner information
            limit: Maximum results to return
            
        Returns:
            List of appropriate items ranked by relevance
        """
        candidates = []
        
        # Start with subject-filtered items
        subject_items = self.subject_indices.get(context.current_subject, [])
        
        for item_id in subject_items:
            item = self.knowledge_base[item_id]
            
            # Skip completed items
            if item_id in context.completed_items:
                continue
            
            # Check appropriateness
            if not item.is_appropriate_for(context.learner_age, context.difficulty_level):
                continue
            
            # Check duration fits session
            if item.estimated_duration_minutes > context.session_duration_remaining:
                continue
            
            # Calculate relevance score
            score = self._calculate_contextual_score(item, context)
            candidates.append((score, item))
        
        # Sort by score descending
        candidates.sort(key=lambda x: x[0], reverse=True)
        return [item for _, item in candidates[:limit]]
    
    def _calculate_contextual_score(self, item: KnowledgeItem, context: RetrievalContext) -> float:
        """Calculate relevance score based on context"""
        score = 0.0
        
        # Topic match
        if context.current_topic and context.current_topic in item.topics:
            score += 0.4
        
        # Interest match
        for interest in context.interests:
            if interest.lower() in [t.lower() for t in item.topics]:
                score += 0.2
                break
        
        # Modality preference match
        for modality in context.preferred_modalities:
            if modality in item.modalities:
                score += 0.15
                break
        
        # Struggling topic - prioritize remedial content
        for struggling in context.struggling_topics:
            if struggling.lower() in [t.lower() for t in item.topics]:
                score += 0.25
                break
        
        # Prerequisites met
        prerequisites_met = all(
            prereq in context.completed_items 
            for prereq in item.prerequisites
        )
        if prerequisites_met:
            score += 0.1
        else:
            score -= 0.3  # Penalize if prerequisites not met
        
        return max(0.0, min(1.0, score))
    
    def get_next_item(self, context: RetrievalContext, current_item_id: Optional[str] = None) -> Optional[KnowledgeItem]:
        """
        Get the next recommended item in the learning sequence.
        
        Args:
            context: Retrieval context
            current_item_id: ID of current item (if any)
            
        Returns:
            Next recommended item or None
        """
        # If we have a current item, try its related items first
        if current_item_id:
            current = self.get_item(current_item_id)
            if current and current.related_items:
                for related_id in current.related_items:
                    if related_id not in context.completed_items:
                        related = self.get_item(related_id)
                        if related and related.is_appropriate_for(context.learner_age, context.difficulty_level):
                            return related
        
        # Otherwise, retrieve based on context
        items = self.retrieve_for_context(context, limit=1)
        return items[0] if items else None
    
    def get_items_by_subject(self, subject: str) -> List[KnowledgeItem]:
        """Get all items for a subject"""
        item_ids = self.subject_indices.get(subject, [])
        return [self.knowledge_base[id] for id in item_ids]
    
    def get_items_by_topic(self, topic: str) -> List[KnowledgeItem]:
        """Get all items for a topic"""
        item_ids = self.topic_indices.get(topic, [])
        return [self.knowledge_base[id] for id in item_ids]
    
    def get_subjects(self) -> List[str]:
        """Get all available subjects"""
        return list(self.subject_indices.keys())
    
    def get_topics(self, subject: Optional[str] = None) -> List[str]:
        """Get all available topics, optionally filtered by subject"""
        if subject:
            items = self.get_items_by_subject(subject)
            topics = set()
            for item in items:
                topics.update(item.topics)
            return list(topics)
        return list(self.topic_indices.keys())
    
    def get_stats(self) -> Dict[str, Any]:
        """Get knowledge base statistics"""
        return {
            "total_items": len(self.knowledge_base),
            "subjects": len(self.subject_indices),
            "topics": len(self.topic_indices),
            "by_subject": {s: len(ids) for s, ids in self.subject_indices.items()},
            "by_type": self._count_by_type()
        }
    
    def _count_by_type(self) -> Dict[str, int]:
        """Count items by content type"""
        counts = {}
        for item in self.knowledge_base.values():
            type_name = item.content_type.value
            counts[type_name] = counts.get(type_name, 0) + 1
        return counts


if __name__ == "__main__":
    # Demo the knowledge retrieval system
    retriever = KnowledgeRetriever()
    
    print("=== Knowledge Retrieval Demo ===\n")
    
    # Show stats
    stats = retriever.get_stats()
    print(f"Knowledge Base: {stats['total_items']} items across {stats['subjects']} subjects")
    print(f"Items by subject: {stats['by_subject']}")
    print(f"Items by type: {stats['by_type']}")
    
    # Search demo
    print("\n--- Search: 'addition' ---")
    results = retriever.search("addition")
    for item in results:
        print(f"  • {item.title} ({item.content_type.value})")
    
    # Context-based retrieval
    print("\n--- Context-Based Retrieval ---")
    context = RetrievalContext(
        learner_id="student_001",
        learner_age=7,
        current_subject="math",
        difficulty_level=DifficultyLevel.BEGINNER,
        preferred_modalities=[LearningModality.VISUAL],
        interests=["animals", "space"]
    )
    
    items = retriever.retrieve_for_context(context)
    print(f"Recommended for 7-year-old learning math:")
    for item in items:
        print(f"  • {item.title}")
        print(f"    Topics: {', '.join(item.topics)}")
        print(f"    Duration: {item.estimated_duration_minutes} min")
