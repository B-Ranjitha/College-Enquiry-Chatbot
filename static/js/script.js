document.addEventListener('DOMContentLoaded', function() {
    // Chat functionality
    const chatMessages = document.getElementById('chatMessages');
    const userInput = document.getElementById('userInput');
    const sendButton = document.getElementById('sendButton');
    
    // Admin functionality
    const addFaqForm = document.getElementById('addFaqForm');
    const editFaqForm = document.getElementById('editFaqForm');
    const editModal = document.getElementById('editModal');
    const closeModal = document.querySelector('.close');
    
    if (userInput && sendButton) {
        // Scroll to bottom of chat
        function scrollToBottom() {
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
        
        scrollToBottom();
        
        // Send message function
        function sendMessage() {
            const message = userInput.value.trim();
            if (message === '') return;
            
            // Add user message to chat
            addMessageToChat('user', message);
            userInput.value = '';
            
            // Show typing indicator
            const typingIndicator = document.createElement('div');
            typingIndicator.className = 'message ai-message';
            typingIndicator.id = 'typing-indicator';
            typingIndicator.innerHTML = `
                <div class="message-content">
                    <div class="typing">
                        <span></span>
                        <span></span>
                        <span></span>
                    </div>
                </div>
            `;
            chatMessages.appendChild(typingIndicator);
            scrollToBottom();
            
            // Send to server and get AI response
            fetch('/send_message', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: message })
            })
            .then(response => response.json())
            .then(data => {
                // Remove typing indicator
                const indicator = document.getElementById('typing-indicator');
                if (indicator) indicator.remove();
                
                if (data.status === 'success') {
                    addMessageToChat('ai', data.response);
                } else {
                    addMessageToChat('ai', 'Sorry, I encountered an error. Please try again.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                // Remove typing indicator
                const indicator = document.getElementById('typing-indicator');
                if (indicator) indicator.remove();
                
                addMessageToChat('ai', 'Sorry, I encountered an error. Please try again.');
            });
        }
        
        // Add message to chat UI
        function addMessageToChat(sender, message) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${sender}-message`;
            
            const contentDiv = document.createElement('div');
            contentDiv.className = 'message-content';
            
            const messageP = document.createElement('p');
            messageP.textContent = message;
            
            contentDiv.appendChild(messageP);
            messageDiv.appendChild(contentDiv);
            chatMessages.appendChild(messageDiv);
            
            scrollToBottom();
        }
        
        // Event listeners
        sendButton.addEventListener('click', sendMessage);
        
        userInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
        
        // Check if URL has a question parameter
        const urlParams = new URLSearchParams(window.location.search);
        const question = urlParams.get('question');
        
        if (question) {
            let predefinedQuestion = '';
            
            switch(question) {
                case 'admission':
                    predefinedQuestion = 'Tell me about the admission process';
                    break;
                case 'courses':
                    predefinedQuestion = 'What courses do you offer?';
                    break;
                case 'fees':
                    predefinedQuestion = 'What is the fee structure?';
                    break;
                case 'scholarships':
                    predefinedQuestion = 'Do you offer scholarships?';
                    break;
            }
            
            if (predefinedQuestion) {
                userInput.value = predefinedQuestion;
                sendMessage();
            }
        }
    }
    
    // Admin functionality
    if (addFaqForm) {
        addFaqForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const question = document.getElementById('newQuestion').value;
            const answer = document.getElementById('newAnswer').value;
            
            fetch('/admin/add_query', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ question: question, answer: answer })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    alert('FAQ added successfully!');
                    window.location.reload();
                } else {
                    alert('Error adding FAQ: ' + data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error adding FAQ. Please try again.');
            });
        });
    }
    
    // Modal functionality
    if (closeModal) {
        closeModal.addEventListener('click', function() {
            editModal.style.display = 'none';
        });
        
        window.addEventListener('click', function(event) {
            if (event.target === editModal) {
                editModal.style.display = 'none';
            }
        });
    }
    
    if (editFaqForm) {
        editFaqForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const id = document.getElementById('editId').value;
            const question = document.getElementById('editQuestion').value;
            const answer = document.getElementById('editAnswer').value;
            
            fetch(`/admin/update_query/${id}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ question: question, answer: answer })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    alert('FAQ updated successfully!');
                    window.location.reload();
                } else {
                    alert('Error updating FAQ: ' + data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error updating FAQ. Please try again.');
            });
        });
    }
});

// Global functions for admin operations
function editFaq(id, question, answer) {
    document.getElementById('editId').value = id;
    document.getElementById('editQuestion').value = question;
    document.getElementById('editAnswer').value = answer;
    document.getElementById('editModal').style.display = 'block';
}

function deleteFaq(id) {
    if (confirm('Are you sure you want to delete this FAQ?')) {
        fetch(`/admin/delete_query/${id}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                alert('FAQ deleted successfully!');
                window.location.reload();
            } else {
                alert('Error deleting FAQ: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error deleting FAQ. Please try again.');
        });
    }
}
