"""
STEM Educational Agent

Specialized agent for teaching Science, Technology, Engineering,
and Mathematics concepts through exploration and experimentation.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from datetime import datetime
import random

from .base_educational_agent import (
    BaseEducationalAgent,
    AgentCapability,
    AgentResponse,
    LearnerContext,
    ResponseType
)


class STEMAgent(BaseEducationalAgent):
    """
    STEM learning agent specializing in hands-on exploration
    of science, technology, engineering, and math concepts.
    """
    
    def __init__(self):
        super().__init__(
            agent_id="stem_explorer",
            name="STEM Explorer",
            subject="stem",
            description="Your friendly guide to exploring Science, Technology, Engineering, and Math!",
            min_age=5,
            max_age=12,
            capabilities=[
                AgentCapability.TEACH,
                AgentCapability.EXPLAIN,
                AgentCapability.ENCOURAGE,
                AgentCapability.VISUALIZE,
                AgentCapability.GAMIFY
            ]
        )
        
        # STEM-specific topics this agent can handle
        self.topics = {
            "science": ["plants", "animals", "weather", "space", "earth", "water", "light", "sound", "magnets"],
            "technology": ["computers", "internet", "robots", "coding basics", "digital tools"],
            "engineering": ["building", "bridges", "machines", "design", "inventions"],
            "math": ["patterns", "shapes", "measurement", "graphs", "logic"]
        }
        
        # Fun experiments for different topics
        self.experiments = {
            "plants": {
                "title": "Growing Bean Seeds",
                "materials": ["bean seeds", "paper towel", "plastic bag", "water"],
                "steps": [
                    "Wet the paper towel",
                    "Place the bean seed on the wet paper towel",
                    "Put them in a plastic bag",
                    "Watch it grow over a few days!"
                ],
                "learning_points": ["Plants need water to grow", "Seeds contain a tiny plant inside"]
            },
            "water": {
                "title": "Floating and Sinking",
                "materials": ["bowl of water", "different small objects (cork, coin, paper clip, leaf)"],
                "steps": [
                    "Fill a bowl with water",
                    "Guess which objects will float",
                    "Place each object in the water",
                    "See which ones float and which sink!"
                ],
                "learning_points": ["Some things float, some sink", "It depends on the material and shape"]
            },
            "magnets": {
                "title": "Magnet Discovery",
                "materials": ["magnet", "various objects (paper clip, coin, plastic toy, wood)"],
                "steps": [
                    "Gather different objects",
                    "Guess which ones the magnet will stick to",
                    "Test each object with the magnet",
                    "Sort objects into 'magnetic' and 'not magnetic'"
                ],
                "learning_points": ["Magnets attract some metals", "Not all metals are magnetic"]
            }
        }
    
    def process_request(self, request: str, context: LearnerContext) -> AgentResponse:
        """Process a STEM learning request"""
        request_lower = request.lower()
        
        # Detect intent
        if any(word in request_lower for word in ["experiment", "try", "do", "make"]):
            return self._handle_experiment_request(request, context)
        elif any(word in request_lower for word in ["why", "how", "what"]):
            return self._handle_question(request, context)
        elif any(word in request_lower for word in ["learn", "teach", "tell"]):
            return self._handle_teaching_request(request, context)
        else:
            return self._handle_general_request(request, context)
    
    def generate_lesson(self, topic: str, context: LearnerContext) -> AgentResponse:
        """Generate a STEM lesson on a topic"""
        topic_lower = topic.lower()
        
        # Find which STEM area this topic belongs to
        stem_area = None
        for area, topics in self.topics.items():
            if topic_lower in topics or any(topic_lower in t for t in topics):
                stem_area = area
                break
        
        if stem_area == "science":
            return self._generate_science_lesson(topic, context)
        elif stem_area == "engineering":
            return self._generate_engineering_lesson(topic, context)
        else:
            return self._generate_general_stem_lesson(topic, context)
    
    def generate_practice(self, topic: str, context: LearnerContext, difficulty: str = "medium") -> AgentResponse:
        """Generate STEM practice activities"""
        activities = self._get_practice_activities(topic, difficulty, context)
        
        content = f"""
🔬 **STEM Practice Time, {context.name}!**

Let's explore {topic} with some fun activities!

{activities}

{self.generate_encouragement(context, "general")}
"""
        return self.create_response(
            content=content,
            response_type=ResponseType.QUESTION,
            context=context,
            requires_input=True,
            input_prompt="Tell me your answer or what you discovered!",
            suggestions=["Try an experiment", "Ask a question", "Learn something new"]
        )
    
    def _generate_science_lesson(self, topic: str, context: LearnerContext) -> AgentResponse:
        """Generate a science-focused lesson"""
        topic_lower = topic.lower()
        
        # Sample lesson content for different topics
        lessons = {
            "plants": f"""
🌱 **Let's Learn About Plants, {context.name}!**

Plants are living things that grow all around us!

