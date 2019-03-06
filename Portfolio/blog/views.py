from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm, SearchForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count   
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.contrib.postgres.search import TrigramSimilarity #TRIGAM SEARCH
from django.db.models.functions import Cast
# =============================================================================
def post_list(request, tag_slug=None):  
    object_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
    paginator = Paginator(object_list, 3) 
    page = request.GET.get('page')     
    try:
        posts = paginator.page(page)    
    except PageNotAnInteger:
# If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
# If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request,
                  'blog/post/list.html',
                  {'page': page,
                   'posts': posts,
                   'tag': tag})
# =============================================================================

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,      
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
# =============================================================================
#     # List of active comments for this post
# =============================================================================
    comments = post.comments.filter(active=True)    
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database. 
            new_comment.save()
    else:
        comment_form = CommentForm()
        
        
# =============================================================================
#     # List of similar posts
# =============================================================================
   
    post_tags_ids = post.tags.values_list('id', flat=True)     
    similar_posts = Post.published.filter(tags__in=post_tags_ids)\
                                  .exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
                                .order_by('-same_tags','-publish')[:4]
                                
    return render(request,
                  'blog/post/detail.html',  # render the retrieved post using a template
                  {'post': post,
                   'comments': comments,
                   'new_comment': new_comment,
                   'comment_form': comment_form,
                   'similar_posts': similar_posts})
    
# =============================================================================
#     USE instead of post_list(request) view
# =============================================================================
    
class PostListView(ListView):
    queryset = Post.published.all() 
    context_object_name = 'posts' 
    paginate_by = 2
    template_name = 'blog/post/list.html'   
    
# =============================================================================
#  Sending e-mail   
# =============================================================================
   
def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='published') 
    sent = False
    
    
    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                                        post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'izabela_granat@o2.pl', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})   
    
# =============================================================================
#     query field to let the users introduce search terms
# =============================================================================
    
def post_search(request):
    form = SearchForm() # instantiate form
    query = None
    results = []
    
    if 'query' in request.GET:      
        form = SearchForm(request.GET) 
        if form.is_valid():             
            query = form.cleaned_data['query']
             #USING TRIGrAM SIMILARITY
          
            results = Post.objects.annotate(
                    similarity=
                    TrigramSimilarity(('body' or 'title'), query), 

                    ).filter(similarity__gt=0.05).order_by('-similarity')
            # USING SearchVector, SearchQuery, SearchRank
            
            #search_vector = SearchVector('title', weight='A') + SearchVector('body',weight='B') 
            #search_query = SearchQuery(query)         
           
            #results = Post.objects.annotate(
                    #search=search_vector,
                    #rank=SearchRank(search_vector, search_query)
           # ).filter(rank__gte=0.2).order_by('-rank')
    return render(request,
                  'blog/post/search.html',
                  {'form': form,
                   'query': query,
                   'results': results})

def contact(request):
    return render(request,
                  'blog/post/contact.html')
    
def idea(request):
    return render(request,
                  'blog/post/idea.html')