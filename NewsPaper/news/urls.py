from django.urls import path
# Импортируем созданное нами представление
from .views import PostsList, PostDetail, PostCreate, PostUpdate, PostDelete, PostSearch


urlpatterns = [

   path('', PostsList.as_view(), name='post_list'),
   path('<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('create/', PostCreate.as_view(), name='post_create'),
   path('<int:pk>/edit/', PostUpdate.as_view(), name='post_update'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('search', PostSearch.as_view(), name='search_list'),
]