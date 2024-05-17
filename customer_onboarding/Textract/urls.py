from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.Login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create-customer/', views.create_customer, name='create_customer'),
    path('upload-images/', views.upload_images, name='upload_images'),
    path('success/', views.success, name='success'),
    path('customers/', views.customer_list, name='customer_list'),
    path('customer_documents/<str:filename>/', views.view_customer_document, name='view_customer_document'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
