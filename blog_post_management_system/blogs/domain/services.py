from .models import BlogPost, BlogPostFactory


class BlogPostService:
    """Domain service for blog post use cases"""

    @staticmethod
    def get_repo():
        return BlogPost.objects

    @staticmethod
    def get_factory():
        return BlogPostFactory

    def get_post_by_id_instance(self, post_id):
        """Retrieve a single post by its ID."""

        return self.get_repo().get(id=post_id)

    def list_posts_instance(self):
        """Retrieve all blog posts."""

        return self.get_repo().all()

    def create_post_instance(self, title, content, author):
        """Create a new blog post."""
        
        post = self.get_factory().create_blog_factory(title, content, author)
        post.save()
        return post

    def delete_post_instance(self, post_id):
        """Delete a blog post by ID."""
        
        post = self.get_repo().get(id=post_id)
        post.delete()
        return True
