from django.urls import path
from .views import *

urlpatterns = [
    # Получение активных опросов
    path('active_poll/', ActivePoll.as_view()),
    # Опросы
    path('create_poll/', CreatePoll.as_view()),
    path('update_poll/<int:poll_id>/', UpdatePoll.as_view()),
    # Вопросы
    path('create_question/', CreateQuestion.as_view()),
    path('update_question/<int:question_id>/', UpdateQuestion.as_view()),
    # Выбор в вопросе
    path('create_option/', CreateOption.as_view()),
    path('update_option/<int:option_id>/', UpdateOption.as_view()),
    # Ответы в опросе
    path('view_submissons/<int:user_id>/', GetSubmission.as_view()),
    path('create_submissons/', CreateSubmission.as_view())
]
