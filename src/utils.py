from typing import Literal

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from .schemas import Department, DepartmentUpdate, Employee, DepartmentInfo, EmployeeReturn
from .models import DepartmentOrm, EmployeeOrm


def get_department(dep_id: int, session: Session) -> DepartmentOrm | None:
    select_dep_stmt = select(DepartmentOrm).where(DepartmentOrm.id == dep_id)
    return session.execute(select_dep_stmt).scalars().first()
    

def get_employee(emp_id: int, session: Session) -> EmployeeOrm | None:
    select_emp_stmt = select(EmployeeOrm).where(EmployeeOrm.id == emp_id)
    return session.execute(select_emp_stmt).scalars().first()


def add_department(department: Department, session: Session) -> DepartmentOrm:
    with session.begin():
        if not(department.parent_id):
            select_dep_stmt = select(DepartmentOrm).where(DepartmentOrm.name == department.name)
            if session.execute(select_dep_stmt).scalars().first():
                raise HTTPException(
                    status_code=400,
                    detail="Department with that name already exists"
                )
        else:
            select_parent_stmt = select(DepartmentOrm).where(DepartmentOrm.id == department.parent_id)
            parent = session.execute(select_parent_stmt).scalars().first()
            department_orm = DepartmentOrm(**department.model_dump())
            # if department.name in parent.children:
            if department_orm in parent.children:
                raise HTTPException(
                    status_code=400,
                    detail="Department can't have subdepartments with the same name"
                )

        department_in_db = DepartmentOrm(**department.model_dump())
        session.add(department_in_db)
        session.flush()
        session.refresh(department_in_db)

        return department_in_db
    

def add_employee(dep_id: int, employee: Employee, session: Session) -> EmployeeOrm:
    with session.begin():
        if not get_department(dep_id, session):
            raise HTTPException(
                status_code=404,
                detail="Employee should have department"            
            )
        employee_in_db = EmployeeOrm(**employee.model_dump(), department_id=dep_id)
        session.add(employee_in_db)
        session.flush()
        session.refresh(employee_in_db)
        
        return employee_in_db
    

def get_department_info(
    id: int, 
    depth: int, 
    include_employees: bool, 
    session: Session,
) -> DepartmentInfo | None:
        department: DepartmentOrm | None = get_department(id, session)
        if not department:
            return None

        employees_lst = []
        if include_employees:
            for emp_in_db in department.employees:
                emp = EmployeeReturn.model_validate(emp_in_db)
                employees_lst.append(emp)

        if depth == 1:
            children = [child.name for child in department.children]
            return DepartmentInfo(
                id=department.id,
                name=department.name,
                parent_id=department.parent_id,
                created_at=department.created_at,
                employees=employees_lst,
                children=children
            )
        else:
            children_lst = []
            for child_dep_in_db in department.children:
                dep_info = get_department_info(child_dep_in_db.id, depth - 1, include_employees, session)
                if dep_info is None:
                    break
                children_lst.append(dep_info)

        return DepartmentInfo(
            id=department.id,
            name=department.name,
            parent_id=department.parent_id,
            created_at=department.created_at,
            employees=employees_lst, 
            children=children_lst
        )
        

def update_department(dep_id: int, dep_changes: DepartmentUpdate, session: Session) -> DepartmentOrm:
    with session.begin():
        department_in_db: DepartmentOrm | None = get_department(dep_id, session)
        if not department_in_db:
            raise HTTPException(
                status_code=404,
                detail="Department not found"
            )
        if dep_changes.name:
            department_in_db.name = dep_changes.name
        if dep_changes.parent_id:
            parent: DepartmentOrm | None = get_department(dep_changes.parent_id, session)
            if not parent:
                raise HTTPException(
                    status_code=404,
                    detail="Parent department not found"
                )
            department_in_db.parent_id = dep_changes.parent_id
            department_in_db.parent = parent
            session.flush()
            session.refresh(department_in_db)

        return department_in_db
    

def remove_department(
    dep_id: int,
    mode: Literal["cascade", "reassign"],
    reassign_to_department_id: int | None,
    session: Session,
) -> None:
    with session.begin():
        dep_to_delete: DepartmentOrm | None = get_department(dep_id, session)
        if not dep_to_delete:
            raise HTTPException(
                status_code=404,
                detail="Department not found"
            )
        if mode == "reassign":
            if not reassign_to_department_id:
                raise ValueError("Required if mode = 'cascade'")
            dep_to_reassign: DepartmentOrm | None = get_department(reassign_to_department_id, session)
            if not dep_to_reassign:
                raise HTTPException(
                    status_code=404,
                    detail="Department to reassign not found",
                )
            dep_to_reassign.employees.extend(dep_to_delete.employees)
            dep_to_reassign.children.extend(dep_to_delete.children)
            dep_to_delete.employees = []
            dep_to_delete.children = []
        session.delete(dep_to_delete)
        session.flush()
