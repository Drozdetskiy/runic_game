from django.contrib import admin

# Register your models here.
from api.models import Link, Game

admin.site.register(Link)
admin.site.register(Game)
