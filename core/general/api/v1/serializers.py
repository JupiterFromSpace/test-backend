from rest_framework import serializers
from general.models import Stone, StoneComment, StoneFAQ


class StoneCommentSerializer(serializers.ModelSerializer):
    '''
    Serializer for creating and listing comments related to a specific Stone
    '''
    class Meta:
        model = StoneComment
        fields = [
            'id',
            'stone',
            'author_name',
            'text',
            'created_at',
        ]


class StoneFAQSerializer(serializers.ModelSerializer):
    '''
    Serializer for creating and listing FAQs related to a specific Stone
    '''
    class Meta:
        model = StoneFAQ
        fields = [
            'id',
            'stone',
            'question',
            'answer',
        ]
        
        extra_kwargs = {
            'answer': {'required': False}
        }


class StoneSerializer(serializers.ModelSerializer):
    '''
    Serializer for creating and listing Stones along with their comments and FAQs
    '''
    comments = StoneCommentSerializer(many=True, read_only=True)
    faqs = StoneFAQSerializer(many=True, read_only=True)
    

    class Meta:
        model = Stone
        fields = [
            'id',
            'name',
            'stone_type',
            'description',
            'main_color',
            'image',
            'comments',
            'faqs',
        ]
