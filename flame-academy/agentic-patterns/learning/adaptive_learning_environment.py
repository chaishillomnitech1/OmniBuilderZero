"""
Adaptive Learning Environment

This module combines all agentic design patterns to create a comprehensive
adaptive learning environment for children. It integrates:
- Prompt chaining for scaffolded learning
- Memory management for personalization
- Goal setting for motivation
- Knowledge retrieval for content delivery
- Multi-agent orchestration for comprehensive education
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Tuple
from datetime import datetime
from enum import Enum
import json
import sys
import os
import random

# Handle imports for both package and standalone usage
try:
    from ..core.prompt_chaining import PromptChain, ChainStep
    from ..core.memory_management import MemoryManager, LearnerMemory, LearnerProfile, LearningStyle
    from ..core.goal_setting import GoalSetter, LearningGoal, GoalType
    from ..core.knowledge_retrieval import KnowledgeRetriever, RetrievalContext, DifficultyLevel, LearningModality
    from ..agents.base_educational_agent import LearnerContext, AgentResponse, ResponseType
    from ..agents.agent_router import AgentRouter, TaskType, create_default_router
    from ..orchestration.multi_agent_orchestrator import MultiAgentOrchestrator, OrchestrationMode
except ImportError:
    # Add parent directory to path for standalone execution
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from core.prompt_chaining import PromptChain, ChainStep
    from core.memory_management import MemoryManager, LearnerMemory, LearnerProfile, LearningStyle
    from core.goal_setting import GoalSetter, LearningGoal, GoalType
    from core.knowledge_retrieval import KnowledgeRetriever, RetrievalContext, DifficultyLevel, LearningModality
    from agents.base_educational_agent import LearnerContext, AgentResponse, ResponseType
    from agents.agent_router import AgentRouter, TaskType, create_default_router
    from orchestration.multi_agent_orchestrator import MultiAgentOrchestrator, OrchestrationMode


class LearnerMood(Enum):
    """Detected or reported learner mood"""
    EXCITED = "excited"
    HAPPY = "happy"
    NEUTRAL = "neutral"
    FRUSTRATED = "frustrated"
    TIRED = "tired"
    CONFUSED = "confused"


@dataclass
class LearnerState:
    """
    Current state of a learner in the environment.
    
    Captures everything needed to provide adaptive, personalized learning.
    """
    learner_id: str
    name: str
    age: int
    current_subject: Optional[str] = None
    current_topic: Optional[str] = None
    mood: LearnerMood = LearnerMood.NEUTRAL
    energy_level: float = 1.0  # 0.0 to 1.0
    attention_span_remaining: int = 15  # minutes
    session_start: str = field(default_factory=lambda: datetime.now().isoformat())
    interactions_this_session: int = 0
    correct_answers_this_session: int = 0
    needs_break: bool = False
    last_response_time: Optional[str] = None
    
    @property
    def session_duration_minutes(self) -> int:
        """Calculate current session duration in minutes"""
        start = datetime.fromisoformat(self.session_start)
        return int((datetime.now() - start).total_seconds() / 60)
    
    @property
    def performance_ratio(self) -> float:
        """Calculate performance ratio for this session"""
        if self.interactions_this_session == 0:
            return 0.5
        return self.correct_answers_this_session / self.interactions_this_session
    
    def record_interaction(self, correct: bool):
        """Record an interaction"""
        self.interactions_this_session += 1
        if correct:
            self.correct_answers_this_session += 1
        self.last_response_time = datetime.now().isoformat()
    
    def check_break_needed(self) -> bool:
        """Check if learner needs a break"""
        # Check session duration
        if self.session_duration_minutes > 20:
            self.needs_break = True
        
        # Check energy level
        if self.energy_level < 0.3:
            self.needs_break = True
        
        # Check frustration
        if self.mood == LearnerMood.FRUSTRATED:
            self.needs_break = True
        
        return self.needs_break


class AdaptiveLearningEnvironment:
    """
    A comprehensive adaptive learning environment that combines all
    agentic design patterns to provide personalized education for children.
    
    This is the main entry point for the ScrollVerse educational system,
    integrating:
    - Memory management for learner profiles and progress
    - Goal setting for motivation and tracking
    - Knowledge retrieval for content
    - Multi-agent orchestration for diverse learning
    - Adaptive difficulty adjustment
    - Break and wellness management
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the adaptive learning environment.
        
        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
        
        # Initialize all components
        self.memory_manager = MemoryManager()
        self.goal_setter = GoalSetter()
        self.knowledge_retriever = KnowledgeRetriever()
        self.orchestrator = MultiAgentOrchestrator()
        
        # Active learner states
        self.active_learners: Dict[str, LearnerState] = {}
        
        # Session history for analytics
        self.session_history: List[Dict[str, Any]] = []
    
    def start_session(
        self,
        learner_id: str,
        name: str,
        age: int,
        interests: Optional[List[str]] = None,
        learning_style: LearningStyle = LearningStyle.VISUAL
    ) -> Dict[str, Any]:
        """
        Start a new learning session for a learner.
        
        Args:
            learner_id: Unique learner identifier
            name: Learner's name
            age: Learner's age
            interests: List of interests
            learning_style: Preferred learning style
            
        Returns:
            Session start information with welcome message
        """
        # Get or create learner memory
        memory = self.memory_manager.get_or_create_learner(
            learner_id=learner_id,
            name=name,
            age=age,
            interests=interests or [],
            learning_style=learning_style
        )
        
        # Start a learning session in memory
        memory.start_session("general")
        
        # Create learner state
        state = LearnerState(
            learner_id=learner_id,
            name=name,
            age=age,
            attention_span_remaining=self._calculate_attention_span(age)
        )
        self.active_learners[learner_id] = state
        
        # Generate welcome message
        welcome = self._generate_welcome_message(memory, state)
        
        # Get suggested goals
        suggested_goals = self.goal_setter.get_suggested_goals(learner_id)
        
        return {
            "session_started": True,
            "learner_id": learner_id,
            "welcome_message": welcome,
            "learner_stats": memory.get_learning_stats(),
            "suggested_goals": suggested_goals[:3],
            "available_subjects": self.knowledge_retriever.get_subjects()
        }
    
    def end_session(self, learner_id: str) -> Dict[str, Any]:
        """
        End a learning session.
        
        Args:
            learner_id: Learner identifier
            
        Returns:
            Session summary
        """
        if learner_id not in self.active_learners:
            return {"error": "No active session found"}
        
        state = self.active_learners[learner_id]
        memory = self.memory_manager.get_learner(learner_id)
        
        # End session in memory
        if memory:
            memory.end_current_session()
        
        # Generate session summary
        summary = self._generate_session_summary(state, memory)
        
        # Store in history
        self.session_history.append({
            "learner_id": learner_id,
            "duration_minutes": state.session_duration_minutes,
            "interactions": state.interactions_this_session,
            "performance": state.performance_ratio,
            "ended_at": datetime.now().isoformat()
        })
        
        # Remove active state
        del self.active_learners[learner_id]
        
        return summary
    
    def learn(
        self,
        learner_id: str,
        topic: str,
        task_type: TaskType = TaskType.LESSON
    ) -> AgentResponse:
        """
        Request a learning experience on a topic.
        
        Args:
            learner_id: Learner identifier
            topic: Topic to learn
            task_type: Type of learning activity
            
        Returns:
            Agent response with learning content
        """
        state = self.active_learners.get(learner_id)
        if not state:
            return self._error_response("No active session. Please start a session first.")
        
        memory = self.memory_manager.get_learner(learner_id)
        
        # Check if break is needed
        if state.check_break_needed():
            return self._generate_break_suggestion(state)
        
        # Update state
        state.current_topic = topic
        
        # Create learner context
        context = self._create_learner_context(state, memory)
        
        # Route to appropriate agent
        response = self.orchestrator.router.route_task(
            task=topic,
            task_type=task_type,
            context=context
        )
        
        # Record interaction
        state.record_interaction(True)  # Accessing content counts as correct
        
        # Update topic in memory
        if memory:
            memory.set_context("current_topic", topic)
        
        return response
    
    def answer(
        self,
        learner_id: str,
        response: str
    ) -> AgentResponse:
        """
        Process a learner's answer or response.
        
        Args:
            learner_id: Learner identifier
            response: Learner's response text
            
        Returns:
            Feedback and next steps
        """
        state = self.active_learners.get(learner_id)
        if not state:
            return self._error_response("No active session.")
        
        memory = self.memory_manager.get_learner(learner_id)
        context = self._create_learner_context(state, memory)
        
        # For now, provide encouraging feedback
        # In a full implementation, this would evaluate the answer
        is_correct = len(response.strip()) > 0  # Simple check
        
        state.record_interaction(is_correct)
        
        if is_correct:
            if memory:
                memory.record_concept_practice(
                    concept_id=state.current_topic or "general",
                    concept_name=state.current_topic or "General",
                    subject=state.current_subject or "general",
                    success=True
                )
            
            content = f"""
🌟 **Great job, {state.name}!**

Thank you for your thoughtful response!

{self._get_encouragement(state)}

**What would you like to do next?**
- Learn more about {state.current_topic}
- Try a practice problem
- Explore a new topic
"""
        else:
            content = f"""
💡 **Keep going, {state.name}!**

Every effort helps you learn!

{self._get_encouragement(state)}

Would you like to try again or get some help?
"""
        
        return AgentResponse(
            agent_id="environment",
            response_type=ResponseType.FEEDBACK,
            content=content,
            requires_input=True,
            input_prompt="What would you like to do?",
            suggestions=["Continue learning", "Practice more", "Try something new"]
        )
    
    def set_goal(
        self,
        learner_id: str,
        template_name: str
    ) -> Dict[str, Any]:
        """
        Set a learning goal for the learner.
        
        Args:
            learner_id: Learner identifier
            template_name: Name of goal template
            
        Returns:
            Created goal information
        """
        goal = self.goal_setter.create_goal_from_template(learner_id, template_name)
        if not goal:
            return {"error": "Goal template not found"}
        
        return {
            "goal_created": True,
            "goal": goal.to_dict(),
            "message": f"🎯 New goal set: {goal.title}!"
        }
    
    def update_goal_progress(
        self,
        learner_id: str,
        goal_id: str,
        progress: float
    ) -> Dict[str, Any]:
        """
        Update progress on a learning goal.
        
        Args:
            learner_id: Learner identifier
            goal_id: Goal identifier
            progress: New progress value
            
        Returns:
            Update result with any celebrations
        """
        result = self.goal_setter.update_goal_progress(goal_id, learner_id, progress)
        return result or {"error": "Goal not found"}
    
    def get_recommendations(
        self,
        learner_id: str,
        subject: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get personalized learning recommendations.
        
        Args:
            learner_id: Learner identifier
            subject: Optional subject filter
            
        Returns:
            Personalized recommendations
        """
        state = self.active_learners.get(learner_id)
        memory = self.memory_manager.get_learner(learner_id)
        
        if not memory:
            return {"error": "Learner not found"}
        
        # Get retrieval context
        retrieval_context = RetrievalContext(
            learner_id=learner_id,
            learner_age=memory.profile.age,
            current_subject=subject or "general",
            difficulty_level=self._determine_difficulty(memory),
            preferred_modalities=[self._style_to_modality(memory.profile.learning_style)],
            completed_items=list(memory.concept_mastery.keys()),
            interests=memory.profile.interests
        )
        
        # Get recommended content
        recommended_items = self.knowledge_retriever.retrieve_for_context(retrieval_context, limit=5)
        
        # Get concepts needing review
        review_concepts = memory.get_recommended_concepts(subject, limit=3)
        
        # Get suggested goals
        suggested_goals = self.goal_setter.get_suggested_goals(learner_id, subject)
        
        return {
            "learner": memory.profile.name,
            "recommended_content": [item.to_dict() for item in recommended_items],
            "needs_review": [c.concept_name for c in review_concepts],
            "suggested_goals": suggested_goals,
            "current_mastery": memory.get_mastery_summary(subject)
        }
    
    def start_learning_journey(
        self,
        learner_id: str,
        name: str,
        topics: List[str],
        mode: OrchestrationMode = OrchestrationMode.SEQUENTIAL
    ) -> Dict[str, Any]:
        """
        Start a multi-topic learning journey.
        
        Args:
            learner_id: Learner identifier
            name: Journey name
            topics: List of topics to cover
            mode: Orchestration mode
            
        Returns:
            Journey information
        """
        state = self.active_learners.get(learner_id)
        if not state:
            return {"error": "No active session"}
        
        memory = self.memory_manager.get_learner(learner_id)
        context = self._create_learner_context(state, memory)
        
        plan = self.orchestrator.create_learning_journey(
            name=name,
            topics=topics,
            context=context,
            mode=mode
        )
        
        return {
            "journey_created": True,
            "plan_id": plan.id,
            "name": plan.name,
            "topics": topics,
            "tasks_count": len(plan.tasks)
        }
    
    def continue_journey(self, learner_id: str, plan_id: str) -> Optional[AgentResponse]:
        """
        Continue to the next step in a learning journey.
        
        Args:
            learner_id: Learner identifier
            plan_id: Plan identifier
            
        Returns:
            Next step response or None if complete
        """
        state = self.active_learners.get(learner_id)
        if not state:
            return None
        
        memory = self.memory_manager.get_learner(learner_id)
        context = self._create_learner_context(state, memory)
        
        return self.orchestrator.execute_next_step(plan_id, context)
    
    def update_mood(self, learner_id: str, mood: LearnerMood):
        """Update learner's reported mood"""
        state = self.active_learners.get(learner_id)
        if state:
            state.mood = mood
    
    def _calculate_attention_span(self, age: int) -> int:
        """Calculate expected attention span based on age"""
        # Rule of thumb: age + 2-3 minutes, capped
        base_span = age + 2
        return min(base_span, 25)  # Cap at 25 minutes
    
    def _determine_difficulty(self, memory: LearnerMemory) -> DifficultyLevel:
        """Determine appropriate difficulty level"""
        mastery = memory.get_mastery_summary()
        avg = mastery.get("average_mastery", 0.5)
        
        if avg < 0.4:
            return DifficultyLevel.BEGINNER
        elif avg < 0.7:
            return DifficultyLevel.ELEMENTARY
        elif avg < 0.9:
            return DifficultyLevel.INTERMEDIATE
        else:
            return DifficultyLevel.ADVANCED
    
    def _style_to_modality(self, style: LearningStyle):
        """Convert learning style to modality"""
        mapping = {
            LearningStyle.VISUAL: LearningModality.VISUAL,
            LearningStyle.AUDITORY: LearningModality.AUDITORY,
            LearningStyle.KINESTHETIC: LearningModality.KINESTHETIC,
            LearningStyle.READING: LearningModality.READING
        }
        return mapping.get(style, LearningModality.MULTIMODAL)
    
    def _create_learner_context(
        self,
        state: LearnerState,
        memory: Optional[LearnerMemory]
    ) -> LearnerContext:
        """Create a learner context from state and memory"""
        return LearnerContext(
            learner_id=state.learner_id,
            name=state.name,
            age=state.age,
            learning_style=memory.profile.learning_style.value if memory else "visual",
            interests=memory.profile.interests if memory else [],
            current_topic=state.current_topic,
            mastery_level=memory.get_mastery_summary().get("average_mastery", 0.5) if memory else 0.5,
            mood=state.mood.value,
            session_duration=state.session_duration_minutes,
            recent_performance=[state.performance_ratio] if state.interactions_this_session > 0 else []
        )
    
    def _generate_welcome_message(
        self,
        memory: LearnerMemory,
        state: LearnerState
    ) -> str:
        """Generate a personalized welcome message"""
        stats = memory.get_learning_stats()
        
        if stats["total_sessions"] == 1:
            # First time user
            return f"""
🌟 **Welcome to ScrollVerse Academy, {state.name}!**

I'm so excited to meet you! This is your first time here, 
and we're going to have so much fun learning together!

**What you can do here:**
- 📚 Learn about math, science, stories, and more!
- 🎯 Set goals and earn achievements
- 🎮 Play learning games
- 🚀 Go on learning adventures

What would you like to explore first?
"""
        else:
            # Returning user
            streak_msg = f"🔥 You're on a {stats['current_streak']} day streak!" if stats['current_streak'] > 1 else ""
            
            return f"""
🎉 **Welcome back, {state.name}!**

Great to see you again! {streak_msg}

**Your Progress:**
- 📊 Total learning time: {stats['total_learning_minutes']} minutes
- 🏆 Achievements: {stats['achievements_count']}
- 📈 Average mastery: {stats['mastery_summary']['average_mastery']:.0%}

Ready to continue your learning journey?
"""
    
    def _generate_session_summary(
        self,
        state: LearnerState,
        memory: Optional[LearnerMemory]
    ) -> Dict[str, Any]:
        """Generate a session summary"""
        summary_message = f"""
🌙 **Great session, {state.name}!**

**Today's Learning:**
- ⏱️ Time learning: {state.session_duration_minutes} minutes
- 💡 Interactions: {state.interactions_this_session}
- ✅ Performance: {state.performance_ratio:.0%}

{"🌟 Amazing work! Keep up the great effort!" if state.performance_ratio > 0.7 else "Every bit of practice makes you stronger! See you next time!"}

Come back soon to continue your learning adventure!
"""
        
        return {
            "session_ended": True,
            "duration_minutes": state.session_duration_minutes,
            "interactions": state.interactions_this_session,
            "performance_ratio": state.performance_ratio,
            "summary_message": summary_message
        }
    
    def _generate_break_suggestion(self, state: LearnerState) -> AgentResponse:
        """Generate a break suggestion"""
        return AgentResponse(
            agent_id="environment",
            response_type=ResponseType.FEEDBACK,
            content=f"""
🌈 **Break Time, {state.name}!**

You've been learning so well! Your brain needs a little rest.

**Fun Break Ideas:**
- 🚶 Take a short walk
- 💧 Get a drink of water
- 🧘 Do some stretches
- 🎵 Listen to your favorite song

Come back in a few minutes when you're ready to continue!
You're doing amazing! 💪
""",
            requires_input=True,
            input_prompt="Type 'ready' when you want to continue!",
            suggestions=["I'm ready!", "End session"]
        )
    
    def _get_encouragement(self, state: LearnerState) -> str:
        """Get context-appropriate encouragement"""
        if state.performance_ratio > 0.8:
            messages = [
                "You're on fire! 🔥",
                "You're crushing it! 💪",
                "Super star learner! ⭐"
            ]
        elif state.performance_ratio > 0.5:
            messages = [
                "Keep going, you're doing great!",
                "Nice work! Every step counts!",
                "You're making progress! 🌱"
            ]
        else:
            messages = [
                "Don't give up! You've got this!",
                "Every mistake is a chance to learn!",
                "I believe in you! 💖"
            ]
        
        return random.choice(messages)
    
    def _error_response(self, message: str) -> AgentResponse:
        """Create an error response"""
        return AgentResponse(
            agent_id="environment",
            response_type=ResponseType.FEEDBACK,
            content=f"❌ {message}",
            requires_input=False
        )
    
    def get_environment_stats(self) -> Dict[str, Any]:
        """Get overall environment statistics"""
        return {
            "active_learners": len(self.active_learners),
            "total_sessions": len(self.session_history),
            "registered_learners": len(self.memory_manager.learner_memories),
            "available_subjects": self.knowledge_retriever.get_subjects(),
            "knowledge_base_size": self.knowledge_retriever.get_stats()["total_items"],
            "orchestration_stats": self.orchestrator.get_orchestration_stats()
        }


if __name__ == "__main__":
    # Demo the adaptive learning environment
    env = AdaptiveLearningEnvironment()
    
    print("=== Adaptive Learning Environment Demo ===\n")
    
    # Start a session
    print("--- Starting Session ---")
    session = env.start_session(
        learner_id="student_001",
        name="Riley",
        age=8,
        interests=["space", "dinosaurs"],
        learning_style=LearningStyle.VISUAL
    )
    print(session["welcome_message"])
    
    # Learn something
    print("\n--- Learning About Addition ---")
    response = env.learn("student_001", "addition", TaskType.LESSON)
    print(f"Agent: {response.agent_id}")
    print(response.content[:500] + "...")
    
    # Get recommendations
    print("\n--- Getting Recommendations ---")
    recs = env.get_recommendations("student_001", "math")
    print(f"Recommended Content: {len(recs['recommended_content'])} items")
    print(f"Current Mastery: {recs['current_mastery']}")
    
    # End session
    print("\n--- Ending Session ---")
    summary = env.end_session("student_001")
    print(summary["summary_message"])
    
    # Show stats
    print("\n--- Environment Statistics ---")
    stats = env.get_environment_stats()
    print(f"Total Sessions: {stats['total_sessions']}")
    print(f"Knowledge Base: {stats['knowledge_base_size']} items")
