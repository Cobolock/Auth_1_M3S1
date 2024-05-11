import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from psqlextra.indexes import UniqueIndex


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_("name"), max_length=255, unique=True)
    description = models.TextField(_("description"), blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'content"."genre'
        verbose_name = _("genre")
        verbose_name_plural = _("genres")


class FilmType(models.TextChoices):
    MOVIE = "movie", _("movie")
    TV_SHOW = "tv_show", _("tv_show")


class Filmwork(UUIDMixin, TimeStampedMixin):
    title = models.CharField(_("title"), max_length=255)
    description = models.TextField(_("description"), blank=True)
    creation_date = models.DateField(_("creation_date"), blank=True)
    rating = models.FloatField(
        _("rating"), blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    type = models.CharField(_("type"), max_length=255, choices=FilmType.choices)
    genres = models.ManyToManyField("Genre", through="GenreFilmwork")
    persons = models.ManyToManyField("Person", through="PersonFilmwork")

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'content"."film_work'
        verbose_name = _("filmwork")
        verbose_name_plural = _("filmworks")
        indexes = [models.Index(fields=["creation_date"], name="film_work_creation_date_idx")]


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey("Filmwork", on_delete=models.CASCADE)
    genre = models.ForeignKey("Genre", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.genre} ({self.film_work})"

    class Meta:
        db_table = 'content"."genre_film_work'
        verbose_name = _("genre_filmwork")
        verbose_name_plural = _("genre_filmworks")
        indexes = [UniqueIndex(fields=["film_work", "genre"], name="film_work_genre_idx")]


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField(_("full_name"), max_length=255)

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = 'content"."person'
        verbose_name = _("person")
        verbose_name_plural = _("persons")


class PersonFilmwork(UUIDMixin):
    film_work = models.ForeignKey("Filmwork", on_delete=models.CASCADE)
    person = models.ForeignKey("Person", on_delete=models.CASCADE)
    role = models.TextField(_("role"))
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.person} - {self.role} ({self.film_work})"

    class Meta:
        db_table = 'content"."person_film_work'
        verbose_name = _("person_filmwork")
        verbose_name_plural = _("person_filmworks")
        indexes = [
            UniqueIndex(fields=["film_work", "person", "role"], name="film_work_person_role_idx")
        ]
