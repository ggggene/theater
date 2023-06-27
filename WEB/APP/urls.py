from django.urls import path
from. import views

# namespace 개념으로 각각의 앱을 구분해줄 앱의 이름을 지정해줌.
app_name = 'APP'

urlpatterns = [
    path('', views.test, name='emotion theater'), # 감정인식 영화추천 메인 페이지
    path('questionlist/', views.quest, name='quest'), # 게시판 질문목록 url 지정
    path('questionlist/<int:question_id>/' , views.detail, name='detail'), # 게시판 질문목록 상세조회 url
    path('questionlist/answer/create/<int:question_id>/', views.answer_create,name='answer_create'), # 게시판 질문에 대한 답변등록 url
    path('questionlist/question/create/', views.question_create, name='question_create'), # 게시판 질문등록 url
]