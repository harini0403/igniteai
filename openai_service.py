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
        
        return json.loads(response.choices[0].message.content)
    
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
        
        return json.loads(response.choices[0].message.content)
    
    except Exception as e:
        return {
            "title": f"Study Plan for {topic}",
            "difficulty_level": "beginner",
            "duration": "2-3 weeks",
            "weekly_goals": [
                {
                    "week": 1,
                    "goal": f"Introduction to {topic}",
                    "activities": ["Read about the basics", "Watch educational videos", "Practice with simple exercises"],
                    "resources": ["Library books", "Educational websites", "Ask a teacher"]
                }
            ],
            "progress_tracking": ["Keep a learning journal", "Take practice quizzes"],
            "fun_challenges": ["Teach someone else what you learned", "Create a poster or presentation"]
        }
