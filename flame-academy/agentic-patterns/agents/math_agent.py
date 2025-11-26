"""
Math Educational Agent

Specialized agent for teaching mathematics through interactive
problems, visualizations, and step-by-step guidance.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Tuple
from datetime import datetime
import random

from .base_educational_agent import (
    BaseEducationalAgent,
    AgentCapability,
    AgentResponse,
    LearnerContext,
    ResponseType
)


class MathAgent(BaseEducationalAgent):
    """
    Mathematics learning agent specializing in arithmetic,
    problem-solving, and mathematical thinking for children.
    """
    
    def __init__(self):
        super().__init__(
            agent_id="math_wizard",
            name="Math Wizard",
            subject="math",
            description="Your friendly helper for all things math! Let's make numbers fun!",
            min_age=4,
            max_age=12,
            capabilities=[
                AgentCapability.TEACH,
                AgentCapability.PRACTICE,
                AgentCapability.ASSESS,
                AgentCapability.EXPLAIN,
                AgentCapability.ENCOURAGE,
                AgentCapability.ADAPT,
                AgentCapability.GAMIFY,
                AgentCapability.VISUALIZE
            ]
        )
        
        # Math topics by difficulty
        self.topics_by_level = {
            "beginner": ["counting", "numbers", "shapes", "patterns", "comparing"],
            "elementary": ["addition", "subtraction", "simple multiplication", "time", "money"],
            "intermediate": ["multiplication", "division", "fractions", "measurement", "geometry"],
            "advanced": ["decimals", "percentages", "algebra basics", "word problems", "data"]
        }
        
        # Visual representations for math
        self.visual_objects = {
            "apple": "🍎",
            "star": "⭐",
            "heart": "❤️",
            "cookie": "🍪",
            "ball": "⚽",
            "flower": "🌸",
            "fish": "🐟",
            "bird": "🐦"
        }
    
    def process_request(self, request: str, context: LearnerContext) -> AgentResponse:
        """Process a math learning request"""
        request_lower = request.lower()
        
        # Detect intent
        if any(word in request_lower for word in ["problem", "practice", "quiz", "exercise"]):
            return self._handle_practice_request(request, context)
        elif any(word in request_lower for word in ["help", "how", "explain", "understand"]):
            return self._handle_help_request(request, context)
        elif any(word in request_lower for word in ["learn", "teach", "what is"]):
            topic = self._extract_topic(request)
            return self.generate_lesson(topic, context)
        elif any(op in request_lower for op in ["+", "-", "×", "÷", "plus", "minus", "times", "divided"]):
            return self._handle_calculation_request(request, context)
        else:
            return self._handle_general_request(request, context)
    
    def generate_lesson(self, topic: str, context: LearnerContext) -> AgentResponse:
        """Generate a math lesson on a topic"""
        topic_lower = topic.lower()
        
        # Route to specific lesson generators
        if "add" in topic_lower:
            return self._generate_addition_lesson(context)
        elif "subtract" in topic_lower:
            return self._generate_subtraction_lesson(context)
        elif "multipl" in topic_lower:
            return self._generate_multiplication_lesson(context)
        elif "divid" in topic_lower or "divis" in topic_lower:
            return self._generate_division_lesson(context)
        elif "count" in topic_lower:
            return self._generate_counting_lesson(context)
        elif "shape" in topic_lower:
            return self._generate_shapes_lesson(context)
        elif "fraction" in topic_lower:
            return self._generate_fractions_lesson(context)
        else:
            return self._generate_general_math_lesson(topic, context)
    
    def generate_practice(self, topic: str, context: LearnerContext, difficulty: str = "medium") -> AgentResponse:
        """Generate math practice problems"""
        topic_lower = topic.lower()
        
        # Get appropriate problems
        if "add" in topic_lower:
            problems = self._generate_addition_problems(context.age, difficulty)
        elif "subtract" in topic_lower:
            problems = self._generate_subtraction_problems(context.age, difficulty)
        elif "multipl" in topic_lower:
            problems = self._generate_multiplication_problems(context.age, difficulty)
        else:
            problems = self._generate_mixed_problems(context.age, difficulty)
        
        content = f"""
