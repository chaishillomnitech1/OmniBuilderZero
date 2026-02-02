"""
Core Agentic Design Patterns for ScrollVerse Education

This package implements the foundational AI design patterns adapted from
Antonio Gulli's 'Agentic Design Patterns' for children-centric education.
"""

from .prompt_chaining import PromptChain, ChainStep
from .memory_management import MemoryManager, LearnerMemory
from .goal_setting import GoalSetter, LearningGoal
from .knowledge_retrieval import KnowledgeRetriever, KnowledgeItem

__all__ = [
    "PromptChain",
    "ChainStep",
    "MemoryManager",
    "LearnerMemory",
    "GoalSetter",
    "LearningGoal",
    "KnowledgeRetriever",
    "KnowledgeItem",
]
