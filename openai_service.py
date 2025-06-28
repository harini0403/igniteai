import json
import os
from openai import OpenAI

# the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
# do not change this unless explicitly requested by the user
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "your_openai_api_key_here")
openai_client = OpenAI(api_key=OPENAI_API_KEY)

def get_age_appropriate_explanation(question, age):
    """Generate age-appropriate explanation for a student question"""
    try:
        # Determine appropriate language level based on age
        if age <= 8:
            language_level = "very simple language with fun examples, like talking to a 6-8 year old"
            content_guide = "Use very basic concepts, short sentences, and relate to toys, animals, or everyday activities"
        elif age <= 12:
            language_level = "simple language with relatable examples, like talking to a 9-12 year old"
            content_guide = "Use elementary concepts, relate to school subjects, sports, or hobbies kids enjoy"
        elif age <= 16:
            language_level = "clear explanations with practical examples, like talking to a teenager"
            content_guide = "Use middle/high school level concepts, relate to social media, technology, or teen interests"
        else:
            language_level = "comprehensive explanations with detailed examples"
            content_guide = "Use advanced concepts while keeping explanations accessible and engaging"

        prompt = f"""
        You are a friendly AI tutor helping a {age}-year-old student understand artificial intelligence concepts.
        
        Question: {question}
        
        IMPORTANT: Only answer questions related to artificial intelligence, machine learning, robotics, computer science, and technology. If the question is not AI-related, politely redirect the student to ask about AI topics instead.
        
        Please provide an age-appropriate explanation using {language_level}.
        {content_guide}
        
        Guidelines:
        - Focus specifically on AI, machine learning, computer vision, robotics, or related technology topics
        - Keep the explanation engaging and fun
        - Use examples the student can relate to
        - Break down complex AI concepts into simple parts
        - Encourage further AI learning
        - Keep it positive and supportive
        - Avoid inappropriate content for the age group
        - If the question is not AI-related, redirect: "That's a great question, but I specialize in teaching about artificial intelligence! Try asking me about AI topics like robots, machine learning, or how computers think."
        
        Respond in JSON format with:
        {{
            "explanation": "your detailed AI-focused explanation here",
            "key_points": ["point 1", "point 2", "point 3"],
            "fun_fact": "an interesting AI-related fact",
            "suggested_activities": ["AI-related activity 1", "AI-related activity 2"]
        }}
        """

        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert AI education specialist that creates age-appropriate explanations specifically about artificial intelligence, machine learning, robotics, and computer science topics for students."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            max_tokens=1000
        )
        
        content = response.choices[0].message.content
        return json.loads(content) if content else {}
    
    except Exception as e:
        return {
            "explanation": "Sorry, I'm having trouble right now. Please try again later!",
            "key_points": ["Try asking your question again"],
            "fun_fact": "Learning is always an adventure!",
            "suggested_activities": ["Ask a teacher or parent for help"]
        }

