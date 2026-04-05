"""
Multi-Agent Orchestrator for Educational Systems

This module implements the multi-agent orchestration design pattern,
coordinating multiple specialized educational agents to provide
comprehensive learning experiences for children.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Callable
from datetime import datetime
from enum import Enum
import json
import sys
import os

# Handle imports for both package and standalone usage
try:
    from ..agents.base_educational_agent import BaseEducationalAgent, AgentResponse, LearnerContext, ResponseType
    from ..agents.agent_router import AgentRouter, TaskType, RoutingDecision, create_default_router
except ImportError:
    # Add parent directory to path for standalone execution
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from agents.base_educational_agent import BaseEducationalAgent, AgentResponse, LearnerContext, ResponseType
    from agents.agent_router import AgentRouter, TaskType, RoutingDecision, create_default_router


class TaskStatus(Enum):
    """Status of an orchestrated task"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


class OrchestrationMode(Enum):
    """Modes of multi-agent orchestration"""
    SEQUENTIAL = "sequential"      # One agent at a time
    PARALLEL = "parallel"          # Multiple agents simultaneously
    ADAPTIVE = "adaptive"          # Dynamically choose based on responses
    COLLABORATIVE = "collaborative" # Agents work together on same topic


@dataclass
class AgentTask:
    """
    A task assigned to a specific agent within an orchestration plan.
    """
    id: str
    agent_id: str
    task_description: str
    task_type: TaskType
    topic: str
    dependencies: List[str] = field(default_factory=list)  # IDs of tasks this depends on
    status: TaskStatus = TaskStatus.PENDING
    result: Optional[AgentResponse] = None
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    priority: int = 1  # Higher = more important
    
    def start(self):
        """Mark task as started"""
        self.status = TaskStatus.IN_PROGRESS
        self.started_at = datetime.now().isoformat()
    
    def complete(self, result: AgentResponse):
        """Mark task as completed with result"""
        self.status = TaskStatus.COMPLETED
        self.result = result
        self.completed_at = datetime.now().isoformat()
    
    def fail(self, error: str):
        """Mark task as failed"""
        self.status = TaskStatus.FAILED
        self.completed_at = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "agent_id": self.agent_id,
            "task": self.task_description,
            "type": self.task_type.value,
            "topic": self.topic,
            "status": self.status.value,
            "priority": self.priority
        }


@dataclass
class OrchestrationPlan:
    """
    A plan for orchestrating multiple agents on a learning journey.
    """
    id: str
    name: str
    description: str
    learner_id: str
    mode: OrchestrationMode
    tasks: List[AgentTask] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def add_task(self, task: AgentTask):
        """Add a task to the plan"""
        self.tasks.append(task)
    
    def get_ready_tasks(self) -> List[AgentTask]:
        """Get tasks that are ready to execute (dependencies met)"""
        completed_ids = {t.id for t in self.tasks if t.status == TaskStatus.COMPLETED}
        ready = []
        
        for task in self.tasks:
            if task.status != TaskStatus.PENDING:
                continue
            
            # Check if all dependencies are met
            if all(dep_id in completed_ids for dep_id in task.dependencies):
                ready.append(task)
        
        # Sort by priority
        ready.sort(key=lambda t: t.priority, reverse=True)
        return ready
    
    def is_complete(self) -> bool:
        """Check if all tasks are completed"""
        return all(t.status in [TaskStatus.COMPLETED, TaskStatus.SKIPPED] for t in self.tasks)
    
    def get_progress(self) -> Dict[str, Any]:
        """Get plan execution progress"""
        total = len(self.tasks)
        completed = sum(1 for t in self.tasks if t.status == TaskStatus.COMPLETED)
        failed = sum(1 for t in self.tasks if t.status == TaskStatus.FAILED)
        
        return {
            "plan_id": self.id,
            "total_tasks": total,
            "completed": completed,
            "failed": failed,
            "pending": total - completed - failed,
            "progress_percentage": (completed / total * 100) if total > 0 else 0,
            "is_complete": self.is_complete()
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "mode": self.mode.value,
            "tasks": [t.to_dict() for t in self.tasks],
            "progress": self.get_progress()
        }


