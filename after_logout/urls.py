from django.urls import path
from .views import PublicCourseListView, PublicCategoriesView, PublicPlatformStatsView , ContactInquiryCreateView 
from .views import PublicMentorStatsView , PublicMentorListView , PublicMentorSpecialtiesView 
from .views import *

                  
    


urlpatterns = [



    # Courses list 
    path('courses/', PublicCourseListView.as_view(), name='public-course-list'),

    # Categories list
    path('categories/', PublicCategoriesView.as_view(), name='public-categories'),

    # Stats for Hero Section
    path('stats/', PublicPlatformStatsView.as_view(), name='public-stats'),

    #for inquiry
    path('contact/', ContactInquiryCreateView.as_view(), name='public-contact'),


    path('mentors/', PublicMentorListView.as_view(), name='public-mentor-list'),
    path('mentors/stats/', PublicMentorStatsView.as_view(), name='public-mentor-stats'),
    path('mentors/specialties/', PublicMentorSpecialtiesView.as_view(), name='public-mentor-specialties'),


    # New URLs
    path('newsletter/', NewsletterSubscribeView.as_view(), name='public-newsletter'),
    path('request-course/', CourseRequestView.as_view(), name='public-course-request'),
    path('mentor-message/', MentorMessageView.as_view(), name='public-mentor-message'), 


    path('team/', PublicTeamView.as_view(), name='public-team'),

    path('about/stats/', AboutStatsView.as_view(), name='about-stats'),


    # Home Page APIs
    path('home/video/', HomeVideoView.as_view(), name='home-video'),
    path('home/testimonials/', TestimonialListView.as_view(), name='home-testimonials'),


    # Classes Page APIs
    path('classes/', PublicLiveClassListView.as_view(), name='public-classes'),
    path('classes/stats/', PublicClassStatsView.as_view(), name='public-classes-stats'),


    # BLOG APIS
    path('blogs/', PublicBlogListView.as_view(), name='public-blogs'),
    path('blogs/categories/', PublicBlogCategoryView.as_view(), name='public-blog-categories'),
    path('blogs/stats/', PublicBlogStatsView.as_view(), name='public-blog-stats'),
    path('blogs/contribute/', ArticleContributionCreateView.as_view(), name='public-blog-contribute'),


    # Contact Page APIs
    path('contact/submit/', ContactInquiryCreateView.as_view(), name='contact-submit'),
    path('contact/offices/', PublicOfficeListView.as_view(), name='contact-offices'),
    path('contact/stats/', PublicContactStatsView.as_view(), name='contact-stats'),
    # Contact Page Support Channels
    path('contact/channels/', PublicSupportChannelListView.as_view(), name='contact-channels'),












]