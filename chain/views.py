from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from .models import ElectronicsChain, Product
from .serializers import ElectronicsChainSerializer, ProductSerializer


class ElectronicsChainViewSet(ModelViewSet):
    """
    ViewSet для модели ElectronicsChain. Обеспечивает CRUD операции и фильтрацию по стране.
    """
    queryset = ElectronicsChain.objects.all()
    serializer_class = ElectronicsChainSerializer

    # Добавляем фильтрацию по полю 'country'
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['country']  # Позволяет фильтровать по стране
    search_fields = ['country']  # Альтернативно, можно использовать поиск


class ProductViewSet(ModelViewSet):
    """
    ViewSet для модели Product. Обеспечивает CRUD операции.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name', 'model']  # Позволяет фильтровать объекты по имени и модели
