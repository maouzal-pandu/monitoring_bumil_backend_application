from datetime import date
from decimal import Decimal
from pydantic import BaseModel, condecimal


class SetHphtSchema(BaseModel):
    user_id: int
    hpht: date
    bb_awal: Decimal
    gravida: int
    paritas: int
    abortus: int
