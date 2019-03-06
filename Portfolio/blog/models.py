from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager



class PublishedManager(models.Manager):
    def get_queryset(self):                 #method of a manager returns the QuerySet that will be executed
        return super(PublishedManager,
                     self).get_queryset()\
                     .filter(status='published')


class Post(models.Model):
    STATUS_CHOICES = (
            ('draft', 'Draft'),
            ('published', 'Published'),
    )
    title = models.CharField(max_length=250) #for the post title
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish') # to be used for SEO friendly URls using publish date and slug
    author = models.ForeignKey(User,                        # many-to-one relationship (same author can write many posts but not other way round)
                               on_delete=models.CASCADE,    #on_delete=what to do when autor will be delated? SQL standard| cascade=delete related posts
                               related_name='blog_posts')   #name of relationship to access related objects easily later
    body = models.TextField()                               #body of the post => textfield (text column in SQLdb)
    publish = models.DateTimeField(default=timezone.now)    #when the post was published
    created = models.DateTimeField(auto_now_add=True)       #when the post was created, date saved automatically when creating an object
    updated = models.DateTimeField(auto_now=True)           #when the post was updated ,date saved automatically when saving an object
    status = models.CharField(max_length=10,                # shows status of a post from choices parameter,we can set one of given choices
                              choices=STATUS_CHOICES,
                              default='draft')
 
    objects = models.Manager() # The default manager.
    published = PublishedManager() # Our custom manager.we can now use it to perform queries
    tags = TaggableManager()

    
    class Meta:
       ordering = ('-publish',) # to sort results in descending(-) order when query the data base. Post published recnetly will apper first
       
    def __str__(self):          # default human-readable representation of the object. Django will use it in many places, such as the administration site
        return self.title
       
    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])
    
# =============================================================================
#                               Comment Model
# =============================================================================

class Comment(models.Model):
    post = models.ForeignKey(Post,               #many-to-one relationship
                             on_delete=models.CASCADE,
                             related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True) # to sort comments in a chronological order by default
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ('created',)
    
    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)