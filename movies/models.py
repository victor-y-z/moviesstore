from django.db import models
from django.contrib.auth.models import User
class MovieQuerySet(models.QuerySet):
    def available(self):
        return self.filter(
            models.Q(amount_left__isnull=True) | models.Q(amount_left__gt=0)
        )
class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='movie_images/')
    amount_left = models.PositiveIntegerField(null=True, blank=True)

    objects = MovieQuerySet.as_manager()  # now works

    def __str__(self):
        return str(self.id) + ' - ' + self.name

class Review(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.id) + ' - ' + self.movie.name