from django.contrib.admin import ModelAdmin, register

from media.models import Video
from media.utils import convert_video


@register(Video)
class VideoAdmin(ModelAdmin):
    exclude = ['is_deleted']
    readonly_fields = ['low_quality_video', 'medium_quality_video', 'convert_time']

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        obj.save(convert=True)

