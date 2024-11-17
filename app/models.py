import enum

from ms_core import AbstractModel
from tortoise import fields

class QuestionType(enum.StrEnum):
    ONE_ANS = enum.auto()
    MULTI_ANS = enum.auto()
    OPEN_ANS = enum.auto()


class Question(AbstractModel):
    course_id = fields.BigIntField()
    topic_id = fields.BigIntField(default=0)
    worth_coins = fields.IntField()
    type = fields.CharEnumField(QuestionType)
    text = fields.TextField()

    answers: fields.ReverseRelation["Answer"]

    class Meta:
        table = "questions"


class Answer(AbstractModel):
    content = fields.TextField()
    is_correct = fields.BooleanField()

    question: fields.ForeignKeyRelation[Question] = fields.ForeignKeyField(
        "models.Question", "answers"
    )

    class Meta:
        table = "answers"


class QuestionsDone(AbstractModel):
    user_id = fields.IntField()

    question: fields.ForeignKeyRelation[Question] = fields.ForeignKeyField(
        "models.Question", "questions_done"
    )

    class Meta:
        table = "questions_done"
