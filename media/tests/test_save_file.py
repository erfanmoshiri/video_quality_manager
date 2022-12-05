import os

from django.test import TestCase
from media.utils import convert_ffmpeg


class TestVideo(TestCase):

    def setUp(self):
        from media.models import Video

        v = Video.objects.create(
            main_video='/home/erfan/Personal/python/Video-Management-Service/video_management_service/media/videos/1.mp4')
        print(v.main_video.url)

    def test_save_and_convert(self):
        from media.models import Video

        video = Video.objects.last()
        video.save(convert=True)
        if video:
            low_path = video.low_quality_video.path
            medium_path = video.medium_quality_video.path

            self.assertTrue(low_path)
            self.assertTrue(os.path.exists(low_path))
            self.assertTrue(medium_path)
            self.assertTrue(os.path.exists(medium_path))

    def test_ffmpeg(self):
        from media.models import Video

        video = Video.objects.last()
        if video:
            temp_path = 'temp.mp4'
            convert_ffmpeg(video.main_video.path, temp_path, 10)
            self.assertTrue(os.path.exists(temp_path))

    def test_converted_exists(self):
        from media.models import Video

        video = Video.objects.last()

        if video:
            self.assertTrue(video.low_quality_video)
            self.assertTrue(video.medium_quality_video)
