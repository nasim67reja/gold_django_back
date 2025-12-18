from django.urls import path
from .views import PriceListAPIView, PriceDetailAPIView,PriceCSVUploadAPIView

urlpatterns = [
    path('prices/', PriceListAPIView.as_view(), name='price-list'),
    path('prices/<int:pk>/', PriceDetailAPIView.as_view(), name='price-detail'),
    path("prices/upload-csv/", PriceCSVUploadAPIView.as_view(), name="price-upload-csv"),
]
