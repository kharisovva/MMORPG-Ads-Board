from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django_ckeditor_5.fields import CKEditor5Field


class Advertisement(models.Model):
    CATEGORIES = [
        ("tanks", "Танки"),
        ("heals", "Хилы"),
        ("dd", "ДД"),
        ("traders", "Торговцы"),
        ("guildmasters", "Гилдмастеры"),
        ("questgivers", "Квестгиверы"),
        ("blacksmiths", "Кузнецы"),
        ("tanners", "Кожевники"),
        ("potions", "Зельевары"),
        ("spellmasters", "Мастера заклинаний"),
    ]

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = CKEditor5Field("Text", config_name="default")
    category = models.CharField(max_length=20, choices=CATEGORIES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("advertisement_detail", kwargs={"pk": self.pk})


class Response(models.Model):
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "На рассмотрении"),
            ("accepted", "Принят"),
            ("rejected", "Отклонён"),
        ],
        default="pending",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Отклик от {self.author.username} на {self.advertisement.title}"
