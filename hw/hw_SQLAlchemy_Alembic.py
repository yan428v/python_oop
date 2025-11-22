from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
import csv
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from auth import auth_router, verify_token

engine = create_engine('sqlite:///students.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)


class StudentCreate(BaseModel):
    surname: str
    name: str
    faculty: str
    course: str
    grade: int

class StudentUpdate(BaseModel):
    surname: Optional[str] = None
    name: Optional[str] = None
    faculty: Optional[str] = None
    course: Optional[str] = None
    grade: Optional[int] = None

class StudentResponse(BaseModel):
    id: int
    surname: str
    name: str
    faculty: str
    course: str
    grade: int

    class Config:
        from_attributes = True



class Student(Base):
    __tablename__ = 'students'

    id = Column(
        Integer,
        primary_key=True
    )
    surname = Column(
        String
    )
    name = Column(
        String
    )
    faculty = Column(
        String
    )
    course = Column(
        String
    )
    grade = Column(
        Integer
    )

Base.metadata.create_all(engine)

class StudentDB:
    def __init__(self):
        self.session = Session()

    def add_student(self, surname, name, faculty, course, grade):
        student = Student(surname=surname, name=name, faculty=faculty,
                          course=course, grade=grade)
        self.session.add(student)
        self.session.commit()
        return student

    def get_all(self):
        return self.session.query(Student).all()

    def load_from_csv(self, filename):
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.add_student(
                    surname=row['Фамилия'],
                    name=row['Имя'],
                    faculty=row['Факультет'],
                    course=row['Курс'],
                    grade=int(row['Оценка'])
                )

    def get_by_faculty(self, faculty):
        return self.session.query(Student).filter(Student.faculty == faculty).all()

    def get_unique_courses(self):
        return [c[0] for c in self.session.query(Student.course).distinct().all()]

    def get_avg_grade_by_faculty(self, faculty):
        return self.session.query(func.avg(Student.grade)) \
            .filter(Student.faculty == faculty).scalar()

    def get_by_course_low_grade(self, course, min_grade=30):
        return self.session.query(Student) \
            .filter(Student.course == course, Student.grade < min_grade).all()

    def get_by_id(self, student_id):
        return self.session.query(Student).filter(Student.id == student_id).first()

    def update_student(self, student_id, surname=None, name=None, faculty=None, course=None, grade=None):
        student = self.get_by_id(student_id)
        if not student:
            return None

        if surname is not None:
            student.surname = surname
        if name is not None:
            student.name = name
        if faculty is not None:
            student.faculty = faculty
        if course is not None:
            student.course = course
        if grade is not None:
            student.grade = grade

        self.session.commit()
        return student

    def delete_student(self, student_id):
        student = self.get_by_id(student_id)
        if not student:
            return False

        self.session.delete(student)
        self.session.commit()

        return True




app = FastAPI(title="Student API", description="API для управления студентами")
app.include_router(auth_router)

def get_db():
    db = StudentDB()
    try:
        yield db
    finally:
        db.session.close()


@app.post("/students/", response_model=StudentResponse, status_code=201)
def create_student(
        student: StudentCreate,
        db: StudentDB = Depends(get_db),
        current_user = Depends(verify_token)
):
    new_student = db.add_student(
        surname=student.surname,
        name=student.name,
        faculty=student.faculty,
        course=student.course,
        grade=student.grade
    )
    return new_student


@app.get("/students/", response_model=List[StudentResponse])
def read_students(
        db: StudentDB = Depends(get_db),
        current_user = Depends(verify_token)
):
    students = db.get_all()
    return students


@app.get("/students/{student_id}", response_model=StudentResponse)
def read_student(
        student_id: int,
        db: StudentDB = Depends(get_db),
        current_user = Depends(verify_token)
):
    student = db.get_by_id(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="студент не найден")
    return student


@app.put("/students/{student_id}", response_model=StudentResponse)
def update_student(
        student_id: int,
        student_update: StudentUpdate,
        db: StudentDB = Depends(get_db),
        current_user = Depends(verify_token)
):
    updated_student = db.update_student(
        student_id=student_id,
        surname=student_update.surname,
        name=student_update.name,
        faculty=student_update.faculty,
        course=student_update.course,
        grade=student_update.grade
    )
    if not updated_student:
        raise HTTPException(status_code=404, detail="студент не найден")
    return updated_student


@app.delete("/students/{student_id}", status_code=204)
def delete_student(
        student_id: int,
        db: StudentDB = Depends(get_db),
        current_user = Depends(verify_token)
):
    success = db.delete_student(student_id)
    if not success:
        raise HTTPException(status_code=404, detail="студент не найден")
    return None