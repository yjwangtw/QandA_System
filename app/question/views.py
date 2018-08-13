from ..models import Expertise
from ..models import QuestionForm
from ..models import AnswerForm
from django.contrib import auth
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponseNotFound
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import filters
from rest_framework.authtoken.models import Token
from .serializer import QuestionSerializer
from .serializer import GetQuestionSerializer
from .serializer import DeleteQuestionSerializer
from .serializer import AnswerSerializer
from .serializer import DeleteAnswerSerializer
from .serializer import GetAnswerSerializer


##--------------------API-------------------##
success_msg = 'Success'
error_msg = 'Error'
httpstatus = status.HTTP_200_OK

def ParseErrorMsg(msg):
    print(msg)
    for k in msg.keys():
        key = k
        break
    return msg[key][0]

@api_view(['POST'])
def PostQuestion(request, format='json'):
    serializer = QuestionSerializer(data=request.data)
    if serializer.is_valid():
        question = serializer.save()
        json = {
                "msg": success_msg, 
                "question_id": question.id
                }
        return Response(json, status=httpstatus)
    json = {
            "msg": error_msg, 
            "errorMsg": ParseErrorMsg(serializer.errors)
            }   
    return Response(json, status=httpstatus)

@api_view(['POST'])
def ModifyQuestion(request, format='json'):
    try: question_id = request.data['question_id']
    except: error_message = 'No question_id or format is wrong'
    else:
        if QuestionForm.objects.filter(id__exact=question_id):
            question_instance = QuestionForm.objects.get(id=question_id)
            serializer = QuestionSerializer(question_instance, data=request.data, partial=True)
            if serializer.is_valid():
                question = serializer.save()
                json = {"msg": success_msg}
                return Response(json, status=httpstatus)
            else: error_message = ParseErrorMsg(serializer.errors)
        else: error_message = 'This question_id does not exist.'
    json = {"msg": error_msg, "errorMsg": error_message}
    return Response(json, status=httpstatus)

@api_view(['POST'])
def DeleteQuestion(request, format='json'):
    serializer = DeleteQuestionSerializer(data=request.data)
    if serializer.is_valid():
        question_id = serializer.data['question_id']
        token = serializer.data['key']
        question = QuestionForm.objects.get(id=question_id)
        if Token.objects.get(key=token).user_id == question.user_id:
            question.delete()
            json = {"msg": success_msg}
            return Response(json, status=httpstatus)
        else: error_message = 'The author of the question does not match the token.'
    else: error_message = ParseErrorMsg(serializer.errors)
    json = {"msg": error_msg, "errorMsg": error_message}
    return Response(json, status=httpstatus)

"""
def GetQuestionByID(id):
    question = QuestionForm.objects.get(id=id)
    exps = []
    for exp in question.expertises.all():
        exps.append(exp.expertise)
    json = {
            "question_id": id,
            "username": question.user.username,
            "title": question.title,
            "content": question.content,
            "create_date": question.create_date,
            "modify_date": question.mod_date,
            "answer_number": question.answer_number,
            "comment_number": question.comment_number,
            "expertises": exps,
            }
    return json

@api_view(['GET'])
def GetQuestion(request, pk):
    if pk == '0':
        quests = []
        for quest in QuestionForm.objects.all():
            quests.append({"question": GetQuestionByID(quest.id)})
        json = {
                "msg": success_msg,
                "questions": quests
                }
        return Response(json, status=httpstatus)
    else:
        if not QuestionForm.objects.filter(id=pk):
            error_message = 'Wrong question id'
        else:
            json =GetQuestionByID(pk)
            return Response(json, status=httpstatus)
        json = {"msg": error_msg, "errorMsg": error_message}
        return Response(json, status=httpstatus)
"""

