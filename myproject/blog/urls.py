from django.urls import path
from blog import views

urlpatterns = [
    path('',views.post_list, name='post_list'),
    path('<int:id>', views.post_detail, name = 'post_detail'),
    
]
