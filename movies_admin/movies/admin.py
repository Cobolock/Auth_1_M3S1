from django.contrib import admin
from .models import Genre, Filmwork, GenreFilmwork, Person, PersonFilmwork
from users.models import (
    Profile, UserPermission,
    UserRole, FilmworkPermission,
    UserRolePermissions
)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name", "description", "id")


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("full_name",)
    search_fields = ("full_name", "id")

admin.site.register(Profile)


class UserRolePermissionsInline(admin.TabularInline):
    model = UserRolePermissions
    extra = 0


class UserPermissionInline(admin.TabularInline):
    model = UserPermission
    extra = 0


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork
    extra = 0


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork
    autocomplete_fields = ("person",)
    extra = 0


class FilmworkPermissionInline(admin.TabularInline):
    model = FilmworkPermission
    autocomplete_fields = ("film_work",)
    extra = 0


@admin.register(UserPermission)
class UserPermissionAdmin(admin.ModelAdmin):
    inlines = [FilmworkPermissionInline]


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = [
        GenreFilmworkInline,
        PersonFilmworkInline,
        FilmworkPermissionInline
    ]
    list_display = ("title", "type", "creation_date", "rating")
    list_filter = ("type",)
    search_fields = ("title", "description", "id")


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    inlines = [UserRolePermissionsInline]
