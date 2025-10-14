from bson import ObjectId
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime


class PyObjectId(ObjectId):
    """Custom type for MongoDB ObjectId"""
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, _schema_generator):
        return {"type": "string"}


class OrderBase(BaseModel):
    """Base order model"""
    product_name: str = Field(..., min_length=1, max_length=200, description="Name of the product")
    quantity: int = Field(..., gt=0, description="Quantity of products (must be > 0)")
    customer_email: EmailStr = Field(..., description="Customer's email address")


class OrderCreate(OrderBase):
    """Model for creating a new order"""
    pass


class OrderResponse(OrderBase):
    """Model for order response"""
    id: str = Field(..., alias="_id", description="Order's unique identifier")
    created_at: datetime = Field(..., description="Order creation timestamp")
    status: str = Field(default="pending", description="Order status")

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "id": "507f1f77bcf86cd799439011",
                "product_name": "Laptop HP",
                "quantity": 2,
                "customer_email": "customer@example.com",
                "created_at": "2025-01-15T10:30:00",
                "status": "pending"
            }
        }


class OrderInDB(OrderBase):
    """Model for order stored in database"""
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    status: str = Field(default="pending")

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
