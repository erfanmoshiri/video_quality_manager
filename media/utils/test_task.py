from time import sleep

from celery import shared_task


@shared_task()
def print_message(msg):
    sleep(5)
    print('your message is : ' + msg)
