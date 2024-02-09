import sys
sys.path.append("..")

from sqlite3 import Date
from fastapi import Depends, HTTPException, APIRouter, Request
from pydantic import BaseModel
import model
from HRdatabase import engine, SessionLocal
from sqlalchemy.orm import Session
from .auth import get_current_user, get_user_exception
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix="/regentcollege",
    tags=["regentcollege"],
    responses ={404: {"description": "Not found"}}
)

model.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_class=HTMLResponse)
async def read_all_by_user(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@router.get("/", response_class=HTMLResponse)
async def read_all_by_user(request: Request, db: Session = Depends(get_db)):

    employees_data = db.query(model.Employees).filter(model.Employees.owner_id == 1).all()
    home_students_data = db.query(model.HomeStudent).filter(model.HomeStudent.owner_id == 1).all()
    international_students_data = db.query(model.InternationalStudent).filter(model.InternationalStudent.owner_id == 1).all()
    student_credit_data = db.query(model.StudentCredit).filter(model.StudentCredit.owner_id == 1).all()
    student_dbs_data = db.query(model.StudentDBS).filter(model.StudentDBS.owner_id == 1).all()
    employee_dbs_data = db.query(model.EmployeeDBS).filter(model.EmployeeDBS.owner_id == 1).all()
    employee_bank_details_data = db.query(model.EmployeeBankDetails).filter(model.EmployeeBankDetails.owner_id == 1).all()


    # Pass the data to the template
    return templates.TemplateResponse("home.html", {
        "request": request,
        "employees_data": employees_data,
        "home_students_data": home_students_data,
        "international_students_data": international_students_data,
        "student_credit_data": student_credit_data,
        "student_dbs": student_dbs_data,
        "employee_dbs": employee_dbs_data,
        "employee_bank_details": employee_bank_details_data
    })

@router.get("/add-regentcollege", response_class=HTMLResponse)
async def add_new_regentcollege(request: Request):
    return templates.TemplateResponse("add-regentcollege.html", {"request": request})

@router.get("/edit-regentcollege/{regentcollege_id}", response_class=HTMLResponse)
async def edit_regentcollege(request: Request):
    return templates.TemplateResponse("edit-regentcollege.html", {"request": request})


