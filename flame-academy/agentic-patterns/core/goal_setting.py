"""
Goal-Setting Pattern for Adaptive Learning

This module implements the goal-setting design pattern for creating,
tracking, and adapting learning objectives based on learner performance
and engagement. Designed for children-centric education with age-appropriate goals.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
from enum import Enum
import json


class GoalType(Enum):
    """Types of learning goals"""
    MASTERY = "mastery"            # Master a specific concept
    COMPLETION = "completion"      # Complete a set of activities
    PRACTICE = "practice"          # Practice for a duration/count
    STREAK = "streak"              # Maintain a learning streak
    ACHIEVEMENT = "achievement"    # Earn a badge or recognition
    EXPLORATION = "exploration"    # Explore new topics


class GoalStatus(Enum):
    """Status of a learning goal"""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    OVERDUE = "overdue"
    PAUSED = "paused"


class GoalPriority(Enum):
    """Priority levels for goals"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class Milestone:
    """
    A checkpoint within a larger goal.
    
    Milestones break down goals into smaller, achievable steps
    to maintain motivation and provide frequent feedback.
    """
    id: str
    name: str
    description: str
    target_value: float
    current_value: float = 0.0
    is_complete: bool = False
    completed_at: Optional[str] = None
    celebration_message: str = "🎉 Great job!"
    
    def update_progress(self, value: float) -> bool:
        """
        Update milestone progress.
        
        Args:
            value: New progress value
            
        Returns:
            True if milestone was just completed
        """
        was_complete = self.is_complete
        self.current_value = value
        
        if self.current_value >= self.target_value and not was_complete:
            self.is_complete = True
            self.completed_at = datetime.now().isoformat()
            return True
        return False
    
    @property
    def progress_percentage(self) -> float:
        """Calculate progress as a percentage"""
        if self.target_value == 0:
            return 100.0 if self.is_complete else 0.0
        return min(100.0, (self.current_value / self.target_value) * 100)


