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
