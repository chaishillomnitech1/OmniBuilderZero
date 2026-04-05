"""
Educational Agents for ScrollVerse Adaptive Learning

This package contains specialized educational agents for different
subject areas, designed for children-centric adaptive learning.
"""

from .base_educational_agent import BaseEducationalAgent, AgentCapability, AgentResponse
from .stem_agent import STEMAgent
from .storytelling_agent import StorytellingAgent
from .math_agent import MathAgent
from .agent_router import AgentRouter, TaskType

__all__ = [
    "BaseEducationalAgent",
    "AgentCapability",
    "AgentResponse",
    "STEMAgent",
    "StorytellingAgent",
    "MathAgent",
    "AgentRouter",
    "TaskType",
]
