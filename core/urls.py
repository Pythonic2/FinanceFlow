from django.urls import path
from .views import Index
from django.contrib.auth import views as auth_views
from .views import CustomLoginView, SignUpView


urlpatterns = [
    path("", Index.as_view(template_name="index.html"), name='index'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),

]