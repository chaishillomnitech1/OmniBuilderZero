"""
Storytelling Educational Agent

Specialized agent for teaching through narratives, reading comprehension,
creative writing, and language arts.
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


class StorytellingAgent(BaseEducationalAgent):
    """
    Storytelling agent specializing in narrative-based learning,
    reading comprehension, creative writing, and language arts.
    """
    
    def __init__(self):
        super().__init__(
            agent_id="story_weaver",
            name="Story Weaver",
            subject="reading",
            description="Your magical guide to the world of stories and imagination!",
            min_age=4,
            max_age=12,
            capabilities=[
                AgentCapability.TEACH,
                AgentCapability.STORYTELL,
                AgentCapability.EXPLAIN,
                AgentCapability.ENCOURAGE,
                AgentCapability.GAMIFY
            ]
        )
        
        # Storytelling topics
        self.topics = [
            "characters", "plot", "setting", "beginning", "middle", "end",
            "vocabulary", "reading", "writing", "poetry", "fairy tales",
            "adventure", "mystery", "friendship", "emotions"
        ]
        
        # Story templates for different themes
        self.story_starters = {
            "adventure": [
                "Once upon a time, in a land far away, there was a young explorer named {name}...",
                "The map glowed mysteriously as {name} held it up to the light...",
                "Nobody believed {name} when they said they found a secret door..."
            ],
            "friendship": [
                "{name} never expected to find a friend in such an unusual place...",
                "The two friends, {name} and their new buddy, decided to share everything...",
                "When {name} moved to a new town, making friends seemed impossible until..."
            ],
            "mystery": [
                "The strange footprints led {name} deeper into the garden...",
                "Every night at midnight, {name} heard a mysterious sound from the attic...",
                "{name} discovered that someone had been leaving secret notes in their locker..."
            ],
            "fantasy": [
                "{name} woke up one morning to find they had grown wings...",
                "The talking cat had a very important message for {name}...",
                "Deep in the enchanted forest, {name} discovered a hidden village..."
            ]
        }
        
        # Story elements for teaching
        self.story_elements = {
            "characters": {
                "title": "Characters - The People (and Creatures!) in Stories",
                "description": "Characters are who the story is about!",
                "types": [
                    "Main Character (Hero/Heroine) - The story follows them!",
                    "Supporting Characters - Friends and helpers",
                    "Villain - Creates problems for the hero"
                ],
                "questions": [
                    "Who is the main character?",
                    "What does the character want?",
                    "How does the character feel?"
                ]
            },
            "setting": {
                "title": "Setting - Where and When Stories Happen",
                "description": "The setting is the place and time of a story!",
                "types": [
                    "Place - Where does it happen? (forest, castle, school)",
                    "Time - When does it happen? (long ago, today, future)",
                    "Weather/Mood - What's it like? (sunny, spooky, magical)"
                ],
                "questions": [
                    "Where does this story take place?",
                    "When does this story happen?",
                    "What does the place look like?"
                ]
            },
            "plot": {
                "title": "Plot - What Happens in the Story",
                "description": "The plot is all the events that happen!",
                "types": [
                    "Beginning - Introduces characters and setting",
                    "Middle - The problem or adventure!",
                    "End - How things work out"
                ],
                "questions": [
                    "What happens first?",
                    "What's the problem?",
                    "How does it end?"
                ]
            }
        }
    
    def process_request(self, request: str, context: LearnerContext) -> AgentResponse:
        """Process a storytelling/reading request"""
        request_lower = request.lower()
        
        # Detect intent
        if any(word in request_lower for word in ["story", "tell me", "once upon"]):
            return self._handle_story_request(request, context)
        elif any(word in request_lower for word in ["write", "create", "make up"]):
            return self._handle_writing_request(request, context)
        elif any(word in request_lower for word in ["read", "understand", "comprehension"]):
            return self._handle_reading_request(request, context)
        elif any(word in request_lower for word in ["character", "setting", "plot"]):
            return self.generate_lesson(request, context)
        else:
            return self._handle_general_request(request, context)
    
    def generate_lesson(self, topic: str, context: LearnerContext) -> AgentResponse:
        """Generate a storytelling/reading lesson"""
        topic_lower = topic.lower()
        
        # Check for specific story elements
        for element, details in self.story_elements.items():
            if element in topic_lower:
                return self._generate_element_lesson(element, context)
        
        # Default to general storytelling lesson
        return self._generate_storytelling_lesson(context)
    
    def generate_practice(self, topic: str, context: LearnerContext, difficulty: str = "medium") -> AgentResponse:
        """Generate storytelling practice activities"""
        activities = self._get_storytelling_activities(topic, difficulty, context)
        
        content = f"""
