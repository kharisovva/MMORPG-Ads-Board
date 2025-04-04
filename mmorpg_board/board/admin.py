from django import forms
from django.contrib import admin
from django_ckeditor_5.widgets import CKEditor5Widget

from board.models import Advertisement, Response


class AdvertisementAdminForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = "__all__"
        widgets = {
            "content": CKEditor5Widget(
                config_name="default", attrs={"class": "django_ckeditor_5"}
            )
        }


class AdvertisementAdmin(admin.ModelAdmin):
    form = AdvertisementAdminForm
    list_display = ("title", "author", "category", "created_at")
    list_filter = ("category", "created_at")
    search_fields = ("title", "content")

    # Для корректного отображения CKEditor 5 в админке
    class Media:
        css = {
            "all": (
                "https://cdn.jsdelivr.net/npm/@ckeditor/ckeditor5-adapter-ckfinder@latest/theme/admin_styles.css",
            )
        }


admin.site.register(Advertisement, AdvertisementAdmin)
admin.site.register(Response)
