from django.contrib import admin
from .models import ElectronicsChain, Product


# Регистрируем модель Product в админке
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'model', 'release_date')
    search_fields = ('name', 'model')


# Регистрируем модель ElectronicsChain в админке
@admin.register(ElectronicsChain)
class ElectronicsChainAdmin(admin.ModelAdmin):
    list_display = ('name', 'node_type', 'city', 'supplier', 'debt', 'created_at')
    search_fields = ('name', 'city')
    list_filter = ('city', 'node_type')
    raw_id_fields = ('supplier',)  # Добавляем ссылку на поставщика
    actions = ['clear_debt']  # Добавляем admin action

    # Добавляем action для очищения задолженности
    def clear_debt(self, request, queryset):
        updated = queryset.update(debt=0)
        self.message_user(request, f"Задолженность очищена у {updated} объекта(-ов).")

    clear_debt.short_description = "Очистить задолженность перед поставщиком"