🔢 **Math Practice Time, {context.name}!**

Let's solve some problems together!

{problems}

**Tips:**
- Take your time
- You can draw pictures to help
- Check your work by counting

{self.generate_encouragement(context, "general")}
"""
        return self.create_response(
            content=content,
            response_type=ResponseType.QUESTION,
            context=context,
            requires_input=True,
            input_prompt="Tell me your answers! You can do it!",
            suggestions=["Get a hint", "Try easier problems", "Try harder problems"]
        )
    
    def check_answer(self, problem: str, answer: str, context: LearnerContext) -> AgentResponse:
        """Check a math answer and provide feedback"""
        try:
            # Parse the problem to get expected answer
            expected = self._evaluate_problem(problem)
            given = float(answer.strip())
            
            is_correct = abs(expected - given) < 0.001
            
            if is_correct:
                feedback = self.generate_encouragement(context, "success")
                response_type = ResponseType.FEEDBACK
                suggestions = ["Try another problem", "Learn something new", "Try harder problems"]
            else:
                feedback = self._generate_hint(problem, expected, given, context)
                response_type = ResponseType.HINT
                suggestions = ["Try again", "Get more help", "Try an easier problem"]
            
            content = f"""
{feedback}

{"✅ **CORRECT!**" if is_correct else "❌ **Not quite right...**"}

**Your answer:** {answer}
{"" if is_correct else f"**Let's figure it out together!**"}
"""
            
            return self.create_response(
                content=content,
                response_type=response_type,
                context=context,
                requires_input=not is_correct,
                input_prompt="Would you like to try again?" if not is_correct else None,
                suggestions=suggestions
            )
        except Exception:
            return self.create_response(
                content="Hmm, I couldn't understand that problem. Can you try writing it differently?",
                response_type=ResponseType.FEEDBACK,
                context=context,
                requires_input=True,
                suggestions=["Try a practice problem", "Get help"]
            )
    
    def _generate_addition_lesson(self, context: LearnerContext) -> AgentResponse:
        """Generate an addition lesson"""
        if context.age < 7:
            content = f"""
➕ **Let's Learn Addition, {context.name}!**

Addition means putting numbers together to make MORE!

**The Plus Sign: +**
When you see +, it means "put together" or "add"

**Let's Try With Pictures!**
🍎🍎 + 🍎 = ?

