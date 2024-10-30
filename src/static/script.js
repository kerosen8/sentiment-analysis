let waitingForFeedback = false;

document.getElementById('messageForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const messageInput = document.getElementById('messageInput');
    const message = messageInput.value.trim();

    const messagesDiv = document.getElementById('messages');

    if (waitingForFeedback) {
        const userFeedbackMessage = document.createElement('div');
        userFeedbackMessage.className = 'message user';
        userFeedbackMessage.textContent = message;
        messagesDiv.appendChild(userFeedbackMessage);

        waitingForFeedback = false;

        fetch('/feedback', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ feedback: message }) 
        })
        .then(response => response.json())
        .then(data => {
            const thankYouMessage = document.createElement('div');
            thankYouMessage.className = 'message server';
            thankYouMessage.textContent = 'Thank you for your feedback!';
            messagesDiv.appendChild(thankYouMessage);
            
            messagesDiv.scrollTop = messagesDiv.scrollHeight;

            messageInput.value = '';
        })
        .catch(error => {
            console.error('Error sending feedback:', error);
            alert('Unable to send feedback.');
        });

        return;
    }

    const userMessage = document.createElement('div');
    userMessage.className = 'message user';
    userMessage.textContent = message;
    messagesDiv.appendChild(userMessage);

    messageInput.value = '';

    const loadingMessage = document.createElement('div');
    loadingMessage.className = 'message server';
    loadingMessage.textContent = 'Generating response...';
    messagesDiv.appendChild(loadingMessage);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;

    let interactionCount = sessionStorage.getItem('interactionCount');
    interactionCount = interactionCount ? parseInt(interactionCount) : 0;

    interactionCount++;
    sessionStorage.setItem('interactionCount', interactionCount);

    const submitButton = document.getElementById('submitButton');
    submitButton.disabled = true;
    messageInput.disabled = true;

    fetch('/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message })
    })
    .then(response => response.json())
    .then(data => {
        loadingMessage.remove();
        
        const serverMessage = document.createElement('div');
        serverMessage.className = 'message server';
        serverMessage.textContent = data.response_message;
        messagesDiv.appendChild(serverMessage);

        if (interactionCount % 3 === 0) {
            const feedbackMessage = document.createElement('div');
            feedbackMessage.className = 'message server';
            feedbackMessage.textContent = 'Rate our service please! :3';
            messagesDiv.appendChild(feedbackMessage);
            waitingForFeedback = true;
        }

        messagesDiv.scrollTop = messagesDiv.scrollHeight;

        submitButton.disabled = false;
        messageInput.disabled = false;
    })
    .catch(error => {
        console.error('Error:', error);
        loadingMessage.textContent = 'Unable to get response';

        submitButton.disabled = false;
        messageInput.disabled = false;
    });
});
