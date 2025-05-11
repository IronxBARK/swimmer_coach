from django.urls import path
from .views import HomePage, DataPage

urlpatterns = [
    path('', HomePage.as_view(), name='main_page'),
    path('data/', DataPage.as_view(), name='data_page'),
]