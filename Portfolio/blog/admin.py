from django.contrib import admin
from .models import Post, Comment

@admin.register(Post)           #decorator, the same function as admin.site.register(), registering and decorating modelAdmin class
class PostAdmin(admin.ModelAdmin):          #our model is registered in the admin site using custom class that inherits form Model Admin
    list_display = ('title', 'slug', 'author', 'publish',   #how to display the model and interact
                    'status')
    list_filter = ('status', 'created', 'publish', 'author')    #right sidebar that allows you to filter the results
    search_fields = ('title', 'body')                           #defined a list of searchable fields
    prepopulated_fields = {'slug': ('title',)}  #slug field is filled in automatically, prepopulate the slug field with the input of the title field
    raw_id_fields = ('author',) #author field is displayed with a lookup widget that can scale much better than a drop-down select input 
    date_hierarchy = 'publish'                            #navigation links to navigate through a date hierarchy
    ordering = ('status', 'publish')                    #posts are ordered by Status and Publish columns by default
    
    
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')