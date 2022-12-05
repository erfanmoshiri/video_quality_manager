import os
from pathlib import Path

import ffmpeg
from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist
from django.core.files import File
from django.utils.datetime_safe import datetime
from pytz import UTC


@shared_task()
def convert_video(obj_id):
    print('function began')
    from media.models import Video

    try:
        video = Video.objects.get(id=obj_id)
    except ObjectDoesNotExist:
        return

    video_type = video.main_video.name.split('/')[-1].split('.')[-1]
    output_file = set_output_path(video_type)

    start_time = datetime.now(tz=UTC)
    convert_low(video, output_file)
    convert_medium(video, output_file)
    end_time = datetime.now(tz=UTC)
    duration = end_time - start_time
    video.convert_time = duration.seconds
    video.save(convert=False)
    print('function finished')


def convert_ffmpeg(in_path, out_path, fps):
    stream = ffmpeg.input(in_path)
    stream = stream.filter('fps', fps=fps, round='up')
    stream = ffmpeg.output(stream, out_path)
    ffmpeg.run(stream)


def convert_medium(video, output_file):
    convert_ffmpeg(video.main_video.path, output_file, 15)

    with open(output_file, 'rb') as f:
        video.medium_quality_video.save('low.mp4', File(f))

    os.remove(output_file)


def convert_low(video, output_file):
    convert_ffmpeg(video.main_video.path, output_file, 10)

    with open(output_file, 'rb') as f:
        video.low_quality_video.save('medium.mp4', File(f))

    os.remove(output_file)


def set_output_path(video_type):
    path = os.getcwd()
    print('path:', path)
    path = os.path.join(path, 'files/videos/converted_temp/')
    Path(path).mkdir(parents=True, exist_ok=True)
    output_file = path + 'temp.' + video_type
    return output_file
