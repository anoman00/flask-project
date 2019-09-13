from app import db, ma


# Question Model


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    difficulty = db.Column(db.Enum("Hard", "Medium", "Easy"))
    question = db.Column(db.Text(), nullable=False)
    example = db.Column(db.PickleType)
    answer = db.Column(db.PickleType, nullable=False)
    solutions = db.relationship('Solution', backref='question', lazy=True)

    def __init__(self, difficulty, question, example, answer):
        self.difficulty = difficulty
        self.question = question
        self.example = example
        self.answer = answer

    def dictate(self):
        return {
            "difficulty": self.difficulty,
            "question": self.question,
            "example": self.example,
            "answer": self.answer
        }


# Solution Model


class Solution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey(
        'question.id'), nullable=False)
    username = db.Column(db.String(100))
    code = db.Column(db.Text(), nullable=False)
    output = db.Column(db.Enum("Pass", "Fail"), nullable=False)

    def __init__(self, question_id, username, code, output):
        self.question_id = question_id
        self.username = username
        self.code = code
        self.output = output


# Solution and Question Schema

class QuestionSchema(ma.Schema):
    class Meta:
        fields = ('id', 'difficulty', 'question', 'example', 'answer')


class SolutionSchema(ma.Schema):
    class Meta:
        fields = ('id', 'question_id', 'username', 'code', 'output')


# Init Schema
question_schema = QuestionSchema()
questions_schema = QuestionSchema(many=True)
solution_schema = SolutionSchema()
solutions_schema = SolutionSchema(many=True)


def question_inserts(question_list):
    db.drop_all()
    db.create_all()
    for question in question_list:
        question_insert = Question(
            question["difficulty"], question["question"], question["example"], question["answer"])
        db.session.add(question_insert)
    db.session.commit()
    return True


question_list = [
    {
        "difficulty": "Medium",
        "question": "Determine if an input is an uppercase English letter.",
        "example": [{"variables": 'A', "result": True}, {"variables": 'a', "result": False}, {"variables": '0', "result": False}],
        "answer": [True, False, False]
    },
    {
        "difficulty": "Easy",
        "question": "Print hello world",
        "example": [],
        "answer": ["hello world"]
    }
]


question_inserts(question_list)