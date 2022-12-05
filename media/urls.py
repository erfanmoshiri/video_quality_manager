from django.urls import path

from media.views import TestSendTask

urlpatterns = [
    path('', TestSendTask.as_view()),

]
