from django.shortcuts import render , redirect
import random
from .serializers import TweetSerializer
from django.utils.http import is_safe_url
from django.conf import settings

from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework.decorators import api_view,authentication_classes ,permission_classes
from rest_framework.permissions import IsAuthenticated 

from django.http import  HttpResponse,Http404 , JsonResponse

from .forms import TweetForm
from .models import Tweet


ALLOWED_HOSTS=settings.ALLOWED_HOSTS

# Create your views here.
def home_view(request , *args , **kwargs):
    #print(args,kwargs)


    #return HttpResponse("<h1>hello world<h1>")
    return render(request, "pages/home.html" ,context={},status=200)

@api_view(['POST'])  #http method the client ==POST
#@authentication_classes([SessionAuthentication , MycustomAuth])
@permission_classes([IsAuthenticated])
def tweet_create_view(request,*args,**kwargs):
    #data=request.POST or None
    serializer =TweetSerializer(data=request.POST )
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user )
        return Response(serializer.data,status=201)
    return Response({},status=400)

@api_view(['GET'])
def tweet_list_view(request,*args,**kwargs):
    qs=Tweet.objects.all()
    serializer=TweetSerializer(qs,many=True)
   
    return Response(serializer.data)

@api_view(['GET'])
def tweet_detail_view(request,tweet_id,*args,**kwargs):
    qs=Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({}, status=404)
    obj=qs.first()
    serializer=TweetSerializer(obj)
   
    return Response(serializer.data, status=200)


def tweet_create_view_pure_django(request,*args,**kwargs):
    user=request.user
    print(user)
    if not request.user.is_authenticated:
        user=None
        if request.is_ajax():
            return JsonResponse({},status=401)
        return redirect(settings.LOGIN_URL)
    
    form=TweetForm(request.POST or None)
    
    next_url=request.POST.get("next") or None
    
    if form.is_valid():
        obj=form.save(commit=False)
        #do other form related logic
        obj.user=request.user or None #Annon User
        obj.save()

        if request.is_ajax():
            return JsonResponse(obj.serialize(),status=201) #201 == created items

        if next_url != None and is_safe_url(next_url,ALLOWED_HOSTS):
            return redirect(next_url)
        form=TweetForm()
    if form.errors:
        return JsonResponse(form.errors,status=400)
    

    


        
    return render(request,'components/form.html',context={"form":form})

def tweet_list_view_pure_django(request,*args,**kwargs):
    """
    REST API VIEW
    Consume by JavaScript or Swift/Java/iOS/Android
    return json data
    """
    qs=Tweet.objects.all()
    tweet_lists=[x.serialize() for x in qs]
    data={
        "isUser":False,
        "response": tweet_lists
    }
    return JsonResponse(data)


def tweet_detail_view_pure_django(request ,tweet_id,*args,**kwargs):
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