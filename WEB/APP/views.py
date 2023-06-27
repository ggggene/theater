import os
import json
from django.shortcuts import render, get_object_or_404, redirect
from .models import CameraImage
from django.conf import settings
from django.http import JsonResponse
from django.http import HttpResponse
from .models import Question
from .models import Answer
from django.utils import timezone
from .forms import QuestionForm, AnswerForm
from django.core.paginator import Paginator

def get_movie_genre(emotion, mappings):
    return mappings[str(emotion)] # match.json 감정과 숫자 매핑

def get_movies_by_genre(genre, movie_data):
    matching_movies = [] # 각 장르별 영화 정보 리스트
    for i in range(len(movie_data['장르'])):
        if movie_data['장르'][str(i)] == genre:
            matching_movies.append({
                '영화명': movie_data['영화명'][str(i)],
                '제작연도': movie_data['제작연도'][str(i)],
                '제작국가': movie_data['제작국가'][str(i)],
                '장르': movie_data['장르'][str(i)]
            })
    return matching_movies

def test(request):
    exp_num = 2 # 초기 exp 폴더 번호
    txt_num = 108 # 초기 txt 파일 번호

    if request.method == 'POST':
        image = request.FILES.get('camera-image') # 웹 -> 서버
        camera_image = CameraImage.objects.create(image=image) # 데이터 베이스 저장

        # 이미지 경로
        img_path = os.path.join(settings.MEDIA_ROOT, camera_image.image.name)  # 이미지 파일 경로

        # detect.py 경로
        detect_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'detect.py'))

        # YOLOv5 detect 명령어 실행
        command = f'python ../detect.py --weights ../best.pt --save-txt --source {img_path}'  # YOLOv5 detect 명령어
        os.system(command)

        # 결과 클래스 경로
        txt_file_path = f'../runs/detect/exp{exp_num}/labels/{txt_num}.txt'
        with open(txt_file_path, 'r') as f:
            emotion = int(f.readline().split()[0])

        # 0 = 기쁨, 1 = 당황, 2 = 분노, 3 = 불안, 4 = 상처, 5 = 슬픔, 6 = 중립

        # match.json 로드
        match_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'json', 'match.json'))
        os.chmod(match_file_path, 0o644) # 파일에 읽기 권한 추가
        with open(match_file_path, 'r', encoding='utf-8') as f:
            match = json.load(f)
        genres = get_movie_genre(emotion, match)

        # movie_data.json 로드
        movie_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'json', 'movie_data.json'))
        os.chmod(movie_file_path, 0o644) # 파일에 읽기 권한 추가
        with open(movie_file_path, 'r', encoding='utf-8') as f:
            movie_data = json.load(f)

        movies = [] # 영화 리스트
        for genre in genres:
            matching_movies = get_movies_by_genre(genre, movie_data)
            movies.extend(matching_movies) # 리스트 안에 추가

        response_data = {
            'movies' : movies
        } # 응답 데이터 담기

        return JsonResponse(response_data) # json형식으로 응답

        exp_num += 1 # 넘버링 카운트
        txt_num += 1 # 넘버링 카운트

    else:
        context = {
            'static': CameraImage.objects.all(),
        } # 이미지 변수 담기
    return render(request, 'html/camera_view.html/', context)

def quest(request):
    # 게시판 질문 목록 출력 urls = 'questionlist/'

    #입력 인자
    page = request.GET.get('page', '1') # 페이지

    # 조회
    question_list = Question.objects.order_by('-create_date')

    # 페이징 처리
    paginator = Paginator(question_list, 10) # 페이지당 10개씩 보여 주기
    page_obj = paginator.get_page(page)

    context = {'question_list' : page_obj}
    return render(request, 'questlist/question_list.html' , context)

def detail(request, question_id):
    # 질문에 대한 내용 출력
    question = get_object_or_404(Question, pk=question_id)
    context = {'question' : question}
    return render(request, 'questlist/question_detail.html', context)

def answer_create(request, question_id):
    # 질문에 대한 답변등록
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            # 답변 등록후 상세화면 이동 - redirect 함수
            return redirect('APP:detail', question_id=question.id)
    else:
        form = AnswerForm()
    context = {'question': question, 'form':form}
    return render(request, 'questlist/question_detail.html', context)

    """
    # Answer 모델 데이터 생성 및 저장방법: Question 모델 이용
    question.answer_set.create(content=request.POST.get('content'),
                               create_date=timezone.now())
                               
    # Answer 모델 데이터 생성 및 저장방법: Answer 모델 이용
    answer = Answer(question=question, content=request.POST.get('content'), create_date=timezone.now())
    answer.save()
    """


def question_create(request):
    # 게시판 질문등록
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.create_date = timezone.now()
            question.save()
            return redirect('APP:quest')
    else:
        form = QuestionForm()
    context = {'form' : form}
    return render(request, 'questlist/question_form.html', context)