**Amazing Plant Facts:**
- 🌿 Plants make their own food using sunlight (it's called photosynthesis!)
- 💧 Plants drink water through their roots
- 🌸 Many plants make flowers that turn into fruits
- 🍃 The green color in leaves is called chlorophyll

**Parts of a Plant:**
```
    🌸 Flower - Makes seeds
     |
    🍃 Leaves - Catch sunlight
     |
    | Stem - Carries water
     |
   ~~~ Roots - Drink water from soil
```

**Fun Question:** Can you find a plant near you right now? What color are its leaves?
""",
            "space": f"""
🚀 **Let's Explore Space, {context.name}!**

Space is the area beyond Earth where stars, planets, and galaxies live!

**Amazing Space Facts:**
- ⭐ Our Sun is actually a star - the closest one to Earth!
- 🌍 Earth is one of 8 planets that orbit (go around) the Sun
- 🌙 The Moon is Earth's only natural satellite
- 🌌 There are more stars in space than grains of sand on all beaches!

**Our Solar System:**
☀️ Sun → Mercury → Venus → 🌍 Earth → Mars → Jupiter → Saturn → Uranus → Neptune

**Fun Question:** If you could visit any planet, which would you choose and why?
""",
            "animals": f"""
🐾 **Let's Learn About Animals, {context.name}!**

Animals are living creatures that move, eat, and grow!

**Animal Groups:**
- 🐕 **Mammals** - Have fur, drink milk as babies (dogs, cats, elephants)
- 🐦 **Birds** - Have feathers and wings (eagles, penguins, parrots)
- 🐠 **Fish** - Live in water, breathe through gills (goldfish, sharks)
- 🐊 **Reptiles** - Have scales, cold-blooded (snakes, lizards, turtles)
- 🐸 **Amphibians** - Live in water AND on land (frogs, salamanders)

**Fun Fact:** Humans are mammals too!

**Fun Question:** What's your favorite animal? Which group does it belong to?
"""
        }
        
        content = lessons.get(topic_lower, self._generate_generic_science_lesson(topic, context))
        
        return self.create_response(
            content=content,
            response_type=ResponseType.LESSON,
            context=context,
            requires_input=True,
            input_prompt="Share your answer or ask me any question!",
            suggestions=["Do an experiment", "Learn about something else", "Take a quiz"]
        )
    
    def _generate_generic_science_lesson(self, topic: str, context: LearnerContext) -> str:
        """Generate a generic science lesson template"""
        return f"""
🔬 **Let's Explore {topic.title()}, {context.name}!**

{topic.title()} is a fascinating part of science!

**What We'll Learn:**
- What {topic} is all about
- Why it's important in our world
- Cool facts that will amaze you!

**Did You Know?**
Science is all about asking questions and discovering answers!
The best scientists are curious - just like you!

**Your Turn:**
What would YOU like to know about {topic}?
Ask me any question!

{self.generate_encouragement(context, "general")}
"""
    
    def _generate_engineering_lesson(self, topic: str, context: LearnerContext) -> AgentResponse:
        """Generate an engineering-focused lesson"""
        content = f"""
🏗️ **Engineering Adventure: {topic.title()}, {context.name}!**

Engineers are problem solvers who design and build amazing things!

**What Engineers Do:**
- 🤔 Think about problems
- 💡 Come up with ideas
- 🔧 Build and test solutions
- 🔄 Improve their designs

**Engineering Challenge:**
Can you think of something you'd like to build or improve?
Maybe a better toy, a helpful tool, or a fun game?

**Remember:** The best engineers aren't afraid to make mistakes - 
that's how we learn what works!

{self.generate_encouragement(context, "general")}
"""
        return self.create_response(
            content=content,
            response_type=ResponseType.LESSON,
            context=context,
            requires_input=True,
            input_prompt="Share your engineering idea with me!",
            suggestions=["Try a building challenge", "Learn about famous inventions", "Design something"]
        )
    
    def _generate_general_stem_lesson(self, topic: str, context: LearnerContext) -> AgentResponse:
        """Generate a general STEM lesson"""
        content = f"""
🌟 **STEM Discovery: {topic.title()}, {context.name}!**

STEM stands for:
- **S**cience 🔬
- **T**echnology 💻
- **E**ngineering 🏗️
- **M**athematics 🔢

Let's explore {topic} together!

**Why STEM is Cool:**
- It helps us understand how things work
- It lets us solve real-world problems
- It's behind everything from video games to rockets!

**Your Mission:**
Think of three things you use every day that were created using STEM.

{self.generate_encouragement(context, "general")}
"""
        return self.create_response(
            content=content,
            response_type=ResponseType.LESSON,
            context=context,
            requires_input=True,
            input_prompt="Share what you thought of!",
            suggestions=["Do an experiment", "Ask a question", "Try a challenge"]
        )
    
    def _handle_experiment_request(self, request: str, context: LearnerContext) -> AgentResponse:
        """Handle requests for experiments"""
        # Try to find a relevant experiment
        request_lower = request.lower()
        selected_experiment = None
        
        for topic, experiment in self.experiments.items():
            if topic in request_lower:
                selected_experiment = experiment
                break
        
        if not selected_experiment:
            # Pick a random experiment
            selected_experiment = random.choice(list(self.experiments.values()))
        
        content = f"""
🧪 **Fun Experiment Time, {context.name}!**

**{selected_experiment['title']}**

**Materials You'll Need:**
{chr(10).join(f"• {m}" for m in selected_experiment['materials'])}

**Steps:**
{chr(10).join(f"{i+1}. {step}" for i, step in enumerate(selected_experiment['steps']))}

**What You'll Learn:**
{chr(10).join(f"✨ {point}" for point in selected_experiment['learning_points'])}

⚠️ **Safety First:** Always do experiments with a grown-up helper!

{self.generate_encouragement(context, "general")}
"""
        return self.create_response(
            content=content,
            response_type=ResponseType.LESSON,
            context=context,
            requires_input=True,
            input_prompt="Tell me what happened when you tried it!",
            suggestions=["Try another experiment", "Ask why it works", "Learn more"]
        )
    
    def _handle_question(self, request: str, context: LearnerContext) -> AgentResponse:
        """Handle science questions"""
        content = f"""
🤔 **Great Question, {context.name}!**

That's exactly the kind of question real scientists ask!

Let me help you find the answer...

**Thinking Like a Scientist:**
1. 🔍 What do we already know?
2. 🤷 What are we trying to find out?
3. 💭 What do we think might happen? (hypothesis)
4. 🧪 How can we test it?
5. 📝 What did we learn?

Would you like me to explain more about your question, 
or would you like to try an experiment to find out?

{self.generate_encouragement(context, "general")}
"""
        return self.create_response(
            content=content,
            response_type=ResponseType.EXPLANATION,
            context=context,
            requires_input=True,
            input_prompt="What would you like to know more about?",
            suggestions=["Explain more", "Do an experiment", "Ask another question"]
        )
    
    def _handle_teaching_request(self, request: str, context: LearnerContext) -> AgentResponse:
        """Handle requests to learn about a topic"""
        # Extract topic from request
        topic = "science"  # Default
        for area_topics in self.topics.values():
            for t in area_topics:
                if t in request.lower():
                    topic = t
                    break
        
        return self.generate_lesson(topic, context)
    
    def _handle_general_request(self, request: str, context: LearnerContext) -> AgentResponse:
        """Handle general STEM requests"""
        content = f"""
🚀 **Welcome to STEM Explorer, {context.name}!**

I'm so excited to explore science, technology, engineering, and math with you!

**What would you like to do?**

🔬 **Science** - Learn about plants, animals, space, and more!
💻 **Technology** - Discover how computers and gadgets work!
🏗️ **Engineering** - Build and create amazing things!
🔢 **Math** - Find patterns and solve puzzles!

**Or try one of these:**
- 🧪 Do a fun experiment
- ❓ Ask me any "why" question
- 🎮 Play a STEM game

{self.generate_encouragement(context, "general")}
"""
        return self.create_response(
            content=content,
            response_type=ResponseType.LESSON,
            context=context,
            requires_input=True,
            input_prompt="What catches your interest?",
            suggestions=["Learn about space", "Do an experiment", "Ask a question"]
        )
    
    def _get_practice_activities(self, topic: str, difficulty: str, context: LearnerContext) -> str:
        """Generate practice activities for a topic"""
        activities = f"""
**Activity 1: Observation Challenge**
Look around you and find 3 things related to {topic}.
Write down or draw what you see!

**Activity 2: Question Time**
Think of 2 questions about {topic} that you'd like to answer.

**Activity 3: Science Journal**
Draw or write about something cool you learned about {topic}!
"""
        return activities
    
    def can_handle_topic(self, topic: str) -> bool:
        """Check if this agent can handle the given topic"""
        topic_lower = topic.lower()
        
        # Check if topic is in any of our areas
        for area, topics in self.topics.items():
            if topic_lower == area or topic_lower in topics:
                return True
            if any(topic_lower in t for t in topics):
                return True
        
        # General STEM keywords
        stem_keywords = ["science", "technology", "engineering", "stem", "experiment", 
                        "discover", "explore", "build", "create", "invent"]
        return any(kw in topic_lower for kw in stem_keywords)


if __name__ == "__main__":
    # Demo the STEM agent
    agent = STEMAgent()
    
    # Create a test context
    context = LearnerContext(
        learner_id="student_001",
        name="Alex",
        age=8,
        learning_style="visual",
        interests=["dinosaurs", "space"]
    )
    
    print("=== STEM Agent Demo ===\n")
    print(f"Agent: {agent.name}")
    print(f"Description: {agent.description}\n")
    
    # Test a lesson
    print("--- Generating Space Lesson ---")
    response = agent.generate_lesson("space", context)
    print(response.content[:500] + "...")
    
    # Test an experiment request
    print("\n--- Handling Experiment Request ---")
    response = agent.process_request("I want to do a water experiment!", context)
    print(response.content[:500] + "...")