📚 **Storytelling Practice, {context.name}!**

Let's have fun with stories!

{activities}

{self.generate_encouragement(context, "general")}
"""
        return self.create_response(
            content=content,
            response_type=ResponseType.QUESTION,
            context=context,
            requires_input=True,
            input_prompt="Share your story or answer with me!",
            suggestions=["Tell me a story", "Learn about characters", "Play a story game"]
        )
    
    def generate_story(self, theme: str, context: LearnerContext, include_learner: bool = True) -> AgentResponse:
        """Generate an interactive story"""
        theme_lower = theme.lower() if theme else "adventure"
        
        # Select theme
        if theme_lower not in self.story_starters:
            theme_lower = random.choice(list(self.story_starters.keys()))
        
        # Get a story starter
        starter = random.choice(self.story_starters[theme_lower])
        if include_learner:
            starter = starter.format(name=context.name)
        else:
            starter = starter.format(name="the young hero")
        
        # Generate a complete short story
        story = self._create_short_story(theme_lower, starter, context)
        
        content = f"""
📖 **Story Time, {context.name}!**

*~*~*~*~*~*~*~*~*~*

{story}

*~*~*~*~*~*~*~*~*~*

**Questions to Think About:**
- Who is the main character?
- What happened in the story?
- How did the story make you feel?

{self.generate_encouragement(context, "success")}
"""
        return self.create_response(
            content=content,
            response_type=ResponseType.STORY,
            context=context,
            requires_input=True,
            input_prompt="What did you think of the story? Or would you like to continue it?",
            suggestions=["Continue the story", "Hear another story", "Create your own story"]
        )
    
    def _create_short_story(self, theme: str, starter: str, context: LearnerContext) -> str:
        """Create a complete short story"""
        # Age-appropriate story templates
        if context.age < 7:
            # Shorter, simpler stories for younger children
            stories = {
                "adventure": f"""
{starter}

One sunny day, they found a shiny key hidden under a flower.
"I wonder what this opens!" they said excitedly.

They walked through the meadow until they found a tiny door in an old tree.
The key fit perfectly! Inside was a beautiful garden with butterflies of every color.

"This is the most wonderful place!" they cheered.
And from that day on, they visited their secret garden every afternoon.

**The End** ✨
""",
                "friendship": f"""
{starter}

It was a little rabbit who was also new to the forest.
"Would you like to play?" asked the rabbit.

They played hide and seek among the flowers.
They shared berries for lunch.
They told each other their favorite jokes.

By sunset, they knew they would be friends forever.

**The End** 💖
""",
                "mystery": f"""
{starter}

Following the footprints carefully, they discovered a family of hedgehogs!
The hedgehogs were building a cozy house for winter.

"Oh! That's what made the mysterious marks!" they laughed.

The hedgehogs showed them around their tiny home.
Mystery solved!

**The End** 🔍
""",
                "fantasy": f"""
{starter}

At first they were scared, but then they felt happy.

"You can fly!" sang the birds outside their window.
They carefully flew up to the clouds, which felt like soft cotton candy.

Up above, they met a friendly cloud dragon who gave them a ride back home.
What an amazing day!

**The End** 🌈
"""
            }
        else:
            # Slightly longer stories for older children
            stories = {
                "adventure": f"""
{starter}

Armed with courage and curiosity, they followed the ancient path marked on the weathered map.
Through whispering forests and across bubbling brooks, each step brought new discoveries.

Suddenly, the path ended at a magnificent waterfall. Behind the curtain of water, 
something sparkled. Taking a deep breath, they stepped through the mist...

There it was - a cave filled with crystals that glowed like captured starlight!
Each crystal hummed with a different musical note.

They carefully selected one crystal as a souvenir. 
From that day forward, whenever they held it, they remembered that 
the greatest adventures await those brave enough to begin.

**The End** ⭐
""",
                "friendship": f"""
{starter}

At first, they were so different they didn't know what to talk about.
One loved sunny days; the other loved rainy afternoons.
One talked a lot; the other was quiet and thoughtful.

But then they discovered something amazing - 
their differences made everything more interesting!

