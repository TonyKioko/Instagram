from django.db import models

# Create your models here.

class Profile(models.Model):
    profilePic = models.ImageField(upload_to='profpics/',default='NO IMAGE')
    bio = models.CharField(max_length=60,blank=True)
    # user = models.ForeignKey(User,on_delete=models.CASCADE)
