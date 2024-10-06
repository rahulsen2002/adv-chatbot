from flask import Flask, render_template, request, jsonify
import re
import long_responses as long

app = Flask(__name__)

def message_probability(user_message, recognised_words, single_response=False, required_words=[]):
    message_certainty = 0
    has_required_words = True

    for word in user_message:
        if word in recognised_words:
            message_certainty += 1

    percentage = float(message_certainty) / float(len(recognised_words))

    for word in required_words:
        if word not in user_message:
            has_required_words = False
            break

    if has_required_words or single_response:
        return int(percentage * 100)
    else:
        return 0

def check_all_messages(message):
    highest_prob_list = {}

    def response(bot_response, list_of_words, single_response=False, required_words=[]):
        nonlocal highest_prob_list
        highest_prob_list[bot_response] = message_probability(message, list_of_words, single_response, required_words)

    # Greeting responses
    response('Hello!', ['hello', 'hi', 'hey', 'sup', 'heyo'], single_response=True)
    response('Goodbye!', ['bye', 'goodbye', 'see you'], single_response=True)

    # General conversation responses
    response('I am a bot, here to help you.', ['who', 'are', 'you'], required_words=['who', 'you'])
    response('I am doing well, thank you!', ['how', 'are', 'you'], required_words=['how', 'you'])
    response('I am a chatbot created to assist with your queries.', ['what', 'are', 'you'], required_words=['what', 'you'])
    response('I love coding!', ['do', 'you', 'like', 'coding'], required_words=['like', 'coding'])

    # More specific responses
    response('Yes, I can assist with that!', ['can', 'you', 'help'], required_words=['help'])
    response('I support Python, JavaScript, and more.', ['what', 'languages', 'support'], required_words=['languages', 'support'])
    response('You can find Flask documentation at https://flask.palletsprojects.com.', ['flask', 'documentation'], required_words=['flask'])
    response('The weather is always sunny in chatbot land!', ['how', 'is', 'the', 'weather'], required_words=['weather'])

    # Programming-related responses
    response('You can use the `for` loop in Python to iterate over elements.', ['how', 'to', 'use', 'for', 'loop'], required_words=['for', 'loop'])
    response('Yes, I can help you with data structures.', ['can', 'you', 'help', 'with', 'data', 'structures'], required_words=['data', 'structures'])
    response('Machine learning is a subset of AI focused on algorithms that improve automatically through experience.', ['what', 'is', 'machine', 'learning'], required_words=['machine', 'learning'])

    # Fun response
    response('I am just a bunch of code, but thank you!', ['you', 'are', 'awesome'], required_words=['awesome'])

    # Yes/No responses
    response('Yes!', ['is', 'it', 'possible'], required_words=['possible'])
    response('No, I am sorry.', ['is', 'it', 'impossible'], required_words=['impossible'])

    # Keep your existing responses
    response('yes its for all users', ['suitable', 'advance', 'users'], required_words=['beginner'])
    response('yes u can do that', ['learn', 'pace', 'can', 'i'], single_response=True)
    response('Thank you!', ['i', 'love', 'code', 'palace'], required_words=['code', 'palace'])
    response('good', ['how', 'is', 'doubt', 'support'], single_response=True)
    response('NO', ['dsa', 'good', 'prerequisite', 'course'], single_response=True)
    response('yes u can pay in emi mode', ['emi', 'pay', 'course'], single_response=True)
    response('only online mode', ['offline', 'online', 'course'], single_response=True)
    response('yes you will get certificate after completing the course', ['does', 'certificate', 'offer', 'course'], single_response=True)
    response('yes', ['market', 'todays', 'relevant'], single_response=True)
    response('good', ['how', 'is', 'the', 'doubt', 'support'], single_response=True)
    response('no sorry', ['financial', 'aid', 'under-privileged'], single_response=True)
    response('there are dedicated placement courses u can look for that', ['course', 'aid', 'opportunities'], single_response=True)
    response('generally there no such fixed salary it depends upon you', ['how', 'much', 'can', 'i', 'make'], single_response=True)
    response('yes u can for refund if its under refund course but u should fulfill its rules', ['money', 'refund', 'back'], single_response=True)
    response('NO', ['pre-requirement', 'course', 'what'], single_response=True)

    # Find best match
    best_match = max(highest_prob_list, key=highest_prob_list.get)
    return long.unknown() if highest_prob_list[best_match] < 1 else best_match

def get_response(user_input):
    split_message = re.split(r'\s+|[,;?!.-]\s*', user_input.lower())
    response = check_all_messages(split_message)
    return response

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_bot_response():
    user_input = request.json['user_input']
    response = get_response(user_input)
    return response  


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
