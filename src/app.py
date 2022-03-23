import json
import numpy as np
import tensorflow as tf
from flask import Flask, render_template, request
from keras_preprocessing.sequence import pad_sequences
from wtforms import Form, TextAreaField, validators

app=Flask(__name__)

# Object to store the inserted Data
class QuestionForm(Form):
    question_user = TextAreaField('', [validators.DataRequired()])

def getTopThreeQuestions(user_question):
    found_questions = []
    encoded_user_question = tokenizer.texts_to_sequences([user_question])
    encoded_user_question = pad_sequences(encoded_user_question, maxlen = 36, padding = 'post')
    something = np.asarray([encoded_user_question[0]]*len(completeQuestionsDict))
    test = model.predict([something, completeQuestionsDict], batch_size = 4096, verbose = 1, use_multiprocessing = True)
    print(np.sort(test.flatten()))
    a = test.flatten()
    ind = np.argpartition(a, -5)[-5:]
    top3 = ind
    print(top3)
    for item in top3:
        decoded_question = tokenizer.sequences_to_texts([completeQuestionsDict[item]])[0]
        found_questions.append(decoded_question)
    return found_questions

@app.route('/')
def index():
    form = QuestionForm(request.form)
    return render_template('question_input.html', form=form)

@app.route('/propsed_question', methods=['POST'])
def hello():
    form = QuestionForm(request.form)
    if request.method == 'POST' and form.validate():
        asked_question = request.form['question_user']
        foundQuestions = getTopThreeQuestions(asked_question)
        proposed_question1 = foundQuestions[0]
        proposed_question2 = foundQuestions[1]
        proposed_question3 = foundQuestions[2]
        proposed_question4 = foundQuestions[3]
        proposed_question5 = foundQuestions[4]
        return render_template(
            'question_proposed.html',
            form=form,
            question_asked=asked_question,
            question_pr1=proposed_question1,
            question_pr2=proposed_question2,
            question_pr3=proposed_question3,
            question_pr4=proposed_question4,
            question_pr5=proposed_question5)
    return render_template('question_input.html', form=form)

def runServer():
    # Read model
    model = tf.keras.models.load_model('models/questions.h5')
    # Read the tokenizer
    with open('models/tokenizer.json') as f:
        data = json.load(f)
        tokenizer = tf.keras.preprocessing.text.tokenizer_from_json(data)
    # Read the whole question catalog
    completeQuestionsDict = np.load('models/questions.npy')
    app.run(debug=True, use_reloader=False)

if __name__ == '__main__' :
    runServer()