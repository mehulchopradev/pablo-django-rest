from django.urls import path, include
from libapi import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('books', views.BookModelViewSet, basename='book')

#/api/libmgmt/
urlpatterns = [
    path('', include(router.urls)),
    path('login/', views.LoginView.as_view()),
    path('publication-houses/', views.PublicationHousesList.as_view())
]

'''path('books/', views.BookListView.as_view()),
path('books/<int:pk>/', views.GetBookView.as_view())'''
