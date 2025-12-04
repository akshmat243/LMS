from rest_framework import serializers
from .models import *

class ContactInquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInquiry
        fields = ['id', 'name', 'email', 'phone_number', 'message', 'created_at']



class NewsletterSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsletterSubscription
        fields = ['email']

class CourseRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseRequest
        fields = '__all__'

class MentorInquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = MentorInquiry
        fields = '__all__'


class TeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = '__all__'


class HomeVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeVideo
        fields = ['id', 'title', 'video_file', 'youtube_url', 'is_active']

class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = '__all__'


class LiveClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = LiveClass
        fields = '__all__'


class BlogCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = ['id', 'name', 'slug']

class BlogPostSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = BlogPost
        fields = '__all__'

class ArticleContributionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleContribution
        fields = '__all__'

class ContactInquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInquiry
        fields = '__all__'


class OfficeLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfficeLocation
        fields = '__all__'


class ContactStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactStat
        fields = '__all__'

class SupportChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportChannel
        fields = '__all__'        

