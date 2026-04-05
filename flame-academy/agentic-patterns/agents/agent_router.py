"""
Agent Router for Educational Task Distribution

Routes learning tasks to the appropriate specialized educational agent
based on subject matter, task type, and learner context.
Implements the routing pattern from agentic design.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Type
from datetime import datetime
from enum import Enum

from .base_educational_agent import BaseEducationalAgent, AgentResponse, LearnerContext


class TaskType(Enum):
    """Types of educational tasks"""
    LESSON = "lesson"           # Learn a new concept
    PRACTICE = "practice"       # Practice existing skills
    QUIZ = "quiz"               # Assessment
    HELP = "help"               # Get help with a problem
    EXPLORE = "explore"         # Open exploration
    STORY = "story"             # Story-based learning
    GAME = "game"               # Game-based learning
    QUESTION = "question"       # Answer a question


@dataclass
class RoutingDecision:
    """
    Represents a routing decision made by the router.
    
    Captures the reasoning and confidence behind agent selection.
    """
    task_id: str
    task_type: TaskType
    selected_agent_id: str
    confidence: float  # 0.0 to 1.0
    reasoning: str
    alternative_agents: List[str] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "task_id": self.task_id,
            "task_type": self.task_type.value,
            "selected_agent": self.selected_agent_id,
            "confidence": self.confidence,
            "reasoning": self.reasoning,
            "alternatives": self.alternative_agents,
            "timestamp": self.timestamp
        }


class AgentRouter:
    """
    Routes educational tasks to appropriate specialized agents.
    
    Implements intelligent routing based on:
    - Task subject matter
    - Task type (lesson, practice, etc.)
    - Learner preferences and history
    - Agent capabilities and availability
    """
    
    def __init__(self):
        """Initialize the agent router"""
        self.agents: Dict[str, BaseEducationalAgent] = {}
        self.routing_history: List[RoutingDecision] = []
        self.subject_mappings: Dict[str, List[str]] = {}
        self._task_counter = 0
    
    def register_agent(self, agent: BaseEducationalAgent):
        """
        Register an educational agent with the router.
        
        Args:
            agent: Agent to register
        """
        self.agents[agent.agent_id] = agent
        
        # Update subject mappings
        if agent.subject not in self.subject_mappings:
            self.subject_mappings[agent.subject] = []
        self.subject_mappings[agent.subject].append(agent.agent_id)
    
    def unregister_agent(self, agent_id: str):
        """Remove an agent from the router"""
        if agent_id in self.agents:
            agent = self.agents[agent_id]
            del self.agents[agent_id]
            
            # Clean up subject mappings
            if agent.subject in self.subject_mappings:
                if agent_id in self.subject_mappings[agent.subject]:
                    self.subject_mappings[agent.subject].remove(agent_id)
    
    def route_task(
        self,
        task: str,
        task_type: TaskType,
        context: LearnerContext,
        preferred_agent: Optional[str] = None
    ) -> AgentResponse:
        """
        Route a task to the appropriate agent and get a response.
        
        Args:
            task: The task or query to process
            task_type: Type of educational task
            context: Learner context
            preferred_agent: Optional preferred agent ID
            
        Returns:
            Response from the selected agent
        """
        # Make routing decision
        decision = self._make_routing_decision(task, task_type, context, preferred_agent)
        self.routing_history.append(decision)
        
        # Get the selected agent
        agent = self.agents.get(decision.selected_agent_id)
        if not agent:
            return self._create_fallback_response(task, context)
        
        # Route to appropriate handler based on task type
        if task_type == TaskType.LESSON:
            return agent.generate_lesson(task, context)
        elif task_type == TaskType.PRACTICE:
            return agent.generate_practice(task, context)
        elif task_type == TaskType.STORY:
            if hasattr(agent, 'generate_story'):
                return agent.generate_story(task, context)
            return agent.process_request(task, context)
        else:
            return agent.process_request(task, context)
    
    def _make_routing_decision(
        self,
        task: str,
        task_type: TaskType,
        context: LearnerContext,
        preferred_agent: Optional[str] = None
    ) -> RoutingDecision:
        """
        Make a routing decision based on task and context.
        
        Args:
            task: The task to route
            task_type: Type of task
            context: Learner context
            preferred_agent: Optional preferred agent
            
        Returns:
            Routing decision
        """
        self._task_counter += 1
        task_id = f"task_{self._task_counter}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # If preferred agent is specified and available, use it
        if preferred_agent and preferred_agent in self.agents:
            return RoutingDecision(
                task_id=task_id,
                task_type=task_type,
                selected_agent_id=preferred_agent,
                confidence=1.0,
                reasoning="Preferred agent selected by request",
                alternative_agents=[]
            )
        
        # Score each agent for this task
        agent_scores = []
        for agent_id, agent in self.agents.items():
            score, reasons = self._score_agent_for_task(agent, task, task_type, context)
            agent_scores.append((agent_id, score, reasons))
        
        # Sort by score descending
        agent_scores.sort(key=lambda x: x[1], reverse=True)
        
        if not agent_scores:
            # No agents available
            return RoutingDecision(
                task_id=task_id,
                task_type=task_type,
                selected_agent_id="none",
                confidence=0.0,
                reasoning="No agents available",
                alternative_agents=[]
            )
        
        # Select the best agent
        best_agent_id, best_score, best_reasons = agent_scores[0]
        alternatives = [aid for aid, score, _ in agent_scores[1:3] if score > 0.3]
        
        return RoutingDecision(
            task_id=task_id,
            task_type=task_type,
            selected_agent_id=best_agent_id,
            confidence=best_score,
            reasoning="; ".join(best_reasons),
            alternative_agents=alternatives
        )
    
    def _score_agent_for_task(
        self,
        agent: BaseEducationalAgent,
        task: str,
        task_type: TaskType,
        context: LearnerContext
    ) -> tuple:
        """
        Score how well an agent matches a task.
        
        Returns:
            Tuple of (score, list of reasons)
        """
        score = 0.0
        reasons = []
        
        # Check age appropriateness
        if agent.is_appropriate_for_age(context.age):
            score += 0.2
            reasons.append(f"Age-appropriate ({context.age} years)")
        else:
            score -= 0.5
            reasons.append("Age mismatch")
        
        # Check topic match
        if agent.can_handle_topic(task):
            score += 0.4
            reasons.append(f"Topic match: {task}")
        
        # Check subject match from context
        if context.current_topic:
            topic_lower = context.current_topic.lower()
            if agent.subject.lower() in topic_lower or topic_lower in agent.subject.lower():
                score += 0.2
                reasons.append(f"Subject match: {agent.subject}")
        
        # Check for keyword matches in task
        task_lower = task.lower()
        
        # Subject-specific keywords
        keyword_scores = {
            "math": ["math", "number", "add", "subtract", "multiply", "divide", "count", "calculate"],
            "reading": ["story", "read", "write", "book", "character", "tale"],
            "stem": ["science", "experiment", "plant", "animal", "space", "build", "engineer"]
        }
        
        for subject, keywords in keyword_scores.items():
            if agent.subject.lower() == subject:
                if any(kw in task_lower for kw in keywords):
                    score += 0.3
                    reasons.append(f"Keyword match for {subject}")
                    break
        
        # Check task type compatibility with capabilities
        task_capability_map = {
            TaskType.LESSON: "teach",
            TaskType.PRACTICE: "practice",
            TaskType.QUIZ: "assess",
            TaskType.STORY: "storytell",
            TaskType.GAME: "gamify"
        }
        
        required_capability = task_capability_map.get(task_type)
        if required_capability:
            if any(cap.value == required_capability for cap in agent.capabilities):
                score += 0.2
                reasons.append(f"Has {required_capability} capability")
        
        # Learner interest matching
        for interest in context.interests:
            if agent.can_handle_topic(interest):
                score += 0.1
                reasons.append(f"Matches interest: {interest}")
                break
        
        return (max(0.0, min(1.0, score)), reasons)
    
    def _create_fallback_response(self, task: str, context: LearnerContext) -> AgentResponse:
        """Create a fallback response when no agent is available"""
        from .base_educational_agent import ResponseType
        
        return AgentResponse(
            agent_id="router",
            response_type=ResponseType.FEEDBACK,
            content=f"""
