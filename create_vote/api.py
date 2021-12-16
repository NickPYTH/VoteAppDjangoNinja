from django.utils.regex_helper import Group
from ninja import NinjaAPI
from .models import *
import json
import random
import pandas as pd
from minio import Minio

api = NinjaAPI()


@api.post("create_form")
def add(request):
    global form_obj
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    try:
        if len(body["form_name"].strip()) == 0:
            return {'error': 'badFormName'}
    except:
        return {'error': 'doesntNotExistFormName'}
    try:
        if len(body["form_description"].strip()) == 0:
            return {'error': 'badFormDesc'}
    except:
        return {'error': 'doesntNotExistFormDesc'}
    try:
        if len(body["form_password"].strip()) == 0:
            return {'error': 'badFormPassword'}
    except:
        return {'error': 'doesntNotExistFormPass'}
    try:
        if len(body["form_date"]) == 0:
            return {'error': 'badFormDate'}
    except:
        return {'error': 'doesntNotExistFormDate'}
    try:
        if len(body["questions"]) == 0:
            return {'error': 'badFormQuestion'}
    except:
        return {'error': 'doesntNotExistFormQuestions'}
    # try:
    form_enter_code = random.randint(1000, 9999)
    if body['form_date'] == 'inf':
        form_obj = FormTable.objects.create(
            name=body["form_name"],
            password=body['form_password'],
            description=body["form_description"],
            is_inf=True,
            start_date=None,
            end_date=None,
            enter_code=form_enter_code,
        )
    elif 'end' in body['form_date']:  # 2021-11-02
        form_obj = FormTable.objects.create(
            name=body["form_name"],
            password=body['form_password'],
            description=body["form_description"],
            is_inf=False,
            start_date="{0}-{1}-{2}".format(body['form_date']['start']['startYear'],
                                            body['form_date']['start']['startMonth'] + 1,
                                            body['form_date']['start']['startDay'],
                                            ),
            end_date="{0}-{1}-{2}".format(body['form_date']['end']['endYear'],
                                          body['form_date']['end']['endMonth'] + 1,
                                          body['form_date']['end']['endDay'],
                                          ),
            enter_code=form_enter_code,
        )
    else:
        form_obj = FormTable.objects.create(
            name=body["form_name"],
            password=body['form_password'],
            description=body["form_description"],
            is_inf=False,
            start_date="{0}-{1}-{2}".format(body['form_date']['startYear'],
                                            body['form_date']['startMonth'] + 1,
                                            body['form_date']['startDay'],
                                            ),
            end_date=None,
            enter_code=form_enter_code,
        )

    for question in (body["questions"]):
        if question['type'] == 'number':
            question_obj = QuestionTable.objects.create(
                name=question["title"],
                description=question["description"],
                serial_number=question['index'],
                type=TypesTable.objects.get(type=question['type']),
                is_comment=question['withComment'],
                range=question['range']
            )
            question_obj.save()
            form_obj.questions.add(question_obj)
        elif question['type'] == 'custom':
            question_obj = QuestionTable.objects.create(
                name=question["title"],
                description=question["description"],
                serial_number=question['index'],
                type=TypesTable.objects.get(type=question['type']),
                is_comment=question['withComment'],
                range=None,
            )
            for answer in question['answers']:
                question_obj.answers.create(value=answer['value'])
            question_obj.save()
            form_obj.questions.add(question_obj)
        elif question['type'] == 'group':
            question_obj = QuestionTable.objects.create(
                name=question["title"],
                description=question["description"],
                serial_number=question['index'],
                type=TypesTable.objects.get(type=question['type']),
                is_comment=question['withComment'],
                range=None,
            )
            for group in question['answers']:
                groups_obj = GroupsTable.objects.create(name=group['groupName'])
                for answer in group["group"]:
                    groups_obj.answers.create(value=answer['value'])
                groups_obj.save()
                question_obj.groups.add(groups_obj)
            question_obj.save()
            form_obj.questions.add(question_obj)
    # except:
    #    return {'error': 'badCreation'}

    return {
        "code": form_enter_code,
        "error": "no",
    }


