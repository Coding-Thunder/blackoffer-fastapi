from typing import Optional
from fastapi import FastAPI, Path
from pydantic import BaseModel

app = FastAPI()


class Student(BaseModel):
    name: str
    age: int
    year: str


students = {
    1: {
        "name": "vinay",
        "age": 17,
        "year": "year 12"
    },
}


@app.get("/")
def index():
    return {"status": "Active"}


@app.get("/get-students")
def getStudent():
    return students


@app.get("/get-specific-student/{student_id}")
def getSpecificStudent(student_id: int = Path(None, description="The Student Id", gt=0)):
    return students[student_id]


@app.get("/get-by-name/{student_id}")
def getStudentByName(*, student_id: int, name: Optional[str] = None):
    for student_id in students:
        if students[student_id]["name"] == name:
            return students[student_id]
    return students


@app.post("/create-student/{student_id}")
def create_student(student_id: int, student: Student):
    if student_id in students:
        return {"error": "student already exists"}

    students[student_id] = student
    return students[student_id]

# path parameters abc.com/student/1       [1]
# query parameters abc.com/student?id=1   [?id=1]
