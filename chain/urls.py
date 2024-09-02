from rest_framework.routers import SimpleRouter

from chain.apps import ChainConfig
from .views import ElectronicsChainViewSet, ProductViewSet

app_name = ChainConfig.name

router = SimpleRouter()
router.register(r'suppliers', ElectronicsChainViewSet)
router.register(r'products', ProductViewSet)

urlpatterns = [

] + router.urls
