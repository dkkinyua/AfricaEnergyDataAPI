from typing import Optional, Any, Dict
from pydantic import BaseModel, Field

class EconomicModel(BaseModel):
    country: str
    country_serial: Optional[int]
    metric: str
    unit: Optional[str]
    sector: Optional[str]
    sub_sector: Optional[str]
    sub_sub_sector: Optional[str]
    source_link: Optional[str]
    source: Optional[str]
    data: Optional[Dict[str, Optional[float]]] = Field(default_factory=dict)

    class Config:
        orm_mode = True

    @classmethod
    def from_db(cls, doc: Dict[str, Any]):
        years = {str(k): v for k, v in doc.items() if str(k).isdigit()}
        base_fields = {k: v for k, v in doc.items() if not str(k).isdigit()}
        return cls(**base_fields, data=years)