import sqlite3
from config import Config

def get_db_connection():
    conn = sqlite3.connect(Config.DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    
    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 username TEXT UNIQUE NOT NULL,
                 email TEXT UNIQUE NOT NULL,
                 password TEXT NOT NULL,
                 is_admin BOOLEAN DEFAULT FALSE)''')
    
    # Chat history table
    c.execute('''CREATE TABLE IF NOT EXISTS chat_history
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 user_id INTEGER NOT NULL,
                 sender TEXT NOT NULL,
                 message TEXT NOT NULL,
                 timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                 FOREIGN KEY (user_id) REFERENCES users (id))''')
    
    # FAQ table for predefined questions and answers
    c.execute('''CREATE TABLE IF NOT EXISTS faqs
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 question TEXT NOT NULL,
                 answer TEXT NOT NULL)''')
    
    # Check if admin user exists, if not create one
    c.execute("SELECT * FROM users WHERE username=?", ('admin',))
    admin = c.fetchone()
    if not admin:
        c.execute("INSERT INTO users (username, email, password, is_admin) VALUES (?, ?, ?, ?)",
                 ('admin', 'admin@bbc.edu.in', 'admin123', True))
    
    # Add BBC College sample FAQs
    c.execute("SELECT COUNT(*) FROM faqs")
    if c.fetchone()[0] == 0:
        sample_faqs = [
            ("What programs does BBC College offer?", "BBC College offers various undergraduate and postgraduate programs including BBA (Bachelor of Business Administration), BCA (Bachelor of Computer Applications), MBA (Master of Business Administration), and other specialized courses."),
            ("How can I apply for admission to BBC College?", "You can apply for admission to BBC College by filling out the application form available on our website https://bbc.edu.in/ or by visiting our admission office. You'll need to submit academic transcripts, identification documents, and other required materials."),
            ("What is the fee structure at BBC College?", "The fee structure varies by program at BBC College. For detailed information about tuition fees and payment schedules, please contact our admission office at +91-XXXXXXXXXX or visit our campus."),
            ("Does BBC College provide hostel facilities?", "Yes, BBC College provides hostel accommodation for outstation students. Our hostels are well-maintained with necessary amenities to ensure a comfortable stay for students."),
            ("What placement opportunities are available at BBC College?", "BBC College has a dedicated placement cell that works with various industries to provide placement opportunities. We have a good track record of placements and also organize training programs to prepare students for their careers."),
            ("What are the facilities available at BBC College?", "BBC College provides excellent facilities including a well-equipped library, modern computer labs, science laboratories, sports facilities, cafeteria, and hostel accommodation for students."),
            ("How can I contact BBC College?", "You can contact BBC College at:\nPhone: +91-XXXXXXXXXX\nEmail: info@bbc.edu.in\nAddress: BBC Educational Campus, [City/Area], [State], India\nWebsite: https://bbc.edu.in/"),
            ("What is the vision of BBC College?", "BBC College is committed to providing quality education and focuses on holistic development of students through academic excellence, extracurricular activities, and value-based education."),
            ("Are there scholarships available at BBC College?", "Yes, BBC College offers various scholarship programs for deserving students. Please contact our admission office for detailed information about scholarship opportunities and eligibility criteria."),
            ("What are the college timings at BBC College?", "The college timing is typically from 9:00 AM to 4:00 PM, Monday to Friday. However, specific timings may vary for different programs. The administrative office is open from 9:00 AM to 5:00 PM on working days.")
        ]
        c.executemany("INSERT INTO faqs (question, answer) VALUES (?, ?)", sample_faqs)
    
    conn.commit()
    conn.close()

def add_user(username, email, password):
    try:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", 
                 (username, email, password))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

def get_user(username):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    user = c.fetchone()
    conn.close()
    return user

def add_chat_message(user_id, sender, message):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("INSERT INTO chat_history (user_id, sender, message) VALUES (?, ?, ?)", 
             (user_id, sender, message))
    conn.commit()
    conn.close()

def get_chat_history(user_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT sender, message, timestamp FROM chat_history WHERE user_id=? ORDER BY timestamp", (user_id,))
    history = c.fetchall()
    conn.close()
    return history

def add_faq(question, answer):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("INSERT INTO faqs (question, answer) VALUES (?, ?)", 
             (question, answer))
    conn.commit()
    conn.close()

def get_faqs():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM faqs ORDER BY id")
    faqs = c.fetchall()
    conn.close()
    return faqs

def get_faq(faq_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM faqs WHERE id=?", (faq_id,))
    faq = c.fetchone()
    conn.close()
    return faq

def update_faq(faq_id, question, answer):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("UPDATE faqs SET question=?, answer=? WHERE id=?", 
             (question, answer, faq_id))
    conn.commit()
    conn.close()

def delete_faq(faq_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("DELETE FROM faqs WHERE id=?", (faq_id,))
    conn.commit()
    conn.close()
