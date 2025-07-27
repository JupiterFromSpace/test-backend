from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from general.models import Stone, StoneComment, StoneFAQ
from .serializers import StoneSerializer, StoneCommentSerializer, StoneFAQSerializer
from core.utils.responses import success_response, error_response, internal_server_error_response


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 10   


class StoneListCreateView(APIView):
    '''
    API view to list all Stones or create a new one
    '''
    
    permission_classes = (AllowAny,)
    search_filter = ('name', 'stone_type')
    ordering_by = ('-created_at',)
    PageNumberPagination = StandardResultsSetPagination
    
    def get(self, request):
        stones = Stone.objects.all()
        serializer = StoneSerializer(stones, many=True)
        return success_response(message="لیست سنگ‌ها با موفقیت دریافت شد.", data=serializer.data)

    def post(self, request):
        serializer = StoneSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(message="سنگ با موفقیت ثبت شد.", data=serializer.data, status_code=status.HTTP_201_CREATED)
        return error_response(message="ثبت سنگ با خطا مواجه شد.", errors=serializer.errors)


class CommentsListPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 10


class StoneCommentListCreateView(APIView):
    '''
    API view to list or create comments for a specific Stone
    '''
    permission_classes = (AllowAny,)
    search_filter = ('stone')
    ordering_by = ('-created_at',)
    PageNumberPagination = CommentsListPagination
    
    def get(self, request, stone_id):
        try:
            comments = StoneComment.objects.filter(stone_id=stone_id)
            serializer = StoneCommentSerializer(comments, many=True)
            return success_response(message="نظرات با موفقیت دریافت شد.", data=serializer.data)
        except Exception as e:
            return internal_server_error_response(message="خطا در دریافت نظرات", exception=e)

    def post(self, request, stone_id):
        data = request.data.copy()
        data['stone'] = stone_id
        serializer = StoneCommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return success_response(message="نظر با موفقیت ثبت شد.", data=serializer.data, status_code=status.HTTP_201_CREATED)
        return error_response(message="ثبت نظر با خطا مواجه شد.", errors=serializer.errors)


class FAQListPagination(PageNumberPagination):
    page_size = 4
    page_size_query_param = 'page_size'
    max_page_size = 10


class StoneFAQListCreateView(APIView):
    '''
    API view to list or create FAQs for a specific Stone
    '''
    permission_classes = (AllowAny,)
    SearchFilter = ('stone')
    ordering_by = ('-created_at',)
    PageNumberPagination = FAQListPagination
    
    def get(self, request, stone_id):
        try:
            faqs = StoneFAQ.objects.filter(stone_id=stone_id)
            serializer = StoneFAQSerializer(faqs, many=True)
            return success_response(message="سوالات با موفقیت دریافت شد.", data=serializer.data)
        except Exception as e:
            return internal_server_error_response(message="خطا در دریافت سوالات", exception=e)

    def post(self, request, stone_id):
        data = request.data.copy()
        data['stone'] = stone_id
        serializer = StoneFAQSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return success_response(message="سوال با موفقیت ثبت شد.", data=serializer.data, status_code=status.HTTP_201_CREATED)
        return error_response(message="ثبت سوال با خطا مواجه شد.", errors=serializer.errors)



class StoneFAQAnswerView(UpdateAPIView):
    '''
    API view to allow admin users to answer a previously submitted FAQ
    '''
    queryset = StoneFAQ.objects.all()
    serializer_class = StoneFAQSerializer
    permission_classes = (IsAdminUser,)

    def patch(self, request, *args, **kwargs):
        faq = self.get_object()
        answer = request.data.get('answer')

        if not answer:
            return error_response(message="فیلد پاسخ نمی‌تواند خالی باشد.")

        faq.answer = answer
        faq.save()
        serializer = self.get_serializer(faq)
        return success_response(message="پاسخ با موفقیت ثبت شد.", data=serializer.data)