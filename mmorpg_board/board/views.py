from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from board.forms import AdvertisementForm, ResponseForm
from board.models import Advertisement, Response


# Список всех объявлений
class AdvertisementListView(ListView):
    model = Advertisement
    template_name = "board/advertisement_list.html"
    context_object_name = "advertisements"
    paginate_by = 10

    def get_queryset(self):
        return Advertisement.objects.order_by("-created_at")


# Детальное view объявления
class AdvertisementDetailView(DetailView):
    model = Advertisement
    template_name = "board/advertisement_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["response_form"] = ResponseForm()
        return context


# Создание объявления (только для авторизованных)
class AdvertisementCreateView(LoginRequiredMixin, CreateView):
    model = Advertisement
    form_class = AdvertisementForm
    template_name = "board/advertisement_form.html"
    success_url = reverse_lazy("advertisement_list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


# Редактирование объявления (только для автора)
class AdvertisementUpdateView(LoginRequiredMixin, UpdateView):
    model = Advertisement
    form_class = AdvertisementForm
    template_name = "board/advertisement_form.html"

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            return redirect("advertisement_detail", pk=obj.pk)
        return super().dispatch(request, *args, **kwargs)


# Создание отклика
class ResponseCreateView(LoginRequiredMixin, CreateView):
    model = Response
    form_class = ResponseForm
    template_name = "board/response_form.html"

    def form_valid(self, form):
        advertisement = get_object_or_404(Advertisement, pk=self.kwargs["pk"])
        form.instance.author = self.request.user
        form.instance.advertisement = advertisement
        # Отправка email-уведомления автору объявления
        send_mail(
            "Новый отклик на ваше объявление",
            f'Пользователь {self.request.user.username} оставил отклик: "{form.instance.text}"',
            "from@example.com",
            [advertisement.author.email],
            fail_silently=False,
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("advertisement_detail", kwargs={"pk": self.kwargs["pk"]})
