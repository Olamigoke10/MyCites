from typing import Literal

from pydantic import BaseModel, Field


CitationStyle = Literal["APA", "MLA", "IEEE"]


class CitationResponse(BaseModel):
    references: list[str] = Field(default_factory=list)
    annotated_text: str = ""
    warnings: list[str] = Field(default_factory=list)
