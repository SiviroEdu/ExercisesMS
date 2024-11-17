from typing import Annotated

from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.params import Depends, Query
from starlette import status
from tortoise.contrib.postgres.functions import Random

from app import QuestionSchema, QuestionComplexCreate, QuestionCRUD, QuestionCreate, Answer, Question, QuestionsDone
from app.bridges.dependencies import get_current_user, get_current_admin
from app.bridges.users import UserSchema, UsersBridge

router = APIRouter(
    prefix="/exercises",
    tags=["exercises"]
)

@router.post("/")
async def create_question(
        payload: QuestionComplexCreate,
        user: Annotated[UserSchema, Depends(get_current_admin)]
):
    question_payload = payload.model_dump()
    answers_payload = question_payload.pop("answers")

    question = await QuestionCRUD.create(QuestionCreate(**question_payload))

    answers = [Answer(**answer, question_id=question.id) for answer in answers_payload]
    await Answer.bulk_create(answers)

    return answers


@router.get("/random")
async def get_random(
        user: Annotated[UserSchema, Depends(get_current_user)],
        course_id: int = Query()
) -> QuestionSchema | None:
    questions_done = await QuestionsDone.filter(user_id=user.id).values_list("question_id", flat=True)

    question = await (Question.annotate(order=Random()).filter(course_id=course_id, id__not_in=questions_done)
                                .order_by("order").limit(1).first())

    if not question:
        return None

    return await QuestionSchema.from_tortoise_orm(question)


async def mark_question_done(user_id: int, question_id: int):
    await QuestionsDone.create(user_id=user_id, question_id=question_id)


async def reward_user(user_id: int, question_id: int):
    worth = await Question.get_or_none(id=question_id).values_list("worth_coins")
    worth = worth[0]

    await UsersBridge.inc_currency(user_id, "coins", worth)


@router.post("/submit")
async def submit_answer(
        user: Annotated[UserSchema, Depends(get_current_user)],
        background_tasks: BackgroundTasks,
        question_id: int = Query(),
        answer_id: int = Query()
) -> bool:
    questions_done = await QuestionsDone.get_or_none(question_id=question_id, user_id=user.id)

    if questions_done:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already solved"
        )

    is_correct = await Answer.get_or_none(id=answer_id, question_id=question_id).values_list("is_correct")

    if is_correct is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This answer does not exist."
        )

    is_correct = is_correct[0]

    if is_correct:
        args = user.id, question_id
        background_tasks.add_task(mark_question_done, *args)
        background_tasks.add_task(reward_user, *args)

    return is_correct
