from django.db import models

# model- userprofile, last_scrape)

# model - Image (all images from the website)

# model - Text (header, article - text from website, assuming that valuable content for machine learning enginners are only headers and acticles)


class Text(models.Model):

    article = models.TextField()  
    created_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.article
    
class Image(models.Model):
    image = models.ImageField(upload_to='images/%Y/%m/%d/') # in case of saving images on database rightaway
    url = models.URLField()
    count = models.IntegerField(default='0')
    
    def __str__(self):
        return self.url
    
    def save(self, *args, **kwargs):
        super(Image, self).save(*args, **kwargs)
    

    
    