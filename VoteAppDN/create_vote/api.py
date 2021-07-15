from ninja import NinjaAPI
from .models import QuestionType, Form, Question, SubAnswer, Answer 
import json
import random
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

    if form_end_date != "inf":
        form = Form(form_name=form_name, form_password=form_password, form_end_date=form_end_date)
    else:
        form = Form(form_name=form_name, form_password=form_password)
    form.save()
    
    for el in body['questions']:
        question_number = el['questionNumber']
        question_title = el['question_title']
        question_description = el['question_description']
        question_comment = el['isComment']
        question_type = el['title']
        question_id = el['id']
        question_data = el['data']

        key = random.randint(0, 1000000)
        question = Question(uniq_key=key, question_type=question_type, form=form, question_name=question_title, question_description=question_description,
                            question_comment=question_comment)
        question.save()
        if question_type == 'numbers':
            pass
        elif question_type == 'custom':
            for el in question_data:
                sub_ans = SubAnswer(uniq_key=key, value=el, question=question)
                sub_ans.save()
        elif question_type == 'group':
            pass

    return "Success"