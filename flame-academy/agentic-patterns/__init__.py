"""
Agentic Design Patterns for ScrollVerse Education

A comprehensive framework implementing key AI design patterns for
children-centric education and multi-agent orchestration.

Based on Antonio Gulli's 'Agentic Design Patterns' framework,
adapted for ScrollVerse educational initiatives.
"""

__version__ = "1.0.0"
__author__ = "ScrollVerse Protocol | OmniTech1"

# Core pattern imports
from .core.prompt_chaining import PromptChain, ChainStep
from .core.memory_management import MemoryManager, LearnerMemory, LearningStyle
from .core.goal_setting import GoalSetter, LearningGoal, GoalType
from .core.knowledge_retrieval import KnowledgeRetriever, KnowledgeItem

# Agent imports
from .agents.base_educational_agent import BaseEducationalAgent, LearnerContext, AgentResponse
from .agents.stem_agent import STEMAgent
from .agents.storytelling_agent import StorytellingAgent
from .agents.math_agent import MathAgent
from .agents.agent_router import AgentRouter, TaskType

__all__ = [
    # Version info
    "__version__",
    "__author__",
    # Core patterns
    "PromptChain",
    "ChainStep",
    "MemoryManager",
    "LearnerMemory",
    "LearningStyle",
    "GoalSetter",
    "LearningGoal",
    "GoalType",
    "KnowledgeRetriever",
    "KnowledgeItem",
    # Agents
    "BaseEducationalAgent",
    "LearnerContext",
    "AgentResponse",
    "STEMAgent",
    "StorytellingAgent",
    "MathAgent",
    "AgentRouter",
    "TaskType",
]
