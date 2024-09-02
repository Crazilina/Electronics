from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from chain.apps import ChainConfig
from .views import ElectronicsChainViewSet, ProductViewSet

app_name = ChainConfig.name

router = SimpleRouter()
router.register(r'suppliers', ElectronicsChainViewSet)
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + router.urls
