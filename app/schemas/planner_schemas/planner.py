from datetime import date

from pydantic import BaseModel


class PlanMetaData(BaseModel):
    plan_name: str
    destination: str
    init_date: date
    end_date: date


class AttractionPlan(BaseModel):
    plan_id: str
    date: str
    attraction_id: str
