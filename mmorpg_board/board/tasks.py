from datetime import timedelta

from celery import shared_task
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils import timezone

from board.models import Advertisement


@shared_task
def send_weekly_newsletter():
    one_week_ago = timezone.now() - timedelta(days=7)
    new_ads = Advertisement.objects.filter(created_at__gte=one_week_ago)

    if not new_ads:
        print("Нет новых объявлений за последнюю неделю.")
        return

    subject = "Еженедельная рассылка: Новые объявления на MMORPG Board"
    message = "Вот новые объявления за последнюю неделю:\n\n"
    for ad in new_ads:
        message += f"- {ad.title} (Категория: {ad.get_category_display()})\n"
        message += f"  Автор: {ad.author.username}\n"
        message += f"  Создано: {ad.created_at.strftime('%Y-%m-%d %H:%M')}\n\n"

    users = User.objects.filter(email__isnull=False).exclude(email="")
    if not users:
        print("Нет пользователей для рассылки.")
        return

    email_list = [user.email for user in users]

    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            email_list,
            fail_silently=False,
        )
        print("Еженедельная рассылка успешно отправлена.")
    except Exception as e:
        print(f"Ошибка отправки рассылки: {e}")
