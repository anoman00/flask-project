from app import app, db
from app.models import (Question, Solution, question_schema,
                        questions_schema, solution_schema, solutions_schema)
from flask import request, jsonify, render_template


# Create a Question
@app.route('/question', methods=['POST'])
def add_question():
    difficulty = request.json['difficulty']
    question = request.json['question']
    example = request.json['example']
    answer = request.json['answer']

    new_question = Question(difficulty, question, example, answer)

    db.session.add(new_question)
    db.session.commit()

    return question_schema.jsonify(new_question)

# Edit a Question
@app.route('/question/<id>', methods=['PUT'])
def edit_question(id):
    question = Question.query.get(id)
    question.difficulty = request.json['difficulty']
    question.question = request.json['question']
    question.example = request.json['example']
    question.answer = request.json['answer']

    db.session.commit()

    return question_schema.jsonify(question)

# Delete a Question
@app.route('/question/<id>', methods=['DELETE'])
def del_question(id):
    Question.query.filter_by(id=id).delete()

    db.session.commit()

    return question_schema.jsonify(questions_schema.dump(Question.query.all()))

# Get all questions
@app.route('/questions', methods=['GET'])
def get_all_questions():
    all_questions = Question.query.all()
    result = questions_schema.dump(all_questions)
    return jsonify(result)

# Get questions by difficulty
@app.route('/questions/<difficulty>', methods=['GET'])
def get_questions(difficulty):
    all_questions = Question.query.filter_by(difficulty=difficulty).all()
    result = questions_schema.dump(all_questions)
    return jsonify(result)

# Get a question
@app.route('/question/<id>', methods=['GET'])
def get_question_by_id(id):
    question = Question.query.get(id)
    return question_schema.jsonify(question)

# Create a Solution in Post
@app.route('/solution', methods=['POST'])
def add_solution():
    question_id = request.json['question_id']
    username = request.json['username']
    code = request.json['code']
    output = request.json['output']

    new_solution = Solution(question_id, username, code, output)

    db.session.add(new_solution)
    db.session.commit()

    return solution_schema.jsonify(new_solution)

# Get all solutions
@app.route('/solutions', methods=['GET'])
def get_all_solutions():
    all_solutions = Solution.query.all()
    result = solutions_schema.dump(all_solutions)
    return jsonify(result)

# Get all solutions by username
@app.route('/solutions/<username>', methods=['GET'])
def get_solutions(username):
    all_solutions = Solution.query.filter_by(username=username).all()
    result = solutions_schema.dump(all_solutions)
    return jsonify(result)

# Get a solution
@app.route('/solution/<id>', methods=['GET'])
def get_solution_by_id(id):
    solution = Solution.query.get(id)
    return solution_schema.jsonify(solution)


@app.route('/')
def get():
    all_questions = Question.query.all()
    questions = questions_schema.dump(all_questions)
    return render_template('index.html', questions=questions)


@app.route('/', methods=['POST'])
def my_form_post():
    question_id = request.form["questionId"]
    username = request.form['username']
    code = request.form['textbox']
    returned = request.form['returnedAnswer']
    true_returned = returned[:-2]
    answer_location = Question.query.get(question_id)
    answer = answer_location.dictate()["answer"]
    if answer == true_returned:
        output = "Pass"
    else:
        output = "Fail"
    new_solution = Solution(question_id, username, code, output)

    db.session.add(new_solution)
    db.session.commit()
    return {'your code': code, 'output': output, 'response': true_returned, 'expected': answer}
