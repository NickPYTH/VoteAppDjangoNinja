from ninja import NinjaAPI
from .models import QuestionType, Form, Question, SubAnswer, Answer 
import json
api = NinjaAPI()

@api.post("create_form")
def add(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    try:
        form_name = body['form_name']
        if len(form_name.strip()) < 3:
            return {"error" : "form name must be longer then 2 symbols"}
    except:
        return {"error" : "form name field is missing"}
    try:
        form_password = body['form_description']
    except:
        return {"error" : "form password field is missing"}
    try:
        form_end_date = body['form_date']
    except:
        return {"error" : "form end date field is missing"}
    try:
        questions = body['questions']
    except:
        return {"error" : "form questions field is missing"}
    
    for el in body['questions']:
        question_number = el['questionNumber']
        

    return "Success"