from app import db
from datetime import datetime

class Question(db.Model):
    """Model to store student questions and AI responses"""
    id = db.Column(db.Integer, primary_key=True)
    student_age = db.Column(db.Integer, nullable=False)
    question = db.Column(db.Text, nullable=False)
    ai_response = db.Column(db.Text, nullable=False)
    topic = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class StudyPlan(db.Model):
    """Model to store generated study plans"""
    id = db.Column(db.Integer, primary_key=True)
    student_age = db.Column(db.Integer, nullable=False)
    topic = db.Column(db.String(100), nullable=False)
    plan_content = db.Column(db.Text, nullable=False)
    difficulty_level = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Quiz(db.Model):
    """Model to store generated quizzes"""
    id = db.Column(db.Integer, primary_key=True)
    student_age = db.Column(db.Integer, nullable=False)
    topic = db.Column(db.String(100), nullable=False)
    quiz_content = db.Column(db.Text, nullable=False)
    difficulty_level = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Assessment(db.Model):
    """Model to store student assessment results"""
    id = db.Column(db.Integer, primary_key=True)
    student_age = db.Column(db.Integer, nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=True)
    score = db.Column(db.Integer, nullable=False)  # Score out of total questions
    total_questions = db.Column(db.Integer, nullable=False)
    knowledge_level = db.Column(db.String(20), nullable=False)  # beginner, intermediate, advanced
    topics_assessed = db.Column(db.Text, nullable=False)  # JSON string of topics
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class StudentProfile(db.Model):
    """Model to track student learning progress and preferences"""
    id = db.Column(db.Integer, primary_key=True)
    student_age = db.Column(db.Integer, nullable=False)
    current_level = db.Column(db.String(20), nullable=False, default='beginner')
    strong_topics = db.Column(db.Text, nullable=True)  # JSON string of topics they're good at
    weak_topics = db.Column(db.Text, nullable=True)  # JSON string of topics to improve
    learning_style = db.Column(db.String(50), nullable=True)  # visual, hands-on, reading, etc.
    completed_assessments = db.Column(db.Integer, default=0)
    last_assessment_date = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
