from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from django.conf import settings
from django.conf.urls.static import static


router = DefaultRouter()
router.register('Post', views.IntruderImage)
router.register('intruderimage', views.IntruderImage, basename='intruderimage')
                
urlpatterns = [
    path('api/', include(router.urls)),
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('api_root/', include(router.urls)),
    path('door_status_update/', views.door_status_update, name='door_status_update'),
    path('door_statuses/', views.door_status_list, name='door_status_list'),
    path('door_statuses/<int:pk>/', views.door_status_detail, name='door_status_detail'),
    path('door_statistics/', views.door_statistics, name='door_statistics'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
