from django.urls import path
from .views import StoneListCreateView, StoneCommentListCreateView, StoneFAQListCreateView, StoneFAQAnswerView

app_name = "general"

urlpatterns = [
    path('stones/', StoneListCreateView.as_view(), name='stone-list-create'), # لیست و ایجاد سنگ‌ها
    path('stones/<int:stone_id>/comments/', StoneCommentListCreateView.as_view(), name='stone-comments'), # لیست و ایجاد نظرات سنگ‌ها
    path('stones/<int:stone_id>/faqs/', StoneFAQListCreateView.as_view(), name='stone-faqs'), # لیست و ایجاد سوالات متداول سنگ‌ها
    path('faqs/<int:pk>/answer/', StoneFAQAnswerView.as_view(), name='answer-faq'), # پاسخ به سوالات متداول سنگ‌ها

]
    