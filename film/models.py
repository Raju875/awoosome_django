from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from abstract_app.models import Common


class Genre(Common):
    name = models.CharField(max_length=100)
    note = models.CharField(max_length=100,default='ok')
    test = models.CharField(max_length=100, default='ok')

    def __str__(self):
        return self.name


class Film(Common):
    title = models.CharField(max_length=200,)
    note1 = models.CharField(max_length=200, default='ok')
    note2 = models.CharField(max_length=200, default='ok')
    length = models.PositiveIntegerField(blank=True, null=True)
    year = models.PositiveIntegerField(blank=True, null=True)
    score = models.FloatField(blank=True, null=True, validators=[
                              MinValueValidator(0), MaxValueValidator(10)])
    genre = models.ForeignKey(
        Genre, blank=True, null=True, on_delete=models.CASCADE, related_name='film')

    def __str__(self):
        if self.year:
            return f"{self.title} ({self.year})"
        return self.title

    def get_fields(self):
        return [(field.verbose_name, field.value_from_object(self))

                if field.verbose_name != 'genre'

                else
                (field.verbose_name,
                 Genre.objects.get(pk=field.value_from_object(self)).name)

                for field in self.__class__._meta.fields[1:]
                ]


class Production(Common):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Director(Common):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
