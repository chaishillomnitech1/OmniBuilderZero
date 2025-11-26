"""
Base Educational Agent for ScrollVerse Learning System

This module defines the base class for all educational agents,
providing common functionality for children-centric adaptive learning.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Callable
from datetime import datetime
from enum import Enum
import json


class AgentCapability(Enum):
    """Capabilities that educational agents can have"""
    TEACH = "teach"                    # Can teach new concepts
    PRACTICE = "practice"              # Can provide practice problems
    ASSESS = "assess"                  # Can assess understanding
    EXPLAIN = "explain"                # Can explain concepts in different ways
    ENCOURAGE = "encourage"            # Can provide encouragement and motivation
    ADAPT = "adapt"                    # Can adapt difficulty dynamically
    STORYTELL = "storytell"            # Can create educational stories
    GAMIFY = "gamify"                  # Can create game-based learning
    VISUALIZE = "visualize"            # Can create visual explanations


class ResponseType(Enum):
    """Types of responses an agent can generate"""
    LESSON = "lesson"
    QUESTION = "question"
    FEEDBACK = "feedback"
    ENCOURAGEMENT = "encouragement"
    HINT = "hint"
    EXPLANATION = "explanation"
    STORY = "story"
    GAME = "game"
    SUMMARY = "summary"


@dataclass
class AgentResponse:
    """
    Response from an educational agent.
    
    Encapsulates all information returned from an agent interaction.
    """
    agent_id: str
    response_type: ResponseType
    content: str
    suggestions: List[str] = field(default_factory=list)
    next_actions: List[Dict[str, Any]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    requires_input: bool = False
    input_prompt: Optional[str] = None
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "agent_id": self.agent_id,
            "response_type": self.response_type.value,
            "content": self.content,
            "suggestions": self.suggestions,
            "next_actions": self.next_actions,
            "requires_input": self.requires_input,
            "input_prompt": self.input_prompt,
            "timestamp": self.timestamp
        }


@dataclass
class LearnerContext:
    """
    Context information about the learner for personalization.
    """
    learner_id: str
    name: str
    age: int
    learning_style: str = "visual"
    interests: List[str] = field(default_factory=list)
    current_topic: Optional[str] = None
    mastery_level: float = 0.0
    mood: str = "neutral"
    session_duration: int = 0  # minutes in current session
    recent_performance: List[float] = field(default_factory=list)
    
    @property
    def average_recent_performance(self) -> float:
        """Calculate average of recent performance scores"""
        if not self.recent_performance:
            return 0.5
        return sum(self.recent_performance) / len(self.recent_performance)


class BaseEducationalAgent(ABC):
    """
    Abstract base class for all educational agents.
    
    Provides common functionality for children-centric adaptive learning
    including personalization, encouragement, and age-appropriate responses.
    """
    
    def __init__(
        self,
        agent_id: str,
        name: str,
        subject: str,
        description: str,
        min_age: int = 5,
        max_age: int = 12,
        capabilities: Optional[List[AgentCapability]] = None
    ):
        """
        Initialize the educational agent.
        
        Args:
            agent_id: Unique identifier for this agent
            name: Friendly name for the agent
            subject: Primary subject area (e.g., "math", "science")
            description: Description of the agent's role
            min_age: Minimum recommended age
            max_age: Maximum recommended age
            capabilities: List of agent capabilities
        """
        self.agent_id = agent_id
        self.name = name
        self.subject = subject
        self.description = description
        self.min_age = min_age
        self.max_age = max_age
        self.capabilities = capabilities or [
            AgentCapability.TEACH,
            AgentCapability.EXPLAIN,
            AgentCapability.ENCOURAGE
        ]
        
        # Personality traits for the agent
        self.personality = {
            "friendliness": 0.9,
            "patience": 0.95,
            "enthusiasm": 0.85,
            "humor": 0.6
        }
        
        # Encouragement templates
        self.encouragement_templates = [
            "🌟 You're doing amazing, {name}!",
            "💪 Great effort! Keep going, {name}!",
            "🎉 Wow, {name}! You're really learning!",
            "✨ I believe in you, {name}!",
            "🚀 Look how far you've come, {name}!",
            "🌈 Every mistake helps us learn, {name}!",
            "🔥 You're on fire, {name}! Keep it up!",
            "💖 I'm so proud of you, {name}!"
        ]
    
    @abstractmethod
    def process_request(self, request: str, context: LearnerContext) -> AgentResponse:
        """
        Process a learning request from a student.
        
        Args:
            request: The student's request or input
            context: Context about the learner
            
        Returns:
            Agent's response
        """
        pass
    
    @abstractmethod
    def generate_lesson(self, topic: str, context: LearnerContext) -> AgentResponse:
        """
        Generate a lesson on a specific topic.
        
        Args:
            topic: Topic to teach
            context: Context about the learner
            
        Returns:
            Lesson content response
        """
        pass
    
    @abstractmethod
    def generate_practice(self, topic: str, context: LearnerContext, difficulty: str = "medium") -> AgentResponse:
        """
        Generate practice problems.
        
        Args:
            topic: Topic for practice
            context: Context about the learner
            difficulty: Difficulty level
            
        Returns:
            Practice problems response
        """
        pass
    
    def generate_encouragement(self, context: LearnerContext, situation: str = "general") -> str:
        """
        Generate age-appropriate encouragement.
        
        Args:
            context: Learner context
            situation: Type of situation (general, struggle, success, mistake)
            
        Returns:
            Encouragement message
        """
        import random
        
        if situation == "struggle":
            messages = [
                f"🌱 It's okay, {context.name}! Learning takes time. Let's try again together.",
                f"💪 You can do this, {context.name}! Every expert was once a beginner.",
                f"🤗 Don't worry, {context.name}! Let me help you understand this better.",
                f"🌟 Mistakes help us grow, {context.name}! You're doing great by trying."
            ]
        elif situation == "success":
            messages = [
                f"🎉 AMAZING, {context.name}! You got it right!",
                f"🌟 WOW! You're a superstar, {context.name}!",
                f"🏆 Incredible work, {context.name}! You should be so proud!",
                f"🚀 You're absolutely brilliant, {context.name}!"
            ]
        elif situation == "mistake":
            messages = [
                f"🌈 Almost there, {context.name}! Let's look at this together.",
                f"💡 Good try, {context.name}! Here's a hint to help you.",
                f"🔍 Interesting answer, {context.name}! Let me show you another way.",
                f"🌻 Not quite, but you're thinking hard, {context.name}! That's what matters."
            ]
        else:
            messages = [t.format(name=context.name) for t in self.encouragement_templates]
        
        return random.choice(messages)
    
    def adapt_language_for_age(self, content: str, age: int) -> str:
        """
        Adapt language complexity for the learner's age.
        
        Args:
            content: Original content
            age: Learner's age
            
        Returns:
            Age-adapted content
        """
        # This is a simplified implementation
        # In production, this would use more sophisticated NLP
        if age < 7:
            # Simplify for younger children
            content = content.replace("calculate", "figure out")
            content = content.replace("determine", "find")
            content = content.replace("evaluate", "check")
            content = content.replace("demonstrate", "show")
            content = content.replace("approximately", "about")
        
        return content
    
    def get_difficulty_adjustment(self, context: LearnerContext) -> float:
        """
        Calculate difficulty adjustment based on recent performance.
        
        Args:
            context: Learner context
            
        Returns:
            Adjustment factor (< 1.0 easier, > 1.0 harder)
        """
        avg_performance = context.average_recent_performance
        
        if avg_performance < 0.4:
            return 0.7  # Make easier
        elif avg_performance < 0.6:
            return 0.85  # Slightly easier
        elif avg_performance > 0.9:
            return 1.2  # Make harder
        elif avg_performance > 0.8:
            return 1.1  # Slightly harder
        
        return 1.0  # Keep same
    
    def create_response(
        self,
        content: str,
        response_type: ResponseType,
        context: LearnerContext,
        requires_input: bool = False,
        input_prompt: Optional[str] = None,
        suggestions: Optional[List[str]] = None
    ) -> AgentResponse:
        """
        Create a standardized agent response.
        
        Args:
            content: Response content
            response_type: Type of response
            context: Learner context
            requires_input: Whether input is needed
            input_prompt: Prompt for input if required
            suggestions: Suggested next actions
            
        Returns:
            Formatted AgentResponse
        """
        # Adapt language for age
        adapted_content = self.adapt_language_for_age(content, context.age)
        
        return AgentResponse(
            agent_id=self.agent_id,
            response_type=response_type,
            content=adapted_content,
            suggestions=suggestions or [],
            requires_input=requires_input,
            input_prompt=input_prompt,
            metadata={
                "subject": self.subject,
                "learner_id": context.learner_id,
                "difficulty_adjustment": self.get_difficulty_adjustment(context)
            }
        )
    
    def can_handle_topic(self, topic: str) -> bool:
        """
        Check if this agent can handle a given topic.
        
        Args:
            topic: Topic to check
            
        Returns:
            True if agent can handle the topic
        """
        # Default implementation - override in subclasses
        topic_lower = topic.lower()
        return self.subject.lower() in topic_lower
    
    def is_appropriate_for_age(self, age: int) -> bool:
        """Check if agent is appropriate for given age"""
        return self.min_age <= age <= self.max_age
    
    def get_agent_info(self) -> Dict[str, Any]:
        """Get information about this agent"""
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "subject": self.subject,
            "description": self.description,
            "age_range": (self.min_age, self.max_age),
            "capabilities": [c.value for c in self.capabilities]
        }


if __name__ == "__main__":
    # This is an abstract class, so we can't instantiate it directly
    # The test will be in the subclass files
    print("BaseEducationalAgent is an abstract class.")
    print("See STEMAgent, StorytellingAgent, and MathAgent for implementations.")
