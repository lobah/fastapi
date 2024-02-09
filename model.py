from sqlalchemy import Column, Integer, String, Date, Boolean
from HRdatabase import Base






class StudentDBS(Base):
    __tablename__ = "studentDBS"

    studentID = Column(Integer, primary_key=True, index=True)
    firstName = Column(String)
    lastName = Column(String)
    dateOfBirth = Column(Date)
    gender = Column(String)
    address = Column(String)
    phoneNumber = Column(String)
    email = Column(String)
    dbsStatus = Column(String)
    dbsExpiryDate = Column(Date)


class StudentCredit(Base):
    __tablename__ = "studentCredit"

    studentID = Column(Integer, primary_key=True, index=True)
    bankAccountNumber = Column(String)
    currentCredits = Column(String)


class InternationalStudent(Base):
    __tablename__ = "internationalStudent"

    studentID = Column(Integer, primary_key=True, index=True)
    firstName = Column(String)
    lastName = Column(String)
    dateOfBirth = Column(Date)
    homeAddress = Column(String)
    homeCountry = Column(String)
    phoneNumber = Column(String)
    PassportNumber = Column(Boolean)
    VisaStatus = Column(String)


class HomeStudent(Base):
    __tablename__ = "homeStudent"

    studentID = Column(Integer, primary_key=True, index=True)
    firstName = Column(String)
    lastName = Column(String)
    dateOfBirth = Column(Date)
    homeAddress = Column(String)
    homeCountry = Column(String)
    homePhone = Column(String)


class EmployeeDBS(Base):
    __tablename__ = "employeeDBS"

    employeeID = Column(Integer, primary_key=True, index=True)
    firstName = Column(String)
    lastName = Column(String)
    dateOfBirth = Column(Date)
    gender = Column(String)
    address = Column(String)
    phoneNumber = Column(String)
    email = Column(String)
    position = Column(String)
    dbsStatus = Column(String)
    dbsExpiryDate = Column(Date)

class EmployeeBankDetails(Base):
    __tablename__ = "employeebankdetails"

    employeeID = Column(Integer, primary_key=True, index=True)
    bankName = Column(String)
    accountHolderName = Column(String)
    AccountNumber = Column(String)
    SortCode = Column(String)
    IBAN = Column(String)
    BIC_SwiftCode = Column(String)


class Employees(Base):
    __tablename__ = "employees"

    employeeID = Column(Integer, primary_key=True, index=True)
    firstName = Column(String)
    lastName = Column(String)
    dateOfBirth = Column(Date)
    address = Column(String)
    phoneNumber = Column(String)
    email = Column(String)
    department = Column(String)
    position = Column(String)
    hireDate = Column(String)
    salary = Column(String)


