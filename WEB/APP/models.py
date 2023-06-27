from django.db import models

# Create your models here.
class CameraImage(models.Model):
    image = models.ImageField(upload_to='upload') # 이미지 필드 정의, 'upload' 디렉터리에 업로드
    timestamp = models.DateTimeField(auto_now_add=True) # 타임스탬프 필드, 자동으로 생성된 현재 시간 저장

    def save(self, *args, **kwargs):
        if not self.id:
            # 인스턴스가 새로 생성될 때만 순차적인 번호를 부여
            last_instance = CameraImage.objects.order_by('-id').first() # 가장 최근의 인스턴스 (첫 번째로)가져오기
            if last_instance:
                self.id = last_instance.id + 1 # 마지막 인스턴스 ID에 1을 더한 값을 현재 인스턴스 ID로 설정
            else:
                self.id = 0 # 첫 번째 인스턴스의 경우 ID를 0으로 설정

        # 이미지 파일 이름 설정
        filename = f'{self.id}.png'
        self.image.name = filename # 이미지 필드의 이름을 설정한 파일 이름으로 변경

        return super().save(*args, **kwargs) # 부모 클래스의 save() 메서드 호출하여 저장 수행

class Question(models.Model):
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()

    def __str__(self):
        return self.subject

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date= models.DateTimeField()
