from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import RecipeViewSet,TagViewSet,UploadImage

router = DefaultRouter()
router.register('recipes',RecipeViewSet)
router.register('tags',TagViewSet)

app_name = 'recipe'
urlpatterns = [
    path('',include(router.urls)),
    path('upload-image/<int:pk>/',UploadImage.as_view())
]