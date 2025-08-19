from pydantic import BaseModel
from typing import Optional

class FAQCategorySchema(BaseModel):
    category_id: int
    title: str

    class Config:
        from_attributes = True

class FAQQuestionListSchema(BaseModel):
    question_id: int
    category_id: int
    question: str

    class Config:
        from_attributes = True

class FAQQuestionDetailSchema(FAQQuestionListSchema):
    answer: str
    reference_title: Optional[str]
    reference_url: Optional[str]