# College-Enquiry-Chatbot

🎓 BBC College Enquiry Chatbot
A fully responsive, AI-powered chatbot for BBC College that provides instant responses to student enquiries about admissions, courses, facilities, and more. Built with Python Flask, OpenAI integration, and modern web technologies.

https://img.shields.io/badge/Python-3.8%252B-blue
https://img.shields.io/badge/Flask-2.3.3-green
https://img.shields.io/badge/OpenAI-GPT--3.5-orange
https://img.shields.io/badge/SQLite-Database-lightgrey
https://img.shields.io/badge/Design-Responsive-blueviolet

🌟 Features
🤖 AI-Powered Responses: Integrated with OpenAI GPT for intelligent conversation

🎨 Modern UI: Responsive design with animations and transitions

🔐 User Authentication: Secure login/registration system

👨‍💼 Admin Panel: Manage FAQs and chatbot knowledge base

💬 Real-time Chat: Interactive chat interface with typing indicators

📱 Mobile-Friendly: Works perfectly on all devices

🎯 BBC College Specific: Customized for https://bbc.edu.in/

🛠️ Technology Stack
Backend: Python Flask, SQLite

Frontend: HTML5, CSS3 (Flexbox & Grid), JavaScript

AI Integration: OpenAI GPT-3.5-turbo

Database: SQLite with custom ORM

Authentication: Session-based user management

Styling: Custom CSS with animations and transitions

🚀 Quick Start
Prerequisites
Python 3.8+

OpenAI API key

Installation
Clone the repository

bash
git clone https://github.com/your-username/bbc-college-chatbot.git
cd bbc-college-chatbot
Install dependencies

bash
pip install -r requirements.txt
Set up environment variables

bash
# Create .env file
SECRET_KEY=your-super-secret-key
OPENAI_API_KEY=your-openai-api-key
Run the application

bash
python app.py
Access the application
Open your browser and navigate to http://localhost:5000

Default Admin Login
Username: admin

Password: admin123

📁 Project Structure

bbc-college-chatbot/
├── app.py                 # Main Flask application
├── database.py           # Database operations
├── config.py            # Configuration settings
├── requirements.txt     # Python dependencies
├── .env                # Environment variables
├── static/
│   ├── css/
│   │   └── style.css   # Custom styles with animations
│   └── js/
│       └── script.js   # Frontend functionality
└── templates/
    ├── base.html       # Base template
    ├── index.html      # Landing page
    ├── login.html      # Login page
    ├── register.html   # Registration page
    ├── dashboard.html  # User dashboard
    ├── chat.html       # Chat interface
    ├── admin.html      # Admin dashboard
    └── admin_queries.html # FAQ management


🎨 Key Features in Detail
AI Integration
Hybrid response system (OpenAI + custom knowledge base)

Fallback mechanism for offline functionality

BBC College-specific training data

User Experience
Smooth animations and transitions

Responsive grid-based layout

Interactive chat interface with typing indicators

Quick action buttons for common queries

Admin Capabilities
Add/edit/delete FAQs

Manage chatbot knowledge base

Monitor user interactions

Security Features
Session-based authentication

Secure password handling

Admin privilege system

🔧 Customization
Adding New Responses
Edit the get_fallback_response() function in app.py to add new question-answer pairs:

'new_topic': {
    'triggers': ['keyword1', 'keyword2', 'keyword3'],
    'response': "Your response here"
}

Modifying Styling
Edit static/css/style.css to customize colors, animations, and layout:

:root {
    --primary-color: #your-color;
    --secondary-color: #your-color;
}

Database Management
Admin users can manage FAQs directly through the web interface at /admin/queries

🤝 Contributing
We welcome contributions! Please feel free to submit a Pull Request.

Fork the project

Create your feature branch (git checkout -b feature/AmazingFeature)

Commit your changes (git commit -m 'Add some AmazingFeature')

Push to the branch (git push origin feature/AmazingFeature)

Open a Pull Request

📄 License
This project is licensed under the MIT License - see the LICENSE.md file for details.

🙏 Acknowledgments
OpenAI for the GPT API

Flask community for the excellent web framework

Font Awesome for icons

Google Fonts for the Poppins typeface

📞 Support
If you have any questions or need help with setup, please open an issue or contact us at branjitha15120032gmail.com .
