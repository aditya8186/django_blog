from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Blogger, BlogPost, Comment

# Create your tests here.

class BloggerModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a test user
        test_user = User.objects.create_user(username='testuser', password='12345')
        # Create a test blogger
        Blogger.objects.create(user=test_user, bio='Test bio')

    def test_bio_label(self):
        blogger = Blogger.objects.get(id=1)
        field_label = blogger._meta.get_field('bio').verbose_name
        self.assertEqual(field_label, 'bio')

    def test_bio_max_length(self):
        blogger = Blogger.objects.get(id=1)
        max_length = blogger._meta.get_field('bio').max_length
        self.assertEqual(max_length, 500)

    def test_object_name_is_username(self):
        blogger = Blogger.objects.get(id=1)
        expected_object_name = blogger.user.username
        self.assertEqual(str(blogger), expected_object_name)

    def test_get_absolute_url(self):
        blogger = Blogger.objects.get(id=1)
        self.assertEqual(blogger.get_absolute_url(), '/blog/blogger/1/')

class BlogPostModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a test user and blogger
        test_user = User.objects.create_user(username='testuser', password='12345')
        test_blogger = Blogger.objects.create(user=test_user, bio='Test bio')
        # Create a test blog post
        BlogPost.objects.create(
            title='Test Blog Post',
            author=test_blogger,
            description='Test description'
        )

    def test_title_label(self):
        blogpost = BlogPost.objects.get(id=1)
        field_label = blogpost._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'title')

    def test_title_max_length(self):
        blogpost = BlogPost.objects.get(id=1)
        max_length = blogpost._meta.get_field('title').max_length
        self.assertEqual(max_length, 200)

    def test_object_name_is_title(self):
        blogpost = BlogPost.objects.get(id=1)
        expected_object_name = blogpost.title
        self.assertEqual(str(blogpost), expected_object_name)

    def test_get_absolute_url(self):
        blogpost = BlogPost.objects.get(id=1)
        self.assertEqual(blogpost.get_absolute_url(), '/blog/blog/1/')

class CommentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a test user and blogger
        test_user = User.objects.create_user(username='testuser', password='12345')
        test_blogger = Blogger.objects.create(user=test_user, bio='Test bio')
        # Create a test blog post
        test_blogpost = BlogPost.objects.create(
            title='Test Blog Post',
            author=test_blogger,
            description='Test description'
        )
        # Create a test comment
        Comment.objects.create(
            description='Test comment',
            author=test_user,
            blog_post=test_blogpost
        )

    def test_description_label(self):
        comment = Comment.objects.get(id=1)
        field_label = comment._meta.get_field('description').verbose_name
        self.assertEqual(field_label, 'description')

    def test_description_max_length(self):
        comment = Comment.objects.get(id=1)
        max_length = comment._meta.get_field('description').max_length
        self.assertEqual(max_length, 1000)

    def test_object_name_is_truncated_description(self):
        comment = Comment.objects.get(id=1)
        expected_object_name = comment.description[:75] + '...' if len(comment.description) > 75 else comment.description
        self.assertEqual(str(comment), expected_object_name)

class BlogListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a test user and blogger
        test_user = User.objects.create_user(username='testuser', password='12345')
        test_blogger = Blogger.objects.create(user=test_user, bio='Test bio')
        # Create 6 blog posts
        for post_num in range(6):
            BlogPost.objects.create(
                title=f'Test Blog Post {post_num}',
                author=test_blogger,
                description=f'Test description {post_num}'
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/blog/blogs/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('blogs'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('blogs'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blogpost_list.html')

    def test_pagination_is_five(self):
        response = self.client.get(reverse('blogs'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['blogpost_list']), 5)
