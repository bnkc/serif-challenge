from typing import Optional

from pydantic import BaseModel


class FileLocation(BaseModel):
    description: str
    location: str


class ReportingPlans(BaseModel):
    plan_name: Optional[str] = None
    plan_id_type: str
    plan_id: str
    plan_market_type: str


class ReportingStructure(BaseModel):
    reporting_plans: list[ReportingPlans]
    in_network_files: Optional[list[FileLocation]] = None
    allowed_amount_file: Optional[FileLocation] = None
