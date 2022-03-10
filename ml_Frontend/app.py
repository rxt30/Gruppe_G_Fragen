from flask import Flask, render_template, request
from wtforms import Form, TextAreaField, validators

app=Flask(__name__)

# Object to store the inserted Data
class QuestionForm(Form):
    question_user = TextAreaField('', [validators.DataRequired()])

@app.route('/')
def index():
    form = QuestionForm(request.form)
    return render_template('question_input.html', form=form)

@app.route('/propsed_question', methods=['POST'])
def hello():
    form = QuestionForm(request.form)
    if request.method == 'POST' and form.validate():
        asked_question = request.form['question_user']
        proposed_question1 = "Test1"
        proposed_question2 = "Test2"
        proposed_question3 = "Test3"
        return render_template(
            'question_proposed.html',
            form=form,
            question_asked=asked_question,
            question_pr1=proposed_question1,
            question_pr2=proposed_question2,
            question_pr3=proposed_question3)
    return render_template('question_input.html', form=form)

if __name__ == '__main__' :
    app.run(debug=True)
