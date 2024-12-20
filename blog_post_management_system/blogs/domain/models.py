from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class BlogPost(models.Model):
    """Core domain entity for BlogPost"""

    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_published = models.DateTimeField(default=timezone.now)
    likes_count = models.ManyToManyField(User, related_name='liked_posts', blank=True)

    def __str__(self):
        return self.title
    
   
class BlogPostFactory:
    @staticmethod
    def create_blog_factory(title, content, author):
        """
        Factory method to create a new blog post.
        """
        blog_post = BlogPost(title=title, content=content, author=author)
        return blog_post
