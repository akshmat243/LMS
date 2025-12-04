from django.contrib import admin

# 1. Imports from CURRENT APP (after_logout)
from .models import (
    ContactInquiry, 
    NewsletterSubscription, 
    CourseRequest, 
    MentorInquiry,
    TeamMember,
    HomeVideo,
    Testimonial,
    LiveClass,
    BlogCategory, 
    BlogPost, 
    ArticleContribution,
    OfficeLocation, 
    ContactStat, 
    SupportChannel
)

# 2. Imports from OTHER APPS (courses)
# Note: Ensure Mentors is NOT registered in courses/admin.py to avoid duplicates
from courses.models import Mentors

# --- Registrations ---

@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    search_fields = ('name', 'email')
    list_filter = ('category', 'created_at')

@admin.register(NewsletterSubscription)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at')
    search_fields = ('email',)

@admin.register(CourseRequest)
class CourseRequestAdmin(admin.ModelAdmin):
    list_display = ('topic', 'email', 'requested_at')
    search_fields = ('topic', 'email')

@admin.register(MentorInquiry)
class MentorInquiryAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'mentor_name', 'sent_at')
    search_fields = ('student_name', 'mentor_name')

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'role')

@admin.register(Mentors)
class MentorsAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'company', 'hourlyRate', 'reviews')
    search_fields = ('name', 'company', 'title')
    list_filter = ('company',)

@admin.register(HomeVideo)
class HomeVideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at')
    list_editable = ('is_active',)

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'rating')

@admin.register(LiveClass)
class LiveClassAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'start_date', 'category', 'price')
    list_filter = ('category', 'start_date')

@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author_name', 'views', 'created_at')
    search_fields = ('title', 'author_name')
    list_filter = ('category', 'created_at')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(ArticleContribution)
class ArticleContributionAdmin(admin.ModelAdmin):
    list_display = ('topic', 'name', 'submitted_at')

@admin.register(OfficeLocation)
class OfficeLocationAdmin(admin.ModelAdmin):
    list_display = ('city', 'phone', 'email')

@admin.register(ContactStat)
class ContactStatAdmin(admin.ModelAdmin):
    list_display = ('title', 'value')

@admin.register(SupportChannel)
class SupportChannelAdmin(admin.ModelAdmin):
    list_display = ('title', 'contact_text', 'availability', 'order')
    list_editable = ('order',)