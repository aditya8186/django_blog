from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from blog.models import Blogger, BlogPost, Comment
from datetime import datetime, timedelta
import random

class Command(BaseCommand):
    help = 'Populates the database with sample data'

    def handle(self, *args, **kwargs):
        # Create sample bloggers
        bloggers = []
        blogger_data = [
            {'username': 'sarah_williams', 'email': 'sarah.williams@example.com', 'bio': 'Tech enthusiast and software developer. Love sharing knowledge about programming and technology.'},
            {'username': 'michael_chen', 'email': 'michael.chen@example.com', 'bio': 'Photography enthusiast and travel blogger. Capturing moments and sharing stories from around the world.'},
            {'username': 'emma_thompson', 'email': 'emma.thompson@example.com', 'bio': 'Health and wellness coach. Sharing tips for a balanced lifestyle and personal growth.'},
            {'username': 'david_kim', 'email': 'david.kim@example.com', 'bio': 'Web developer and UI/UX designer. Passionate about creating beautiful and functional digital experiences.'},
            {'username': 'lisa_parker', 'email': 'lisa.parker@example.com', 'bio': 'Food blogger and culinary enthusiast. Exploring cuisines and sharing recipes from different cultures.'}
        ]

        users = []  # Store user instances
        for data in blogger_data:
            user = User.objects.create_user(
                username=data['username'],
                email=data['email'],
                password='password123'
            )
            users.append(user)  # Add user to the list
            blogger = Blogger.objects.create(
                user=user,
                bio=data['bio']
            )
            bloggers.append(blogger)
            self.stdout.write(self.style.SUCCESS(f'Created blogger: {data["username"]}'))

        # Sample blog post titles and contents
        blog_contents = [
            {
                'title': 'Getting Started with Python Programming',
                'content': '''Python is an excellent choice for beginners in programming. Its clean syntax and extensive library ecosystem make it perfect for learning the fundamentals of coding.

Key benefits of Python:
• Readable and maintainable code
• Large community support
• Versatile applications
• Rich library ecosystem

In this guide, we'll explore the basics of Python programming, from setting up your development environment to writing your first program. We'll cover variables, data types, control structures, and functions.

Setting up your environment:
1. Download and install Python from python.org
2. Choose an IDE (PyCharm, VS Code, or IDLE)
3. Create your first project

Let's start with a simple "Hello, World!" program:
```python
print("Hello, World!")
```

This is just the beginning of your Python journey. Stay tuned for more advanced topics and practical examples!'''
            },
            {
                'title': 'Mastering Digital Photography',
                'content': '''Digital photography has revolutionized how we capture and share moments. Whether you're using a DSLR or a smartphone, understanding the fundamentals can significantly improve your photos.

Essential photography concepts:
• Exposure triangle (aperture, shutter speed, ISO)
• Composition techniques
• Lighting fundamentals
• Post-processing basics

Composition tips:
1. Rule of thirds
2. Leading lines
3. Framing
4. Symmetry and patterns

Lighting is crucial in photography. Natural light is often the best choice, especially during the golden hours (sunrise and sunset). Understanding how to work with different lighting conditions will help you create more compelling images.

Remember, practice makes perfect. Don't be afraid to experiment with different settings and techniques!'''
            },
            {
                'title': 'Healthy Living: Tips for a Better Lifestyle',
                'content': '''Maintaining a healthy lifestyle is crucial for both physical and mental well-being. In this comprehensive guide, we'll explore various aspects of healthy living.

Key areas to focus on:
• Balanced nutrition
• Regular exercise
• Mental health
• Sleep hygiene

Nutrition tips:
1. Eat a variety of whole foods
2. Stay hydrated
3. Practice portion control
4. Limit processed foods

Exercise recommendations:
• 150 minutes of moderate activity per week
• Strength training 2-3 times per week
• Flexibility exercises
• Regular movement throughout the day

Mental health is equally important:
• Practice mindfulness
• Maintain social connections
• Manage stress effectively
• Seek professional help when needed

Remember, small changes can lead to significant improvements in your overall health!'''
            },
            {
                'title': 'Exploring Hidden Gems: Travel Guide',
                'content': '''Traveling is one of life's greatest pleasures, offering opportunities for growth, learning, and unforgettable experiences. This guide will help you discover lesser-known destinations and travel tips.

Planning your trip:
• Research destinations
• Set a budget
• Create an itinerary
• Pack efficiently

Travel tips:
1. Travel off-season
2. Stay in local accommodations
3. Learn basic phrases in the local language
4. Respect local customs

Hidden gems to consider:
• Lesser-known national parks
• Small towns with rich history
• Local food markets
• Cultural festivals

Safety considerations:
• Travel insurance
• Emergency contacts
• Local emergency numbers
• Health precautions

Remember to be respectful of local cultures and environments while exploring new places!'''
            },
            {
                'title': 'Modern Web Development Trends',
                'content': '''The web development landscape is constantly evolving, with new technologies and frameworks emerging regularly. Let's explore current trends and best practices.

Current trends:
• Progressive Web Apps (PWAs)
• Serverless architecture
• AI integration
• WebAssembly

Frontend development:
1. React and Next.js
2. Vue.js and Nuxt.js
3. Tailwind CSS
4. TypeScript

Backend technologies:
• Node.js and Express
• Python with Django/Flask
• GraphQL
• Microservices architecture

Development tools:
• Git and GitHub
• Docker
• CI/CD pipelines
• Testing frameworks

Stay updated with the latest developments and continuously improve your skills!'''
            },
            {
                'title': 'The Future of Artificial Intelligence',
                'content': '''Artificial Intelligence is transforming various industries and aspects of our daily lives. Let's explore current developments and future possibilities.

Key areas of AI:
• Machine Learning
• Deep Learning
• Natural Language Processing
• Computer Vision

Applications:
1. Healthcare
2. Finance
3. Transportation
4. Education

Ethical considerations:
• Privacy concerns
• Bias in AI systems
• Job displacement
• Responsible AI development

Future possibilities:
• General AI
• AI in space exploration
• Climate change solutions
• Personalized medicine

Stay informed about AI developments and their impact on society!'''
            },
            {
                'title': 'Culinary Adventures: Global Cuisine',
                'content': '''Exploring different cuisines is a wonderful way to learn about cultures and expand your culinary horizons. Let's dive into various global cuisines and cooking techniques.

Popular cuisines:
• Italian
• Japanese
• Indian
• Mexican

Cooking techniques:
1. Sautéing
2. Braising
3. Grilling
4. Baking

Essential ingredients:
• Herbs and spices
• Oils and vinegars
• Grains and legumes
• Fresh produce

Kitchen tools:
• Quality knives
• Pots and pans
• Small appliances
• Measuring tools

Remember to experiment and have fun in the kitchen!'''
            },
            {
                'title': 'Digital Marketing Strategies',
                'content': '''Effective digital marketing is crucial for businesses in today's connected world. Let's explore various strategies and tools for successful online marketing.

Key components:
• Content Marketing
• Social Media Marketing
• Email Marketing
• SEO

Strategy development:
1. Define your target audience
2. Set clear goals
3. Choose appropriate channels
4. Create valuable content

Analytics and tracking:
• Google Analytics
• Social media metrics
• Conversion tracking
• ROI measurement

Tools and platforms:
• Marketing automation
• Social media management
• Email marketing software
• Analytics tools

Stay updated with the latest digital marketing trends and best practices!'''
            },
            {
                'title': 'Mindfulness and Meditation Guide',
                'content': '''Mindfulness and meditation can significantly improve mental well-being and overall quality of life. Let's explore various techniques and benefits.

Benefits:
• Reduced stress
• Improved focus
• Better emotional regulation
• Enhanced self-awareness

Meditation techniques:
1. Mindfulness meditation
2. Loving-kindness meditation
3. Body scan
4. Breath awareness

Daily practices:
• Morning routine
• Mindful eating
• Walking meditation
• Gratitude practice

Getting started:
• Find a quiet space
• Set a regular schedule
• Start with short sessions
• Be patient with yourself

Remember, consistency is key to experiencing the benefits of mindfulness!'''
            },
            {
                'title': 'Sustainable Living Guide',
                'content': '''Sustainable living is essential for preserving our planet for future generations. Let's explore ways to reduce our environmental impact.

Key areas:
• Energy conservation
• Waste reduction
• Sustainable transportation
• Eco-friendly products

Home sustainability:
1. Energy-efficient appliances
2. Water conservation
3. Waste management
4. Green cleaning

Lifestyle changes:
• Reduce, reuse, recycle
• Sustainable fashion
• Plant-based diet
• Minimalist living

Community involvement:
• Local initiatives
• Environmental advocacy
• Community gardens
• Sustainable events

Together, we can make a difference for our planet!'''
            }
        ]

        # Create blog posts
        for i, content in enumerate(blog_contents):
            post = BlogPost.objects.create(
                title=content['title'],
                author=random.choice(bloggers),
                description=content['content'],
                post_date=datetime.now().date() - timedelta(days=i)
            )
            self.stdout.write(self.style.SUCCESS(f'Created blog post: {content["title"]}'))

            # Create comments for each blog post
            num_comments = random.randint(2, 4)
            for j in range(num_comments):
                comment = Comment.objects.create(
                    blog_post=post,
                    author=random.choice(users),  # Use User instance instead of Blogger
                    description=f'Sample comment {j+1} for {content["title"]}',
                    post_date=post.post_date + timedelta(days=j+1)
                )
                self.stdout.write(self.style.SUCCESS(f'Created comment for {content["title"]}'))

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with sample data')) 