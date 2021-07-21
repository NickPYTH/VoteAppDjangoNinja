from django.utils.regex_helper import Group
from ninja import NinjaAPI
from .models import Form, Question, Answer, SendedForm, SendedComments
import json
import random
api = NinjaAPI()

@api.post("login_private_stats")
def get_public_results(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    form_name = body['form_name']
    password = body['password']

    try:
        form = Form.objects.get(form_name=form_name, form_password=password)
        return form.uniq_key
    except:
        return "Failed"


@api.post("get_form_private_results")
def get_public_results(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    form_key = body['form_key']

    sended_forms = SendedForm.objects.filter(form_key=form_key)
    questions_short = []
    questions=[]
    for sf in sended_forms:
        if sf.question not in questions_short:
            questions_short.append(sf.question)
            questions.append({"question":sf.question, "answers":[]})
    for question in questions:
        for sf in sended_forms:
            if sf.question == question["question"]:
                question["answers"].append(sf.answer)

    sended_comments = SendedComments.objects.filter(form_key=form_key)
    comments_short = []
    comments=[]
    for sc in sended_comments:
        if sc.question not in comments_short:
            comments_short.append(sc.question)
            comments.append({"question":sc.question, "comments":[]})
    for question in comments:
        for sc in sended_comments:
            if sc.question == question["question"]:
                question["comments"].append(sc.comment)
    
    to_excel = []
    for question in questions:
        for answer in question["answers"]:
           date = SendedForm.objects.filter(form_key=form_key, question=question["question"], answer=answer)[0].date
           group = Answer.objects.filter(
               #question=Question.objects.get (question_name=question["question"]), 
               answer=answer)[0].group
           print(group)

    return {
            "questions": questions, 
            "comments": comments, 
            "just_questions": questions_short, 
            }

@api.post("get_form_public_results")
def get_public_results(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    form_key = body['form_key']

    sended_forms = SendedForm.objects.filter(form_key=form_key)
    questions_short = []
    questions=[]
    for sf in sended_forms:
        if sf.question not in questions_short:
            questions_short.append(sf.question)
            questions.append({"question":sf.question, "answers":[]})
    for question in questions:
        for sf in sended_forms:
            if sf.question == question["question"]:
                question["answers"].append(sf.answer)

    sended_comments = SendedComments.objects.filter(form_key=form_key)
    comments_short = []
    comments=[]
    for sc in sended_comments:
        if sc.question not in comments_short:
            comments_short.append(sc.question)
            comments.append({"question":sc.question, "comments":[]})
    for question in comments:
        for sc in sended_comments:
            if sc.question == question["question"]:
                question["comments"].append(sc.comment)

    return {"questions": questions, "comments": comments, "just_questions": questions_short}

@api.post("send_form")
def send(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    answers = body['answers']
    comments = body['comments']
    form_key = body['form_key']
    for answer in answers:
        SendedForm(form_key=form_key , question=answer, answer=answers[answer]).save()   
    for comment in comments:
        SendedComments(form_key=form_key , question=comment, comment=comments[comment]).save()
    return "Success"

@api.post("get_form")
def add(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    form_key = body['form_key']
    form = Form.objects.filter(uniq_key=form_key).first()
    questions = Question.objects.filter(form=form)
    data = []
    for question in questions:
        question_and_answers = {}
        answers = Answer.objects.filter(question=question)
        answers_list = []
        for answer in answers:
            answers_list.append({
                "question": question.question_name,
                "answer": answer.answer,
                "group": answer.group,
            })
        question_and_answers["form_name"] = form.form_name
        question_and_answers["date"] = str(form.form_end_date)
        question_and_answers["question_name"] = question.question_name
        question_and_answers["question_description"] = question.question_description
        question_and_answers["question_comment"] = question.question_comment
        question_and_answers["question_type"] = question.question_type
        question_and_answers["answers"] = answers_list
        data.append(question_and_answers)

    
    return json.dumps(data)


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
        form = Form(uniq_key=link_to_vote, form_name=form_name, form_password=form_password, form_link=link_to_vote)
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