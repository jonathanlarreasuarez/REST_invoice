from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r'invoice', views.InvoiceViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
