// Ignite AI - Client-side JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Form validation and enhancement
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
                
                // Find first invalid field and focus it
                const firstInvalidField = form.querySelector(':invalid');
                if (firstInvalidField) {
                    firstInvalidField.focus();
                    
                    // Add shake animation to invalid field
                    firstInvalidField.classList.add('animate-shake');
                    setTimeout(() => {
                        firstInvalidField.classList.remove('animate-shake');
                    }, 500);
                }
            }
            form.classList.add('was-validated');
        });
    });

    // Age input validation with real-time feedback
    const ageInputs = document.querySelectorAll('input[name="age"]');
    ageInputs.forEach(input => {
        input.addEventListener('input', function() {
            const age = parseInt(this.value);
            const feedback = this.parentNode.parentNode.querySelector('.age-feedback');
            
            if (feedback) {
                feedback.remove();
            }
            
            if (age && (age < 5 || age > 18)) {
                const feedbackEl = document.createElement('div');
                feedbackEl.className = 'age-feedback text-danger small mt-1';
                feedbackEl.innerHTML = '<i class="fas fa-exclamation-circle me-1"></i>Age must be between 5 and 18';
                this.parentNode.parentNode.appendChild(feedbackEl);
                this.classList.add('is-invalid');
            } else if (age >= 5 && age <= 18) {
                this.classList.remove('is-invalid');
                this.classList.add('is-valid');
                
                // Show age-appropriate encouragement
                const encouragement = getAgeEncouragement(age);
                if (encouragement) {
                    const feedbackEl = document.createElement('div');
                    feedbackEl.className = 'age-feedback text-success small mt-1';
                    feedbackEl.innerHTML = `<i class="fas fa-smile me-1"></i>${encouragement}`;
                    this.parentNode.parentNode.appendChild(feedbackEl);
                }
            }
        });
    });

    // Question textarea character counter
    const questionTextareas = document.querySelectorAll('textarea[name="question"]');
    questionTextareas.forEach(textarea => {
        const maxLength = textarea.getAttribute('maxlength') || 500;
        
        // Create character counter
        const counter = document.createElement('div');
        counter.className = 'text-muted small text-end mt-1';
        counter.innerHTML = `<span class="char-count">0</span>/${maxLength} characters`;
        textarea.parentNode.appendChild(counter);
        
        textarea.addEventListener('input', function() {
            const count = this.value.length;
            const charCountSpan = counter.querySelector('.char-count');
            charCountSpan.textContent = count;
            
            if (count > maxLength * 0.9) {
                counter.classList.add('text-warning');
            } else {
                counter.classList.remove('text-warning');
            }
            
            if (count >= maxLength) {
                counter.classList.add('text-danger');
            } else {
                counter.classList.remove('text-danger');
            }
        });
    });

    // Topic input suggestions
    const topicInputs = document.querySelectorAll('input[name="topic"]');
    topicInputs.forEach(input => {
        const suggestions = [
            'Machine Learning', 'Neural Networks', 'Computer Vision', 'Natural Language Processing', 'Robotics',
            'Deep Learning', 'AI Ethics', 'Artificial Intelligence', 'Data Science', 'Reinforcement Learning',
            'Chatbots', 'Computer Graphics', 'AI Programming', 'Automation', 'AI History'
        ];
        
        // Create datalist for autocomplete
        const datalist = document.createElement('datalist');
        datalist.id = 'topic-suggestions';
        suggestions.forEach(suggestion => {
            const option = document.createElement('option');
            option.value = suggestion;
            datalist.appendChild(option);
        });
        
        input.setAttribute('list', 'topic-suggestions');
        input.parentNode.appendChild(datalist);
    });

    // Smooth scrolling for anchor links
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add loading animation to buttons
    const submitButtons = document.querySelectorAll('button[type="submit"]');
    submitButtons.forEach(button => {
        button.addEventListener('click', function() {
            const form = this.closest('form');
            if (form && form.checkValidity()) {
                addLoadingState(this);
            }
        });
    });

    // Auto-resize textareas
    const textareas = document.querySelectorAll('textarea');
    textareas.forEach(textarea => {
        autoResize(textarea);
        textarea.addEventListener('input', function() {
            autoResize(this);
        });
    });

    // Add hover effects to cards
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        if (card.classList.contains('hover-lift')) {
            card.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-5px)';
            });
            
            card.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0)';
            });
        }
    });

    // Initialize progress bars if any
    const progressBars = document.querySelectorAll('.progress-bar');
    progressBars.forEach(bar => {
        const width = bar.getAttribute('data-width');
        if (width) {
            setTimeout(() => {
                bar.style.width = width + '%';
            }, 500);
        }
    });
});

