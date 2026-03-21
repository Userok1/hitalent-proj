from pydantic import BaseModel, Field
import datetime


class Department(BaseModel):
    name: str
    parent_id: int | None = Field(
        default=None,
        examples=[None]
    )
    

class DepartmentReturn(BaseModel):
    id: int
    name: str
    parent_id: int | None
    created_at: datetime.datetime
    
    model_config = {"from_attributes": True}
    

class Employee(BaseModel):
    full_name: str
    position: str
    hired_at: datetime.datetime | None = Field(
        default=None,
        examples=[None]
    )
    

class EmployeeReturn(BaseModel):
    id: int
    department_id: int
    full_name: str
    position: str
    hired_at: datetime.datetime | None
    created_at: datetime.datetime
    
    model_config = {"from_attributes": True}
    

class DepartmentInfo(BaseModel):
    id: int
    name: str
    parent_id: int | None
    created_at: datetime.datetime
    employees: list[EmployeeReturn]
    children: list[DepartmentInfo] | list[str]
    

class DepartmentUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        examples=[None]
    )
    parent_id: int | None = Field(
        default=None,
        examples=[None]
    )