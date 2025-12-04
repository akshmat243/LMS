from rest_framework import generics, views, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Sum
from .serializers import ContactInquirySerializer
from courses.models import Course, Mentors
from django.db.models import Sum, Avg
from courses.serializers import CourseSerializer
from .models import ContactInquiry
from .models import *
from courses.models import *
from .serializers import *
from courses.serializers import *
from accounts.models import *
from courses.models import *
from django.contrib.auth import get_user_model



# ---------------------------------------------------
# 1. PUBLIC COURSE LIST API (Search & Filter ke saath)
# ---------------------------------------------------
class PublicCourseListView(generics.ListAPIView):
    """
    Returns list of PUBLISHED courses with Search, Filtering (Category, Level), and Ordering.
    Access: Public (No Login Required)
    """
    queryset = Course.objects.filter(is_published=True).order_by('-created_at')
    serializer_class = CourseSerializer
    permission_classes = [AllowAny]  

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    
    filterset_fields = ['category', 'level' ] 
    
    search_fields = ['title', 'description', 'instructor', 'skills__icontains']
    
    ordering_fields = ['price', 'rating', 'created_at']

# ---------------------------------------------------
# 2. CATEGORIES LIST API (Dropdowns/Buttons ke liye)
# ---------------------------------------------------
class PublicCategoriesView(views.APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        categories = Course.objects.filter(is_published=True).values_list('category', flat=True).distinct()
        
        clean_categories = [cat for cat in categories if cat]
        return Response({"categories": clean_categories}, status=status.HTTP_200_OK)

# ---------------------------------------------------
# 3. PLATFORM STATS API (Hero Section ke liye)
# ---------------------------------------------------
User = get_user_model()

class PublicPlatformStatsView(views.APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # 1. Total Courses (Published)
        total_courses = Course.objects.filter(is_published=True).count()

        # 2. Total Instructors/Mentors
        total_instructors = Mentors.objects.count()

        # 3. Total Hours (Duration sum)
        total_minutes = Course.objects.filter(is_published=True).aggregate(Sum('duration_minutes'))['duration_minutes__sum'] or 0
        total_hours = int(total_minutes // 60)

        # 4. Active Learners (Real Users Count)
       
        active_learners_count = User.objects.count()

        # 5. Success Rate (Completion %)
        total_enrollments = CourseEnrollment.objects.count()
        completed_enrollments = CourseEnrollment.objects.filter(is_completed=True).count()
        
        if total_enrollments > 0:
            success_rate = int((completed_enrollments / total_enrollments) * 100)
        else:
            success_rate = 0 # IF THERE IS NO ANY STUDENT 

        data = {
            "total_courses": total_courses,
            "total_instructors": total_instructors,
            "total_course_hours": total_hours,
            "success_rate": f"{success_rate}%",      
            "active_learners": f"{active_learners_count}+" 
        }
        return Response(data, status=status.HTTP_200_OK)
    


# ---------------------------------------------------
# 4. CONTACT US API (POST Form Data)
# ---------------------------------------------------
class ContactInquiryCreateView(generics.CreateAPIView):
    """
    Allows any user (Guest) to submit a 'Get in Touch' form.
    No Token Required.
    """
    queryset = ContactInquiry.objects.all()
    serializer_class = ContactInquirySerializer
    permission_classes = [AllowAny]




# ---------------------------------------------------
# 5. PUBLIC MENTOR LIST API (Search & Filters)
# ---------------------------------------------------
class PublicMentorListView(generics.ListAPIView):
    """
    Returns list of Mentors with Search (Name, Company, Skills) and Ordering (Price, Rating).
    Access: Public
    """
    queryset = Mentors.objects.all().order_by('-reviews') # Default sorting: Most reviewed first
    serializer_class = MentorsSerializer
    permission_classes = [AllowAny]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    
    # Dropdown Filters (Company, Location wagera ke liye)
    filterset_fields = ['company', 'locations', 'title']
    
    # Search Bar (Naam, Company, ya Skills dhoondhne ke liye)
    search_fields = ['name', 'company', 'title', 'specialties', 'expertise']
    
    # Sorting Options (Price Low/High, Rating)
    ordering_fields = ['hourlyRate', 'reviews', 'rating']

# ---------------------------------------------------
# 6. MENTOR STATS API (Hero Section)
# 
class PublicMentorStatsView(views.APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # 1. Total Mentors
        total_mentors = Mentors.objects.count()

        # 2. Sessions Completed (Real Logic)
        
        real_sessions_count = Meeting.objects.count()
        
        # 3. Average Rating (Real Logic for CharField)
        
        mentors = Mentors.objects.all()
        total_rating = 0.0
        rated_mentors_count = 0

        for mentor in mentors:
            try:
                
                if mentor.rating:
                    total_rating += float(mentor.rating)
                    rated_mentors_count += 1
            except ValueError:
                continue # Agar rating mein "Best" likha ho to ignore karo

        if rated_mentors_count > 0:
            avg_rating = round(total_rating / rated_mentors_count, 1)
        else:
            avg_rating = 0

        # 4. Success Rate (General Platform Success)
        
        total_enrollments = CourseEnrollment.objects.count()
        completed_enrollments = CourseEnrollment.objects.filter(is_completed=True).count()
        success_percentage = int((completed_enrollments / total_enrollments) * 100) if total_enrollments > 0 else 0

        data = {
            "total_mentors": total_mentors,
            "sessions_completed": f"{real_sessions_count}+", 
            "average_rating": str(avg_rating),               
            "success_rate": f"{success_percentage}%"         
        }
        return Response(data, status=status.HTTP_200_OK)

# ---------------------------------------------------
# 7. MENTOR EXPERTISE/SKILLS API (Dropdowns)
# ---------------------------------------------------

class PublicMentorSpecialtiesView(views.APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        mentors = Mentors.objects.all()
        all_skills = set() # Set use kar rahe hain taaki duplicate na ho
        
        for mentor in mentors:
            
            if mentor.expertise and isinstance(mentor.expertise, list):
                for skill in mentor.expertise:
                    all_skills.add(skill)
            
           
            if mentor.specialties and isinstance(mentor.specialties, list):
                for skill in mentor.specialties:
                    all_skills.add(skill)
                    
        return Response({"specialties": list(all_skills)}, status=status.HTTP_200_OK)


# 1. NEWSLETTER API
class NewsletterSubscribeView(generics.CreateAPIView):
    queryset = NewsletterSubscription.objects.all()
    serializer_class = NewsletterSerializer
    permission_classes = [AllowAny]

# 2. COURSE REQUEST API
class CourseRequestView(generics.CreateAPIView):
    queryset = CourseRequest.objects.all()
    serializer_class = CourseRequestSerializer
    permission_classes = [AllowAny]

# 3. MENTOR MESSAGE API
class MentorMessageView(generics.CreateAPIView):
    queryset = MentorInquiry.objects.all()
    serializer_class = MentorInquirySerializer
    permission_classes = [AllowAny]




# 1. TEAM API (New)
class PublicTeamView(generics.ListAPIView):
    queryset = TeamMember.objects.all().order_by('created_at')
    serializer_class = TeamMemberSerializer
    permission_classes = [AllowAny]


User = get_user_model()
class AboutStatsView(views.APIView):
    """
    Returns 100% REAL calculated stats from Database (Users + Profiles).
    """
    permission_classes = [AllowAny]

    def get(self, request):
        # 1. Total Students
        total_students = User.objects.count()

        # 2. Completion Rate
        total_enrollments = CourseEnrollment.objects.count()
        completed_enrollments = CourseEnrollment.objects.filter(is_completed=True).count()
        completion_rate = int((completed_enrollments / total_enrollments) * 100) if total_enrollments > 0 else 0

        # 3. Career Advancement (Real Calculation)
        
        placed_students = StudentProfile.objects.filter(got_job_after_course=True).count()
        career_rate = int((placed_students / total_students) * 100) if total_students > 0 else 0

        # 4. Countries Served (Real Calculation)
       
        unique_countries = StudentProfile.objects.values('country').distinct().count()

        data = [
            {
                "id": 1,
                "value": f"{total_students}+",
                "label": "Students Worldwide",
                "description": "Active learners joining our platform"
            },
            {
                "id": 2,
                "value": f"{completion_rate}%",
                "label": "Course Completion",
                "description": "Real-time course completion rate"
            },
            {
                "id": 3,
                "value": f"{career_rate}%", 
                "label": "Career Advancement",
                "description": "Students got jobs after learning"
            },
            {
                "id": 4,
                "value": f"{unique_countries}+",
                "label": "Countries Served",
                "description": "Global reach and impact"
            }
        ]
        return Response(data, status=status.HTTP_200_OK)
    


# 1. HOME VIDEO API
class HomeVideoView(views.APIView):
    permission_classes = [AllowAny]

    def get(self, request):
       
        video = HomeVideo.objects.filter(is_active=True).first()
        if video:
            serializer = HomeVideoSerializer(video)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"message": "No active video found"}, status=status.HTTP_404_NOT_FOUND)

# 2. TESTIMONIALS API
class TestimonialListView(generics.ListAPIView):
    queryset = Testimonial.objects.all().order_by('-created_at')
    serializer_class = TestimonialSerializer
    permission_classes = [AllowAny]



# 1. LIVE CLASSES LIST API
class PublicLiveClassListView(generics.ListAPIView):
    """
    Returns list of Live Classes with Filtering & Search.
    """
    queryset = LiveClass.objects.all().order_by('start_date')
    serializer_class = LiveClassSerializer
    permission_classes = [AllowAny]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    
    # Filter by Tab (Live, On-Demand, Event)
    filterset_fields = ['category'] 
    
    # Search by Title or Instructor
    search_fields = ['title', 'instructor', 'tags']
    
    ordering_fields = ['price', 'start_date', 'rating']

# 2. CLASSES STATS API (Hero Section)
class PublicClassStatsView(views.APIView):
    """
    Returns REAL dynamic stats calculated from LiveClass data.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        # 1. Total Live Sessions (Count)
        total_sessions = LiveClass.objects.count()

        # 2. Expert Instructors (Count Unique Instructors)
        
        total_instructors = LiveClass.objects.values('instructor').distinct().count()

       
        total_participants = LiveClass.objects.aggregate(Sum('enrolled_count'))['enrolled_count__sum'] or 0

        # 4. Satisfaction Rate (Average Rating -> Percentage)
        
        avg_rating = LiveClass.objects.aggregate(Avg('rating'))['rating__avg'] or 0
        
        if avg_rating > 0:
            satisfaction_percentage = int((avg_rating / 5) * 100)
        else:
            satisfaction_percentage = 0 # IF THERE IS NO ANY RATING 

        data = {
            "live_sessions": f"{total_sessions}+",
            "expert_instructors": f"{total_instructors}+",
            "active_participants": f"{total_participants}+",
            "satisfaction_rate": f"{satisfaction_percentage}%"
        }
        return Response(data, status=status.HTTP_200_OK)
    




# 1. BLOG LIST API (Search & Filter)
class PublicBlogListView(generics.ListAPIView):
    queryset = BlogPost.objects.filter(is_published=True).order_by('-created_at')
    serializer_class = BlogPostSerializer
    permission_classes = [AllowAny]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    
    # Filter by Category ID or Name
    filterset_fields = ['category', 'author_name']
    
    # Search by Title, Tags, or Author
    search_fields = ['title', 'tags', 'author_name', 'excerpt']
    
    ordering_fields = ['views', 'created_at']

# 2. BLOG CATEGORIES API (For Chips/Tabs)
class PublicBlogCategoryView(generics.ListAPIView):
    queryset = BlogCategory.objects.all()
    serializer_class = BlogCategorySerializer
    permission_classes = [AllowAny]

# 3. BLOG STATS API (Header Section)
class PublicBlogStatsView(views.APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        total_articles = BlogPost.objects.filter(is_published=True).count()
        # Count unique authors
        total_authors = BlogPost.objects.values('author_name').distinct().count()
        # Sum of all views
        total_readers = BlogPost.objects.aggregate(Sum('views'))['views__sum'] or 0

        data = {
            "articles_published": f"{total_articles}+",
            "expert_authors": f"{total_authors}+",
            "monthly_readers": f"{total_readers}+", # Real view count sum
            "new_content": "Weekly"
        }
        return Response(data, status=status.HTTP_200_OK)

# 4. CONTRIBUTE IDEA API
class ArticleContributionCreateView(generics.CreateAPIView):
    queryset = ArticleContribution.objects.all()
    serializer_class = ArticleContributionSerializer
    permission_classes = [AllowAny]


# 1. CONTACT FORM SUBMIT (Updated)
class ContactInquiryCreateView(generics.CreateAPIView):
    queryset = ContactInquiry.objects.all()
    serializer_class = ContactInquirySerializer
    permission_classes = [AllowAny]

# 2. OFFICE LOCATIONS LIST API
class PublicOfficeListView(generics.ListAPIView):
    queryset = OfficeLocation.objects.all()
    serializer_class = OfficeLocationSerializer
    permission_classes = [AllowAny]

# 3. CONTACT STATS LIST API
class PublicContactStatsView(generics.ListAPIView):
    queryset = ContactStat.objects.all()
    serializer_class = ContactStatSerializer
    permission_classes = [AllowAny]    


# 4. SUPPORT CHANNELS LIST API
class PublicSupportChannelListView(generics.ListAPIView):
    """
    Returns list of support channels (Email, Phone, Chat cards).
    """
    queryset = SupportChannel.objects.all()
    serializer_class = SupportChannelSerializer
    permission_classes = [AllowAny]

    


