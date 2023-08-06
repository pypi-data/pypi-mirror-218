import re
from typing import Dict, List, Optional

import paperqa
from paperqa.types import Answer
from pydantic import BaseModel, validator

# NOTE: Do not edit these - they come from the paperqa-sever


def _extract_doi(citation: str) -> Optional[str]:
    doi = re.findall(r"10\.\d{4}/\S+", citation, re.IGNORECASE)
    if len(doi) > 0:
        return doi[-1]
    return None


class UploadMetadata(BaseModel):
    filename: str
    citation: str
    key: Optional[str] = None


class Doc(paperqa.Doc):
    doi: Optional[str] = None

    @validator("doi", pre=True)
    def citation_to_doi(cls, v: Optional[str], values: Dict) -> Optional[str]:
        if v is None and "citation" in values:
            return _extract_doi(values["citation"])
        return v


class DocsStatus(BaseModel):
    name: str
    llm: str
    summary_llm: str
    docs: List[Doc]
    doc_count: int
    writeable: bool = False


class QueryRequest(BaseModel):
    query: str
    llm: str = "gpt-4"
    summary_llm: str = "gpt-3.5-turbo"
    length: str = "about 200 words, but can be longer if necessary"
    max_sources: int = 7
    consider_sources: int = 10

    @validator("max_sources")
    def max_sources_for_gpt(cls, v: int, values: dict, **kwargs) -> int:
        if "gpt" in values["llm"] and v > 8:
            raise ValueError("Max sources for GPT models is 8")
        return v


class AnswerResponse(BaseModel):
    answer: Answer
    usage: Dict[str, List[int]]
    bibtex: Dict[str, str]
