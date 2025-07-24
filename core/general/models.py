from django.db import models

class Stone(models.Model):
    STONE_TYPE_CHOICES = [
        ('igneous', 'آذرین'),
        ('sedimentary', 'رسوبی'),
        ('metamorphic', 'دگرگونی'),
    ]

    name = models.CharField(max_length=100, verbose_name='نام سنگ')
    stone_type = models.CharField(max_length=50, choices=STONE_TYPE_CHOICES, verbose_name='نوع سنگ')
    description = models.TextField(blank=True, verbose_name='توضیح کوتاه')
    main_color = models.CharField(max_length=50, blank=True, verbose_name='رنگ اصلی')
    image = models.ImageField(upload_to='stones/', blank=True, null=True, verbose_name='تصویر')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'stone'
        verbose_name_plural = 'stones'

class StoneComment(models.Model):
    '''
    نظرات          
    '''
    stone = models.ForeignKey(Stone, on_delete=models.CASCADE, related_name='comments')
    author_name = models.CharField(max_length=100, verbose_name='نام نویسنده')
    text = models.TextField(verbose_name='متن نظر')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')

    def __str__(self):
        return f'نظر توسط {self.author_name} برای {self.stone.name}'

class StoneFAQ(models.Model):
    '''
    سوالات متداول           
    '''
    stone = models.ForeignKey(Stone, on_delete=models.CASCADE, related_name='faqs')
    question = models.CharField(max_length=255, verbose_name='سوال')
    answer = models.TextField(verbose_name='پاسخ')

    def __str__(self):
        return f'سوال: {self.question} درباره {self.stone.name}'
