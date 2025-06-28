from flask import render_template, request, redirect, url_for, flash, jsonify
from app import app, db
from models import Question, StudyPlan
from openai_service import get_age_appropriate_explanation, generate_study_plan
import logging

@app.route('/')
def index():
    """Homepage with introduction and navigation"""
    return render_template('index.html')

@app.route('/ask_question', methods=['GET', 'POST'])
def ask_question():
    """Page for students to ask questions and get AI explanations"""
    if request.method == 'POST':
        try:
            # Get form data
            age = request.form.get('age', type=int)
            question = request.form.get('question', '').strip()
            
            # Validate input
            if not age or age < 5 or age > 18:
                flash('Please enter a valid age between 5 and 18.', 'error')
                return render_template('ask_question.html')
            
            if not question:
                flash('Please enter a question.', 'error')
                return render_template('ask_question.html')
            
            if len(question) < 10:
                flash('Please enter a more detailed question (at least 10 characters).', 'error')
                return render_template('ask_question.html')
            
            # Get AI explanation
            ai_response = get_age_appropriate_explanation(question, age)
            
            # Save to database
            question_record = Question(
                student_age=age,
                question=question,
                ai_response=str(ai_response),
                topic=question[:50]  # Use first 50 chars as topic
            )
            db.session.add(question_record)
            db.session.commit()
            
            return render_template('explanation.html', 
                                 question=question, 
                                 age=age, 
                                 ai_response=ai_response)
        
        except Exception as e:
            logging.error(f"Error processing question: {e}")
            flash('Something went wrong. Please try again!', 'error')
            return render_template('ask_question.html')
    
    return render_template('ask_question.html')

@app.route('/study_plan', methods=['GET', 'POST'])
def study_plan():
    """Page for generating personalized study plans"""
    if request.method == 'POST':
        try:
            # Get form data
            age = request.form.get('age', type=int)
            topic = request.form.get('topic', '').strip()
            
            # Validate input
            if not age or age < 5 or age > 18:
                flash('Please enter a valid age between 5 and 18.', 'error')
                return render_template('study_plan.html')
            
            if not topic:
                flash('Please enter a topic to study.', 'error')
                return render_template('study_plan.html')
            
            if len(topic) < 3:
                flash('Please enter a more specific topic (at least 3 characters).', 'error')
                return render_template('study_plan.html')
            
            # Generate study plan
            plan_data = generate_study_plan(topic, age)
            
            # Save to database
            study_plan_record = StudyPlan(
                student_age=age,
                topic=topic,
                plan_content=str(plan_data),
                difficulty_level=plan_data.get('difficulty_level', 'beginner')
            )
            db.session.add(study_plan_record)
            db.session.commit()
            
            return render_template('study_plan.html', 
                                 topic=topic, 
                                 age=age, 
                                 plan_data=plan_data,
                                 show_plan=True)
        
        except Exception as e:
            logging.error(f"Error generating study plan: {e}")
            flash('Something went wrong. Please try again!', 'error')
            return render_template('study_plan.html')
    
    return render_template('study_plan.html')

@app.route('/recent_questions')
def recent_questions():
    """Display recent questions and explanations"""
    try:
        questions = Question.query.order_by(Question.created_at.desc()).limit(10).all()
        return render_template('recent_questions.html', questions=questions)
    except Exception as e:
        logging.error(f"Error fetching recent questions: {e}")
        flash('Unable to load recent questions.', 'error')
        return redirect(url_for('index'))

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
