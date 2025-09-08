from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from database import init_db, add_user, get_user, add_chat_message, get_chat_history, add_faq, get_faqs, get_faq, update_faq, delete_faq
import sqlite3
import json
from datetime import datetime
import openai
from config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)

# Initialize OpenAI if API key is available
if app.config['OPENAI_API_KEY']:
    openai.api_key = app.config['OPENAI_API_KEY']
else:
    print("OpenAI API key not found. Using fallback responses only.")

# Initialize database
init_db()

# Enhanced AI response function with fallback
def get_ai_response(message, user_id=None):
    # First check if we have a predefined answer in our FAQ database
    try:
        faqs = get_faqs()
        for faq in faqs:
            if faq[1].lower() in message.lower():
                return faq[2]
    except Exception as e:
        print(f"Error accessing FAQs: {e}")
    
    # If no predefined answer, try OpenAI
    try:
        # Only try OpenAI if the API key is configured
        if app.config['OPENAI_API_KEY']:
            # Create a BBC College-specific prompt for OpenAI
            prompt = f"""You are a helpful college enquiry chatbot for BBC College (https://bbc.edu.in/). 
            Provide accurate, helpful information about BBC College. 
            
            Important information about BBC College:
            - Offers programs like BBA, BCA, MBA and other UG/PG courses
            - Located in India
            - Has facilities like library, labs, hostel, sports facilities
            - Has a placement cell for career opportunities
            - Focuses on quality education and holistic development
            
            If you don't know something specific about BBC College, politely say so and suggest 
            contacting the college directly or visiting their website https://bbc.edu.in/
            
            User question: {message}
            
            Helpful response as BBC College chatbot:"""
            
            response = openai.Completion.create(
                engine="gpt-3.5-turbo-instruct",
                prompt=prompt,
                max_tokens=250,
                temperature=0.7,
                top_p=1,
                frequency_penalty=0.5,
                presence_penalty=0.5
            )
            
            return response.choices[0].text.strip()
        else:
            # If no OpenAI API key, use fallback
            return get_fallback_response(message)
    
    except Exception as e:
        print(f"OpenAI error, using fallback: {e}")
        # If OpenAI fails, use the fallback response system
        return get_fallback_response(message)

# BBC College-specific response function
def get_fallback_response(message):
    message_lower = message.lower()
    
    # BBC College-related responses
    response_map = {
        'admission': {
            'triggers': ['admission', 'admit', 'apply', 'application', 'enroll', 'enrollment'],
            'response': "BBC College offers admissions to various undergraduate and postgraduate programs. The admission process typically begins in May each year. You'll need to submit your academic transcripts, identification documents, and complete the application form available on our website or at the admission office."
        },
        'courses': {
            'triggers': ['course', 'program', 'degree', 'study', 'major', 'curriculum', 'bachelor', 'master', 'bba', 'bca', 'mba'],
            'response': "BBC College offers a wide range of programs including:\n\n- BBA (Bachelor of Business Administration)\n- BCA (Bachelor of Computer Applications)\n- MBA (Master of Business Administration)\n- Various other undergraduate and postgraduate programs\n\nVisit our website https://bbc.edu.in/ for detailed information about each program."
        },
        'fees': {
            'triggers': ['fee', 'cost', 'tuition', 'price', 'payment', 'financial', 'scholarship'],
            'response': "The fee structure varies by program at BBC College. For detailed information about tuition fees, payment schedules, and scholarship opportunities, please contact our admission office at +91-XXXXXXXXXX or visit our campus. We offer various scholarship programs for deserving students."
        },
        'contact': {
            'triggers': ['contact', 'email', 'phone', 'address', 'location', 'where', 'visit'],
            'response': "You can contact BBC College at:\n\nAddress: BBC Educational Campus, [City/Area], [State], India\nPhone: +91-XXXXXXXXXX\nEmail: info@bbc.edu.in\nWebsite: https://bbc.edu.in/\n\nVisit our website for more contact details and location information."
        },
        'facility': {
            'triggers': ['facility', 'library', 'lab', 'laboratory', 'hostel', 'accommodation', 'sports', 'canteen'],
            'response': "BBC College provides excellent facilities including:\n- Well-equipped library with extensive resources\n- Modern computer labs with latest technology\n- Science laboratories for practical learning\n- Hostel accommodation for outstation students\n- Sports facilities and playground\n- Cafeteria serving hygienic food\n\nVisit our campus to see these facilities firsthand."
        },
        'placement': {
            'triggers': ['placement', 'job', 'career', 'internship', 'company', 'recruitment'],
            'response': "BBC College has a dedicated placement cell that works with various industries to provide placement opportunities for our students. We have a good track record of placements in reputed companies. The placement cell also organizes training programs, workshops, and pre-placement talks to prepare students for their careers."
        },
        'about': {
            'triggers': ['about', 'history', 'establish', 'found', 'vision', 'mission'],
            'response': "BBC College is a premier educational institution committed to providing quality education. We focus on holistic development of students through academic excellence, extracurricular activities, and value-based education. Our vision is to create responsible citizens and future leaders through innovative teaching methods and practical learning experiences."
        },
        'greeting': {
            'triggers': ['hi', 'hello', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening'],
            'response': "Hello! Welcome to BBC College enquiry chatbot. How can I assist you with information about our college today?"
        },
        'thanks': {
            'triggers': ['thank', 'thanks', 'appreciate', 'grateful'],
            'response': "You're welcome! Is there anything else you'd like to know about BBC College? Feel free to ask any questions about admissions, courses, facilities, or any other aspect of our college."
        },
        'goodbye': {
            'triggers': ['bye', 'goodbye', 'see you', 'farewell', 'exit', 'quit'],
            'response': "Thank you for contacting BBC College. Have a great day! If you have more questions later, feel free to chat with us again. You can also visit our website https://bbc.edu.in/ for more information."
        },
        'website': {
            'triggers': ['website', 'online', 'portal', 'web', 'internet'],
            'response': "Our official website is https://bbc.edu.in/. You can find detailed information about all our programs, admission procedures, faculty, facilities, and much more on our website. You can also contact us through the website for specific queries."
        },
        'faculty': {
            'triggers': ['faculty', 'professor', 'teacher', 'instructor', 'lecturer', 'staff'],
            'response': "BBC College has highly qualified and experienced faculty members who are dedicated to providing quality education. Our teachers are experts in their respective fields and use innovative teaching methods to ensure effective learning. Many of our faculty members have industry experience and advanced degrees."
        },
        'timing': {
            'triggers': ['timing', 'time', 'hour', 'schedule', 'when', 'open', 'close'],
            'response': "The college timing is typically from 9:00 AM to 4:00 PM, Monday to Friday. However, specific timings may vary for different programs and departments. The administrative office is open from 9:00 AM to 5:00 PM on working days. Please contact the college for specific schedule information."
        }
    }
    
    # Check for keywords in the message
    for category, data in response_map.items():
        for trigger in data['triggers']:
            if trigger in message_lower:
                return data['response']
    
    # Default response if no keywords matched
    return "I'm not sure I understand your question about BBC College. Could you please rephrase it? I can help with information about admissions, courses, fees, facilities, placements, faculty, and other aspects of our college. You can also visit our website https://bbc.edu.in/ for detailed information."

@app.route('/')
def index():
    if 'user_id' in session:
        if session.get('is_admin'):
            return redirect(url_for('admin_dashboard'))
        else:
            return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Add user to database
        if add_user(username, email, password):
            return redirect(url_for('login'))
        else:
            return render_template('register.html', error="Username or email already exists")
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = get_user(username)
        if user and user[3] == password:  # In real applications, use password hashing!
            session['user_id'] = user[0]
            session['username'] = user[1]
            session['is_admin'] = user[4] == 1  # Check if user is admin
            
            if session['is_admin']:
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="Invalid credentials")
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if session.get('is_admin'):
        return redirect(url_for('admin_dashboard'))
    
    return render_template('dashboard.html', username=session['username'])

