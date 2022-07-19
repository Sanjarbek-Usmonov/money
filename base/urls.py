from django.urls import path
from rest_framework import routers
from .views import UserRegisterView, CategoryViewset, WalletTransactionView, CategoryOutcomeView

router = routers.SimpleRouter()
router.register(r'category', CategoryViewset)

urlpatterns = [
    path('register', UserRegisterView.as_view(), name='register'),
    path('transactions', WalletTransactionView.as_view()),
    path('category_outcome', CategoryOutcomeView.as_view()),
] + router.urls
