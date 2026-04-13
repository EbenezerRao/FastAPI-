from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid

app = FastAPI()

gradebook = {}

class StudentGrades(BaseModel):
    stud_name : str
    math_score : int
    science_score : int
    english_score : int

@app.post('/api/v1/grades')
def add_grades(stud_data : StudentGrades):
    stud_id = str(uuid.uuid4())[:6]
    gradebook[stud_id] = {
        'stud_name' : stud_data.stud_name,
        'math_score' : stud_data.math_score,
        'science_score' : stud_data.science_score,
        'english_score' : stud_data.english_score
    }
    return {'message' : 'Grades added for student with id' + stud_id, 'student_id' : stud_id}

@app.get('/api/v1/grades/{stud_id}')
def get_grades(stud_id : str):
    if stud_id not in gradebook:
        raise HTTPException(status_code=404, detail= "Student not found")
    else:
        studentids = gradebook[stud_id]
        avg_score = (studentids['math_score'] + studentids['science_score'] + studentids['english_score']) / 3
        return {
            'student_record' : studentids,
            'average_score' : round(avg_score, 2)
        }