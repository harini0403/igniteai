# Ignite AI - Replit Development Guide

## Overview

Ignite AI is a Flask-based web application that provides personalized AI education to students aged 5-18. The application leverages OpenAI's GPT models to generate age-appropriate explanations for AI-related questions and create customized AI study plans. The system emphasizes user-friendly interfaces with responsive design and engaging animations to create an enjoyable learning experience focused specifically on artificial intelligence concepts.

## System Architecture

### Backend Architecture
- **Framework**: Flask with SQLAlchemy ORM
- **Database**: SQLite (development) with support for PostgreSQL (production via DATABASE_URL environment variable)
- **AI Integration**: OpenAI API (GPT-4o) for generating educational content
- **Session Management**: Flask sessions with configurable secret keys
- **Deployment**: WSGI-compatible with ProxyFix middleware for production deployments

### Frontend Architecture
- **Template Engine**: Jinja2 (Flask's default templating)
- **CSS Framework**: Bootstrap 5 with Replit's dark theme
- **Icons**: Font Awesome 6.0
- **JavaScript**: Vanilla JS with Bootstrap components
- **Responsive Design**: Mobile-first approach with Bootstrap grid system

### Database Schema
The application uses two main models:
- **Question**: Stores student questions, AI responses, age, topic, and timestamps
- **StudyPlan**: Stores generated study plans with difficulty levels and metadata

## Key Components

### Core Application (`app.py`)
- Flask application factory pattern
- SQLAlchemy configuration with connection pooling
- Environment-based configuration (DATABASE_URL, SESSION_SECRET)
- Automatic table creation and model registration

### Data Models (`models.py`)
- **Question Model**: Captures student interactions with fields for age, question text, AI response, topic categorization, and creation timestamp
- **StudyPlan Model**: Stores personalized study plans with difficulty levels and structured content

### OpenAI Service (`openai_service.py`)
- Age-appropriate content generation based on developmental stages
- Structured response format with explanations, key points, fun facts, and activities
- Input validation and error handling for API interactions
- Language complexity adjustment based on student age groups

### Route Handlers (`routes.py`)
- RESTful endpoint design with form validation
- Database transaction management
- Error handling with user-friendly flash messages
- Template rendering with context data passing

### Frontend Templates
- **Base Template**: Consistent navigation, Bootstrap integration, and responsive layout
- **Index**: Landing page with feature highlights and call-to-action buttons
- **Ask Question**: Interactive form with real-time validation and age-specific guidance
- **Explanation**: Structured display of AI responses with visual hierarchy
- **Study Plan**: Multi-step form for generating personalized learning plans

## Data Flow

1. **Question Processing Flow**:
   - User submits question with age via web form
   - Input validation (age range 5-18, minimum question length)
   - OpenAI API call with age-appropriate prompting
   - Response parsing and database storage
   - Structured display of explanation with key points and activities

2. **Study Plan Generation Flow**:
   - User provides age, topic, and difficulty preferences
   - AI generates comprehensive study plan based on parameters
   - Plan storage with metadata for future reference
   - Presentation in organized, actionable format

3. **Database Persistence**:
   - All interactions stored for analytics and improvement
   - Timestamp tracking for usage patterns
   - Topic categorization for content organization

## External Dependencies

### Required APIs
- **OpenAI API**: GPT-4o model for educational content generation
  - Requires OPENAI_API_KEY environment variable
  - Handles rate limiting and error responses
  - Structured JSON response format for consistent parsing

### Frontend Libraries
- **Bootstrap 5**: UI framework with Replit dark theme customization
- **Font Awesome 6.0**: Comprehensive icon library for visual enhancement
- **CDN Delivery**: External hosting for faster load times and reduced bandwidth

### Python Packages
- **Flask**: Web framework with templating and session management
- **SQLAlchemy**: ORM with database abstraction and migration support
- **OpenAI**: Official API client with authentication and request handling
- **Werkzeug**: WSGI utilities including ProxyFix for deployment

## Deployment Strategy

### Environment Configuration
- **Development**: SQLite database with debug mode enabled
- **Production**: PostgreSQL via DATABASE_URL with connection pooling
- **Security**: Environment-based secret key management
- **Scalability**: WSGI deployment with proxy support

### Database Management
- **Automatic Migrations**: Table creation on application startup
- **Connection Pooling**: Configured for production reliability
- **Health Checks**: Pre-ping validation for connection stability

### Static Asset Delivery
- **CSS**: Custom styles with CSS variables for theming consistency
- **JavaScript**: Progressive enhancement with form validation and animations
- **Images**: Optimized loading with responsive breakpoints

## Changelog
- June 28, 2025. Initial setup

## User Preferences

Preferred communication style: Simple, everyday language.