from django.db.models import FileField, DateTimeField, PositiveIntegerField

from media.models import BaseModel
from media.utils import convert_video


class Video(BaseModel):
    main_video = FileField(
        verbose_name='کیفیت اصلی',
        upload_to='videos',
    )

    medium_quality_video = FileField(
        null=True,
        blank=True,
        verbose_name='کیفیت متوسط',
        upload_to='videos',
    )

    low_quality_video = FileField(
        null=True,
        blank=True,
        verbose_name='کیفیت پایین',
        upload_to='videos',
    )

    convert_time = PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='زمان تبدیل',
    )

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None, convert=False
    ):
        super().save(force_insert, force_update, using, update_fields)
        if convert:
            self.convert_me()
            print('queued')


    def convert_me(self):
        convert_video.delay(self.id)
