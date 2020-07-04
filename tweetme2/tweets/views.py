from django.shortcuts import render
import random

from django.http import  HttpResponse,Http404 , JsonResponse

from .forms import TweetForm
from .models import Tweet

# Create your views here.


def home_view(request , *args , **kwargs):
    #print(args,kwargs)


    #return HttpResponse("<h1>hello world<h1>")
    return render(request, "pages/home.html" ,context={},status=200)

def tweet_create_view(request,*args,**kwargs):
    

def tweet_list_view(request,*args,**kwargs):
    qs=Tweet.objects.all()

    tweet_lists=[{"Id":x.id,"content":x.content,"likes":random.randint(0,100)} for x in qs]
    data={
        "isUser":False,
        "response": tweet_lists
    }
    return JsonResponse(data)
def tweet_detail_view(request ,tweet_id,*args,**kwargs):
    """
    REST API VIEW
    Consume by JavaScript or Swift/Java/iOS/Android
    return json data
    """
    data={
        "id":tweet_id,
        #"content":obj.content,
        #"image_path":obj.image.url
    }
    status=200

    try:
        obj=Tweet.objects.get(id=tweet_id)
        data['content']=obj.content
    except:
        data['message']="Not found"
        status=404

   
    #return HttpResponse(f"<h1>hello {tweet_id}- {obj.content}world<h1>")
    return JsonResponse(data , status=status) #json.dumps content_type='application/json'