@app.route('/chat')
def chat():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if session.get('is_admin'):
        return redirect(url_for('admin_dashboard'))
    
    chat_history = get_chat_history(session['user_id'])
    return render_template('chat.html', username=session['username'], chat_history=chat_history)

@app.route('/send_message', methods=['POST'])
def send_message():
    if 'user_id' not in session:
        return jsonify({'status': 'error', 'message': 'Not logged in'})
    
    user_message = request.json['message']
    ai_response = get_ai_response(user_message, session['user_id'])
    
    # Save messages to database
    add_chat_message(session['user_id'], 'user', user_message)
    add_chat_message(session['user_id'], 'ai', ai_response)
    
    return jsonify({'status': 'success', 'response': ai_response})

@app.route('/admin')
def admin_dashboard():
    if 'user_id' not in session or not session.get('is_admin'):
        return redirect(url_for('login'))
    
    return render_template('admin.html')

@app.route('/admin/queries')
def admin_queries():
    if 'user_id' not in session or not session.get('is_admin'):
        return redirect(url_for('login'))
    
    faqs = get_faqs()
    return render_template('admin_queries.html', faqs=faqs)

@app.route('/admin/add_query', methods=['POST'])
def add_query():
    if 'user_id' not in session or not session.get('is_admin'):
        return jsonify({'status': 'error', 'message': 'Unauthorized'})
    
    question = request.json['question']
    answer = request.json['answer']
    
    add_faq(question, answer)
    return jsonify({'status': 'success'})

@app.route('/admin/update_query/<int:faq_id>', methods=['POST'])
def update_query(faq_id):
    if 'user_id' not in session or not session.get('is_admin'):
        return jsonify({'status': 'error', 'message': 'Unauthorized'})
    
    question = request.json['question']
    answer = request.json['answer']
    
    update_faq(faq_id, question, answer)
    return jsonify({'status': 'success'})

@app.route('/admin/delete_query/<int:faq_id>', methods=['POST'])
def delete_query(faq_id):
    if 'user_id' not in session or not session.get('is_admin'):
        return jsonify({'status': 'error', 'message': 'Unauthorized'})
    
    delete_faq(faq_id)
    return jsonify({'status': 'success'})

@app.route('/test_openai')
def test_openai():
    """Test route to check if OpenAI API is working"""
    try:
        if not app.config['OPENAI_API_KEY']:
            return "OpenAI API key not configured. Using fallback responses."
        
        test_response = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",
            prompt="Test response",
            max_tokens=10
        )
        return f"OpenAI connection successful: {test_response.choices[0].text.strip()}"
    except Exception as e:
        return f"OpenAI error: {str(e)}"

@app.route('/test_fallback')
def test_fallback():
    """Test route to check fallback responses"""
    test_questions = [
        "What programs does BBC College offer?",
        "How do I apply for BBA at BBC College?",
        "What are the facilities at BBC College?",
        "Does BBC College have hostel facilities?",
        "How can I contact BBC College?",
        "What is the fee structure for MBA at BBC College?"
    ]
    
    results = []
    for question in test_questions:
        response = get_fallback_response(question)
        results.append(f"Q: {question}\nA: {response}\n")
    
    return "<pre>" + "\n".join(results) + "</pre>"

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Check if OpenAI API key is available
    if app.config['OPENAI_API_KEY']:
        print("OpenAI API key found. AI integration enabled.")
    else:
        print("OpenAI API key not found. Using fallback responses only.")
    
    app.run(debug=True)
