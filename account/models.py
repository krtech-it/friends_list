from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profiles/%Y/%m/%d', blank=True)
    tg_id = models.IntegerField(blank=True, null=True)
    friends = models.ManyToManyField("Profile", blank=True)

    def __str__(self):
        return f"{self.user.username} profile"

    def clean(self):
        if self.image:
            name = (self.image.name).rsplit('.', 1)[1].lower()
            if name not in ['jpg','png', 'jpeg']:
                raise ValidationError('Формат изображениея неправильный')

class Case(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='cases')
    title = models.CharField(max_length=250)
    description = models.TextField(blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    deadline = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return f' by {self.profile}, {self.title}'

class Friend_Request(models.Model):
    from_user = models.ForeignKey(Profile,
                                  related_name='from_user',
                                  on_delete=models.CASCADE)
    to_user = models.ForeignKey(Profile,
                                related_name='to_user',
                                on_delete=models.CASCADE)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()