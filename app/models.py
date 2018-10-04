from django.db import models
import datetime as dt


# Create your models here.

class Profile(models.Model):
    profilePhoto = models.ImageField(upload_to='profpics/',default='NO IMAGE')
    bio = models.CharField(max_length=60,blank=True)
    # user = models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        return self.bio

    def save_profile(self):
        self.save()

    def delete_profile(self):
        self.delete()

    @classmethod
    def get_profile(cls):
        profile = Profile.objects.all()
        return profile

class Image(models.Model):
    image = models.ImageField(upload_to='uploads/', default='NO IMAGE')
    caption = models.CharField(max_length = 80)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveIntegerField(default=0)
    # user = models.ForeignKey(User,on_delete=models.CASCADE)
    # profile = models.ForeignKey(Profile,on_delete=models.CASCADE

    def __str__(self):
        return self.caption

    def save_image(self):
        self.save()

    def delete_image(self):
        self.delete()

    @classmethod
    def update_caption(cls,id,caption):
        updated_caption = Image.objects.filter(id=id).update(caption = caption)
        return updated_caption

    class Meta:
        ordering = ['-timestamp']
