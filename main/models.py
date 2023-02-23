from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Trip(models.Model):
    driver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dtrip', blank=True)
    info = models.TextField()
    from_city = models.CharField(max_length=50)
    to_city = models.CharField(max_length=50)
    date = models.DateField()
    time = models.TimeField()
    price = models.IntegerField()
    capacity = models.IntegerField()
    passangers = models.ManyToManyField(User, blank=True)

    def get_absolute_url(self):
        return reverse('show_trip', kwargs={'trip_id': self.pk})

    def __str__(self):
        return "Поездка №" + str(self.pk)


class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    info = models.TextField(blank=True)
    photo = models.ImageField(upload_to='photos/', blank=True)

    def get_absolute_url(self):
        return reverse('show_profile', kwargs={'profile_id': self.pk})

    def __str__(self):
        return "User №" + str(self.pk) + " Info"