😊 Hi {context.name}!

I'm looking for the best helper for your question about {task}, 
but I don't have a specialized agent available right now.

**What you can try:**
- Ask about math, reading, or science topics
- Try a different way of asking your question
- Check back later when more helpers are available

I'm still learning and growing!
""",
            requires_input=True,
            input_prompt="Would you like to try a different topic?"
        )
    
    def get_available_agents(self) -> List[Dict[str, Any]]:
        """Get information about all available agents"""
        return [agent.get_agent_info() for agent in self.agents.values()]
    
    def get_agent_for_subject(self, subject: str) -> Optional[BaseEducationalAgent]:
        """Get an agent for a specific subject"""
        agent_ids = self.subject_mappings.get(subject.lower(), [])
        if agent_ids:
            return self.agents.get(agent_ids[0])
        
        # Try partial match
        for subj, ids in self.subject_mappings.items():
            if subject.lower() in subj or subj in subject.lower():
                return self.agents.get(ids[0])
        
        return None
    
    def get_best_agent_for_task(self, task: str, context: LearnerContext) -> Optional[BaseEducationalAgent]:
        """Get the best agent for a specific task without executing it"""
        decision = self._make_routing_decision(task, TaskType.EXPLORE, context, None)
        return self.agents.get(decision.selected_agent_id)
    
    def get_routing_stats(self) -> Dict[str, Any]:
        """Get statistics about routing decisions"""
        if not self.routing_history:
            return {"total_routings": 0}
        
        agent_counts = {}
        type_counts = {}
        total_confidence = 0.0
        
        for decision in self.routing_history:
            # Count by agent
            agent_counts[decision.selected_agent_id] = agent_counts.get(decision.selected_agent_id, 0) + 1
            
            # Count by task type
            type_name = decision.task_type.value
            type_counts[type_name] = type_counts.get(type_name, 0) + 1
            
            total_confidence += decision.confidence
        
        return {
            "total_routings": len(self.routing_history),
            "routings_by_agent": agent_counts,
            "routings_by_type": type_counts,
            "average_confidence": total_confidence / len(self.routing_history),
            "registered_agents": len(self.agents)
        }
    
    def clear_history(self):
        """Clear routing history"""
        self.routing_history = []


def create_default_router() -> AgentRouter:
    """
    Create a router with all default educational agents registered.
    
    Returns:
        Configured AgentRouter with STEM, Storytelling, and Math agents
    """
    from .stem_agent import STEMAgent
    from .storytelling_agent import StorytellingAgent
    from .math_agent import MathAgent
    
    router = AgentRouter()
    
    # Register default agents
    router.register_agent(STEMAgent())
    router.register_agent(StorytellingAgent())
    router.register_agent(MathAgent())
    
    return router


if __name__ == "__main__":
    # Demo the agent router
    from .stem_agent import STEMAgent
    from .storytelling_agent import StorytellingAgent
    from .math_agent import MathAgent
    
    # Create router and register agents
    router = AgentRouter()
    router.register_agent(STEMAgent())
    router.register_agent(StorytellingAgent())
    router.register_agent(MathAgent())
    
    # Create test context
    context = LearnerContext(
        learner_id="student_001",
        name="Alex",
        age=8,
        learning_style="visual",
        interests=["dinosaurs", "space"]
    )
    
    print("=== Agent Router Demo ===\n")
    print(f"Registered Agents: {len(router.agents)}")
    for agent in router.get_available_agents():
        print(f"  - {agent['name']} ({agent['subject']})")
    
    # Test routing different tasks
    test_tasks = [
        ("I want to learn addition", TaskType.LESSON),
        ("Tell me a story about dragons", TaskType.STORY),
        ("How do plants grow?", TaskType.LESSON),
        ("Practice multiplication", TaskType.PRACTICE)
    ]
    
    print("\n--- Routing Tests ---")
    for task, task_type in test_tasks:
        response = router.route_task(task, task_type, context)
        print(f"\nTask: '{task}'")
        print(f"Routed to: {response.agent_id}")
        print(f"Response type: {response.response_type.value}")
    
    # Show stats
    print("\n--- Routing Statistics ---")
    stats = router.get_routing_stats()
    print(f"Total Routings: {stats['total_routings']}")
    print(f"Average Confidence: {stats['average_confidence']:.2f}")
    print(f"By Agent: {stats['routings_by_agent']}")