class GetQuestionList(generics.ListAPIView):
    serializer_class = GetQuestionSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('user_id', 'id')
    def get_queryset(self):
        queryset = QuestionForm.objects.all()
        uid = self.request.query_params.get('uid', None)
        qid = self.request.query_params.get('qid', None)
        if uid is None and qid is None:
            return queryset
        elif uid is not None and qid is not None:
            return queryset.filter(user__exact=uid).filter(id__exact=qid)
        elif uid is not None:
            return queryset.filter(user__exact=uid)
        else:
            return queryset.filter(id__exact=qid)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = GetQuestionSerializer(queryset, many=True)
        usernames = {}
        for quest in serializer.data:
            quest['user_id'] = quest['user']
            quest['user'] = User.objects.get(id=quest['user_id']).username
            exps = []
            for eid in quest['expertises']:
                exps.append(Expertise.objects.get(id=eid).expertise)
            quest['expertises'] = exps
            quest['username'] = quest['user'] 
            del quest['user'] 
            quest['question_id'] = quest['id'] 
            del quest['id'] 
        return Response(serializer.data)

@api_view(['POST'])
def PostAnswer(request, format='json'):
    serializer = AnswerSerializer(data=request.data)
    if serializer.is_valid():
        answer = serializer.save()
        json = {
                "msg": success_msg, 
                "answer_id": answer.id
                }
        return Response(json, status=httpstatus)
    json = {
            "msg": error_msg, 
            "errorMsg": ParseErrorMsg(serializer.errors)
            }   
    return Response(json, status=httpstatus)

@api_view(['POST'])
def ModifyAnswer(request, format='json'):
    try: answer_id = request.data['answer_id']
    except: error_message = 'No answer ID or format is wrong'
    else:
        if AnswerForm.objects.filter(id__exact=answer_id):
            answer_instance = AnswerForm.objects.get(id=answer_id)
            serializer = AnswerSerializer(answer_instance, data=request.data, partial=True)
            if serializer.is_valid():
                answer = serializer.save()
                json = {"msg": success_msg}
                return Response(json, status=httpstatus)
            else: error_message = ParseErrorMsg(serializer.errors)
        else: error_message = 'This answer ID does not exist.'
    json = {"msg": error_msg, "errorMsg": error_message}
    return Response(json, status=httpstatus)

@api_view(['POST'])
def DeleteAnswer(request, format='json'):
    serializer = DeleteAnswerSerializer(data=request.data)
    if serializer.is_valid():
        AnswerForm.objects.get(id=serializer.data['answer_id']).delete()
        json = {"msg": success_msg}
        return Response(json, status=httpstatus)
    json = {"msg": error_msg, "errorMsg": ParseErrorMsg(serializer.errors)}
    return Response(json, status=httpstatus)

class GetQuestion(generics.ListAPIView):
    serializer_class = GetQuestionSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('question_id', 'answer_id')
    def get_queryset(self):
        queryset = QuestionForm.objects.all()
        qid = self.request.query_params.get('qid', None)
        if qid is None :
            return QuestionForm.objects.none()
        else:
            return queryset.filter(id__exact=qid)

    def get_queryset_answer(self):
        queryset = AnswerForm.objects.all()
        qid = self.request.query_params.get('qid', None)
        aid = self.request.query_params.get('aid', None)
        if aid is None:
            return queryset.filter(question__exact=qid)
        else:
            return queryset.filter(question__exact=qid, id__exact=aid)

    def list(self, request):
        queryset = self.get_queryset()
        if not queryset:
            return Response(queryset)
        else:
            question_serializer = GetQuestionSerializer(queryset, many=True)
            user = User.objects.get(id=question_serializer.data[0]['user'])
            question_serializer.data[0]['user_id'] = user.id
            question_serializer.data[0]['user'] = user.username
            result = {"question": question_serializer.data}
        queryset = self.get_queryset_answer()
        if queryset:
            answer_serializer = GetAnswerSerializer(queryset, many=True)
            print(answer_serializer.data) 
            for ans in answer_serializer.data:               
                user = User.objects.get(id=ans['user'])
                ans['user_id'] = user.id
                ans['user'] = user.username
            result['answers'] = answer_serializer.data                

        return Response(result)

