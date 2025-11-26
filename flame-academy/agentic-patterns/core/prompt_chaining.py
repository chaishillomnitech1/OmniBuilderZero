"""
Prompt Chaining Pattern for Educational Content Delivery

This module implements the prompt chaining design pattern, allowing for
sequential, scaffolded learning experiences that build upon each other.
Adapted for children-centric education with age-appropriate progressions.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Callable, Any
from enum import Enum
from datetime import datetime
import json


class ChainStepType(Enum):
    """Types of steps in a prompt chain"""
    INTRODUCTION = "introduction"
    EXPLANATION = "explanation"
    EXAMPLE = "example"
    PRACTICE = "practice"
    ASSESSMENT = "assessment"
    REINFORCEMENT = "reinforcement"
    REFLECTION = "reflection"


class DifficultyLevel(Enum):
    """Difficulty levels for adaptive content"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


@dataclass
class ChainStep:
    """
    A single step in a prompt chain.
    
    Each step represents a discrete learning moment that builds
    toward mastery of a concept.
    """
    id: str
    step_type: ChainStepType
    prompt_template: str
    success_criteria: Dict[str, Any]
    difficulty: DifficultyLevel = DifficultyLevel.BEGINNER
    age_range: tuple = (6, 12)
    prerequisites: List[str] = field(default_factory=list)
    next_steps: Dict[str, str] = field(default_factory=dict)  # outcome -> next_step_id
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def generate_prompt(self, context: Dict[str, Any]) -> str:
        """
        Generate the actual prompt by filling in the template with context.
        
        Args:
            context: Dictionary containing learner context and variables
            
        Returns:
            Filled prompt string ready for presentation
        """
        prompt = self.prompt_template
        for key, value in context.items():
            placeholder = f"{{{key}}}"
            if placeholder in prompt:
                prompt = prompt.replace(placeholder, str(value))
        return prompt
    
    def evaluate_response(self, response: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate a learner's response against success criteria.
        
        Args:
            response: The learner's response to evaluate
            context: Current learning context
            
        Returns:
            Evaluation result with score, feedback, and next step recommendation
        """
        evaluation = {
            "step_id": self.id,
            "timestamp": datetime.now().isoformat(),
            "passed": False,
            "score": 0.0,
            "feedback": "",
            "next_step_id": None
        }
        
        # Basic evaluation logic - can be extended with more sophisticated checks
        keywords = self.success_criteria.get("keywords", [])
        min_length = self.success_criteria.get("min_length", 0)
        
        # Check minimum length
        if len(response) >= min_length:
            evaluation["score"] += 0.3
        
        # Check for keywords
        response_lower = response.lower()
        found_keywords = sum(1 for kw in keywords if kw.lower() in response_lower)
        if keywords:
            keyword_score = found_keywords / len(keywords)
            evaluation["score"] += keyword_score * 0.7
        
        # Determine pass/fail
        pass_threshold = self.success_criteria.get("pass_threshold", 0.6)
        evaluation["passed"] = evaluation["score"] >= pass_threshold
        
        # Generate age-appropriate feedback
        if evaluation["passed"]:
            evaluation["feedback"] = self._generate_success_feedback(evaluation["score"])
            evaluation["next_step_id"] = self.next_steps.get("success")
        else:
            evaluation["feedback"] = self._generate_encouragement_feedback(evaluation["score"])
            evaluation["next_step_id"] = self.next_steps.get("needs_help")
        
        return evaluation
    
    def _generate_success_feedback(self, score: float) -> str:
        """Generate encouraging success feedback appropriate for children"""
        if score >= 0.9:
            return "🌟 Amazing work! You really understand this! Keep up the great job!"
        elif score >= 0.7:
            return "🎉 Great job! You're doing really well! Let's keep learning!"
        else:
            return "✅ Good work! You passed! There's always more to discover!"
    
    def _generate_encouragement_feedback(self, score: float) -> str:
        """Generate encouraging feedback for incorrect or incomplete answers"""
        if score >= 0.4:
            return "🌱 You're on the right track! Let's try looking at this another way."
        elif score >= 0.2:
            return "💪 Good effort! Learning takes practice. Let's explore this together!"
        else:
            return "🤗 It's okay! Everyone learns at their own pace. Let me help you understand this better."


@dataclass
class PromptChain:
    """
    A sequence of prompts that guide a learner through a concept.
    
    Implements the prompt chaining pattern for scaffolded learning,
    with adaptive pathways based on learner responses.
    """
    id: str
    name: str
    description: str
    subject: str
    target_age: tuple = (6, 12)
    steps: List[ChainStep] = field(default_factory=list)
    current_step_index: int = 0
    completed_steps: List[str] = field(default_factory=list)
    learner_context: Dict[str, Any] = field(default_factory=dict)
    
    def add_step(self, step: ChainStep):
        """Add a step to the chain"""
        self.steps.append(step)
    
    def get_current_step(self) -> Optional[ChainStep]:
        """Get the current step in the chain"""
        if 0 <= self.current_step_index < len(self.steps):
            return self.steps[self.current_step_index]
        return None
    
    def get_step_by_id(self, step_id: str) -> Optional[ChainStep]:
        """Find a step by its ID"""
        for step in self.steps:
            if step.id == step_id:
                return step
        return None
    
    def advance_to_step(self, step_id: str) -> bool:
        """
        Move to a specific step in the chain.
        
        Args:
            step_id: The ID of the step to move to
            
        Returns:
            True if successful, False if step not found
        """
        for i, step in enumerate(self.steps):
            if step.id == step_id:
                self.current_step_index = i
                return True
        return False
    
    def process_response(self, response: str) -> Dict[str, Any]:
        """
        Process a learner's response to the current step.
        
        Args:
            response: The learner's response
            
        Returns:
            Processing result including evaluation and next step info
        """
        current_step = self.get_current_step()
        if not current_step:
            return {"error": "No current step available"}
        
        # Evaluate the response
        evaluation = current_step.evaluate_response(response, self.learner_context)
        
        # Mark step as completed if passed
        if evaluation["passed"] and current_step.id not in self.completed_steps:
            self.completed_steps.append(current_step.id)
        
        # Navigate to next step if recommended
        if evaluation["next_step_id"]:
            self.advance_to_step(evaluation["next_step_id"])
        elif evaluation["passed"]:
            # Move to next sequential step if no specific next step
            self.current_step_index += 1
        
        return {
            "evaluation": evaluation,
            "chain_progress": self.get_progress(),
            "next_step": self.get_current_step()
        }
    
    def get_progress(self) -> Dict[str, Any]:
        """Get the learner's progress through the chain"""
        return {
            "chain_id": self.id,
            "chain_name": self.name,
            "total_steps": len(self.steps),
            "completed_steps": len(self.completed_steps),
            "current_step_index": self.current_step_index,
            "completion_percentage": (len(self.completed_steps) / len(self.steps) * 100) if self.steps else 0,
            "is_complete": len(self.completed_steps) == len(self.steps)
        }
    
    def reset(self):
        """Reset the chain to the beginning"""
        self.current_step_index = 0
        self.completed_steps = []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the chain to a dictionary for serialization"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "subject": self.subject,
            "target_age": self.target_age,
            "current_step_index": self.current_step_index,
            "completed_steps": self.completed_steps,
            "progress": self.get_progress()
        }


