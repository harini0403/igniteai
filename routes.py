from flask import render_template, request, redirect, url_for, flash, jsonify, session
from app import app, db
from models import Question, StudyPlan, Quiz, Assessment, StudentProfile
from openai_service import get_age_appropriate_explanation, generate_study_plan, generate_knowledge_assessment, generate_personalized_roadmap
import logging
import json
from datetime import datetime

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

@app.route('/assessment', methods=['GET', 'POST'])
def assessment():
    """AI Knowledge Assessment page"""
    if request.method == 'POST':
        try:
            age = request.form.get('age', type=int)
            
            if not age or age < 5 or age > 18:
                flash('Please enter a valid age between 5 and 18.', 'error')
                return render_template('assessment.html')
            
            # Generate assessment
            assessment_data = generate_knowledge_assessment(age)
            
            # Store in session for result processing
            session['current_assessment'] = {
                'age': age,
                'assessment_data': assessment_data,
                'start_time': str(datetime.utcnow())
            }
            
            return render_template('take_assessment.html', 
                                 assessment=assessment_data, 
                                 age=age)
        
        except Exception as e:
            logging.error(f"Error generating assessment: {e}")
            flash('Something went wrong. Please try again!', 'error')
            return render_template('assessment.html')
    
    return render_template('assessment.html')

@app.route('/submit_assessment', methods=['POST'])
def submit_assessment():
    """Process assessment results and show personalized roadmap"""
    try:
        current_assessment = session.get('current_assessment')
        if not current_assessment:
            flash('No active assessment found. Please start a new assessment.', 'error')
            return redirect(url_for('assessment'))
        
        # Get answers from form
        answers = {}
        assessment_data = current_assessment['assessment_data']
        age = current_assessment['age']
        
        for question in assessment_data['questions']:
            answer = request.form.get(f"question_{question['id']}")
            answers[question['id']] = answer
        
        # Calculate score
        correct_answers = 0
        total_questions = len(assessment_data['questions'])
        results = []
        
        for question in assessment_data['questions']:
            user_answer = answers.get(question['id'])
            is_correct = user_answer == question['correct_answer']
            if is_correct:
                correct_answers += 1
            
            results.append({
                'question': question['question'],
                'user_answer': user_answer,
                'correct_answer': question['correct_answer'],
                'is_correct': is_correct,
                'explanation': question['explanation'],
                'topic': question['topic']
            })
        
        # Determine knowledge level
        score_percentage = (correct_answers / total_questions) * 100
        if score_percentage >= 80:
            knowledge_level = 'advanced'
        elif score_percentage >= 60:
            knowledge_level = 'intermediate'
        else:
            knowledge_level = 'beginner'
        
        # Analyze strong and weak topics
        topic_scores = {}
        for result in results:
            topic = result['topic']
            if topic not in topic_scores:
                topic_scores[topic] = {'correct': 0, 'total': 0}
            topic_scores[topic]['total'] += 1
            if result['is_correct']:
                topic_scores[topic]['correct'] += 1
        
        strong_topics = []
        weak_topics = []
        for topic, scores in topic_scores.items():
            percentage = (scores['correct'] / scores['total']) * 100
            if percentage >= 70:
                strong_topics.append(topic)
            elif percentage < 50:
                weak_topics.append(topic)
        
        # Save assessment result
        assessment_record = Assessment(
            student_age=age,
            score=correct_answers,
            total_questions=total_questions,
            knowledge_level=knowledge_level,
            topics_assessed=json.dumps(list(topic_scores.keys()))
        )
        db.session.add(assessment_record)
        
        # Update or create student profile
        profile = StudentProfile.query.filter_by(student_age=age).first()
        if not profile:
            profile = StudentProfile(
                student_age=age,
                current_level=knowledge_level,
                strong_topics=json.dumps(strong_topics),
                weak_topics=json.dumps(weak_topics),
                completed_assessments=1,
                last_assessment_date=datetime.utcnow()
            )
            db.session.add(profile)
        else:
            profile.current_level = knowledge_level
            profile.strong_topics = json.dumps(strong_topics)
            profile.weak_topics = json.dumps(weak_topics)
            profile.completed_assessments += 1
            profile.last_assessment_date = datetime.utcnow()
        
        db.session.commit()
        
        # Generate personalized roadmap
        roadmap = generate_personalized_roadmap(age, knowledge_level, strong_topics, weak_topics)
        
        # Clear session
        session.pop('current_assessment', None)
        
        return render_template('assessment_results.html',
                             score=correct_answers,
                             total=total_questions,
                             percentage=score_percentage,
                             level=knowledge_level,
                             strong_topics=strong_topics,
                             weak_topics=weak_topics,
                             roadmap=roadmap,
                             results=results)
        
    except Exception as e:
        logging.error(f"Error processing assessment: {e}")
        flash('Something went wrong processing your assessment. Please try again!', 'error')
        return redirect(url_for('assessment'))

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    """Generate topic-specific quizzes"""
    if request.method == 'POST':
        try:
            age = request.form.get('age', type=int)
            topic = request.form.get('topic', '').strip()
            difficulty = request.form.get('difficulty', 'beginner')
            
            if not age or age < 5 or age > 18:
                flash('Please enter a valid age between 5 and 18.', 'error')
                return render_template('quiz.html')
            
            if not topic:
                flash('Please enter a topic for the quiz.', 'error')
                return render_template('quiz.html')
            
            # Generate quiz using assessment function with topic focus
            quiz_data = generate_knowledge_assessment(age, [topic])
            quiz_data['title'] = f"{topic} Quiz"
            
            # Save quiz
            quiz_record = Quiz(
                student_age=age,
                topic=topic,
                quiz_content=json.dumps(quiz_data),
                difficulty_level=difficulty
            )
            db.session.add(quiz_record)
            db.session.commit()
            
            return render_template('take_quiz.html',
                                 quiz=quiz_data,
                                 topic=topic,
                                 age=age)
        
        except Exception as e:
            logging.error(f"Error generating quiz: {e}")
            flash('Something went wrong. Please try again!', 'error')
            return render_template('quiz.html')
    
    return render_template('quiz.html')

@app.route('/roadmap')
def roadmap():
    """Show personalized learning roadmap"""
    age = request.args.get('age', type=int)
    if not age:
        flash('Please specify your age to see a personalized roadmap.', 'error')
        return redirect(url_for('index'))
    
    # Get student profile
    profile = StudentProfile.query.filter_by(student_age=age).first()
    
    if not profile:
        flash('Take an assessment first to get your personalized roadmap!', 'info')
        return redirect(url_for('assessment'))
    
    # Generate current roadmap
    strong_topics = json.loads(profile.strong_topics) if profile.strong_topics else []
    weak_topics = json.loads(profile.weak_topics) if profile.weak_topics else []
    
    roadmap = generate_personalized_roadmap(
        age, 
        profile.current_level, 
        strong_topics, 
        weak_topics
    )
    
    return render_template('roadmap.html',
                         roadmap=roadmap,
                         profile=profile,
                         strong_topics=strong_topics,
                         weak_topics=weak_topics)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
