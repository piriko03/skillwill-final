from django.db import models


class Author(models.Model):
    class Meta:
        db_table = 'author'

    name = models.CharField(max_length=200)
    biography = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
