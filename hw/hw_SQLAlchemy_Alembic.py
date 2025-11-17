from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
import csv

engine = create_engine('sqlite:///students.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)

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
        return self.session.query(func.avg(Student.grade))\
            .filter(Student.faculty == faculty).scalar()

    def get_by_course_low_grade(self, course, min_grade=30):
        return self.session.query(Student)\
            .filter(Student.course == course, Student.grade < min_grade).all()