When it rained, they'd read books together.
When it was sunny, they'd explore outside.
The quiet one listened; the talkative one shared stories.

They learned that true friendship isn't about being the same.
It's about celebrating what makes each person special.

**The End** 🌟
""",
                "mystery": f"""
{starter}

Each clue led to another, like a trail of breadcrumbs through a puzzle.
A feather here. A footprint there. A piece of ribbon caught on a branch.

They gathered all the evidence in their notebook, thinking hard.
Who could be behind this mystery?

Finally, the last clue pointed to the old garden shed.
Heart pounding, they opened the creaky door...

Inside, they found the neighborhood cat and her three tiny kittens!
She had been collecting soft things to make a cozy nest.

Sometimes the best mysteries have the sweetest endings.

**The End** 🐱
""",
                "fantasy": f"""
{starter}

The cat led them through a doorway made of moonbeams into a world where everything was different.
Trees sang lullabies. Rivers flowed with colors instead of water.
Stars were close enough to hold in your hands.

"You've been chosen," the cat explained, "to help restore the magic."

They planted a seed of kindness, watered it with laughter, 
and watched as a magnificent rainbow tree grew before their eyes.

The magical world was saved, and they returned home with a gift:
the ability to see magic in everyday things.

**The End** ✨🌙
"""
            }
        
        return stories.get(theme, stories["adventure"])
    
    def _generate_element_lesson(self, element: str, context: LearnerContext) -> AgentResponse:
        """Generate a lesson about a specific story element"""
        details = self.story_elements[element]
        
        content = f"""
📚 **Learning About {details['title']}, {context.name}!**

{details['description']}

**Types of {element.title()}:**
{chr(10).join(f"• {t}" for t in details['types'])}

**Questions to Ask When Reading:**
{chr(10).join(f"❓ {q}" for q in details['questions'])}

**Try This!**
Think about your favorite story. Can you identify the {element}?

{self.generate_encouragement(context, "general")}
"""
        return self.create_response(
            content=content,
            response_type=ResponseType.LESSON,
            context=context,
            requires_input=True,
            input_prompt=f"Tell me about the {element} in your favorite story!",
            suggestions=["Hear a story", "Learn another element", "Practice identifying elements"]
        )
    
    def _generate_storytelling_lesson(self, context: LearnerContext) -> AgentResponse:
        """Generate a general storytelling lesson"""
        content = f"""
📖 **Welcome to Storytelling, {context.name}!**

Stories are like magic carpets that can take us anywhere!

**Every Great Story Has:**
🎭 **Characters** - The people or creatures in the story
📍 **Setting** - Where and when the story happens
📈 **Plot** - What happens (beginning, middle, end!)
💭 **Theme** - The lesson or message

**Why Stories Are Amazing:**
- They help us understand feelings
- They teach us about the world
- They let our imagination fly!
- They connect us with others

**Story Structure:**
```
    📖 Beginning: Meet the characters and setting
         ↓
    ⚡ Middle: The adventure or problem!
         ↓
    🌟 End: How everything works out
```

Would you like to hear a story, or learn to write your own?

{self.generate_encouragement(context, "general")}
"""
        return self.create_response(
            content=content,
            response_type=ResponseType.LESSON,
            context=context,
            requires_input=True,
            input_prompt="What would you like to do?",
            suggestions=["Hear a story", "Write a story", "Learn about characters"]
        )
    
    def _handle_story_request(self, request: str, context: LearnerContext) -> AgentResponse:
        """Handle requests for a story"""
        # Detect preferred theme
        theme = "adventure"
        for t in self.story_starters.keys():
            if t in request.lower():
                theme = t
                break
        
        return self.generate_story(theme, context)
    
    def _handle_writing_request(self, request: str, context: LearnerContext) -> AgentResponse:
        """Handle creative writing requests"""
        content = f"""
✏️ **Let's Write a Story, {context.name}!**

Creating your own story is so exciting! Let me help you get started.

**Story Building Blocks:**

1️⃣ **Choose Your Character**
   - Is it a person, animal, or magical creature?
   - What's their name?
   - What do they want?

2️⃣ **Pick Your Setting**
   - A magical forest? A busy city? Outer space?
   - Is it day or night? Summer or winter?

3️⃣ **Create a Problem**
   - What challenge does your character face?
   - This makes the story exciting!

4️⃣ **Solve the Problem**
   - How does your character overcome the challenge?
   - Maybe with help from a friend?