class MultiAgentOrchestrator:
    """
    Orchestrates multiple educational agents for comprehensive learning experiences.
    
    Implements the multi-agent orchestration pattern with support for:
    - Sequential learning journeys
    - Parallel topic exploration
    - Adaptive learning paths
    - Collaborative agent interactions
    """
    
    def __init__(self, router: Optional[AgentRouter] = None):
        """
        Initialize the orchestrator.
        
        Args:
            router: Optional pre-configured router. If not provided, creates default.
        """
        self.router = router or create_default_router()
        self.active_plans: Dict[str, OrchestrationPlan] = {}
        self.completed_plans: List[OrchestrationPlan] = []
        self._plan_counter = 0
    
    def create_learning_journey(
        self,
        name: str,
        topics: List[str],
        context: LearnerContext,
        mode: OrchestrationMode = OrchestrationMode.SEQUENTIAL
    ) -> OrchestrationPlan:
        """
        Create a multi-topic learning journey.
        
        Args:
            name: Name of the journey
            topics: List of topics to cover
            context: Learner context
            mode: Orchestration mode
            
        Returns:
            Created orchestration plan
        """
        self._plan_counter += 1
        plan_id = f"plan_{self._plan_counter}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        plan = OrchestrationPlan(
            id=plan_id,
            name=name,
            description=f"Learning journey covering: {', '.join(topics)}",
            learner_id=context.learner_id,
            mode=mode,
            metadata={"topics": topics, "learner_age": context.age}
        )
        
        # Create tasks for each topic
        previous_task_id = None
        for i, topic in enumerate(topics):
            # Find the best agent for this topic
            agent = self.router.get_best_agent_for_task(topic, context)
            agent_id = agent.agent_id if agent else "router"
            
            task = AgentTask(
                id=f"{plan_id}_task_{i+1}",
                agent_id=agent_id,
                task_description=f"Learn about {topic}",
                task_type=TaskType.LESSON,
                topic=topic,
                dependencies=[previous_task_id] if mode == OrchestrationMode.SEQUENTIAL and previous_task_id else [],
                priority=len(topics) - i  # Earlier topics have higher priority
            )
            
            plan.add_task(task)
            previous_task_id = task.id
        
        self.active_plans[plan_id] = plan
        return plan
    
    def create_cross_subject_session(
        self,
        theme: str,
        context: LearnerContext
    ) -> OrchestrationPlan:
        """
        Create a session that spans multiple subjects around a theme.
        
        For example, a "Space" theme might include:
        - Science: Solar system facts
        - Math: Counting planets, distances
        - Reading: Space stories
        
        Args:
            theme: Central theme for the session
            context: Learner context
            
        Returns:
            Cross-subject orchestration plan
        """
        self._plan_counter += 1
        plan_id = f"cross_plan_{self._plan_counter}"
        
        plan = OrchestrationPlan(
            id=plan_id,
            name=f"{theme.title()} Exploration",
            description=f"Explore {theme} from multiple angles!",
            learner_id=context.learner_id,
            mode=OrchestrationMode.COLLABORATIVE,
            metadata={"theme": theme}
        )
        
        # Create tasks for different subjects
        subjects_tasks = self._generate_cross_subject_tasks(theme, context, plan_id)
        
        for task in subjects_tasks:
            plan.add_task(task)
        
        self.active_plans[plan_id] = plan
        return plan
    
    def _generate_cross_subject_tasks(
        self,
        theme: str,
        context: LearnerContext,
        plan_id: str
    ) -> List[AgentTask]:
        """Generate tasks across subjects for a theme"""
        tasks = []
        
        # Theme-based task definitions
        theme_tasks = {
            "space": [
                ("stem_explorer", "Learn about planets and the solar system", TaskType.LESSON, "space"),
                ("math_wizard", "Count the planets and learn about space distances", TaskType.LESSON, "counting space"),
                ("story_weaver", "Read a story about space adventure", TaskType.STORY, "space story")
            ],
            "animals": [
                ("stem_explorer", "Learn about different animal groups", TaskType.LESSON, "animals"),
                ("math_wizard", "Count legs on different animals", TaskType.PRACTICE, "counting"),
                ("story_weaver", "Read a story about animal friends", TaskType.STORY, "animal story")
            ],
            "nature": [
                ("stem_explorer", "Learn about plants and how they grow", TaskType.LESSON, "plants"),
                ("math_wizard", "Measure plant growth", TaskType.PRACTICE, "measurement"),
                ("story_weaver", "Read a story about the forest", TaskType.STORY, "nature story")
            ]
        }
        
        # Get tasks for theme or use defaults
        theme_lower = theme.lower()
        task_defs = theme_tasks.get(theme_lower, [
            ("stem_explorer", f"Explore the science of {theme}", TaskType.LESSON, theme),
            ("math_wizard", f"Math with {theme}", TaskType.PRACTICE, "math"),
            ("story_weaver", f"Story about {theme}", TaskType.STORY, theme)
        ])
        
        for i, (agent_id, description, task_type, topic) in enumerate(task_defs):
            # Verify agent exists
            if agent_id not in self.router.agents:
                agent = self.router.get_best_agent_for_task(topic, context)
                agent_id = agent.agent_id if agent else "router"
            
            tasks.append(AgentTask(
                id=f"{plan_id}_task_{i+1}",
                agent_id=agent_id,
                task_description=description,
                task_type=task_type,
                topic=topic,
                priority=3 - i
            ))
        
        return tasks
    
    def execute_plan(
        self,
        plan_id: str,
        context: LearnerContext,
        step_callback: Optional[Callable[[AgentTask, AgentResponse], None]] = None
    ) -> Dict[str, Any]:
        """
        Execute an orchestration plan.
        
        Args:
            plan_id: ID of the plan to execute
            context: Learner context
            step_callback: Optional callback after each task completion
            
        Returns:
            Execution results
        """
        plan = self.active_plans.get(plan_id)
        if not plan:
            return {"error": f"Plan {plan_id} not found"}
        
        plan.started_at = datetime.now().isoformat()
        results = []
        
        while not plan.is_complete():
            ready_tasks = plan.get_ready_tasks()
            
            if not ready_tasks:
                # Check if any tasks are still in progress
                in_progress = [t for t in plan.tasks if t.status == TaskStatus.IN_PROGRESS]
                if not in_progress:
                    # Deadlock or all failed - break out
                    break
                continue
            
            # Execute ready tasks based on mode
            if plan.mode in [OrchestrationMode.SEQUENTIAL, OrchestrationMode.ADAPTIVE]:
                # Execute one at a time
                task = ready_tasks[0]
                result = self._execute_task(task, context)
                results.append(result)
                
                if step_callback:
                    step_callback(task, task.result)
            else:
                # Execute all ready tasks (parallel/collaborative)
                for task in ready_tasks:
                    result = self._execute_task(task, context)
                    results.append(result)
                    
                    if step_callback:
                        step_callback(task, task.result)
        
        # Mark plan as completed
        plan.completed_at = datetime.now().isoformat()
        del self.active_plans[plan_id]
        self.completed_plans.append(plan)
        
        return {
            "plan_id": plan_id,
            "status": "completed",
            "progress": plan.get_progress(),
            "results_count": len(results),
            "tasks_completed": sum(1 for r in results if r["status"] == "completed")
        }
    
    def _execute_task(self, task: AgentTask, context: LearnerContext) -> Dict[str, Any]:
        """Execute a single task"""
        task.start()
        
        try:
            # Route to appropriate agent
            response = self.router.route_task(
                task=task.topic,
                task_type=task.task_type,
                context=context,
                preferred_agent=task.agent_id
            )
            
            task.complete(response)
            
            return {
                "task_id": task.id,
                "status": "completed",
                "agent_id": task.agent_id,
                "response_type": response.response_type.value
            }
        except Exception as e:
            task.fail(str(e))
            return {
                "task_id": task.id,
                "status": "failed",
                "error": str(e)
            }
    
    def execute_next_step(
        self,
        plan_id: str,
        context: LearnerContext
    ) -> Optional[AgentResponse]:
        """
        Execute just the next step in a plan (for interactive use).
        
        Args:
            plan_id: ID of the plan
            context: Learner context
            
        Returns:
            Response from the executed task or None if no tasks ready
        """
        plan = self.active_plans.get(plan_id)
        if not plan:
            return None
        
        ready_tasks = plan.get_ready_tasks()
        if not ready_tasks:
            return None
        
        task = ready_tasks[0]
        self._execute_task(task, context)
        
        return task.result
    
    def get_plan_status(self, plan_id: str) -> Optional[Dict[str, Any]]:
        """Get the current status of a plan"""
        plan = self.active_plans.get(plan_id)
        if plan:
            return plan.to_dict()
        
        # Check completed plans
        for completed in self.completed_plans:
            if completed.id == plan_id:
                result = completed.to_dict()
                result["status"] = "completed"
                return result
        
        return None
    
    def get_combined_response(
        self,
        plan_id: str,
        context: LearnerContext
    ) -> AgentResponse:
        """
        Get a combined response from all completed tasks in a plan.
        
        Useful for providing a summary of multi-agent learning.
        
        Args:
            plan_id: ID of the plan
            context: Learner context
            
        Returns:
            Combined response
        """
        plan = None
        for completed in self.completed_plans:
            if completed.id == plan_id:
                plan = completed
                break
        
        if not plan:
            plan = self.active_plans.get(plan_id)
        
        if not plan:
            return AgentResponse(
                agent_id="orchestrator",
                response_type=ResponseType.FEEDBACK,
                content="Plan not found.",
                requires_input=False
            )
        
        # Combine all completed task results
        completed_tasks = [t for t in plan.tasks if t.status == TaskStatus.COMPLETED and t.result]
        
        if not completed_tasks:
            return AgentResponse(
                agent_id="orchestrator",
                response_type=ResponseType.FEEDBACK,
                content="No completed tasks yet.",
                requires_input=False
            )
        
        # Build combined content
        content_parts = [f"🎓 **Your Learning Journey: {plan.name}**\n"]
        content_parts.append(f"Hi {context.name}! Here's what we explored together:\n")
        
        for i, task in enumerate(completed_tasks, 1):
            content_parts.append(f"\n**Part {i}: {task.task_description}**")
            if task.result:
                # Include a summary of each response
                summary = task.result.content[:300] + "..." if len(task.result.content) > 300 else task.result.content
                content_parts.append(summary)
        
        progress = plan.get_progress()
        content_parts.append(f"\n\n🏆 **Progress: {progress['progress_percentage']:.0f}% Complete!**")
        content_parts.append(f"\nYou covered {progress['completed']} topics!")
        
        return AgentResponse(
            agent_id="orchestrator",
            response_type=ResponseType.SUMMARY,
            content="\n".join(content_parts),
            requires_input=False,
            metadata={"plan_progress": progress}
        )
    
    def get_available_agents(self) -> List[Dict[str, Any]]:
        """Get information about available agents"""
        return self.router.get_available_agents()
    
    def get_orchestration_stats(self) -> Dict[str, Any]:
        """Get orchestration statistics"""
        return {
            "active_plans": len(self.active_plans),
            "completed_plans": len(self.completed_plans),
            "total_plans_created": self._plan_counter,
            "routing_stats": self.router.get_routing_stats()
        }


