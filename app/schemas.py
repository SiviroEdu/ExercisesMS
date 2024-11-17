import enum
from typing import ClassVar

from pydantic import BaseModel
from tortoise import Tortoise
from tortoise.contrib.pydantic import pydantic_model_creator

from app import Question
from app.models import Answer

Tortoise.init_models(
    ["app.models"], "models"
)

QuestionSchema = pydantic_model_creator(Question, name="QuestionSchema")
QuestionCreate = pydantic_model_creator(
    Question,
    name="QuestionCreate",
    exclude_readonly=True,
)

AnswerSchema = pydantic_model_creator(Answer, name="AnswerSchema")
AnswerCreate = pydantic_model_creator(
    Answer,
    name="AnswerCreate",
    exclude_readonly=True,
)


class AnswerCreateQuestion(AnswerCreate):
    question_id: ClassVar[int]


class QuestionComplexCreate(QuestionCreate):
    answers: list[AnswerCreateQuestion]
