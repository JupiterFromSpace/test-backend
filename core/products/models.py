from django.db import models
from django.conf import settings

class ProductStone(models.Model):
    """
    مدل مربوط به محصول سنگ که ویژگی‌های دقیق سنگ را شامل می‌شود.
    این مدل اطلاعاتی مثل نام، نوع سنگ، رنگ‌ها، سختی، چگالی، توضیحات، کاربردها،
    محل استخراج، تصویر، قیمت و مقدار موجودی محصول را نگهداری می‌کند.
    """

    STONE_TYPE_CHOICES = [
        ('igneous', 'آذرین'),
        ('sedimentary', 'رسوبی'),
        ('metamorphic', 'دگرگونی'),
    ]

    name = models.CharField(max_length=150, verbose_name='نام سنگ')
    scientific_name = models.CharField(max_length=150, blank=True, verbose_name='نام علمی')
    stone_type = models.CharField(max_length=50, choices=STONE_TYPE_CHOICES, verbose_name='نوع سنگ')
    colors = models.CharField(max_length=100, blank=True, verbose_name='رنگ‌ها')
    hardness = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True, verbose_name='سختی (مقیاس موس)')
    density = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name='چگالی (g/cm³)')
    description = models.TextField(blank=True, verbose_name='توضیحات')
    applications = models.TextField(blank=True, verbose_name='کاربردها')
    extraction_sites = models.TextField(blank=True, verbose_name='محل‌های استخراج')
    image = models.ImageField(upload_to='product_stones/', blank=True, null=True, verbose_name='تصویر')
    price_per_kg = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='قیمت هر کیلوگرم')
    available_quantity = models.PositiveIntegerField(default=0, verbose_name='مقدار موجود')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='آخرین بروزرسانی')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'محصول سنگ'
        verbose_name_plural = 'محصولات سنگ'


class Order(models.Model):
    """
    مدل سفارش که اطلاعات مربوط به سفارش‌های کاربران را نگهداری می‌کند.
    شامل ارتباط با کاربر، وضعیت سفارش (پرداخت شده، در انتظار پرداخت، پرداخت نشده)،
    قیمت کل سفارش و زمان‌های ایجاد و به‌روزرسانی سفارش است.
    """

    STATUS_CHOICES = [
        ('paid', 'پرداخت شده'),
        ('pending', 'در انتظار پرداخت'),
        ('failed', 'پرداخت نشده'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='کاربر')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ سفارش')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='آخرین بروزرسانی')
    total_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='قیمت کل', default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name='وضعیت سفارش')
    payment_date = models.DateTimeField(blank=True, null=True, verbose_name='تاریخ پرداخت')

    def __str__(self):
        return f'سفارش #{self.id} توسط {self.user} - وضعیت: {self.get_status_display()}'

    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارش‌ها'


class OrderItem(models.Model):
    """
    مدل آیتم‌های هر سفارش، که هر آیتم شامل محصول، تعداد سفارش داده شده و قیمت واحد است.
    این مدل به سفارش مربوط است و لیست آیتم‌های هر سفارش را تشکیل می‌دهد.
    """

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='سفارش')
    product = models.ForeignKey(ProductStone, on_delete=models.PROTECT, verbose_name='محصول')
    quantity = models.PositiveIntegerField(verbose_name='تعداد')
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='قیمت واحد')

    def __str__(self):
        return f'{self.quantity} x {self.product.name}'

    def get_total_price(self):
        return self.quantity * self.price_per_unit

    class Meta:
        verbose_name = 'آیتم سفارش'
        verbose_name_plural = 'آیتم‌های سفارش'
