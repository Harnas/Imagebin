from django.urls import path, re_path


from . import views

urlpatterns = [
    path('', views.upload_file, name='upload'),
    re_path(r'view/(?P<filename>.*)$', views.view_file),
    path('clean', views.cleanup),
    path('classify', views.classify),
]