def generate_study_plan(topic, age):
    """Generate an age-appropriate study plan for a given topic"""
    try:
        # Determine study plan complexity based on age
        if age <= 8:
            complexity = "very basic with lots of fun activities and short learning sessions"
            duration = "1-2 weeks with 15-20 minute daily activities"
        elif age <= 12:
            complexity = "elementary level with interactive activities and games"
            duration = "2-3 weeks with 30-45 minute daily sessions"
        elif age <= 16:
            complexity = "intermediate level with projects and practical applications"
            duration = "3-4 weeks with 45-60 minute daily sessions"
        else:
            complexity = "comprehensive with in-depth study and research components"
            duration = "4-6 weeks with 60-90 minute daily sessions"

        prompt = f"""
        Create a personalized AI study plan for a {age}-year-old student to learn about: {topic}
        
        IMPORTANT: Only create study plans for AI-related topics such as artificial intelligence, machine learning, robotics, computer vision, natural language processing, neural networks, etc. If the topic is not AI-related, politely redirect to suggest AI topics instead.
        
        The plan should be {complexity} and span {duration}.
        
        Include:
        - Weekly breakdown of AI learning goals
        - Age-appropriate AI activities and exercises
        - Fun ways to practice and reinforce AI learning
        - AI-focused resources suitable for the age group
        - Ways to track AI learning progress
        
        Respond in JSON format with:
        {{
            "title": "AI Study Plan Title",
            "difficulty_level": "beginner/intermediate/advanced",
            "duration": "estimated time to complete",
            "weekly_goals": [
                {{
                    "week": 1,
                    "goal": "what AI concept to learn this week",
                    "activities": ["AI-related activity 1", "AI-related activity 2", "AI-related activity 3"],
                    "resources": ["AI resource 1", "AI resource 2"]
                }}
            ],
            "progress_tracking": ["AI learning tracking method 1", "AI learning tracking method 2"],
            "fun_challenges": ["AI challenge 1", "AI challenge 2"]
        }}
        """

        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert AI education curriculum designer specializing in age-appropriate AI learning plans and artificial intelligence education."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            max_tokens=1500
        )
        
        content = response.choices[0].message.content
        return json.loads(content) if content else {}
    
    except Exception as e:
        return {
            "title": f"AI Study Plan for {topic}",
            "difficulty_level": "beginner",
            "duration": "2-3 weeks",
            "weekly_goals": [
                {
                    "week": 1,
                    "goal": f"Introduction to {topic}",
                    "activities": ["Read about AI basics", "Watch educational AI videos", "Try simple AI demos"],
                    "resources": ["AI learning websites", "Kid-friendly AI books", "Interactive AI games"]
                }
            ],
            "progress_tracking": ["Keep an AI learning journal", "Take AI knowledge quizzes"],
            "fun_challenges": ["Build a simple AI project", "Explain AI to family members"]
        }

def generate_knowledge_assessment(age, topics=None):
    """Generate an adaptive assessment to gauge student's AI knowledge level"""
    try:
        # Determine assessment complexity based on age
        if age <= 8:
            complexity = "very simple multiple choice questions with pictures and basic AI concepts"
            question_count = 5
        elif age <= 12:
            complexity = "elementary level questions covering fundamental AI concepts"
            question_count = 8
        elif age <= 16:
            complexity = "intermediate questions with practical AI applications"
            question_count = 10
        else:
            complexity = "comprehensive questions covering advanced AI topics"
            question_count = 12

        topics_text = f"focusing on: {', '.join(topics)}" if topics else "covering general AI knowledge"

        prompt = f"""
        Create an adaptive AI knowledge assessment for a {age}-year-old student {topics_text}.
        
        Generate {question_count} {complexity} that will help determine their current understanding level.
        
        Include questions about:
        - Basic AI concepts (what is AI, how it works)
        - Machine learning fundamentals
        - Real-world AI applications
        - AI ethics and safety (age-appropriate)
        - Future of AI technology
        
        Each question should have:
        - Clear, age-appropriate language
        - 4 multiple choice options (A, B, C, D)
        - One correct answer
        - Brief explanation of why the answer is correct
        
        Respond in JSON format with:
        {{
            "title": "AI Knowledge Assessment",
            "age_group": "{age} years old",
            "total_questions": {question_count},
            "estimated_time": "time to complete",
            "questions": [
                {{
                    "id": 1,
                    "question": "question text here",
                    "options": {{
                        "A": "option A",
                        "B": "option B", 
                        "C": "option C",
                        "D": "option D"
                    }},
                    "correct_answer": "A",
                    "explanation": "why this answer is correct",
                    "topic": "AI concept being tested",
                    "difficulty": "easy/medium/hard"
                }}
            ]
        }}
        """

        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert AI education assessment designer who creates age-appropriate quizzes to evaluate students' understanding of artificial intelligence concepts."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            max_tokens=2000
        )
        
        content = response.choices[0].message.content
        if content is None:
            return {}
        return json.loads(content)
    
    except Exception as e:
        return {
            "title": "AI Knowledge Assessment",
            "age_group": f"{age} years old",
            "total_questions": 5,
            "estimated_time": "10-15 minutes",
            "questions": [
                {
                    "id": 1,
                    "question": "What is Artificial Intelligence?",
                    "options": {
                        "A": "A computer that can think like humans",
                        "B": "A robot that looks like a person",
                        "C": "A video game character",
                        "D": "A type of smartphone"
                    },
                    "correct_answer": "A",
                    "explanation": "AI is technology that allows computers to perform tasks that typically require human intelligence.",
                    "topic": "AI Basics",
                    "difficulty": "easy"
                }
            ]
        }

