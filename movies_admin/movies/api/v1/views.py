from django.contrib.postgres.expressions import ArraySubquery
from django.db.models import OuterRef
from django.http import JsonResponse
from django.views.generic import DetailView
from django.views.generic.list import BaseListView

from movies.models import Filmwork, GenreFilmwork, PersonFilmwork


class MoviesApiMixin:
    http_method_names = ["get"]

    def get_queryset(self):
        """
        ArrayAgg генерирует JOIN 3 таблиц для каждой ArrayAgg в annotate.
        Для двух ArrayAgg (persons, genres) уже получается запрос с JOIN'ом
        из 5 таблиц. Django делает декартово произведение и в результирующих
        списках образуются дубликаты. Я считаю, что лучше иметь несколько
        простых JOIN'ов в подзапросах, чем один большой JOIN почти всех таблиц в БД
        с дальнейшей дедупликацией.
        """

        genres_names_subquery = GenreFilmwork.objects.filter(film_work_id=OuterRef("id")).values(
            "genre__name"
        )

        actors_subquery = PersonFilmwork.objects.filter(
            film_work_id=OuterRef("id"), role="actor"
        ).values("person__full_name")

        directors_subquery = PersonFilmwork.objects.filter(
            film_work_id=OuterRef("id"), role="director"
        ).values("person__full_name")

        writers_subquery = PersonFilmwork.objects.filter(
            film_work_id=OuterRef("id"), role="writer"
        ).values("person__full_name")

        filmwork_qs = Filmwork.objects.values().annotate(
            genres=ArraySubquery(genres_names_subquery),
            actors=ArraySubquery(actors_subquery),
            directors=ArraySubquery(directors_subquery),
            writers=ArraySubquery(writers_subquery),
        )
        return filmwork_qs

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)


class MoviesListApi(MoviesApiMixin, BaseListView):
    paginate_by = 50

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = self.get_queryset()
        paginator, page, queryset, is_paginated = self.paginate_queryset(queryset, self.paginate_by)
        return {
            "count": paginator.count,
            "total_pages": paginator.num_pages,
            "next": page.next_page_number() if page.has_next() else None,
            "prev": page.previous_page_number() if page.has_previous() else None,
            "results": list(queryset),
        }


class MoviesDetailApi(MoviesApiMixin, DetailView):
    def get_context_data(self, object, **kwargs):
        return object
