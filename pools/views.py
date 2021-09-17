from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import *
from .serializers import *
from django.utils import timezone
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)


class ActivePoll(GenericAPIView):
    queryset = ''
    permission_classes = (IsAuthenticated,)
    serializer_class = PollSerializer

    def get(self, request, format=None):

        polls = Poll.objects.filter(finishDate__gte=timezone.now()).filter(
            startDate__lte=timezone.now())
        serializer = PollSerializer(polls, many=True)
        return Response(serializer.data)


class CreatePoll(GenericAPIView):
    queryset = ''
    permission_classes =(IsAuthenticated, IsAdminUser)
    serializer_class = PollSerializer

    def post(self, request, format=None):
        serializer = PollSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            poll = serializer.save()
            return Response(PollSerializer(poll).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdatePoll(GenericAPIView):
    queryset = ''
    permission_classes =(IsAuthenticated, IsAdminUser)
    serializer_class = PollSerializer

    def post(self, request, poll_id, format=None):
        poll = get_object_or_404(Poll, pk=poll_id)
        serializer = PollSerializer(poll, data=request.data, partial=True)
        if serializer.is_valid():
            poll = serializer.save()
            return Response(f"Опрос обновлён {PollSerializer(poll).data}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, poll_id, format=None):
        poll = get_object_or_404(Poll, pk=poll_id)
        poll.delete()
        return Response("Опрос удалён", status=status.HTTP_204_NO_CONTENT)


class CreateQuestion(GenericAPIView):
    queryset = ''
    permission_classes =(IsAuthenticated, IsAdminUser)
    serializer_class = QuestionSerializer

    def post(self, request, format=None):
        serializer = QuestionSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            question = serializer.save()
            return Response(QuestionSerializer(question).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateQuestion(GenericAPIView):
    queryset = ''
    permission_classes =(IsAuthenticated, IsAdminUser)
    serializer_class = QuestionSerializer

    def post(self, request, question_id, format=None):
        question = get_object_or_404(Question, pk=question_id)
        serializer = QuestionSerializer(
            question, data=request.data, partial=True)
        if serializer.is_valid():
            question = serializer.save()
            return Response(f"Вопрос обновлён {QuestionSerializer(question).data}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, question_id, format=None):
        question = get_object_or_404(Question, pk=question_id)
        question.delete()
        return Response("Вопрос удалён", status=status.HTTP_204_NO_CONTENT)


class CreateOption(GenericAPIView):
    queryset = ''
    permission_classes =(IsAuthenticated, IsAdminUser)
    serializer_class = OptionSerializer

    def post(self, request, format=None):
        serializer = OptionSerializer(data=request.data)
        if serializer.is_valid():
            option = serializer.save()
            return Response(OptionSerializer(option).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateOption(GenericAPIView):
    queryset = ''
    permission_classes =(IsAuthenticated, IsAdminUser)
    serializer_class = OptionSerializer

    def post(self, request, option_id, format=None):
        option = get_object_or_404(Option, pk=option_id)
        serializer = OptionSerializer(option, data=request.data, partial=True)
        if serializer.is_valid():
            option = serializer.save()
            return Response(f"Выбор обновлён {OptionSerializer(option).data}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, option_id, format=None):
        option = get_object_or_404(Option, pk=option_id)
        option.delete()
        return Response("Выбор удалён", status=status.HTTP_204_NO_CONTENT)


class GetSubmission(GenericAPIView):
    queryset = ''
    permission_classes = (IsAuthenticated,)
    serializer_class = SubmissionsSerializer

    def get(self, request, user_id, format=None):
        submission = Submission.objects.filter(userId=user_id)
        serializer = SubmissionsSerializer(submission, many=True)
        return Response(serializer.data)


class CreateSubmission(GenericAPIView):
    queryset = ''
    permission_classes = (IsAuthenticated,)
    serializer_class = SubmissionsSerializer

    def post(self, request, format=None):

        user_id = User.objects.get(username=request.user).id
        request.data._mutable = True
        request.data['userId'] = user_id
        request.data._mutable = False

        serializer = SubmissionsSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            submission = serializer.save()
            return Response(SubmissionsSerializer(submission).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