def generate_personalized_roadmap(age, current_level, strong_topics=None, weak_topics=None):
    """Generate a personalized learning roadmap based on assessment results"""
    # Initialize variables for scope
    duration = "8-12 weeks"
    session_length = "30-45 minutes"
    
    try:
        strong_text = f"Strong areas: {', '.join(strong_topics)}" if strong_topics else "No identified strengths yet"
        weak_text = f"Areas to improve: {', '.join(weak_topics)}" if weak_topics else "No identified weaknesses yet"
        
        if age <= 8:
            duration = "4-6 weeks"
            session_length = "15-20 minutes"
        elif age <= 12:
            duration = "6-8 weeks"
            session_length = "25-30 minutes"
        elif age <= 16:
            duration = "8-10 weeks"
            session_length = "30-45 minutes"
        else:
            duration = "10-12 weeks"
            session_length = "45-60 minutes"

        prompt = f"""
        Create a personalized AI learning roadmap for a {age}-year-old student.
        
        Current Knowledge Level: {current_level}
        {strong_text}
        {weak_text}
        
        The roadmap should span {duration} with {session_length} daily sessions.
        
        Structure the roadmap to:
        - Build on their strengths
        - Address weak areas with extra support
        - Progress logically from their current level
        - Include hands-on projects and activities
        - Provide regular assessment checkpoints
        
        Respond in JSON format with:
        {{
            "title": "Personalized AI Learning Roadmap",
            "student_level": "{current_level}",
            "duration": "{duration}",
            "daily_commitment": "{session_length}",
            "learning_path": [
                {{
                    "phase": 1,
                    "title": "Phase title",
                    "duration": "weeks X-Y",
                    "focus_areas": ["topic 1", "topic 2"],
                    "goals": ["goal 1", "goal 2"],
                    "activities": ["activity 1", "activity 2"],
                    "assessment": "how progress will be measured"
                }}
            ],
            "milestones": [
                {{
                    "week": 2,
                    "milestone": "what student should achieve",
                    "assessment_type": "quiz/project/discussion"
                }}
            ],
            "resources": {{
                "beginner": ["resource 1", "resource 2"],
                "intermediate": ["resource 1", "resource 2"],
                "advanced": ["resource 1", "resource 2"]
            }},
            "success_metrics": ["how to measure overall progress"]
        }}
        """

        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert AI education advisor who creates personalized learning paths based on individual student assessments and abilities."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            max_tokens=2000
        )
        
        content = response.choices[0].message.content
        if content is None:
            return {}
        return json.loads(content)
    
    except Exception as e:
        # Set default values for variables
        duration = "8-12 weeks"
        session_length = "30-45 minutes"
        
        return {
            "title": "Personalized AI Learning Roadmap",
            "student_level": current_level,
            "duration": duration,
            "daily_commitment": session_length,
            "learning_path": [
                {
                    "phase": 1,
                    "title": "AI Foundations",
                    "duration": "weeks 1-2",
                    "focus_areas": ["What is AI", "AI in daily life"],
                    "goals": ["Understand basic AI concepts", "Identify AI in everyday tools"],
                    "activities": ["Watch AI videos", "Try AI apps", "Draw AI examples"],
                    "assessment": "Simple quiz on AI basics"
                }
            ],
            "milestones": [
                {
                    "week": 2,
                    "milestone": "Can explain what AI is in simple terms",
                    "assessment_type": "verbal explanation"
                }
            ],
            "resources": {
                "beginner": ["AI4ALL educational content", "Scratch programming"],
                "intermediate": ["MIT AI courses", "Python basics"],
                "advanced": ["TensorFlow tutorials", "AI research papers"]
            },
            "success_metrics": ["Regular quiz scores", "Project completion", "Engagement level"]
        }
