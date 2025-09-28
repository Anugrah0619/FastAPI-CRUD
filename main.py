from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel
app = FastAPI() 

#for POST we create class of BaseModel using pydantic
class Student(BaseModel):
    name:str
    PRN:str
    class_name :str
    CGPA : float

class UpdateStudent(BaseModel):
    name:Optional[str]=None
    PRN:Optional[str]=None
    class_name:Optional[str]=None
    CGPA:Optional[float]=None


students = {
    1:{
        "name":"Anugrah Kulkarni",
        "PRN" : "22UF17555CM154",
        "class_name" : "BTECH9",
        "CGPA" : 8.5
    },
    2:{
        "name":"Kartik Limbachiya",
        "PRN" : "22UF16994CM155",
        "class_name":"BTECH9",
        "CGPA":7.5
    },
    3:{
        "name":"Ashaaf Khan",
        "PRN" : "22UF11111CM152",
        "class_name":"BTECH3",
        "CGPA":9.0
    }
}

#homepage 
@app.get("/")
def homepage():
    return {"message":"Welcome to student dashboard"}

#all student details - as query parameter is implemented below it is integrated into one.
#@app.get("/students")
#def allStudents():
#    return students

#particular student (path parameter)
@app.get("/students/{student_id}")
def particularStudent(student_id : int = Path(..., description="Enter student_id for particular student details - ",le=len(students),gt = 0)):
    if student_id in students:
        return students[student_id]
    else:
        return {"message":f"Student with {student_id} doesn't exist."}


#Search by name(query parameter)
@app.get("/students")
def byName(name:Optional[str]=None):
    if name:
        for id in students:
            if students[id]["name"] == name:
                return {"id":id,"data":students[id]}
        return {"message":"name not found"}
    else:
        return students



    
@app.post("/students/{student_id}")
def createStudent(student_id:int, stu:Student):
    if student_id in students:
        return {"message":"Student already exists."}
    else:
        students[student_id] = stu
        return {"message":f"student with id {student_id} added successfully."}


@app.put("/students/{student_id}")
def updateStudent(student_id:int,stu1:UpdateStudent):
    if student_id not in students:
        return{"message":f"student with id {student_id} doesnot exists."}
    else:
        if stu1.name != None:
            students[student_id]["name"] = stu1.name
        if stu1.PRN != None:
            stu1[student_id]["PRN"] = stu1.PRN
        if stu1.class_name != None:
            students[student_id]["class_name"] = stu1.class_name
        if stu1.CGPA != None:
            students[student_id]["CGPA"] = stu1.CGPA
        
        
        return {"message":f"Student with id {student_id} updated successfully.","updated":students[student_id]}
    


@app.delete("/students/{student_id}")
def deleteStudent(student_id:int):
    if student_id not in students:
        return {"message":f"Student with id {student_id} doesnt exist."}
    else:
        del students[student_id]
        return {"message":f"Student with id {student_id} deleted successfully."}