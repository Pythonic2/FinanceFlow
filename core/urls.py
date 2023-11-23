from django.urls import path
from .views import Index
from django.contrib.auth import views as auth_views
from .views import CustomLoginView, SignUpView,NewCategory, ListCategory,NewFlux,UpdateCategory,DeletCategory

urlpatterns = [
    path("", Index.as_view(template_name="index.html"), name='index'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('new-category/', NewCategory.as_view(), name='new_category'),
    path('new-flux/', NewFlux.as_view(), name='new_flux'),
    path("list/", ListCategory.as_view(), name="category_list"),
    path("update/<int:pk>/", UpdateCategory.as_view(), name='update_category'),
    path("delete/<int:pk>/", DeletCategory.as_view(), name='delete_category'),

]