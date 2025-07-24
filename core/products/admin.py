from django.contrib import admin
from .models import ProductStone, Order, OrderItem

@admin.register(ProductStone)
class ProductStoneAdmin(admin.ModelAdmin):
    list_display = ('name', 'scientific_name', 'stone_type', 'price_per_kg', 'available_quantity', 'created_at')
    list_filter = ('stone_type',)
    search_fields = ('name', 'scientific_name', 'colors')
    readonly_fields = ('created_at', 'updated_at')


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('price_per_unit', 'total_price_display')
    # can_delete = True  # حذف این خط یا True بذار

    def total_price_display(self, obj):
        if obj.price_per_unit and obj.quantity:
            return obj.price_per_unit * obj.quantity
        return "-"
    total_price_display.short_description = 'قیمت کل آیتم'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'total_price', 'created_at', 'payment_date')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'user__email', 'id')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [OrderItemInline]

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('total_price',)
        return self.readonly_fields


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price_per_unit', 'total_price_display')
    search_fields = ('order__id', 'product__name')
    readonly_fields = ('total_price_display',)

    def total_price_display(self, obj):
        if obj.price_per_unit and obj.quantity:
            return obj.price_per_unit * obj.quantity
        return "-"
    total_price_display.short_description = 'قیمت کل آیتم'
