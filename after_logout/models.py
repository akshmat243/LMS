from django.db import models
import uuid
from django.utils.text import slugify

class ContactInquiry(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    subject = models.CharField(max_length=200, blank=True, null=True) 
    category = models.CharField(max_length=100, default="General Inquiry") 
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"
    

# 2. Newsletter (New)
class NewsletterSubscription(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

# 3. Course Request (New)
class CourseRequest(models.Model):

    topic = models.CharField(max_length=200)
    email = models.EmailField()
    description = models.TextField(blank=True, null=True)
    requested_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.topic

# 4. Mentor Inquiry / Message (New)
class MentorInquiry(models.Model):

    mentor_name = models.CharField(max_length=200) # Frontend se mentor ka naam bhejdena
    student_name = models.CharField(max_length=200)
    student_email = models.EmailField()
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Msg for {self.mentor_name} from {self.student_name}"
    


class TeamMember(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100) # e.g., CEO, CTO
    bio = models.TextField()
    image = models.ImageField(upload_to='team/', blank=True, null=True) # Photo ke liye
    linkedin_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    


# 1. VIDEO MODEL (Jo Sir ne bola)
class HomeVideo(models.Model):
    title = models.CharField(max_length=100, default="Demo Video")
    video_file = models.FileField(upload_to='home_videos/', blank=True, null=True) # Direct upload ke liye
    youtube_url = models.URLField(blank=True, null=True) # Agar YouTube link lagana ho
    is_active = models.BooleanField(default=False) # Jo active hoga wahi dikhega
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# 2. TESTIMONIALS MODEL (Reviews)
class Testimonial(models.Model):
    name = models.CharField(max_length=100) # e.g. Sarah Johnson
    role = models.CharField(max_length=100) # e.g. Software Developer
    content = models.TextField() # "This course changed my life..."
    image = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    rating = models.IntegerField(default=5) # 1 to 5 stars
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    


class LiveClass(models.Model):
    CLASS_TYPES = [
        ('live', 'Live Class'),
        ('on-demand', 'On-Demand'),
        ('event', 'Event'),
    ]

    title = models.CharField(max_length=200)
    instructor = models.CharField(max_length=100) # Name like "Dr. Sarah"
    description = models.TextField()
    
    # Timing
    start_date = models.DateField()
    start_time = models.TimeField()
    duration = models.CharField(max_length=50) # e.g. "2 hours"
    
    # Seats & Price
    total_seats = models.IntegerField(default=50)
    enrolled_count = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    # Meta
    rating = models.FloatField(default=4.5)
    tags = models.JSONField(default=list) # ["AI", "Python"]
    category = models.CharField(max_length=20, choices=CLASS_TYPES, default='live')
    
    # Link
    meeting_link = models.URLField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
   


# 1. BLOG CATEGORY (e.g., Web Dev, AI/ML)
class BlogCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

# 2. BLOG POST
class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True, related_name='posts')
    
    # Author Details (Manually daal sakte hain bina User link kiye, easy management ke liye)
    author_name = models.CharField(max_length=100) # e.g. Alex Chen
    author_role = models.CharField(max_length=100) # e.g. Data Scientist
    author_image = models.ImageField(upload_to='blog_authors/', blank=True, null=True)
    
    # Content
    content = models.TextField() # Pura article HTML/Text
    excerpt = models.TextField(max_length=300, help_text="Short summary for card")
    thumbnail = models.ImageField(upload_to='blog_thumbnails/', blank=True, null=True)
    
    # Meta Data
    tags = models.JSONField(default=list) # ["React", "Frontend"]
    read_time = models.CharField(max_length=20, default="5 min read")
    views = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            # Slug banana: "My Title" -> "my-title-a1b2"
            base_slug = slugify(self.title)
            unique_suffix = str(uuid.uuid4())[:4]
            self.slug = f"{base_slug}-{unique_suffix}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

# 3. ARTICLE CONTRIBUTION (Form Submission)
class ArticleContribution(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    topic = models.CharField(max_length=200)
    description = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Idea: {self.topic} by {self.name}"


# after_logout/models.py

# ... purane models ...

# 1. CONTACT FORM (Update Existing)
# Agar pehle se ContactInquiry bana hai, to usme ye naye fields add karne honge.
# Ya fir isse replace kar de.
# class ContactInquiry(models.Model):
#     name = models.CharField(max_length=200)
#     email = models.EmailField()
#     subject = models.CharField(max_length=200, blank=True, null=True) # ✅ New Field
#     category = models.CharField(max_length=100, default="General Inquiry") # ✅ New Field (Dropdown ke liye)
#     message = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.name} - {self.subject}"

# 2. GLOBAL OFFICES (New)
class OfficeLocation(models.Model):
    city = models.CharField(max_length=100) # e.g. London
    badge_text = models.CharField(max_length=20, default="GMT") # e.g. PST, EST
    address = models.TextField() # e.g. 789 Learning Lane...
    phone = models.CharField(max_length=50)
    email = models.EmailField()
    
    # Business Hours (Simple text field)
    opening_hours = models.CharField(max_length=200, default="Mon-Fri 9AM-6PM") 
    
    def __str__(self):
        return self.city

# 3. CONTACT PAGE STATS (New)
class ContactStat(models.Model):
    title = models.CharField(max_length=100) # e.g. "Response Time"
    value = models.CharField(max_length=50)  # e.g. "< 1hr"
    description = models.CharField(max_length=200, blank=True) # e.g. "Speak directly..."
    icon_name = models.CharField(max_length=50, default="clock") # Frontend icon mapping
    
    def __str__(self):
        return self.title
    

# 4. SUPPORT CHANNELS (Email, Phone, Chat Cards)
class SupportChannel(models.Model):
    title = models.CharField(max_length=100)       # e.g. "Email Support"
    description = models.CharField(max_length=255) # e.g. "Get help from our support team"
    contact_text = models.CharField(max_length=200)# e.g. "support@ailearn.com" or "+1 (555) 123-4567"
    availability = models.CharField(max_length=100)# e.g. "< 24 hours" or "Mon-Fri 9AM-6PM"
    icon_name = models.CharField(max_length=50)    # e.g. "mail", "phone", "chat" (Frontend icon name)
    order = models.IntegerField(default=0)         # Card ka sequence set karne ke liye

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title