@dataclass
class LearningGoal:
    """
    A learning goal with tracking and adaptation capabilities.
    
    Goals are designed to be achievable, motivating, and adaptable
    to each learner's pace and progress.
    """
    id: str
    learner_id: str
    title: str
    description: str
    goal_type: GoalType
    subject: str
    target_value: float
    current_value: float = 0.0
    status: GoalStatus = GoalStatus.NOT_STARTED
    priority: GoalPriority = GoalPriority.MEDIUM
    milestones: List[Milestone] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    due_date: Optional[str] = None
    completed_at: Optional[str] = None
    difficulty_adjusted: bool = False
    original_target: Optional[float] = None
    celebration_emoji: str = "🏆"
    reward_badge: Optional[str] = None
    
    def update_progress(self, value: float) -> Dict[str, Any]:
        """
        Update goal progress and check for completion.
        
        Args:
            value: New progress value
            
        Returns:
            Progress update result with any celebrations
        """
        result = {
            "goal_id": self.id,
            "previous_value": self.current_value,
            "new_value": value,
            "milestones_completed": [],
            "goal_completed": False,
            "celebration": None
        }
        
        self.current_value = value
        
        # Update status
        if self.status == GoalStatus.NOT_STARTED and value > 0:
            self.status = GoalStatus.IN_PROGRESS
        
        # Check milestones
        for milestone in self.milestones:
            # Calculate milestone target based on goal progress
            milestone_value = (value / self.target_value) * milestone.target_value if self.target_value > 0 else 0
            if milestone.update_progress(milestone_value):
                result["milestones_completed"].append({
                    "name": milestone.name,
                    "celebration": milestone.celebration_message
                })
        
        # Check goal completion
        if self.current_value >= self.target_value:
            self.status = GoalStatus.COMPLETED
            self.completed_at = datetime.now().isoformat()
            result["goal_completed"] = True
            result["celebration"] = f"{self.celebration_emoji} Congratulations! You completed: {self.title}!"
            if self.reward_badge:
                result["reward_badge"] = self.reward_badge
        
        return result
    
    def adjust_difficulty(self, factor: float, reason: str):
        """
        Adjust goal difficulty based on learner performance.
        
        Args:
            factor: Multiplier for the target (< 1 makes easier, > 1 makes harder)
            reason: Explanation for the adjustment
        """
        if not self.difficulty_adjusted:
            self.original_target = self.target_value
        
        self.target_value = self.target_value * factor
        self.difficulty_adjusted = True
        
        # Also adjust milestones
        for milestone in self.milestones:
            milestone.target_value = milestone.target_value * factor
    
    def add_milestone(self, name: str, description: str, target_percentage: float, celebration: str = "🎉 Milestone reached!"):
        """
        Add a milestone to the goal.
        
        Args:
            name: Milestone name
            description: What the milestone represents
            target_percentage: Percentage of goal completion for this milestone (0-100)
            celebration: Message to show when milestone is reached
        """
        milestone_target = (target_percentage / 100) * self.target_value
        milestone = Milestone(
            id=f"{self.id}_milestone_{len(self.milestones) + 1}",
            name=name,
            description=description,
            target_value=milestone_target,
            celebration_message=celebration
        )
        self.milestones.append(milestone)
    
    @property
    def progress_percentage(self) -> float:
        """Calculate overall progress as a percentage"""
        if self.target_value == 0:
            return 100.0 if self.status == GoalStatus.COMPLETED else 0.0
        return min(100.0, (self.current_value / self.target_value) * 100)
    
    @property
    def is_overdue(self) -> bool:
        """Check if the goal is past its due date"""
        if not self.due_date or self.status == GoalStatus.COMPLETED:
            return False
        return datetime.now() > datetime.fromisoformat(self.due_date)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert goal to dictionary"""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "type": self.goal_type.value,
            "subject": self.subject,
            "target": self.target_value,
            "current": self.current_value,
            "progress_percentage": self.progress_percentage,
            "status": self.status.value,
            "priority": self.priority.value,
            "milestones_completed": sum(1 for m in self.milestones if m.is_complete),
            "total_milestones": len(self.milestones),
            "due_date": self.due_date,
            "is_overdue": self.is_overdue
        }


class GoalSetter:
    """
    Manages goal creation, tracking, and adaptation for learners.
    
    Provides intelligent goal-setting that adapts to each learner's
    pace and maintains motivation through achievable challenges.
    """
    
    def __init__(self):
        """Initialize the goal setter"""
        self.goals: Dict[str, List[LearningGoal]] = {}  # learner_id -> goals
        self.goal_templates: Dict[str, Dict[str, Any]] = {}
        self._init_default_templates()
    
    def _init_default_templates(self):
        """Initialize default goal templates for common learning objectives"""
        self.goal_templates = {
            "math_basics": {
                "title": "Math Explorer",
                "description": "Master the basics of mathematics",
                "goal_type": GoalType.MASTERY,
                "subject": "math",
                "target_value": 10,  # Complete 10 math concepts
                "milestones": [
                    ("Getting Started", "Complete your first math lesson", 10),
                    ("Making Progress", "Complete 5 math concepts", 50),
                    ("Almost There", "Master 8 math concepts", 80)
                ],
                "celebration_emoji": "🔢",
                "reward_badge": "Math Explorer Badge"
            },
            "reading_adventure": {
                "title": "Reading Adventure",
                "description": "Explore the world through stories",
                "goal_type": GoalType.COMPLETION,
                "subject": "reading",
                "target_value": 5,  # Read 5 stories
                "milestones": [
                    ("First Story", "Complete your first story", 20),
                    ("Bookworm", "Read 3 stories", 60)
                ],
                "celebration_emoji": "📚",
                "reward_badge": "Bookworm Badge"
            },
            "science_explorer": {
                "title": "Science Explorer",
                "description": "Discover the wonders of science",
                "goal_type": GoalType.EXPLORATION,
                "subject": "science",
                "target_value": 8,  # Explore 8 science topics
                "milestones": [
                    ("Curious Mind", "Explore your first topic", 12.5),
                    ("Scientist in Training", "Explore 4 topics", 50),
                    ("Expert Explorer", "Explore 7 topics", 87.5)
                ],
                "celebration_emoji": "🔬",
                "reward_badge": "Science Explorer Badge"
            },
            "daily_practice": {
                "title": "Daily Learner",
                "description": "Practice learning every day",
                "goal_type": GoalType.STREAK,
                "subject": "general",
                "target_value": 7,  # 7 day streak
                "milestones": [
                    ("Day 1", "Complete your first day", 14.3),
                    ("Half Week", "Reach 3 days", 42.9),
                    ("Almost There", "Reach 5 days", 71.4)
                ],
                "celebration_emoji": "⭐",
                "reward_badge": "Consistency Star"
            }
        }
    
    def create_goal_from_template(
        self,
        learner_id: str,
        template_name: str,
        customizations: Optional[Dict[str, Any]] = None
    ) -> Optional[LearningGoal]:
        """
        Create a goal from a template with optional customizations.
        
        Args:
            learner_id: ID of the learner
            template_name: Name of the template to use
            customizations: Optional overrides for template values
            
        Returns:
            Created LearningGoal or None if template not found
        """
        if template_name not in self.goal_templates:
            return None
        
        template = self.goal_templates[template_name].copy()
        if customizations:
            template.update(customizations)
        
        goal = LearningGoal(
            id=f"{learner_id}_{template_name}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            learner_id=learner_id,
            title=template["title"],
            description=template["description"],
            goal_type=template["goal_type"],
            subject=template["subject"],
            target_value=template["target_value"],
            celebration_emoji=template.get("celebration_emoji", "🏆"),
            reward_badge=template.get("reward_badge")
        )
        
        # Add milestones
        for name, desc, percentage in template.get("milestones", []):
            goal.add_milestone(name, desc, percentage)
        
        # Store the goal
        if learner_id not in self.goals:
            self.goals[learner_id] = []
        self.goals[learner_id].append(goal)
        
        return goal
    
    def create_custom_goal(
        self,
        learner_id: str,
        title: str,
        description: str,
        goal_type: GoalType,
        subject: str,
        target_value: float,
        due_date: Optional[datetime] = None,
        priority: GoalPriority = GoalPriority.MEDIUM
    ) -> LearningGoal:
        """
        Create a custom goal with specified parameters.
        
        Args:
            learner_id: ID of the learner
            title: Goal title
            description: Goal description
            goal_type: Type of goal
            subject: Subject area
            target_value: Target to achieve
            due_date: Optional deadline
            priority: Goal priority
            
        Returns:
            Created LearningGoal
        """
        goal = LearningGoal(
            id=f"{learner_id}_custom_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            learner_id=learner_id,
            title=title,
            description=description,
            goal_type=goal_type,
            subject=subject,
            target_value=target_value,
            due_date=due_date.isoformat() if due_date else None,
            priority=priority
        )
        
        # Auto-generate milestones
        goal.add_milestone("Quarter Way", "25% complete", 25, "🌱 Great start!")
        goal.add_milestone("Halfway", "50% complete", 50, "💪 Halfway there!")
        goal.add_milestone("Almost Done", "75% complete", 75, "🔥 Almost there!")
        
        # Store the goal
        if learner_id not in self.goals:
            self.goals[learner_id] = []
        self.goals[learner_id].append(goal)
        
        return goal
    
    def get_learner_goals(self, learner_id: str, status: Optional[GoalStatus] = None) -> List[LearningGoal]:
        """
        Get all goals for a learner.
        
        Args:
            learner_id: ID of the learner
            status: Optional filter by status
            
        Returns:
            List of matching goals
        """
        goals = self.goals.get(learner_id, [])
        if status:
            goals = [g for g in goals if g.status == status]
        return goals
    
    def get_active_goals(self, learner_id: str) -> List[LearningGoal]:
        """Get all active (in-progress) goals for a learner"""
        return self.get_learner_goals(learner_id, GoalStatus.IN_PROGRESS)
    
    def get_suggested_goals(self, learner_id: str, subject: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get suggested goals based on learner profile and progress.
        
        Args:
            learner_id: ID of the learner
            subject: Optional subject to filter suggestions
            
        Returns:
            List of suggested goal templates
        """
        existing_goals = self.get_learner_goals(learner_id)
        existing_subjects = {g.subject for g in existing_goals}
        
        suggestions = []
        for template_name, template in self.goal_templates.items():
            # Skip if learner already has this goal
            if any(template_name in g.id for g in existing_goals):
                continue
            
            # Filter by subject if specified
            if subject and template["subject"] != subject and template["subject"] != "general":
                continue
            
            suggestions.append({
                "template_name": template_name,
                "title": template["title"],
                "description": template["description"],
                "subject": template["subject"],
                "reward_badge": template.get("reward_badge")
            })
        
        return suggestions
    
    def update_goal_progress(self, goal_id: str, learner_id: str, new_value: float) -> Optional[Dict[str, Any]]:
        """
        Update progress for a specific goal.
        
        Args:
            goal_id: ID of the goal
            learner_id: ID of the learner
            new_value: New progress value
            
        Returns:
            Update result or None if goal not found
        """
        goals = self.goals.get(learner_id, [])
        for goal in goals:
            if goal.id == goal_id:
                return goal.update_progress(new_value)
        return None
    
    def adapt_goal_difficulty(self, learner_id: str, goal_id: str, performance_ratio: float):
        """
        Adapt goal difficulty based on learner performance.
        
        Args:
            learner_id: ID of the learner
            goal_id: ID of the goal
            performance_ratio: Performance score (0-1, where 1 is excellent)
        """
        goals = self.goals.get(learner_id, [])
        for goal in goals:
            if goal.id == goal_id and goal.status == GoalStatus.IN_PROGRESS:
                if performance_ratio < 0.4:
                    # Struggling - make goal easier
                    goal.adjust_difficulty(0.8, "Adjusted for better success experience")
                elif performance_ratio > 0.9:
                    # Excelling - make goal more challenging
                    goal.adjust_difficulty(1.2, "Increased challenge for growth")
                break
    
    def get_goal_summary(self, learner_id: str) -> Dict[str, Any]:
        """
        Get a summary of all goals for a learner.
        
        Args:
            learner_id: ID of the learner
            
        Returns:
            Summary statistics and goal list
        """
        goals = self.goals.get(learner_id, [])
        
        return {
            "total_goals": len(goals),
            "completed": sum(1 for g in goals if g.status == GoalStatus.COMPLETED),
            "in_progress": sum(1 for g in goals if g.status == GoalStatus.IN_PROGRESS),
            "not_started": sum(1 for g in goals if g.status == GoalStatus.NOT_STARTED),
            "overdue": sum(1 for g in goals if g.is_overdue),
            "badges_earned": [g.reward_badge for g in goals if g.status == GoalStatus.COMPLETED and g.reward_badge],
            "goals": [g.to_dict() for g in goals]
        }


