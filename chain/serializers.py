from rest_framework.serializers import ModelSerializer, ValidationError, DateTimeField, PrimaryKeyRelatedField
from .models import ElectronicsChain, Product


class ProductSerializer(ModelSerializer):
    """
    Сериализатор для модели Product.
    """

    class Meta:
        model = Product
        fields = '__all__'  # Включаем все поля модели


class ElectronicsChainSerializer(ModelSerializer):
    """
    Сериализатор для модели ElectronicsChain. Обеспечивает работу с продуктами через PrimaryKeyRelatedField
    для обновления связей, а также использует ProductSerializer для отображения полной информации о продуктах.
    """
    # Используем PrimaryKeyRelatedField для обновления связей
    products = PrimaryKeyRelatedField(queryset=Product.objects.all(), many=True)
    created_at = DateTimeField(format="%d-%m-%Y %H:%M:%S", read_only=True)

    class Meta:
        model = ElectronicsChain
        fields = [
            'id',
            'name',
            'node_type',
            'email',
            'country',
            'city',
            'street',
            'house_number',
            'products',
            'supplier',
            'debt',
            'created_at'
        ]

    def validate(self, data):
        """
        Валидация цепочки поставок и продукта:
        - Завод не может иметь поставщика.
        - Розничная сеть и ИП должны иметь поставщика.
        - Продукт не может принадлежать нескольким заводам.
        """
        node_type = data.get('node_type')
        supplier = data.get('supplier')
        products = data.get('products', [])

        # Завод не может иметь поставщика
        if node_type == ElectronicsChain.FACTORY and supplier is not None:
            raise ValidationError("Завод не может иметь поставщика.")

        # Розничная сеть и ИП должны иметь поставщика
        if node_type in [ElectronicsChain.RETAIL, ElectronicsChain.ENTREPRENEUR] and supplier is None:
            raise ValidationError(f"{node_type} должен иметь поставщика.")

        # Продукт не может принадлежать нескольким заводам
        if node_type == ElectronicsChain.FACTORY:
            for product in products:
                other_chains = ElectronicsChain.objects.filter(products=product).exclude(id=self.instance.id if self.instance else None)
                if other_chains.exists():
                    raise ValidationError(f"Продукт '{product.name}' уже принадлежит другому заводу.")

        return data

    def move_product(self, from_chain, to_chain, product):
        """
        Перемещает продукт от одного звена к другому.
        """
        if product in from_chain.products.all():
            from_chain.products.remove(product)
            to_chain.products.add(product)
        else:
            raise ValidationError(f"Продукт с ID {product.id} отсутствует у поставщика.")

    def update(self, instance, validated_data):
        """
        Обновление цепочки и перемещение продуктов.
        """
        if 'debt' in validated_data:
            raise ValidationError({"debt": "Поле 'Задолженность перед поставщиком' не может быть изменено."})

        if 'products' in validated_data:
            new_products = validated_data.pop('products')

            if instance.node_type == ElectronicsChain.FACTORY:
                # Если это завод, просто обновляем список продуктов
                instance.products.set(new_products)
            elif instance.supplier:
                # Если это не завод, проверяем наличие поставщика и перемещаем продукты
                for product in new_products:
                    self.move_product(instance.supplier, instance, product)
            else:
                raise ValidationError("Поставщик должен быть указан для перемещения продуктов.")

        return super().update(instance, validated_data)


