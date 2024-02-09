from sqlite3 import Date  # Import Date from sqlite3 module (Note: Date from sqlite3 might not be used in the code)
from fastapi import FastAPI, Depends, HTTPException  # Import FastAPI and related modules
from pydantic import BaseModel  # Import BaseModel from pydantic module
import model  # Import the 'model' module
from HRdatabase import engine, SessionLocal  # Import 'engine' and 'SessionLocal' from 'HRdatabase'
from sqlalchemy.orm import Session  # Import Session from sqlalchemy.orm module

app = FastAPI()  # Create a FastAPI app instance

model.Base.metadata.create_all(bind=engine)  # Create database tables based on the defined models


def get_db():
    try:
        db = SessionLocal()  # Create a database session
        yield db  # Yield the database session to be used in the route functions
    finally:
        db.close()  # Close the database session when done


# Define Pydantic models for different entities

class Internationalstudent(BaseModel):  # ... (attributes for Internationalstudent)
    studentID: int
    firstName: str
    lastName: str
    dateOfBirth: Date
    homeAddress: str
    homeCountry: str
    phoneNumber: str
    PassportNumber: int
    VisaStatus: str


class Employees(BaseModel):  # ... (attributes for Employees)
    employeeID: int
    firstName: str
    lastName: str
    dateOfBirth: Date
    address: str
    phoneNumber: str
    email: str
    department: str
    position: str
    hireDate: str
    salary: int


class EmpBankDetails(BaseModel):
    employeeID: int
    bankName: str
    accountHolderName: str
    AccountNumber: int
    SortCode: int
    IBAN: int
    BIC_SwiftCode: int


class EmployeeDBS(BaseModel):
    employeeID: int
    firstName: str
    lastName: str
    dateOfBirth: Date
    gender: str
    address: str
    phoneNumber: str
    email: str
    position: str
    dbsStatus: str
    dbsExpiryDate: Date


class HomeStudent(BaseModel):
    studentID: int
    firstName: str
    lastName: str
    dateOfBirth: Date
    homeAddress: str
    homeCountry: str
    homePhone: str


class StudentCredit(BaseModel):
    studentID: int
    bankAccountNumber: str
    currentCredits: str


class StudentDBS(BaseModel):
    studentID: int
    firstName: str
    lastName: str
    dateOfBirth: Date
    gender: str
    address: str
    phoneNumber: str
    email: str
    dbsStatus: str
    dbsExpiryDate: Date


class MultiTableData(BaseModel):
    international_student: Internationalstudent
    employees: Employees
    empBank_details: EmpBankDetails
    employee_dbs: EmployeeDBS
    student_dbs: StudentDBS
    student_credit: StudentCredit
    home_student: HomeStudent


class MultiTableUpdate(BaseModel):
    international_student: Internationalstudent
    employees: Employees
    empBank_details: EmpBankDetails
    employee_dbs: EmployeeDBS
    student_dbs: StudentDBS
    student_credit: StudentCredit
    home_student: HomeStudent

    # Route to create entries in multiple tables


@app.post("/create_entries")
async def create_entries(data: MultiTableData, db: Session = Depends(get_db)):
    international_student_model = model.InternationalStudent(**data.international_student.dict())
    db.add(international_student_model)

    student_dbs_model = model.StudentDBS(**data.student_dbs.dict())
    db.add(student_dbs_model)

    student_credit_model = model.StudentCredit(**data.student_credit.dict())
    db.add(student_credit_model)

    home_student_model = model.HomeStudent(**data.home_student.dict())
    db.add(home_student_model)

    employee_dbs_model = model.EmployeeDBS(**data.employee_dbs.dict())
    db.add(employee_dbs_model)

    empBank_details_model = model.EmployeeBankDetails(**data.empBank_details.dict())
    db.add(empBank_details_model)

    employees_model = model.Employees(**data.employees.dict())
    db.add(employees_model)

    db.commit()