if __name__ == "__main__":
    # Demo the goal setting system
    setter = GoalSetter()
    learner_id = "student_001"
    
    print("=== Goal Setting Demo ===\n")
    
    # Create goals from templates
    math_goal = setter.create_goal_from_template(learner_id, "math_basics")
    print(f"Created goal: {math_goal.title}")
    print(f"  Target: {math_goal.target_value} concepts")
    print(f"  Milestones: {len(math_goal.milestones)}")
    
    # Update progress
    print("\n--- Updating Progress ---")
    result = math_goal.update_progress(3)
    print(f"Progress: {math_goal.progress_percentage:.0f}%")
    for milestone in result.get("milestones_completed", []):
        print(f"  🎉 {milestone['name']}: {milestone['celebration']}")
    
    # Continue progress
    result = math_goal.update_progress(6)
    print(f"Progress: {math_goal.progress_percentage:.0f}%")
    for milestone in result.get("milestones_completed", []):
        print(f"  🎉 {milestone['name']}: {milestone['celebration']}")
    
    # Complete the goal
    result = math_goal.update_progress(10)
    print(f"Progress: {math_goal.progress_percentage:.0f}%")
    if result.get("goal_completed"):
        print(f"\n{result['celebration']}")
        if result.get("reward_badge"):
            print(f"  Badge earned: {result['reward_badge']}")
    
    # Get summary
    print("\n--- Goal Summary ---")
    summary = setter.get_goal_summary(learner_id)
    print(f"Total Goals: {summary['total_goals']}")
    print(f"Completed: {summary['completed']}")
    print(f"Badges Earned: {summary['badges_earned']}")
