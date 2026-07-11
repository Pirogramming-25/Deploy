from django.conf import settings
from django.db import models
from django.urls import reverse


class DevTool(models.Model):
    KIND_CHOICES = [
        ("language", "프로그래밍 언어"),
        ("framework", "프레임워크"),
        ("library", "라이브러리"),
        ("ide", "IDE / 에디터"),
        ("design", "디자인 툴"),
        ("infra", "인프라 / 배포"),
        ("etc", "기타"),
    ]

    name = models.CharField("이름", max_length=100)
    kind = models.CharField("종류", max_length=20, choices=KIND_CHOICES, default="etc")
    content = models.TextField("설명", blank=True)
    created_at = models.DateTimeField("등록일", auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("devtool_detail", args=[self.pk])


class Idea(models.Model):
    title = models.CharField("제목", max_length=200)
    image = models.ImageField("이미지", upload_to="ideas/", blank=True, null=True)
    content = models.TextField("내용", blank=True)
    interest = models.IntegerField("관심도", default=0)
    devtool = models.ForeignKey(
        DevTool,
        verbose_name="개발툴",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ideas",
    )
    created_at = models.DateTimeField("등록일", auto_now_add=True)
    updated_at = models.DateTimeField("수정일", auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("idea_detail", args=[self.pk])

    def is_starred_by(self, user):
        if not user.is_authenticated:
            return False
        return self.stars.filter(user=user).exists()


class IdeaStar(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="stars",
    )
    idea = models.ForeignKey(
        Idea,
        on_delete=models.CASCADE,
        related_name="stars",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "idea")

    def __str__(self):
        return f"{self.user} ★ {self.idea}"