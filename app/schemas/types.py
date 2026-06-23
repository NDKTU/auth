from typing import Annotated

from pydantic import BeforeValidator

StrStripped = Annotated[str, BeforeValidator(str.strip)]
StrNormalized = Annotated[str, BeforeValidator(lambda v: v.strip().lower())]
