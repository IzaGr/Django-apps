from django.shortcuts import render, redirect
import requests
requests.packages.urllib3.disable_warnings()
from bs4 import BeautifulSoup
from .models import Image, Text
import os
import shutil
import urllib
from django.utils import timezone
from djqscsv import write_csv

# =============================================================================
# Display list of images and total count. User decides if download
# =============================================================================

def image_list(request):
    images = Image.objects.all()
    count = Image.objects.count()
    
    context = {
        'image_list': images,
        'count' : count
            }
    return render(request, "webscrap/content/image.html", context)
# =============================================================================
# Scrap images urls from the website and save on datebase
# =============================================================================

def image_scraper(request):
    

    session = requests.Session()
    session.headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36"}
    url= 'https://www.theonion.com/' # EXAMPLE WEBSITE WITH LITTLE JAVASCRIPT on it
    content = session.get(url, verify=False).content
    soup = BeautifulSoup(content, "html.parser")
    img_urls=[]
    Image.objects.all().delete()        #delete old objects
    try:
        img = soup.find_all('source',{'data-srcset':True})
        for number, link in enumerate(img):
            img_source = link.get('data-srcset')
            img_urls.append(img_source)                     
            new_image = Image()
            new_image.url = img_source
            new_image.count = number + 1
            new_image.save()
          
    except:
        print("No images found")
        
    return redirect('/home/')

# =============================================================================
# Download images from urls saved in database
# =============================================================================

def image_downloader(request, commit=True):
    
    session = requests.Session()
    paths = Image.objects.all().values_list('url', flat=True)
    media_root = '/Users/Izis/Pictures/media_root' #YOUR MEDIA-ROOT
    for number, path in enumerate(paths):
        local_filename = str(number+1)+path.split('/')[-1].split("?")[0] #to download all pictures even with the same shortname but different size
        r = session.get(path, stream=True, verify=False)
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024): 
                f.write(chunk)
    
        current_image_absolute_path = os.path.abspath(local_filename)
        shutil.move(current_image_absolute_path, media_root)
    
    return redirect('/home/')
# =============================================================================
# Scrape text and remove javascript tags. Create TextField object and save in database 
# =============================================================================
def text_scraper(request):
    
    url= 'https://www.theonion.com/' # EXAMPLE WEBSITE WITH LITTLE JAVASCRIPT on it
    sauce = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(sauce,'lxml')
    
    for script in soup(["script", "style"]):
        script.decompose()
      
    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    pieces = (phrase.strip() for line in lines for phrase in line.split("  "))
    words = '\n'.join(pc for pc in pieces if pc)
    
    new_text=Text()
    new_text.article = words
    new_text.created_at = timezone.now()
    new_text.save()
    
    context = {'words': words }
    
    return render(request, "webscrap/content/text.html", context)

# =============================================================================
# Download all texts from database and save in csv file in project directory
# =============================================================================

def download_csv(request):
    all_text = Text.objects.values('article')
    with open('all_text.csv', 'wb') as csv_file:
        write_csv(all_text, csv_file)
    return render (request, "webscrap/content/text.html")


