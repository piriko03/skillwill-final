from django.db import models

class Genre(models.Model):
    class Meta:
        db_table = 'genre'

    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name