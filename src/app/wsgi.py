import os
import random
import pandas as pd
from flask import Flask, render_template, request, jsonify, session
from service.analyst_service import AnalystService

# Initialize the Flask application with specified template and static folder paths, and configure session settings

app = Flask(__name__, 
            template_folder=os.path.join(os.path.dirname(__file__), '../templates'),
            static_folder=os.path.join(os.path.dirname(__file__), '../static'))

app.config['SECRET_KEY'] = 'ea51834edcd806007efef947'
app.config['SESSION_TYPE'] = 'filesystem'

service = AnalystService()

def __generate_answer(message):
    """
    Generates a response based on the input message by classifying it 
    (greeting, farewell, question) and assessing its sentiment 
    (positive, neutral, negative). 

    Returns a list containing:
        - A generated response string.
        - The classification of the message (e.g., 'greetings', 'farewell', 'question').
    """
    response = ''

    greetings_responces = ["Hello! ", "Hi! ", "Howdy! "]
    farewells_responces = ["Goodbye! ", "Bye! ", "See you soon! "]
    question_responces = ["I'm sorry, but I'm unable to assist with that right now. ", "Apologies, but I can't help with this at the moment. ", 
                          "Sorry, I'm not able to handle this request right now. "]

    positive_responces = ["I am glad to hear that! :)", "Great news! :)", "Awesome! :)"]
    negative_responces = ["I'm sorry about that. How can I assist you further?", "Apologies for the confusion. Let me know how I can help.", 
                          "I'm sorry you are facing issues :( "]
    neutral_responces = ["How else can I assist?", "I'm here for any questions.", "Anything else?"]

    unexpected_result = service.unexpected_text_classifier(message)
    if unexpected_result == 'unexpected':
        return ["Apologies, I'm not sure I understand. Could you rephrase?", 'neutral']
        
    message_classification = service.message_classifier(message)
    if message_classification == 'greetings':
        response += random.choice(greetings_responces)
    elif message_classification == 'farewell':
        response += random.choice(farewells_responces)
    elif message_classification == 'question':
        response += random.choice(question_responces)
        
    sentiment_rate = service.sentiment(message)
    if sentiment_rate == 'positive': 
        response += random.choice(positive_responces)
    elif sentiment_rate == 'neutral':
        response += random.choice(neutral_responces)
    elif sentiment_rate == 'negative':
        response += random.choice(negative_responces)
    
    return [response, message_classification]

@app.route("/", methods=['GET', 'POST'])
def chat():
    """
    Manages the chat interface by storing user messages in the session.
    Handles both GET requests to render the chat page and POST requests to process
    user messages, generate responses, and update the message history.
    """
    if 'messages' in session:
        session['messages'] = session.get('messages')
    else:
        session['messages'] = []
    messages = session['messages']
    
    if request.method == 'POST':
        data = request.json
        message = data.get('message')   

        generated_answer = __generate_answer(message)   
        response_message = generated_answer[0]
        message_classification = generated_answer[1]
        
        messages.append({'text': message, 'sender': 'user', 'text_class': message_classification})
        messages.append({'text': response_message, 'sender': 'server'})
        
        return jsonify(messages=messages, response_message=response_message)

    return render_template('index.html', messages=messages)

@app.route('/feedback', methods=['POST'])
def feedback():
    """
    Handles feedback submissions by analyzing the sentiment of the provided feedback message.
    If the sentiment is not neutral, it logs the last three user messages along with the sentiment 
    grade to a CSV file for further analysis.
    """
    data = request.json
    feedback_message = data.get('feedback') 

    sentiment_rate = service.sentiment(feedback_message)

    if sentiment_rate != 'neutral':
        messages = session['messages'] 
        feedback_messeges = [messages[-6]['text'], messages[-4]['text'], messages[-2]['text']]    
        feedback_class = [messages[-6]['text_class'], messages[-4]['text_class'], messages[-2]['text_class']]    
        df = pd.DataFrame(feedback_messeges)
        df['grade'] = sentiment_rate
        df['class'] = feedback_class
        df.to_csv(os.path.join(os.path.dirname(__file__), '..', 'data', 'feedback.csv'), mode='a', header=False, index=False)
        
    return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(debug=True)
