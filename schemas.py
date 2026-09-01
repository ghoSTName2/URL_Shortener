from datetime import datetime
from pydantic import BaseModel, ConfigDict, HttpUrl

class URLCreate(BaseModel):
    url : HttpUrl

class URLResponse(BaseModel):
    short_code: str
    original_url: HttpUrl
    
    model_config = ConfigDict(from_attributes=True)
    
class URLStatsResponse(URLResponse):
    clicks: int
    created_at: datetime
    last_clicked_at: datetime | None = None
    
    