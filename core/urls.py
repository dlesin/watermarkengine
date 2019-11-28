from django.conf import settings
from django.urls import path
from .views import HomeView, LinkView, GetLinkView, AboutView

urlpatterns = [
    path('', HomeView.as_view(), name='home_view_url'),
    path('link/', LinkView.as_view(), name='link_view_url'),
    path('about/', AboutView.as_view(), name='about_view_url'),
    path('getlink/', GetLinkView.as_view(), name='getlink_view_url'),
]