if __name__ == "__main__":
    # Demo the multi-agent orchestrator
    orchestrator = MultiAgentOrchestrator()
    
    # Create test context
    context = LearnerContext(
        learner_id="student_001",
        name="Jordan",
        age=8,
        learning_style="visual",
        interests=["space", "animals"]
    )
    
    print("=== Multi-Agent Orchestrator Demo ===\n")
    
    # Show available agents
    print("Available Agents:")
    for agent in orchestrator.get_available_agents():
        print(f"  - {agent['name']} ({agent['subject']})")
    
    # Create a learning journey
    print("\n--- Creating Learning Journey ---")
    plan = orchestrator.create_learning_journey(
        name="Math and Stories",
        topics=["addition", "fairy tales"],
        context=context,
        mode=OrchestrationMode.SEQUENTIAL
    )
    
    print(f"Created plan: {plan.name}")
    print(f"Tasks: {len(plan.tasks)}")
    for task in plan.tasks:
        print(f"  - {task.task_description} (Agent: {task.agent_id})")
    
    # Execute the plan
    print("\n--- Executing Plan ---")
    results = orchestrator.execute_plan(plan.id, context)
    print(f"Execution complete!")
    print(f"Tasks completed: {results['tasks_completed']}")
    
    # Get combined response
    print("\n--- Combined Learning Summary ---")
    summary = orchestrator.get_combined_response(plan.id, context)
    print(summary.content[:800] + "...")
    
    # Create a cross-subject session
    print("\n--- Creating Cross-Subject Session ---")
    cross_plan = orchestrator.create_cross_subject_session("space", context)
    print(f"Created cross-subject plan: {cross_plan.name}")
    print(f"Tasks:")
    for task in cross_plan.tasks:
        print(f"  - {task.task_description} ({task.agent_id})")
    
    # Show stats
    print("\n--- Orchestration Statistics ---")
    stats = orchestrator.get_orchestration_stats()
    print(f"Active Plans: {stats['active_plans']}")
    print(f"Completed Plans: {stats['completed_plans']}")
