from django.db import models

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