**Story Starter for You:**
One day, in a [place], there was a [character] who wanted to [goal]...

Now you fill in the blanks and continue!

{self.generate_encouragement(context, "general")}
"""
        return self.create_response(
            content=content,
            response_type=ResponseType.LESSON,
            context=context,
            requires_input=True,
            input_prompt="Share your story with me! I'd love to hear it!",
            suggestions=["Get a different prompt", "Learn about plot", "Read an example story"]
        )
    
    def _handle_reading_request(self, request: str, context: LearnerContext) -> AgentResponse:
        """Handle reading comprehension requests"""
        content = f"""
📖 **Reading Comprehension Tips, {context.name}!**

Let's become super readers together!

**Before Reading:**
- 🔍 Look at the title and pictures
- 🤔 What do you think it will be about?
- ❓ What questions do you have?

**While Reading:**
- 📝 Notice the characters and setting
- 🎯 Follow what happens
- 🤷 If confused, re-read that part

**After Reading:**
- 📋 Summarize: What happened?
- 💭 Think: What was the message?
- 🌟 Connect: Does it remind you of anything?

**The Magic Questions:**
- WHO is in the story?
- WHAT happens?
- WHERE does it happen?
- WHEN does it happen?
- WHY do things happen?
- HOW does it end?

Would you like to practice with a story?

{self.generate_encouragement(context, "general")}
"""
        return self.create_response(
            content=content,
            response_type=ResponseType.LESSON,
            context=context,
            requires_input=True,
            input_prompt="Would you like to practice reading comprehension?",
            suggestions=["Read a story together", "Practice with questions", "Learn vocabulary"]
        )
    
    def _handle_general_request(self, request: str, context: LearnerContext) -> AgentResponse:
        """Handle general storytelling requests"""
        content = f"""
📚 **Welcome to Story Weaver, {context.name}!**

I'm your magical guide to the world of stories!

**What Would You Like to Do?**

📖 **Listen** - Hear an exciting story
✏️ **Create** - Write your own story
🎓 **Learn** - Understand how stories work
🎮 **Play** - Story games and activities

**Story Types:**
- 🗡️ Adventure - Exciting journeys and quests
- 💖 Friendship - Stories about friends
- 🔍 Mystery - Solve puzzles and clues
- ✨ Fantasy - Magic and wonder

Just tell me what you'd like, and we'll begin our story adventure!

{self.generate_encouragement(context, "general")}
"""
        return self.create_response(
            content=content,
            response_type=ResponseType.LESSON,
            context=context,
            requires_input=True,
            input_prompt="What kind of story adventure would you like?",
            suggestions=["Tell me a story", "Help me write", "Learn about stories"]
        )
    
    def _get_storytelling_activities(self, topic: str, difficulty: str, context: LearnerContext) -> str:
        """Generate storytelling practice activities"""
        activities = f"""
**Activity 1: Story Starter**
Continue this story: "One morning, I woke up and found a tiny dragon in my backpack..."
Write or tell me what happens next!

**Activity 2: Character Creator**
Create a character with:
- A fun name
- A special talent
- A favorite thing

**Activity 3: Setting Detective**
Describe a place where a story could happen.
What do you see? Hear? Smell?
"""
        return activities
    
    def can_handle_topic(self, topic: str) -> bool:
        """Check if this agent can handle the given topic"""
        topic_lower = topic.lower()
        
        if any(t in topic_lower for t in self.topics):
            return True
        
        story_keywords = ["story", "read", "write", "book", "tale", "narrative",
                         "character", "fiction", "imagination", "creative"]
        return any(kw in topic_lower for kw in story_keywords)


if __name__ == "__main__":
    # Demo the Storytelling agent
    agent = StorytellingAgent()
    
    # Create a test context
    context = LearnerContext(
        learner_id="student_001",
        name="Emma",
        age=7,
        learning_style="auditory",
        interests=["princesses", "animals"]
    )
    
    print("=== Storytelling Agent Demo ===\n")
    print(f"Agent: {agent.name}")
    print(f"Description: {agent.description}\n")
    
    # Test a story request
    print("--- Generating Adventure Story ---")
    response = agent.generate_story("adventure", context)
    print(response.content[:800] + "...")
    
    # Test a lesson
    print("\n--- Character Lesson ---")
    response = agent.generate_lesson("characters", context)
    print(response.content[:500] + "...")
