from fastapi import APIRouter, Depends, Query, HTTPException
from typing import Annotated, Literal
from sqlalchemy.orm import Session

from .utils import add_department, add_employee, get_department_info, remove_department, update_department
from .schemas import Department, DepartmentReturn, Employee, EmployeeReturn, DepartmentInfo, DepartmentUpdate
from .models import DepartmentOrm, EmployeeOrm
from .database import get_session

router = APIRouter()


@router.post("/departments", response_model=DepartmentReturn, status_code=201)
def create_department(department: Department, session: Annotated[Session, Depends(get_session)]):
    department_in_db: DepartmentOrm = add_department(department, session)
    return DepartmentReturn.model_validate(department_in_db)


@router.post("/departments/{id}/employees", response_model=EmployeeReturn, status_code=201)
def create_employee(id: int, employee: Employee, session: Annotated[Session, Depends(get_session)]):
    employee_in_db: EmployeeOrm = add_employee(id, employee, session)
    return EmployeeReturn.model_validate(employee_in_db)


@router.get("/departments/{id}", response_model=DepartmentInfo)
def read_department_info(
    id: int,
    session: Annotated[Session, Depends(get_session)],
    depth: Annotated[int, Query(ge=1, le=5)] = 1,
    include_employees: bool = True,
):
    with session.begin():
        info = get_department_info(id, depth, include_employees, session)
        if not info:
            raise HTTPException(
                status_code=404,
                detail="Not found",
            )
        # return DepartmentInfo.model_validate(info)
        return info
    

@router.patch("/departments/{id}")
def move_department(id: int, dep_changes: DepartmentUpdate, session: Annotated[Session, Depends(get_session)]):
    updated_dep: DepartmentOrm = update_department(id, dep_changes, session)
    return DepartmentReturn.model_validate(updated_dep)


@router.delete("/departments/{id}", status_code=204)
def delete_department(
    id: int,
    mode: Literal["cascade", "reassign"], 
    session: Annotated[Session, Depends(get_session)],
    reassign_to_department_id: Annotated[int | None, Query(description="Required id mode = 'reassign'")] = None,
):
    try:
        remove_department(id, mode, reassign_to_department_id, session)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
