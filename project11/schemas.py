from pydantic import BaseModel

class ReviewBase(BaseModel):
    restraunt_name: str
    dish_type: str
    rating: int
    
class ReviewCreate(ReviewBase):
    pass

class ReviewResponse(ReviewBase):
    id : int
    
    class Config:
        form_attributes = True