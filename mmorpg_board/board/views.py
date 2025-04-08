from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
    View,
)

from board.forms import AdvertisementForm, ResponseForm
from board.models import Advertisement, Response
from mmorpg_board.settings import DEFAULT_FROM_EMAIL


class AdvertisementListView(ListView):
    model = Advertisement
    template_name = "board/advertisement_list.html"
    context_object_name = "advertisements"
    paginate_by = 10

    def get_queryset(self):
        return Advertisement.objects.order_by("-created_at")


class AdvertisementDetailView(DetailView):
    model = Advertisement
    template_name = "board/advertisement_detail.html"
    context_object_name = "advertisement"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["response_form"] = ResponseForm()
        return context


class AdvertisementCreateView(LoginRequiredMixin, CreateView):
    model = Advertisement
    form_class = AdvertisementForm
    template_name = "board/advertisement_form.html"
    success_url = reverse_lazy("advertisement_list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class AdvertisementUpdateView(LoginRequiredMixin, UpdateView):
    model = Advertisement
    form_class = AdvertisementForm
    template_name = "board/advertisement_form.html"

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            return redirect("advertisement_detail", pk=obj.pk)
        return super().dispatch(request, *args, **kwargs)


class ResponseCreateView(LoginRequiredMixin, CreateView):
    model = Response
    form_class = ResponseForm

    def form_valid(self, form):
        advertisement = get_object_or_404(Advertisement, pk=self.kwargs["pk"])
        form.instance.author = self.request.user
        form.instance.advertisement = advertisement

        send_mail(
            "Новый отклик на ваше объявление",
            f'Пользователь {self.request.user.username} оставил отклик: "{form.instance.text}"',
            DEFAULT_FROM_EMAIL,
            [advertisement.author.email],
            fail_silently=False,
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("advertisement_list")


class ResponsesListView(LoginRequiredMixin, ListView):
    model = Response
    template_name = "board/responses_list.html"
    context_object_name = "responses"

    def get_queryset(self):
        return Response.objects.filter(
            advertisement__author=self.request.user
        ).order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["advertisements"] = Advertisement.objects.filter(
            author=self.request.user
        )
        ad_id = self.request.GET.get("advertisement")
        if ad_id:
            context["selected_ad"] = get_object_or_404(
                Advertisement, id=ad_id, author=self.request.user
            )
        return context

    def get(self, request, *args, **kwargs):
        ad_id = request.GET.get("advertisement")
        if ad_id:
            self.queryset = Response.objects.filter(
                advertisement__author=self.request.user, advertisement__id=ad_id
            ).order_by("-created_at")
        return super().get(request, *args, **kwargs)


class ResponseAcceptView(LoginRequiredMixin, View):
    def post(self, request, pk):
        response = get_object_or_404(
            Response, pk=pk, advertisement__author=request.user
        )
        response.status = "accepted"
        response.save()

        send_mail(
            "Ваш отклик принят",
            f'Ваш отклик на объявление "{response.advertisement.title}" был принят автором.',
            DEFAULT_FROM_EMAIL,
            [response.author.email],
            fail_silently=False,
        )
        return HttpResponseRedirect(reverse_lazy("responses_list"))


class ResponseRejectView(LoginRequiredMixin, View):
    def post(self, request, pk):
        response = get_object_or_404(
            Response, pk=pk, advertisement__author=request.user
        )
        response.status = "rejected"
        response.save()
        return HttpResponseRedirect(reverse_lazy("responses_list"))


class ResponseDeleteView(LoginRequiredMixin, DeleteView):
    model = Response
    success_url = reverse_lazy("responses_list")

    def get_queryset(self):
        return Response.objects.filter(advertisement__author=self.request.user)
