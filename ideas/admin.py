from django.contrib import admin

from .models import DevTool, Idea, IdeaStar


@admin.register(DevTool)
class DevToolAdmin(admin.ModelAdmin):
    list_display = ("name", "kind", "created_at")
    list_filter = ("kind",)
    search_fields = ("name",)


@admin.register(Idea)
class IdeaAdmin(admin.ModelAdmin):
    list_display = ("title", "devtool", "interest", "created_at")
    list_filter = ("devtool",)
    search_fields = ("title", "content")


@admin.register(IdeaStar)
class IdeaStarAdmin(admin.ModelAdmin):
    list_display = ("user", "idea", "created_at")