@api.post("get_form")
def get(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    data = {}
    try:
        form = FormTable.objects.get(enter_code=body['formKey']['code'])
        data['formName'] = form.name
        data['formDescription'] = form.description
        if form.is_inf:
            data['formStartDate'] = None
            data['formEndDate'] = None
        elif form.end_date is None:
            data['formStartDate'] = form.start_date
            data['formEndDate'] = None
        else:
            data['formStartDate'] = form.start_date
            data['formEndDate'] = form.end_date
        data['formQuestions'] = []
        questions = form.questions.all()
        for question in questions:
            tmp = {}
            if question.type == TypesTable.objects.get(type='number'):
                tmp = {
                    'questionTitle': question.name,
                    'questionDescription': question.description,
                    'answerRange': question.range,
                    'isComment': question.is_comment,
                    'type': 'number',
                }
                data['formQuestions'].append(tmp)
            elif question.type == TypesTable.objects.get(type='custom'):
                ans_list = [answer.value for answer in question.answers.all()]
                tmp = {
                    'questionTitle': question.name,
                    'questionDescription': question.description,
                    'isComment': question.is_comment,
                    'answers': ans_list,
                    'type': 'custom',
                }
                data['formQuestions'].append(tmp)
            elif question.type == TypesTable.objects.get(type='group'):
                data['formQuestions'].append({
                    'questionTitle': question.name,
                    'questionDescription': question.description,
                    'isComment': question.is_comment,
                    'type': 'group',
                    'groups': [{'groupName': group.name, 'answers': [answer.value for answer in group.answers.all()]}
                               for group in question.groups.all()]})
    except:
        return {
            "error": "formDoesntExist",
        }
    return data


@api.post("send_form")
def send(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    try:
        form_name = body['formName']
        questions = body['formQuestions']
        form_model = FormTable.objects.get(name=form_name)
        send_form = SendFormTable.objects.create(form=form_model)
        for question in questions:
            title = question['questionTitle']
            question_model = QuestionTable.objects.get(name=title)
            if 'comment' in question:
                SendFormCommentsTable.objects.create(form=send_form, question=question_model, value=question['comment'])
            group = None
            answer = None
            if question['type'] == 'number':
                answer = question['activeAnswer']
                send_form.answers.add(
                    SendAnswerTable.objects.create(question=QuestionTable.objects.get(name=title), answer=answer))
            elif question['type'] == 'custom':
                answer = question['activeAnswer']
                send_form.answers.add(
                    SendAnswerTable.objects.create(question=QuestionTable.objects.get(name=title), answer=answer))
            elif question['type'] == 'group':
                answer = question['activeAnswer']
                group = question['activeGroup']
                send_form.answers.add(
                    SendAnswerTable.objects.create(question=QuestionTable.objects.get(name=title), answer=answer,
                                                   group=GroupsTable.objects.get(name=group)))
        send_form.save()
        return {'status': 'success'}


    except:
        return {'status': 'error'}


@api.post("get_form_stats")
def get_stats(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    try:
        FormTable.objects.get(enter_code=body['formKey'], password=body['formPassword'])
    except:
        return {'status': 'error'}
    return {'status': 'success'}


@api.post("get_form_stats_excel")
def get_stats_excel(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    try:
        forms = SendFormTable.objects.filter(form=FormTable.objects.get(enter_code=body['formKey']['code']))
    except:
        return {'status': 'error'}
    answers = {answer.question.name: [] for answer in forms[0].answers.all()}
    answers['id'] = []
    answers['Дата'] = []
    answers['Время'] = []
    comments = {
        'id': [],
        'Вопрос': [],
        'Комментарий': [],
    }
    for form in forms:
        id_ = random.randint(1000, 9999)
        answers['id'].append(id_)
        answers['Дата'].append(str(form.data)[:10].replace('-', '.', 2))
        answers['Время'].append(str(form.data)[11:19])
        for ans in form.answers.all():
            if ans.group is None:
                answers[ans.question.name].append(ans.answer)
            else:
                answers[ans.question.name].append(ans.group.name + ":" + ans.answer)
        comments_model = SendFormCommentsTable.objects.filter(form=form)
        if len(comments_model) != 0:
            for comment in comments_model:
                if len(comment.value.strip()) != 0:
                    comments['id'].append(id_)
                    comments['Вопрос'].append(comment.question.name)
                    comments['Комментарий'].append(comment.value)
    comments_df = pd.DataFrame(comments)
    comments_df.set_index('id')
    answers_df = pd.DataFrame(answers)
    answers_df.set_index('id')
    with pd.ExcelWriter('output.xlsx') as writer:
        answers_df.to_excel(writer, sheet_name='Ответы')
        comments_df.to_excel(writer, sheet_name='Комментарии')

    client = Minio("176.57.217.201:9000", "minioadmin", "minioadmin", secure=False)

    file_name = random.randint(7000, 199320323233)
    if client.bucket_exists("voteapp"):
        client.fput_object("voteapp", str(file_name) + ".xlsx", "output.xlsx")

    return {
        "file_link": "http://176.57.217.201:9000/voteapp/" + str(file_name) + ".xlsx",
    }


@api.post("get_stats_data")
def get_stats_data(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    try:
        forms = SendFormTable.objects.filter(form=FormTable.objects.get(enter_code=body['formKey']['code']))
    except:
        return {'status': 'error'}
    answers = {answer.question.name: [] for answer in forms[0].answers.all()}
    for form in forms:
        for ans in form.answers.all():
            if ans.group is None:
                answers[ans.question.name].append(ans.answer)
            else:
                answers[ans.question.name].append(ans.group.name + ":" + ans.answer)
    return {
        "data": answers
    }
