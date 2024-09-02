from django.db import models
from django.conf import settings

NULLABLE = {'blank': True, 'null': True}


class Product(models.Model):
    """
    Модель, представляющая продукт, который производится и продается в торговой сети.
    """

    # Название продукта
    name = models.CharField(max_length=255, verbose_name="Название продукта")

    # Модель продукта
    model = models.CharField(max_length=100, verbose_name="Модель продукта")

    # Дата выхода продукта на рынок
    release_date = models.DateField(**NULLABLE, verbose_name="Дата выхода на рынок")

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):
        return f"{self.name} ({self.model})"


class ElectronicsChain(models.Model):
    """
    Модель, представляющая звено в торговой сети по продаже электроники.
    Включает в себя заводы, розничные сети и индивидуальных предпринимателей.
    """

    FACTORY = 'factory'
    RETAIL = 'retail'
    ENTREPRENEUR = 'entrepreneur'
    NODE_TYPE_CHOICES = [
        (FACTORY, 'Завод'),
        (RETAIL, 'Розничная сеть'),
        (ENTREPRENEUR, 'Индивидуальный предприниматель'),
    ]

    # Название звена торговой сети
    name = models.CharField(max_length=255, verbose_name="Название звена")

    # Тип звена в торговой сети (завод, розничная сеть, индивидуальный предприниматель)
    node_type = models.CharField(max_length=20, choices=NODE_TYPE_CHOICES, verbose_name="Тип звена")

    # Ссылка на поставщика, который находится выше в иерархии
    supplier = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='clients', **NULLABLE,
                                 verbose_name="Поставщик")

    # Контактный email для связи с представителями звена
    email = models.EmailField(**NULLABLE, verbose_name="Email для связи")

    # Страна, в которой находится звено сети
    country = models.CharField(max_length=100, verbose_name="Страна расположения")

    # Город, в котором находится звено сети
    city = models.CharField(max_length=100, **NULLABLE, verbose_name="Город расположения")

    # Улица, на которой находится звено сети
    street = models.CharField(max_length=100, **NULLABLE, verbose_name="Улица расположения")

    # Номер дома, где расположено звено сети
    house_number = models.CharField(max_length=20, **NULLABLE, verbose_name="Номер дома")

    # Продукты, которые связаны с этим звеном сети
    products = models.ManyToManyField(Product, related_name='electronics_chains', verbose_name="Продукты", blank=True)

    # Задолженность перед поставщиком в денежном выражении с точностью до копеек
    debt = models.DecimalField(max_digits=10, decimal_places=2, **NULLABLE,
                               verbose_name="Задолженность перед поставщиком")

    # Дата и время создания записи в базе данных
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время создания")

    class Meta:
        verbose_name = "Звено сети электроники"
        verbose_name_plural = "Звенья сети электроники"

    def __str__(self):
        return f"{self.name} ({self.get_node_type_display()})"