def create_sample_math_chain() -> PromptChain:
    """
    Create a sample prompt chain for teaching basic addition.
    
    This demonstrates how prompt chains scaffold learning for children.
    """
    chain = PromptChain(
        id="math_addition_basics",
        name="Addition Adventure",
        description="Learn the basics of adding numbers together!",
        subject="math",
        target_age=(6, 8)
    )
    
    # Step 1: Introduction
    chain.add_step(ChainStep(
        id="intro",
        step_type=ChainStepType.INTRODUCTION,
        prompt_template="""
🎈 Welcome to Addition Adventure, {learner_name}!

Today we're going to learn about ADDING numbers together.
When we add, we put things together to make more!

🍎 + 🍎 = 🍎🍎

Can you tell me: What does it mean to add things together?
        """,
        success_criteria={
            "keywords": ["together", "more", "combine", "plus"],
            "min_length": 10,
            "pass_threshold": 0.5
        },
        next_steps={
            "success": "example_1",
            "needs_help": "intro_help"
        }
    ))
    
    # Step 2: First Example
    chain.add_step(ChainStep(
        id="example_1",
        step_type=ChainStepType.EXAMPLE,
        prompt_template="""
🌟 Great thinking, {learner_name}!

Let's look at an example:
If you have 2 apples 🍎🍎 and I give you 1 more apple 🍎,
how many apples do you have now?

2 + 1 = ?

Can you count them and tell me the answer?
        """,
        success_criteria={
            "keywords": ["3", "three"],
            "pass_threshold": 0.6
        },
        next_steps={
            "success": "practice_1",
            "needs_help": "example_help"
        }
    ))
    
    # Step 3: Practice
    chain.add_step(ChainStep(
        id="practice_1",
        step_type=ChainStepType.PRACTICE,
        prompt_template="""
🎯 You're doing great, {learner_name}!

Now try this one:
3 + 2 = ?

You can use your fingers or draw dots to help you count!
        """,
        success_criteria={
            "keywords": ["5", "five"],
            "pass_threshold": 0.6
        },
        next_steps={
            "success": "reflection",
            "needs_help": "practice_help"
        }
    ))
    
    # Step 4: Reflection
    chain.add_step(ChainStep(
        id="reflection",
        step_type=ChainStepType.REFLECTION,
        prompt_template="""
🏆 Amazing work, {learner_name}! You've learned about addition!

Let's think about what we learned:
- Adding means putting numbers together
- We can use objects or fingers to help us count
- 2 + 1 = 3 and 3 + 2 = 5

What was your favorite part of learning about addition today?
        """,
        success_criteria={
            "min_length": 5,
            "pass_threshold": 0.3
        },
        next_steps={}
    ))
    
    return chain


if __name__ == "__main__":
    # Demo the prompt chain
    chain = create_sample_math_chain()
    chain.learner_context = {"learner_name": "Alex"}
    
    print("=== Addition Adventure Demo ===\n")
    
    current = chain.get_current_step()
    if current:
        print(current.generate_prompt(chain.learner_context))
        print("\n--- Simulating response: 'Adding means putting things together!' ---\n")
        
        result = chain.process_response("Adding means putting things together!")
        print(f"Feedback: {result['evaluation']['feedback']}")
        print(f"Progress: {result['chain_progress']['completion_percentage']:.0f}%")
