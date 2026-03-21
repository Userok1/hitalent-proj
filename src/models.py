from typing import Any

from fastapi import HTTPException
from sqlalchemy import ForeignKey, select, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
import datetime

from src.database import Base


class DepartmentOrm(Base):
    __tablename__ = "departments"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(length=200), nullable=False, unique=True)
    parent_id: Mapped[int | None] = mapped_column(ForeignKey("departments.id", ondelete="CASCADE"))
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    
    children: Mapped[list["DepartmentOrm"]] = relationship(
        back_populates="parent", 
        cascade="all, delete-orphan", 
    )
    parent: Mapped["DepartmentOrm"] = relationship(
        back_populates="children",
        remote_side=[id],
    )
    
    employees: Mapped[list["EmployeeOrm"]] = relationship(
        back_populates="department",
        cascade="all, delete-orphan",
    )
    
    @validates("name", "parent")
    def validate_attrs(self, key, value):
        if value is None:
            return None
        
        if key == "name":
            if len(value) < 1 or len(value) > 200:
                raise ValueError("Name's length should be between 1 and 200")
            return value.strip()

        if key == "parent":
            if value:
                if self is value:
                    raise HTTPException(
                        status_code=400,
                        detail="Department can't be the parent to itself",
                    )
        
                current = value
                visited = {self}
                while current:
                    if current in visited:
                        raise HTTPException(
                            status_code=400,
                            detail="Department can't be cycled"
                        )
                    visited.add(current)
                    current = current.parent
            
            return value
            

class EmployeeOrm(Base):
    __tablename__ = "employees"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id"), nullable=False)
    full_name: Mapped[str] = mapped_column(String(length=200), nullable=False)
    position: Mapped[str] = mapped_column(String(length=200), nullable=False)
    hired_at: Mapped[datetime.datetime | None]
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    
    department: Mapped["DepartmentOrm"] = relationship(
        back_populates="employees",
    )

    @validates("department_id", "full_name", "position", "department")
    def validate_attrs(self, key, value):
        if key == "full_name" or key == "position":
            if len(value) < 1 or len(value) > 200:
                raise ValueError(f"{key}'s length should be between 1 and 200")

            return value
        
        if key == "department" or key == "department_id":
            _exc = HTTPException(
                status_code=404,
                detail="Parent not found"
            )
            if key == "department" and value is None:
                raise _exc
            if key == "department_id" and value is None:
                raise _exc

            return value
    

if __name__ == "__main__":
    # Тест 1: Сам себе родитель
    # dept = DepartmentOrm(id=1, name="IT")
    # dept.parent = dept
    
    # Тест 2: Цикл
    # d1 = DepartmentOrm(id=1, name="1")
    # d2 = DepartmentOrm(id=2, parent=d1, name="2")
    # d3 = DepartmentOrm(id=3, parent=d2, name="3")
    # d1.parent = d3
    pass