# Route to read entries from multiple tables
@app.get("/")
async def read_all(db: Session = Depends(get_db)):
    international_student = db.query(model.InternationalStudent).all()
    home_student = db.query(model.HomeStudent).all()
    employees_dbs = db.query(model.EmployeeDBS).all()
    employees_bank = db.query(model.EmployeeBankDetails).all()
    student_dbs = db.query(model.StudentDBS).all()
    student_credit = db.query(model.StudentCredit).all()
    employees = db.query(model.Employees).all()

    result = {
        "international_student": international_student,
        "home_student": home_student,
        "employees_DBS": employees_dbs,
        "employees_bank": employees_bank,
        "student_DBS": student_dbs,
        "student_credit": student_credit,
        "employees": employees
    }

    return result




    # Route to update entries in multiple tables
@app.put("/update_entries/{record_id}")
async def update_entries(record_id: int, data: MultiTableUpdate, db: Session = Depends(get_db)):
    home_student_model = db.query(model.HomeStudent).filter(model.HomeStudent.id == record_id).first()
    if home_student_model is None:
        raise HTTPException(status_code=404, detail="HomeStudent not found")

    home_student_model.studentID = data.home_student.studentID
    home_student_model.firstName = data.home_student.firstName
    home_student_model.lastName = data.home_student.lastName
    home_student_model.dateOfBirth = data.home_student.dateOfBirth
    home_student_model.homeAddress = data.home_student.homeAddress
    home_student_model.homeCountry = data.home_student.homeCountry
    home_student_model.homePhone = data.home_student.homePhone

    db.commit()

    international_student_model = db.query(model.InternationalStudent).filter(
        model.InternationalStudent.id == record_id).first()
    if international_student_model is None:
        raise HTTPException(status_code=404, detail="InternationalStudent not found")

    international_student_model.studentID = data.international_student.studentID
    international_student_model.firstName = data.international_student.firstName
    international_student_model.lastName = data.international_student.lastName
    international_student_model.dateOfBirth = data.international_student.dateOfBirth
    international_student_model.homeAddress = data.international_student.homeAddress
    international_student_model.homeCountry = data.international_student.homeCountry
    international_student_model.phoneNumber = data.international_student.phoneNumber
    international_student_model.passportNumber = data.international_student.PassportNumber
    international_student_model.visaStatus = data.international_student.VisaStatus

    db.commit()

    employees_model = db.query(model.Employees).filter(model.Employees.id == record_id).first()
    if employees_model is None:
        raise HTTPException(status_code=404, detail="Employees not found")

    employees_model.employeeID = data.employees.employeeID
    employees_model.firstName = data.employees.firstName
    employees_model.lastName = data.employees.lastName
    employees_model.dateOfBirth = data.employees.dateOfBirth
    employees_model.address = data.employees.address
    employees_model.phoneNumber = data.employees.phoneNumber
    employees_model.email = data.employees.email
    employees_model.department = data.employees.department
    employees_model.position = data.employees.position
    employees_model.hireDate = data.employees.hireDate
    employees_model.salary = data.employees.salary

    db.commit()

    student_dbs_model = db.query(model.StudentDBS).filter(model.StudentDBS.id == record_id).first()
    if student_dbs_model is None:
        raise HTTPException(status_code=404, detail="StudentDBS not found")

    student_dbs_model.studentID = data.student_dbs.studentID
    student_dbs_model.firstName = data.student_dbs.firstName
    student_dbs_model.lastName = data.student_dbs.lastName
    student_dbs_model.dateOfBirth = data.student_dbs.dateOfBirth
    student_dbs_model.gender = data.student_dbs.gender
    student_dbs_model.address = data.student_dbs.address
    student_dbs_model.phoneNumber = data.student_dbs.phoneNumber
    student_dbs_model.email = data.student_dbs.email
    student_dbs_model.dbsStatus = data.student_dbs.dbsStatus
    student_dbs_model.dbsExpiryDate = data.student_dbs.dbsExpiryDate

    db.commit()

    employee_dbs_model = db.query(model.EmployeeDBS).filter(model.EmployeeDBS.id == record_id).first()
    if employee_dbs_model is None:
        raise HTTPException(status_code=404, detail="EmployeeDBS not found")

    employee_dbs_model.employeeID = data.employee_dbs.employeeID
    employee_dbs_model.firstName = data.employee_dbs.firstName
    employee_dbs_model.lastName = data.employee_dbs.lastName
    employee_dbs_model.dateOfBirth = data.employee_dbs.dateOfBirth
    employee_dbs_model.gender = data.employee_dbs.gender
    employee_dbs_model.address = data.employee_dbs.address
    employee_dbs_model.phoneNumber = data.employee_dbs.phoneNumber
    employee_dbs_model.email = data.employee_dbs.email
    employee_dbs_model.position = data.employee_dbs.position
    employee_dbs_model.dbsStatus = data.employee_dbs.dbsStatus
    employee_dbs_model.dbsExpiryDate = data.employee_dbs.dbsExpiryDate

    db.commit()

    empBank_details_model = db.query(model.EmployeeBankDetails).filter(
        model.EmployeeBankDetails.id == record_id).first()
    if empBank_details_model is None:
        raise HTTPException(status_code=404, detail="EmpBankDetails not found")

    empBank_details_model.employeeID = data.empBank_details.employeeID
    empBank_details_model.bankName = data.empBank_details.bankName
    empBank_details_model.accountHolderName = data.empBank_details.accountHolderName
    empBank_details_model.AccountNumber = data.empBank_details.AccountNumber
    empBank_details_model.SortCode = data.empBank_details.SortCode
    empBank_details_model.IBAN = data.empBank_details.IBAN
    empBank_details_model.BIC_SwiftCode = data.empBank_details.BIC_SwiftCode

    db.commit()

    student_credit_model = db.query(model.StudentCredit).filter(model.StudentCredit.id == record_id).first()
    if student_credit_model is None:
        raise HTTPException(status_code=404, detail="StudentCredit not found")

    student_credit_model.studentID = data.student_credit.studentID
    student_credit_model.bankAccountNumber = data.student_credit.bankAccountNumber
    student_credit_model.currentCredits = data.student_credit.currentCredits

    db.commit()



