from django.contrib import admin

from .models import Dataset, DataUseAgreement, DataAccess, DataProvider, Keyword

# customize the look of the admin site:
admin.site.site_header = 'Data Catalog Management Page'
admin.site.site_title = "DCMP"
admin.site.index_title = "Back end administration"

# customize the individual model views:
@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    date_hierarchy = 'period_start'
    list_display = ("title",
                    "period_start",
                    "period_end" ,
                    "landing_url" ,
                    "comments" ,
                    "curated",
                    "published",
                    )
    list_filter = ('curated', 'published',)
    search_fields = ('title', 'description', 'comments')
    
admin.site.register(DataUseAgreement)
admin.site.register(DataAccess)
admin.site.register(DataProvider)
admin.site.register(Keyword)