from django.db import models
import datetime as dt
from django.contrib.auth.models import User
from tinymce.models import HTMLField
from django.db.models.signals import post_save
from django.dispatch import receiver



# Create your models here.

class Profile(models.Model):
    profilePhoto = models.ImageField(upload_to='profpics/',default='NO IMAGE')
    bio = models.CharField(max_length=60,blank=True)
    # user = models.ForeignKey(User,on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    # @receiver(post_save, sender=User)
    # def create_user_profile(sender, instance, created, **kwargs):
    #     if created:
    #         Profile.objects.create(user=instance)
    #
    # @receiver(post_save, sender=User)
    # def save_user_profile(sender, instance, **kwargs):
    #     instance.profile.save()

    def __str__(self):
        return self.bio

    def save_profile(self):
        self.save()

    def delete_profile(self):
        self.delete()
    @classmethod
    def search_by_username(cls,search_term):
        users = cls.objects.filter(user__username__icontains=search_term)
        return users

    @classmethod
    def get_profile(cls):
        profile = Profile.objects.all()
        return profile
    @classmethod
    def profile_by_id(cls, id):
        profile = Profile.objects.get(user = id)
        return profile

class Image(models.Model):
    image = models.ImageField(upload_to='uploads/', default='NO IMAGE')
    caption = HTMLField()
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveIntegerField(default=0)
    # user = models.ForeignKey(User,on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True)

    profile = models.ForeignKey(Profile,null=True,on_delete=models.CASCADE)

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
    @classmethod
    def search_by_caption(cls,search_term):
    	images = cls.objects.filter(caption__icontains=search_term)
    	return images

    class Meta:
        ordering = ['-timestamp']

class Comment(models.Model):
    # comment = models.CharField(max_length=80)
    comment = HTMLField()

    timestamp = models.DateTimeField(auto_now_add=True)
    # user = models.ForeignKey(User)
    user = models.ForeignKey(User, null=True)
    # user = models.ForeignKey(User,on_delete=models.CASCADE)
    image = models.ForeignKey(Image,on_delete=models.CASCADE)

    def __str__(self):
        return self.comment

    def save_comment(self):
        return self.save()

    def delete_comment(self):
        self.delete()
    class Meta:
        ordering = ['-timestamp']
