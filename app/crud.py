from ms_core import BaseCRUD

from app.models import Question, Answer
from app.schemas import QuestionSchema, AnswerSchema


class QuestionCRUD(BaseCRUD[Question, QuestionSchema]):
    model = Question
    schema = QuestionSchema

class AnswerCRUD(BaseCRUD[Answer, AnswerSchema]):
    model = Answer
    schema = AnswerSchema
