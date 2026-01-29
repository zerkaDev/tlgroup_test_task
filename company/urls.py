from django.urls import path
from company.views import index

urlpatterns = [
    path('index/', index, name='index'),
]
