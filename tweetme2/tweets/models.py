from django.db import models
from django.conf import settings
import random

# Create your models here.

User=settings.AUTH_USER_MODEL

class TweetLike(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    tweet=models.ForeignKey("Tweet",on_delete=models.CASCADE)
    timestamp =models.DateTimeField(auto_now_add=True)
class Tweet(models.Model):
    #id=models.AutoField(primary_key=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    likes=models.ManyToManyField(User , related_name='tweet_user',blank=True,through=TweetLike)
    content=models.TextField(blank=True ,null=True)
    image=models.FileField(upload_to='images/',blank=True)

    class Meta:
        #for displaying the latest tweets first
        ordering=['-id']

    def serialize(self):
        return {
            "id":self.id,
            "content":self.content,
            "likes":random.randint(1,100)

        }