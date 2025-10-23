from typing import Optional, Any, Dict
from pydantic import BaseModel, Field

class EconomicModel(BaseModel):
    country: str
    country_serial: Optional[int] = None
    metric: str
    unit: Optional[str] = None
    sector: Optional[str] = None
    sub_sector: Optional[str] = None
    sub_sub_sector: Optional[str] = None
    source_link: Optional[str] = None
    source: Optional[str] = None
    data: Optional[Dict[str, float]] = Field(default_factory=dict)

    class Config:
        from_attributes = True

    @classmethod
    def from_db(cls, doc: Dict[str, Any]):
        years = {str(k): v for k, v in doc.items() if str(k).isdigit()}
        base_fields = {k: v for k, v in doc.items() if not str(k).isdigit()}
        return cls(**base_fields, data=years)