from django.conf.urls.static import static
from django.conf import settings
from django.urls import path

from . import views

app_name = 'datacatalog'
urlpatterns = [ 
    # index showing top items and search bar:
    path('', views.IndexView.as_view(), name='index'),
    path('project', views.IndexProjectByUserView.as_view(), name='projects-byuser'),
    path('datasets', views.IndexDatasetView.as_view(), name='datasets'),
    path('duas', views.IndexDUAView.as_view(), name='duas'),
    path('access', views.IndexDataAccessView.as_view(), name='access'),
    path('keywords', views.IndexKeywordView.as_view(), name='keywords'),
    path('providers', views.IndexDataProviderView.as_view(), name='providers'),
    
    # autocomplete functions:
    path('autocomplete-dataset', 
        views.DatasetAutocomplete.as_view(), 
        name='autocomplete-dataset',
        ),
    path('autocomplete-publisher', 
        views.PublisherAutocomplete.as_view(), 
        name='autocomplete-publisher',
        ),
    path('autocomplete-project-byuser',
         views.ProjectByUserAutocomplete.as_view(),
         name='autocomplete-project-byuser',
        ),
    path('autocomplete-access', 
        views.AccessAutocomplete.as_view(),
        name='autocomplete-access',
        ),
    path('autocomplete-access-byproject',
         views.AccessByProjectAutocomplete.as_view(),
         name='autocomplete-access-byproject',
    ),
    path('autocomplete-dua', 
        views.DUAAutocomplete.as_view(),
        name='autocomplete-dua',
        ),
    path('autocomplete-keyword', 
        views.KeywordAutocomplete.as_view(),
        name='autocomplete-keyword',
        ),
    path('autocomplete-datafield', 
        views.DataFieldAutocomplete.as_view(),
        name='autocomplete-datafield',
        ),
    path('autocomplete-mediatype', 
        views.MediaSubTypeAutocomplete.as_view(),
        name='autocomplete-mediatype',
        ),
    path('autocomplete-cil', 
        views.CILAutocomplete.as_view(),
        name='autocomplete-cil',
        ),

    # detail views
    path('project/<int:pk>', views.ProjectDetailView.as_view(), name='project-view'),
    path('datasets/<int:pk>', views.DatasetDetailView.as_view(), name='dataset-view'),
    path('ddictionary/<int:pk>', views.file_view, name='ddict-file'),
    path('access/<int:pk>', views.DataAccessDetailView.as_view(), name='access-view'),
    path('providers/<int:pk>', views.DataProviderDetailView.as_view(),
         name='provider-view'
    ),
    path('duas/<int:pk>', views.DataUseAgreementDetailView.as_view(), name='dua-view'),
    path('keywords/<int:pk>', views.KeywordDetailView.as_view(), name='keyword-view'),
    path('datafield/<int:pk>', 
            views.DataFieldDetailView.as_view(), 
            name='datafield-view'
    ),
    path('retention/<int:pk>', views.RetentionDetailView.as_view(), name='retention-view'),

    # create views
    path('project/add', views.ProjectCreateView.as_view(), name='project-add'),
    path('datasets/add', views.DatasetCreateView.as_view(), name='dataset-add'),
    path('access/add', views.DataAccessCreateView.as_view(), name='access-add'),
    path('providers/add', views.DataProviderCreateView.as_view(),name='provider-add'),
    path('duas/add', views.DataUseAgreementCreateView.as_view(), name='dua-add'),
    path('keywords/add', views.KeywordCreateView.as_view(), name='keyword-add'),
    path('datafield/add', views.DataFieldCreateView.as_view(), name='datafield-add'),
    path('retention/add', views.RetentionRequestCreateView.as_view(), name='retention-add'),

    # update views
    path('project/update/<int:pk>', views.ProjectUpdateView.as_view(),
       name='project-update'
       ),
    path('datasets/update/<int:pk>', views.DatasetUpdateView.as_view(),
         name='dataset-update'
    ),
    path('access/update/<int:pk>', views.DataAccessUpdateView.as_view(), 
         name='access-update'
    ),
    path('providers/update/<int:pk>', views.DataProviderUpdateView.as_view(), 
         name='provider-update'
    ),
    path('duas/update/<int:pk>', views.DataUseAgreementUpdateView.as_view(), 
         name='dua-update'
    ),
    path('keywords/update/<int:pk>', views.KeywordUpdateView.as_view(), 
         name='keyword-update'
    ),
   
    # search view:
    path('search/all', views.FullSearch.as_view(), name="full-search"),
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


