from flask import Flask, render_template, request, redirect, flash
from flask import session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my secret'


@app.route('/')
def startpage():
    return render_template('start-page.html')

@app.route('/start', methods=["POST"])
def startsession():
    session['responses'] = []
    return redirect('/questions/0')

@app.route('/questions/<int:q_num>')
def show_question(q_num):
    if not q_num == len(session['responses']):
        flash("Answer previous questions first")
        return redirect(f'/questions/{len(session["responses"])}')
    question = satisfaction_survey.questions[q_num].question
    choices = satisfaction_survey.questions[q_num].choices
    button_text = "Next Question" if len(session['responses']) < len(satisfaction_survey.questions) - 1 else "Finish"
    return render_template('question.html', question=question, choices=choices, button_text=button_text)

@app.route('/answer', methods=["POST"])
def answer_post():
    answer = request.form
    new_responses = session['responses']
    new_responses.append(answer['choice'])
    session['responses'] = new_responses
    if len(session['responses']) == len(satisfaction_survey.questions):
        return redirect('thank-you')
    return redirect(f'/questions/{len(session["responses"])}')

@app.route('/thank-you')
def thanks():
    return '<h2>Thank you for filling out the survery</h2>'