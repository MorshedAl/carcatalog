from django.contrib import admin

from core.models import Car



class CarAdmin(admin.ModelAdmin):
    list_display = ('id','title')

    prepopulated_fields = {
        'slug':('title',)
    }


admin.site.register(Car, CarAdmin)
