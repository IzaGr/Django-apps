from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from .models import Post

#subclass the Feed class of the syndication framework
#The title, link, and description attributes correspond to the <title>, <link>, and <description> RSS elements, respectively.

class LatestPostsFeed(Feed):
    title = 'My blog'
    link = '/blog/'
    description = 'New posts of my blog.'
    #The items() method retrieves the objects to be included in the feed.
    #We are retrieving only the last five published posts for this feed
    def items(self):
        return Post.published.all()[:5]
    def item_title(self, item):
        return item.title
    def item_description(self, item):
        return truncatewords(item.body, 30)

