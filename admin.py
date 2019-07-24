from django.contrib import admin

from .models import Dataset, DataUseAgreement, DataAccess, DataProvider, Keyword
from .models import MediaSubType, DataField

# customize the look of the admin site:
admin.site.site_header = 'Data Catalog Management Page'
admin.site.site_title = "DCMP"
admin.site.index_title = "Back end administration"

# create custom actions:
def make_published(modeladmin, request, queryset):
    queryset.update(published=True)
make_published.short_description = "Publish selected items"

def make_unpublished(modeladmin, request, queryset):
    queryset.update(published=False)
make_unpublished.short_description = "Un-publish selected items"

def make_curated(modeladmin, request, queryset):
    queryset.update(curated=True)
make_curated.short_description = "Mark selected items as curated"


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
    actions = [make_published, make_unpublished, make_curated]
    
@admin.register(DataUseAgreement)
class DataUseAgreementAdmin(admin.ModelAdmin):
    list_display = ("duaid", 
                    "title",
                    "start_date",
                    "end_date", 
                    "destruction_required", 
                    "mixing_allowed",
                    "curated",
                    "published",
    )
    list_filter = ('curated', 'published',)
    search_fields = ('title', 'description', 'duaid')
    actions = [make_published, make_unpublished, make_curated]
    
@admin.register(DataAccess)
class DataAccessAdmin(admin.ModelAdmin):
    list_display = ("name", 
                    "dua_required",
                    "prj_desc_required",
                    "curated",
                    "published",
    )
    list_filter = ('curated', 'published',)
    search_fields = ('name',)
    actions = [make_published, make_unpublished, make_curated]
    
@admin.register(DataProvider)
class DataProviderAdmin(admin.ModelAdmin):
    list_display = ("name", 
                    "dept",
                    "curated",
                    "published",
    )
    list_filter = ('curated', 'published','dept')
    search_fields = ('name',)
    actions = [make_published, make_unpublished, make_curated]

@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    list_display = ("keyword", 
                    "curated",
                    "published",
                    "definition",
    )
    list_filter = ('curated', 'published',)
    search_fields = ('keyword', 'definition',)
    actions = [make_published, make_unpublished, make_curated]
    
@admin.register(MediaSubType)
class MediaSubTypeAdmin(admin.ModelAdmin):
    list_display = ("name", 
                    "template",
                    "reference",
                    "obsolete",
    )
    list_filter = ('obsolete', )
    search_fields = ('name', 'template',)

@admin.register(DataField)
class DataFieldAdmin(admin.ModelAdmin):
    list_display = ("name", 
                    "description",
                    "scope",
    )
    search_fields = ('name', 'description',)