Count the apples:
🍎🍎 (that's 2)
🍎 (that's 1)
Put them together: 🍎🍎🍎 (that's 3!)

**So: 2 + 1 = 3**

**Your Turn!**
Try counting these:
⭐⭐ + ⭐⭐ = ?

Count all the stars to find the answer!

{self.generate_encouragement(context, "general")}
"""
        else:
            content = f"""
➕ **Mastering Addition, {context.name}!**

Addition combines numbers to find their total (sum).

**Addition Vocabulary:**
- **Addends**: The numbers being added (3 + 5: both 3 and 5 are addends)
- **Sum**: The answer (3 + 5 = 8: 8 is the sum)
- **Plus Sign (+)**: Means "add together"

**Addition Strategies:**

1️⃣ **Count On**
   Start with the bigger number, count up from there
   7 + 3: Start at 7, count "8, 9, 10"

2️⃣ **Make a Ten**
   8 + 5: Think "8 + 2 = 10, then + 3 more = 13"

3️⃣ **Doubles**
   6 + 6 = 12 (memorize these!)

4️⃣ **Near Doubles**
   6 + 7 = 6 + 6 + 1 = 13

**Practice Problem:**
If you have 15 stickers and your friend gives you 8 more,
how many stickers do you have now?

{self.generate_encouragement(context, "general")}
"""
        return self.create_response(
            content=content,
            response_type=ResponseType.LESSON,
            context=context,
            requires_input=True,
            input_prompt="What's your answer? Take your time!",
            suggestions=["Practice more addition", "Learn subtraction", "Play a math game"]
        )
    
    def _generate_subtraction_lesson(self, context: LearnerContext) -> AgentResponse:
        """Generate a subtraction lesson"""
        if context.age < 7:
            content = f"""
➖ **Let's Learn Subtraction, {context.name}!**

Subtraction means taking away to find what's LEFT!

**The Minus Sign: -**
When you see -, it means "take away"

**Let's Try With Pictures!**
🍪🍪🍪🍪🍪 - 🍪🍪 = ?

Start with 5 cookies: 🍪🍪🍪🍪🍪
Take away 2: ❌❌🍪🍪🍪
What's left? 🍪🍪🍪 (3 cookies!)

**So: 5 - 2 = 3**

**Your Turn!**
❤️❤️❤️❤️ - ❤️ = ?

How many hearts are left?

{self.generate_encouragement(context, "general")}
"""
        else:
            content = f"""
➖ **Mastering Subtraction, {context.name}!**

Subtraction finds the difference between numbers.

**Subtraction Vocabulary:**
- **Minuend**: The number you start with (8 - 3: 8 is minuend)
- **Subtrahend**: The number you take away (8 - 3: 3 is subtrahend)
- **Difference**: The answer (8 - 3 = 5: 5 is the difference)

**Subtraction Strategies:**

1️⃣ **Count Back**
   10 - 3: Start at 10, count "9, 8, 7"

2️⃣ **Think Addition**
   15 - 8 = ? Think: 8 + ? = 15 → 8 + 7 = 15, so 15 - 8 = 7

3️⃣ **Break Apart**
   14 - 6: Take away 4 first (14 - 4 = 10), then 2 more (10 - 2 = 8)

**Practice Problem:**
You have 23 candies. You give 9 to your friend.
How many candies do you have left?

{self.generate_encouragement(context, "general")}
"""
        return self.create_response(
            content=content,
            response_type=ResponseType.LESSON,
            context=context,
            requires_input=True,
            input_prompt="Tell me your answer!",
            suggestions=["Practice subtraction", "Learn addition", "Try word problems"]
        )
    
    def _generate_multiplication_lesson(self, context: LearnerContext) -> AgentResponse:
        """Generate a multiplication lesson"""
        content = f"""
✖️ **Let's Learn Multiplication, {context.name}!**

Multiplication is a fast way to add the same number many times!

**The Times Sign: ×**
3 × 4 means "3 groups of 4" or "add 4 three times"

**Let's See It!**
3 × 4 = ?

Group 1: ⭐⭐⭐⭐ (4 stars)
Group 2: ⭐⭐⭐⭐ (4 stars)
Group 3: ⭐⭐⭐⭐ (4 stars)

Count all: 4 + 4 + 4 = 12
**So: 3 × 4 = 12**

**Easy Way to Remember:**
```
    ×  | 1  2  3  4  5
   ----+----------------
    1  | 1  2  3  4  5
    2  | 2  4  6  8  10
    3  | 3  6  9  12 15
    4  | 4  8  12 16 20
    5  | 5  10 15 20 25
```

**Your Turn!**
If you have 4 bags with 5 marbles in each bag,
how many marbles do you have in total?

{self.generate_encouragement(context, "general")}
"""
        return self.create_response(
            content=content,
            response_type=ResponseType.LESSON,
            context=context,
            requires_input=True,
            input_prompt="What's your answer?",
            suggestions=["Practice times tables", "Learn division", "Try more problems"]
        )
    
    def _generate_division_lesson(self, context: LearnerContext) -> AgentResponse:
        """Generate a division lesson"""
        content = f"""
➗ **Let's Learn Division, {context.name}!**

Division means sharing equally or making groups!

**The Division Sign: ÷**
12 ÷ 3 means "split 12 into 3 equal groups"

**Let's See It!**
12 ÷ 3 = ?

Start with 12 cookies: 🍪🍪🍪🍪🍪🍪🍪🍪🍪🍪🍪🍪
Share among 3 friends:

Friend 1: 🍪🍪🍪🍪 (4 cookies)
Friend 2: 🍪🍪🍪🍪 (4 cookies)
Friend 3: 🍪🍪🍪🍪 (4 cookies)

Each friend gets 4!
**So: 12 ÷ 3 = 4**

**Connection to Multiplication:**
Division is the opposite of multiplication!
- If 3 × 4 = 12, then 12 ÷ 3 = 4

**Your Turn!**
You have 20 stickers to share equally among 4 friends.
How many stickers does each friend get?

{self.generate_encouragement(context, "general")}
"""
        return self.create_response(
            content=content,
            response_type=ResponseType.LESSON,
            context=context,
            requires_input=True,
            input_prompt="How many stickers for each friend?",
            suggestions=["Practice division", "Learn multiplication", "Try word problems"]
        )
    
    def _generate_counting_lesson(self, context: LearnerContext) -> AgentResponse:
        """Generate a counting lesson"""
        content = f"""
🔢 **Let's Learn Counting, {context.name}!**

Counting tells us HOW MANY things there are!

**Count With Me!**
1️⃣ One
2️⃣ Two
3️⃣ Three
4️⃣ Four
5️⃣ Five
6️⃣ Six
7️⃣ Seven
8️⃣ Eight
9️⃣ Nine
🔟 Ten

**Let's Practice!**
Count the stars: ⭐⭐⭐⭐⭐⭐

That's 6 stars!

**Counting Tips:**
- 👆 Point to each thing as you count
- 🎵 Count slowly and carefully
- ✅ Count each thing only once!

**Your Turn!**
How many fish do you see?
🐟🐟🐟🐟🐟🐟🐟🐟

Count them carefully!

{self.generate_encouragement(context, "general")}
"""
        return self.create_response(
            content=content,
            response_type=ResponseType.LESSON,
            context=context,
            requires_input=True,
            input_prompt="How many fish did you count?",
            suggestions=["Count more things", "Learn numbers", "Practice counting"]
        )
    
    def _generate_shapes_lesson(self, context: LearnerContext) -> AgentResponse:
        """Generate a shapes lesson"""
        content = f"""
🔷 **Let's Learn Shapes, {context.name}!**

Shapes are all around us!

**Basic Shapes:**

⬜ **Square**
- 4 sides (all the same length!)
- 4 corners
- Like a window or a cracker

🔺 **Triangle**
- 3 sides
- 3 corners
- Like a slice of pizza!

⭕ **Circle**
- Round with no corners
- Like a ball or the sun

▬ **Rectangle**
- 4 sides (2 long, 2 short)
- 4 corners
- Like a door or a book

**Shape Hunt!**
Look around you right now. Can you find:
- Something shaped like a circle? 
- Something shaped like a rectangle?
- Something shaped like a triangle?

**Your Turn!**
What shapes can you see in your room right now?

{self.generate_encouragement(context, "general")}
"""
        return self.create_response(
            content=content,
            response_type=ResponseType.LESSON,
            context=context,
            requires_input=True,
            input_prompt="Tell me what shapes you found!",
            suggestions=["Learn more shapes", "Draw shapes", "Count shapes"]
        )
    
    def _generate_fractions_lesson(self, context: LearnerContext) -> AgentResponse:
        """Generate a fractions lesson"""
        content = f"""
🍕 **Let's Learn Fractions, {context.name}!**

Fractions show PARTS of a whole!

**What is a Fraction?**
When we split something into equal pieces, each piece is a fraction.

**Pizza Example:**
Imagine a pizza cut into 4 equal slices: 🍕🍕🍕🍕

If you eat 1 slice, you ate 1/4 (one-fourth) of the pizza!
- **1** = number of slices you ate (numerator)
- **4** = total slices the pizza was cut into (denominator)

**Reading Fractions:**
- 1/2 = "one half" (one out of two pieces)
- 1/4 = "one fourth" (one out of four pieces)
- 3/4 = "three fourths" (three out of four pieces)

**Visual Example:**
Half (1/2): [▓▓▓▓|░░░░]
One Fourth (1/4): [▓▓|░░|░░|░░]
Three Fourths (3/4): [▓▓|▓▓|▓▓|░░]

**Your Turn!**
If a cake is cut into 8 pieces and you eat 2 pieces,
what fraction of the cake did you eat?

{self.generate_encouragement(context, "general")}
"""
        return self.create_response(
            content=content,
            response_type=ResponseType.LESSON,
            context=context,
            requires_input=True,
            input_prompt="What fraction did you eat?",
            suggestions=["Practice fractions", "Learn about halves", "Try fraction problems"]
        )
    
    def _generate_general_math_lesson(self, topic: str, context: LearnerContext) -> AgentResponse:
        """Generate a general math lesson"""
        content = f"""
🧮 **Math Adventure: {topic.title()}, {context.name}!**

Math is like a superpower - it helps us understand the world!

**Why Math is Amazing:**
- 🛒 It helps us buy things at the store
- ⏰ It helps us tell time
- 🏠 It helps us measure and build
- 🎮 It's in all our favorite games!

**Math Tools:**
- Numbers (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
- Operations (+, -, ×, ÷)
- Shapes and patterns
- Problem-solving skills

**What would you like to learn about?**
- ➕ Addition (putting together)
- ➖ Subtraction (taking away)
- ✖️ Multiplication (groups of numbers)
- ➗ Division (sharing equally)
- 🔷 Shapes
- 🔢 Counting
- 🍕 Fractions

{self.generate_encouragement(context, "general")}
"""
        return self.create_response(
            content=content,
            response_type=ResponseType.LESSON,
            context=context,
            requires_input=True,
            input_prompt="What math topic interests you?",
            suggestions=["Learn addition", "Learn multiplication", "Practice problems"]
        )
    
    def _generate_addition_problems(self, age: int, difficulty: str) -> str:
        """Generate addition problems based on age and difficulty"""
        problems = []
        
        if age < 7 or difficulty == "easy":
            # Single digit, small numbers
            for i in range(3):
                a, b = random.randint(1, 5), random.randint(1, 5)
                obj = random.choice(list(self.visual_objects.values()))
                visual = obj * a + " + " + obj * b + " = ?"
                problems.append(f"**{i+1}.** {a} + {b} = ?\n   {visual}")
        elif difficulty == "hard":
            # Double digit
            for i in range(3):
                a, b = random.randint(10, 50), random.randint(10, 50)
                problems.append(f"**{i+1}.** {a} + {b} = ?")
        else:
            # Single to double digit
            for i in range(3):
                a, b = random.randint(5, 20), random.randint(5, 20)
                problems.append(f"**{i+1}.** {a} + {b} = ?")
        
        return "\n\n".join(problems)
    
    def _generate_subtraction_problems(self, age: int, difficulty: str) -> str:
        """Generate subtraction problems"""
        problems = []
        
        if age < 7 or difficulty == "easy":
            for i in range(3):
                a = random.randint(5, 10)
                b = random.randint(1, a)
                obj = random.choice(list(self.visual_objects.values()))
                visual = obj * a + f" - {b} = ?"
                problems.append(f"**{i+1}.** {a} - {b} = ?\n   {visual}")
        else:
            for i in range(3):
                a = random.randint(20, 50)
                b = random.randint(5, a)
                problems.append(f"**{i+1}.** {a} - {b} = ?")
        
        return "\n\n".join(problems)
    
    def _generate_multiplication_problems(self, age: int, difficulty: str) -> str:
        """Generate multiplication problems"""
        problems = []
        
        if difficulty == "easy":
            for i in range(3):
                a, b = random.randint(1, 5), random.randint(1, 5)
                problems.append(f"**{i+1}.** {a} × {b} = ?")
        elif difficulty == "hard":
            for i in range(3):
                a, b = random.randint(6, 12), random.randint(6, 12)
                problems.append(f"**{i+1}.** {a} × {b} = ?")
        else:
            for i in range(3):
                a, b = random.randint(2, 10), random.randint(2, 10)
                problems.append(f"**{i+1}.** {a} × {b} = ?")
        
        return "\n\n".join(problems)
    
    def _generate_mixed_problems(self, age: int, difficulty: str) -> str:
        """Generate mixed math problems"""
        problems = []
        
        if age < 7:
            ops = ["+", "-"]
            max_num = 10
        else:
            ops = ["+", "-", "×"]
            max_num = 20 if difficulty != "hard" else 50
        
        for i in range(3):
            op = random.choice(ops)
            if op == "-":
                a = random.randint(5, max_num)
                b = random.randint(1, a)
            elif op == "×":
                a, b = random.randint(2, 10), random.randint(2, 10)
            else:
                a, b = random.randint(1, max_num), random.randint(1, max_num)
            
            problems.append(f"**{i+1}.** {a} {op} {b} = ?")
        
        return "\n\n".join(problems)
    
    def _evaluate_problem(self, problem: str) -> float:
        """Safely evaluate a simple math problem"""
        # Clean and parse the problem
        problem = problem.replace("×", "*").replace("÷", "/").replace("x", "*")
        problem = problem.replace("=", "").replace("?", "").strip()
        
        # Only allow safe characters
        allowed = set("0123456789+-*/. ()")
        if not all(c in allowed for c in problem):
            raise ValueError("Invalid characters in problem")
        
        return eval(problem)
    
    def _generate_hint(self, problem: str, expected: float, given: float, context: LearnerContext) -> str:
        """Generate a helpful hint for an incorrect answer"""
        hints = [
            f"🤔 Let's think about this together, {context.name}!",
            f"💡 Here's a hint to help you, {context.name}:",
            f"🌟 You're close! Let me help, {context.name}:"
        ]
        
        hint = random.choice(hints)
        
        if given < expected:
            hint += "\nYour answer is a little too small. Try counting again!"
        else:
            hint += "\nYour answer is a little too big. Let's count more carefully!"
        
        hint += f"\n\n{self.generate_encouragement(context, 'mistake')}"
        
        return hint
    
    def _extract_topic(self, request: str) -> str:
        """Extract the math topic from a request"""
        request_lower = request.lower()
        
        topic_keywords = {
            "addition": ["add", "plus", "sum"],
            "subtraction": ["subtract", "minus", "take away", "difference"],
            "multiplication": ["multiply", "times", "product"],
            "division": ["divide", "split", "share"],
            "counting": ["count", "number"],
            "shapes": ["shape", "circle", "square", "triangle"],
            "fractions": ["fraction", "half", "quarter"]
        }
        
        for topic, keywords in topic_keywords.items():
            if any(kw in request_lower for kw in keywords):
                return topic
        
        return "math"
    
    def _handle_practice_request(self, request: str, context: LearnerContext) -> AgentResponse:
        """Handle practice problem requests"""
        topic = self._extract_topic(request)
        
        # Determine difficulty from recent performance
        if context.average_recent_performance < 0.5:
            difficulty = "easy"
        elif context.average_recent_performance > 0.8:
            difficulty = "hard"
        else:
            difficulty = "medium"
        
        return self.generate_practice(topic, context, difficulty)
    
    def _handle_help_request(self, request: str, context: LearnerContext) -> AgentResponse:
        """Handle help requests"""
        topic = self._extract_topic(request)
        
        content = f"""
🆘 **Let Me Help You, {context.name}!**

I can see you want help with {topic}. No worries - that's what I'm here for!

**Remember:**
- Take your time - there's no rush
- It's okay to not know something yet
- Asking for help is SMART!

Let me show you step by step...

"""
        # Add topic-specific help
        return self.generate_lesson(topic, context)
    
    def _handle_calculation_request(self, request: str, context: LearnerContext) -> AgentResponse:
        """Handle direct calculation requests"""
        try:
            result = self._evaluate_problem(request)
            
            content = f"""
🧮 **Let's solve this, {context.name}!**

Problem: {request}

**Answer: {result}**

**How we got it:**
{self._explain_calculation(request, result)}

{self.generate_encouragement(context, "success")}
"""
            return self.create_response(
                content=content,
                response_type=ResponseType.EXPLANATION,
                context=context,
                suggestions=["Try another problem", "Learn more about this", "Practice on your own"]
            )
        except Exception:
            return self.create_response(
                content=f"I couldn't understand that problem, {context.name}. Can you write it more clearly?",
                response_type=ResponseType.FEEDBACK,
                context=context,
                requires_input=True,
                suggestions=["Try a practice problem", "Ask for help"]
            )
    
    def _explain_calculation(self, problem: str, result: float) -> str:
        """Generate a simple explanation of the calculation"""
        if "+" in problem:
            return f"We added the numbers together to get {result}!"
        elif "-" in problem:
            return f"We subtracted to find the difference: {result}!"
        elif "×" in problem or "*" in problem or "x" in problem.lower():
            return f"We multiplied the numbers to get {result}!"
        elif "÷" in problem or "/" in problem:
            return f"We divided to share equally and got {result}!"
        return f"The answer is {result}!"
    
    def _handle_general_request(self, request: str, context: LearnerContext) -> AgentResponse:
        """Handle general math requests"""
        content = f"""
🧙‍♂️ **Welcome to Math Wizard, {context.name}!**

I'm so excited to explore math with you!

**What Would You Like to Do?**

📚 **Learn** - New math concepts
✏️ **Practice** - Solve fun problems
🎮 **Play** - Math games and challenges
❓ **Ask** - Any math question

**Math Topics We Can Explore:**
- 🔢 Counting and Numbers
- ➕ Addition (putting together)
- ➖ Subtraction (taking away)
- ✖️ Multiplication (groups)
- ➗ Division (sharing)
- 🔷 Shapes and Geometry
- 🍕 Fractions

**Quick Math Fact:**
Did you know? The word "hundred" comes from a word meaning "long finger" 
because people used to count on their ten fingers, then start over!

{self.generate_encouragement(context, "general")}
"""
        return self.create_response(
            content=content,
            response_type=ResponseType.LESSON,
            context=context,
            requires_input=True,
            input_prompt="What math adventure would you like to go on?",
            suggestions=["Practice addition", "Learn multiplication", "Solve word problems"]
        )
    
    def can_handle_topic(self, topic: str) -> bool:
        """Check if this agent can handle the given topic"""
        topic_lower = topic.lower()
        
        # Check all topic levels
        all_topics = []
        for topics in self.topics_by_level.values():
            all_topics.extend(topics)
        
        if any(t in topic_lower for t in all_topics):
            return True
        
        math_keywords = ["math", "number", "calculate", "add", "subtract", 
                        "multiply", "divide", "count", "fraction", "arithmetic"]
        return any(kw in topic_lower for kw in math_keywords)


if __name__ == "__main__":
    # Demo the Math agent
    agent = MathAgent()
    
    # Create a test context
    context = LearnerContext(
        learner_id="student_001",
        name="Sam",
        age=7,
        learning_style="visual",
        interests=["dinosaurs", "space"]
    )
    
    print("=== Math Agent Demo ===\n")
    print(f"Agent: {agent.name}")
    print(f"Description: {agent.description}\n")
    
    # Test a lesson
    print("--- Addition Lesson ---")
    response = agent.generate_lesson("addition", context)
    print(response.content[:600] + "...")
    
    # Test practice problems
    print("\n--- Practice Problems ---")
    response = agent.generate_practice("addition", context, "easy")
    print(response.content)
