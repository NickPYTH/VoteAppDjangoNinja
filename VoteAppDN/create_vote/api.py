from ninja import NinjaAPI
from .models import Form, Question, Answer 
import json
import random
api = NinjaAPI()

@api.post("get_form")
def add(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    form_key = body['form_key']
    return form_key


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

    link_to_vote = random.randint(100, 10000000000)

    if form_end_date != "inf":
        form = Form(uniq_key=link_to_vote, form_name=form_name, form_password=form_password, form_end_date=form_end_date, form_link=link_to_vote)
    else:
        form = Form(form_name=form_name, form_password=form_password, form_link=link_to_vote)
    form.save()
    try:
        for el in questions:
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
                for ell in question_data:
                    answer = Answer(uniq_key=key, question=question, answer=ell)
                    answer.save()
            elif question_type == 'group':
                if len(el["data"]) != 0:
                    for ell in el["data"]:
                        answer = Answer(uniq_key=key, question=question, answer=ell["value"], group=ell["group_name"])
                        answer.save()
            
    except:
        return "some error"

    return {
        "link": link_to_vote,
    }