from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# Create your models here.


class Billboard(models.Model):
    # Creating separate billboard table, as we might have to manually create boards from twitter tweets!
    message = models.CharField(max_length=150)
    user = models.ForeignKey(User, null=True, blank=True)
    upvotes = models.ImageField(default=0)
    sign = models.CharField(max_length=100)
    # Adding image after testing and creating with PIL, it would be dynamically generated using the name and sign of the billboard
    image = models.ImageField(upload_to='billboard')

    def __unicode__(self):
        return self.user


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    first_name = models.CharField(max_length=125)
    last_name = models.CharField(max_length=125)
    email = models.EmailField(blank=True, null=True)
    upvoted_boards = models.ManyToManyField(Billboard, blank=True)

    def __unicode__(self):
        return "{}'s profile".format(self.user.username)


UserProfile.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        newuser = UserProfile.objects.create(user=instance)
        newuser.first_name = instance.first_name
        newuser.last_name = instance.last_name
        newuser.email = instance.email
        newuser.save()

post_save.connect(create_user_profile, sender=User)