# Route to delete entries from multiple tables
@app.delete("/delete_entries/{record_id}")
async def delete_entries(record_id: int, db: Session = Depends(get_db)):
    # Keep track of found models to delete
    models_to_delete = []

    # Check and add StudentCredit model
    student_credit_model = db.query(model.StudentCredit).filter(model.StudentCredit.id == record_id).first()
    if student_credit_model:
        models_to_delete.append(model.StudentCredit)

    # Check and add HomeStudent model
    home_student_model = db.query(model.HomeStudent).filter(model.HomeStudent.id == record_id).first()
    if home_student_model:
        models_to_delete.append(model.HomeStudent)

    international_student_model = db.query(model.InternationalStudent).filter(
        model.InternationalStudent.id == record_id).first()
    if international_student_model:
        models_to_delete.append(model.InternationalStudent)

    student_dbs_model = db.query(model.StudentDBS).filter(model.StudentDBS.id == record_id).first()
    if student_dbs_model:
        models_to_delete.append(model.StudentDBS)

    employees_model = db.query(model.Employees).filter(model.Employees.id == record_id).first()
    if employees_model:
        models_to_delete.append(model.Employees)

    empbank_details_model = db.query(model.EmployeeBankDetails).filter(
        model.EmployeeBankDetails.id == record_id).first()
    if empbank_details_model:
        models_to_delete.append(model.EmployeeBankDetails)

    employee_dbs_model = db.query(model.EmployeeDBS).filter(model.EmployeeDBS.id == record_id).first()
    if employee_dbs_model:
        models_to_delete.append(model.EmployeeDBS)

    # Perform all delete operations
    for model_type in models_to_delete:
        db.query(model_type).filter(model_type.id == record_id).delete()

    # Commit changes after all delete operations
    db.commit()

    # Raise 404 only if none of the models were found
    if not models_to_delete:
        raise HTTPException(status_code=404, detail="No matching records found")

    return {
        'status': 201,
        'transaction': 'Successful'
    }


def http_exception():
    return HTTPException(status_code=404, detail="Regentcollege not found")