// Helper functions
function getAgeEncouragement(age) {
    if (age >= 5 && age <= 8) {
        return "Perfect! I'll explain things in a fun, easy way!";
    } else if (age >= 9 && age <= 12) {
        return "Great! I'll use examples you can relate to!";
    } else if (age >= 13 && age <= 16) {
        return "Awesome! I'll give you detailed, practical explanations!";
    } else if (age >= 17 && age <= 18) {
        return "Excellent! I'll provide comprehensive, advanced explanations!";
    }
    return null;
}

function addLoadingState(button) {
    const originalText = button.innerHTML;
    const loadingText = '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';
    
    button.innerHTML = loadingText;
    button.disabled = true;
    
    // Reset after form submission (fallback)
    setTimeout(() => {
        button.innerHTML = originalText;
        button.disabled = false;
    }, 10000);
}

function autoResize(textarea) {
    textarea.style.height = 'auto';
    textarea.style.height = (textarea.scrollHeight) + 'px';
}

// Add shake animation class
const style = document.createElement('style');
style.textContent = `
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        10%, 30%, 50%, 70%, 90% { transform: translateX(-10px); }
        20%, 40%, 60%, 80% { transform: translateX(10px); }
    }
    .animate-shake {
        animation: shake 0.5s;
    }
`;
document.head.appendChild(style);

// Handle accordion animations
document.addEventListener('shown.bs.collapse', function(e) {
    e.target.scrollIntoView({
        behavior: 'smooth',
        block: 'nearest'
    });
});

// Add copy functionality to code blocks if any
function addCopyButton(element) {
    const button = document.createElement('button');
    button.className = 'btn btn-sm btn-outline-secondary position-absolute top-0 end-0 m-2';
    button.innerHTML = '<i class="fas fa-copy"></i>';
    button.title = 'Copy to clipboard';
    
    button.addEventListener('click', function() {
        navigator.clipboard.writeText(element.textContent).then(() => {
            button.innerHTML = '<i class="fas fa-check text-success"></i>';
            setTimeout(() => {
                button.innerHTML = '<i class="fas fa-copy"></i>';
            }, 2000);
        });
    });
    
    element.style.position = 'relative';
    element.appendChild(button);
}

// Initialize copy buttons for any code blocks
document.querySelectorAll('pre, code').forEach(addCopyButton);

// Add print functionality
function printPage() {
    window.print();
}

// Add keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl + / to focus search/question input
    if (e.ctrlKey && e.key === '/') {
        e.preventDefault();
        const searchInput = document.querySelector('input[name="question"], textarea[name="question"]');
        if (searchInput) {
            searchInput.focus();
        }
    }
    
    // Escape to close modals
    if (e.key === 'Escape') {
        const modals = document.querySelectorAll('.modal.show');
        modals.forEach(modal => {
            const modalInstance = bootstrap.Modal.getInstance(modal);
            if (modalInstance) {
                modalInstance.hide();
            }
        });
    }
});

// Add focus management for accessibility
document.addEventListener('keydown', function(e) {
    if (e.key === 'Tab') {
        document.body.classList.add('keyboard-navigation');
    }
});

document.addEventListener('mousedown', function() {
    document.body.classList.remove('keyboard-navigation');
});

// Style for keyboard navigation
const keyboardStyle = document.createElement('style');
keyboardStyle.textContent = `
    .keyboard-navigation *:focus {
        outline: 2px solid var(--bs-primary) !important;
        outline-offset: 2px !important;
    }
`;
document.head.appendChild(keyboardStyle);
