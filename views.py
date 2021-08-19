import csv
import os

from dal import autocomplete

from django.shortcuts import render

from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.db.models import Q

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required

from django.urls import reverse_lazy, reverse

from .models import Dataset, DataUseAgreement, DataAccess, Keyword, DataProvider
from .models import MediaSubType, DataField, ConfidentialityImpact

from .forms import DatasetForm, DUAForm

####################################
######  AUTOCOMPLETE  VIEWS   ######
####################################

class DatasetAutocomplete(LoginRequiredMixin, autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Dataset.objects.all()

        if self.q:
            qs = qs.filter(
                            Q(ds_id__istartswith=self.q) | 
                            Q(title__istartswith=self.q)
                            )
        return qs

class PublisherAutocomplete(LoginRequiredMixin, autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = DataProvider.objects.all()

        if self.q:
            qs =  qs.filter(name__icontains=self.q)
        return qs

class AccessAutocomplete(LoginRequiredMixin, autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = DataAccess.objects.all()

        if self.q:
            qs =  qs.filter(name__icontains=self.q)
        return qs

class DUAAutocomplete(LoginRequiredMixin, autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = DataUseAgreement.objects.all()

        if self.q:
            qs =  qs.filter(
                            Q(duaid__icontains=self.q) |
                            Q(title__icontains=self.q)
            ) 
        return qs
        
class KeywordAutocomplete(LoginRequiredMixin, autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Keyword.objects.all()

        if self.q:
            qs =  qs.filter(
                            Q(keyword__icontains=self.q) |
                            Q(definition__icontains=self.q)
            ) 
        return qs        

class DataFieldAutocomplete(LoginRequiredMixin, autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = DataField.objects.all()

        if self.q:
            qs =  qs.filter(
                            Q(name__icontains=self.q) |
                            Q(description__icontains=self.q)
            ) 
        return qs        

class MediaSubTypeAutocomplete(LoginRequiredMixin, autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = MediaSubType.objects.all()

        if self.q:
            qs =  qs.filter(
                            Q(name__icontains=self.q) |
                            Q(template__istartswith=self.q)
            ) 
        return qs    

class CILAutocomplete(LoginRequiredMixin, autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = ConfidentialityImpact.objects.all()

        if self.q:
            qs =  qs.filter(
                            Q(impact_level__icontains=self.q) |
                            Q(standard__icontains=self.q) |
                            Q(definition_level__icontains=self.q)
            ) 
        return qs       

###################
### Index views ###
###################

class IndexView(LoginRequiredMixin, generic.ListView):
    login_url='/login/'
    
    template_name = 'datacatalog/index.html'
    context_object_name = 'dataset_list'

    def get_queryset(self):
        ds = Dataset.objects.filter(published=True
                                    ).order_by('-record_update'
                                    )[:5]
        
        return ds
        
    def get_context_data(self, **kwargs):
        ds_count = Dataset.objects.filter(published=True).count()
        pub_count = DataProvider.objects.filter(published=True).count()
        kw_count = Keyword.objects.filter(published=True).count()
        dua_count = DataUseAgreement.objects.filter(published=True).count()
        access_count = DataAccess.objects.filter(published=True).count()
        
        context = super(IndexView, self).get_context_data(**kwargs)
        context.update({
                        'ds_count'    : ds_count, 
                        'pub_count'   : pub_count,
                        'kw_count'    : kw_count,
                        'dua_count'   : dua_count,
                        'access_count': access_count,
        })
        return context

class IndexDatasetView(LoginRequiredMixin, generic.ListView):
    login_url='/login/'
    
    template_name = 'datacatalog/index_datasets.html'
    context_object_name = 'dataset_list'

    def get_queryset(self):
        ds = Dataset.objects.filter(published=True)
        # ds.sort()
        return ds
        
    def get_context_data(self, **kwargs):
        context = super(IndexDatasetView, self).get_context_data(**kwargs)
        context.update({
                        'empty_list'    : [],  
        })
        return context
        
class IndexDUAView(PermissionRequiredMixin, generic.ListView):
    login_url='/login/'
    
    template_name = 'datacatalog/index_duas.html'
    context_object_name = 'dua_list'
    permission_required = 'datacatalog.view_datauseagreement'

    def get_queryset(self):
        duas = DataUseAgreement.objects.filter(published=True)
        return duas
        
    def get_context_data(self, **kwargs):
        context = super(IndexDUAView, self).get_context_data(**kwargs)
        context.update({
                        'empty_list'    : [],  
        })
        return context
        
class IndexKeywordView(LoginRequiredMixin, generic.ListView):
    login_url='/login/'
    
    template_name = 'datacatalog/index_keywords.html'
    context_object_name = 'keyword_list'

    def get_queryset(self):
        kws = Keyword.objects.filter(published=True)
        # kws.sort()
        return kws
        
    def get_context_data(self, **kwargs):
        context = super(IndexKeywordView, self).get_context_data(**kwargs)
        context.update({
                        'empty_list'    : [],  
        })
        return context
        
class IndexDataAccessView(LoginRequiredMixin, generic.ListView):
    login_url='/login/'
    
    template_name = 'datacatalog/index_dataaccess.html'
    context_object_name = 'access_list'

    def get_queryset(self):
        ins = DataAccess.objects.filter(published=True)
        # ins.sort()
        return ins
        
    def get_context_data(self, **kwargs):
        context = super(IndexDataAccessView, self).get_context_data(**kwargs)
        context.update({
                        'empty_list'    : [],  
        })
        return context
        
class IndexDataProviderView(LoginRequiredMixin, generic.ListView):
    login_url='/login/'
    
    template_name = 'datacatalog/index_dataproviders.html'
    context_object_name = 'provider_list'

    def get_queryset(self):
        pvs = DataProvider.objects.filter(published=True)
        
        # only show published providers that themselves have published datasets
        pvs_with_data = []
        for pv in pvs:
            # see if provider has any published datasets which it is related to 
            # either as publisher or as source
            as_source = pv.dataset_source.filter(published=True).count()
            as_publisher = pv.dataset_publisher.filter(published=True).count()

            if as_source > 0 or as_publisher > 0:
                pvs_with_data.append(pv)

        return pvs_with_data
        
    def get_context_data(self, **kwargs):
        context = super(IndexDataProviderView, self).get_context_data(**kwargs)
        context.update({
                        'empty_list'    : [],  
        })
        return context
        
####################
### Detail views ###
####################

class DatasetDetailView(LoginRequiredMixin, generic.DetailView):
    model = Dataset
    template_name = 'datacatalog/detail_dataset.html'
    
    def get_context_data(self, **kwargs):
        published_data = Dataset.objects.filter(published=True)
        published_duas = self.object.datauseagreement_set.filter(published=True)
        
        context = super(DatasetDetailView, self).get_context_data(**kwargs)
        context.update({'published_data'    : published_data, 
                        'published_duas'    : published_duas, 
        })
        return context
        
class DataAccessDetailView(LoginRequiredMixin, generic.DetailView):
    model = DataAccess
    template_name = 'datacatalog/detail_access.html'
    
    def get_context_data(self, **kwargs):
        da_obj = self.object
        published_data = Dataset.objects.filter(published=True, 
                                                access_requirements=da_obj.pk
        )
        context = super(DataAccessDetailView, self).get_context_data(**kwargs)
        context.update({'published_data'    : published_data,  
        })
        return context

class DataUseAgreementDetailView(PermissionRequiredMixin, generic.DetailView):
    model = DataUseAgreement
    template_name = 'datacatalog/detail_dua.html'
    permission_required = 'datacatalog.view_datauseagreement'

    def get_context_data(self, **kwargs):
        dua_obj = self.object
        published_data = dua_obj.datasets.filter(published=True)
        context = super(DataUseAgreementDetailView, self).get_context_data(**kwargs)
        context.update({'published_data'    : published_data,  
        })
        return context
        
class KeywordDetailView(LoginRequiredMixin, generic.DetailView):
    model = Keyword
    template_name = 'datacatalog/detail_keyword.html'
    
    def get_context_data(self, **kwargs):
        kw_obj = self.object
        published_data = kw_obj.dataset_set.filter(published=True)
        context = super(KeywordDetailView, self).get_context_data(**kwargs)
        context.update({'published_data'    : published_data,  
        })
        return context
        
class DataProviderDetailView(LoginRequiredMixin, generic.DetailView):
    model = DataProvider
    template_name = 'datacatalog/detail_dataprovider.html'
    
    def get_context_data(self, **kwargs):
        dp_obj = self.object
        published_data = Dataset.objects.filter(published=True, 
                                                publisher=dp_obj.pk
        )
        context = super(DataProviderDetailView, self).get_context_data(**kwargs)
        context.update({'published_data'    : published_data,  
        })
        return context

class DataFieldDetailView(LoginRequiredMixin, generic.DetailView):
    model = DataField
    template_name = 'datacatalog/detail_datafield.html'
    
    def get_context_data(self, **kwargs):
        df_obj = self.object
        containing_datasets = df_obj.dataset_set.filter(published=True,)
        
        context = super(DataFieldDetailView, self).get_context_data(**kwargs)
        context.update({'containing_datasets'    : containing_datasets,  
        })
        return context

def get_file_response(dd_file, content_type):
    try:
        with open(str(dd_file), 'rb') as fh:
            response = HttpResponse(fh.read(),
                                    content_type="application/vnd.ms-word"
                                    )
            response['Content-Disposition'] = 'inline; filename={}'.format(
                                                        os.path.basename( str(dd_file))
                                                                            )  
            return response
    
    except FileNotFoundError:
        raise Http404()
        
@login_required()
def file_view(request, pk):
    dataset = Dataset.objects.get(pk=pk)
    # check to see if file is associated:
    try:
        dd_file = dataset.data_dictionary.file
        dd_name = dataset.data_dictionary.name
    except (FileNotFoundError, ValueError) as e:
        raise Http404()
    
    dd_filename, dd_extension = os.path.splitext(dd_file)
        
    if dd_extension == "pdf":
        try:
            return FileResponse(dd_file, content_type='application/pdf')
        except FileNotFoundError:
            raise Http404()
    elif dd_extension == "csv":
        try:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

            writer = csv.writer(response)
            with open(str(dd_file), 'rb') as fh:
                for line in fh:
                    writer.writerow(line.split(','))
            return response
        except (FileNotFoundError, ValueError) as e:
            raise Http404()
            
    elif dd_extension == "docx":
        get_file_response(dd_file, content_type="application/vnd.ms-word")
    elif dd_extension == "xlsx":
        get_file_response(dd_file, content_type="application/vnd.ms-excel")
    else:
        raise Http404()

####################
### Create views ###
####################

class DatasetCreateView(LoginRequiredMixin, CreateView):
    model = Dataset
    form_class = DatasetForm
    template_name = "datacatalog/basic_crispy_form.html"
    # default success_url should be to the object page defined in model.
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        # update who last edited record
        self.object.record_author = self.request.user

        self.object.save()
        return super(DatasetCreateView, self).form_valid(form)

class DataProviderCreateView(PermissionRequiredMixin, CreateView):
    model = DataProvider
    fields = [  'name',
                'dept',
                'phone',
                'email',
                'country',
                'affiliation',
    ]
    template_name = "datacatalog/basic_form.html"
    permission_required = 'datacatalog.add_dataprovider'
    # default success_url should be to the object page defined in model.
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        # update who last edited record
        self.object.record_author = self.request.user
        self.object.save()
        return super(DataProviderCreateView, self).form_valid(form)

class DataAccessCreateView(LoginRequiredMixin, CreateView):
    model = DataAccess
    fields = [  'name',
                'dua_required',
                'prj_desc_required',
                'sys_desc_required',
                'help_required',
                'access_cost',
                'public',
                'time_required',
    ]
    template_name = "datacatalog/basic_form.html"
    # default success_url should be to the object page defined in model.
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        # update who last edited record
        self.object.record_author = self.request.user
        self.object.save()
        return super(DataAccessCreateView, self).form_valid(form)

class DataUseAgreementCreateView(LoginRequiredMixin, CreateView):
    model = DataUseAgreement
    form_class = DUAForm
    template_name = "datacatalog/basic_crispy_form.html"
    # default success_url should be to the object page defined in model.
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        # update who last edited record
        self.object.record_author = self.request.user
        self.object.save()
        return super(DataUseAgreementCreateView, self).form_valid(form)

class KeywordCreateView(LoginRequiredMixin, CreateView):
    model = Keyword
    fields = ['keyword', 'definition', ]
    template_name = "datacatalog/basic_form.html"
    # default success_url should be to the object page defined in model.
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        # update who last edited record
        self.object.record_author = self.request.user
        self.object.save()
        return super(KeywordCreateView, self).form_valid(form)

class DataFieldCreateView(LoginRequiredMixin, CreateView):
    model = DataField
    fields = ['name', 'description','scope' ]
    template_name = "datacatalog/basic_form.html"
    # default success_url should be to the object page defined in model.
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        # update who last edited record
        self.object.record_author = self.request.user
        self.object.save()
        return super(DataFieldCreateView, self).form_valid(form)
        
####################
### Update views ###
####################

class DatasetUpdateView(PermissionRequiredMixin, UpdateView):
    model = Dataset
    form_class = DatasetForm
    template_name = "datacatalog/basic_crispy_form.html"
    permission_required = 'datacatalog.change_dataset'

class DataAccessUpdateView(PermissionRequiredMixin, UpdateView):
    model = DataAccess
    template_name = "datacatalog/basic_form.html"
    fields = [  'name',
                'dua_required',
                'prj_desc_required',
                'sys_desc_required',
                'help_required',
                'access_cost',
                'public',
                'time_required',
    ]
    permission_required = 'datacatalog.change_dataaccess'

class DataProviderUpdateView(PermissionRequiredMixin, UpdateView):
    model = DataProvider
    template_name = "datacatalog/basic_form.html"
    fields = [  'name',
                'dept',
                'phone',
                'email',
                'country',
                'affiliation',
    ]
    permission_required = 'datacatalog.change_dataprovider'
  
class DataUseAgreementUpdateView(PermissionRequiredMixin, UpdateView):
    model = DataUseAgreement
    form_class = DUAForm
    template_name = "datacatalog/basic_crispy_form.html"
    permission_required = 'datacatalog.change_datauseagreement'
    
class KeywordUpdateView(PermissionRequiredMixin, UpdateView):
    model = Keyword
    template_name = "datacatalog/basic_form.html"
    fields = ['keyword', 'definition', ]               
    permission_required = 'datacatalog.change_keyword'
 
 
##############################
######  SEARCH  VIEWS   ######
##############################

class FullSearch(LoginRequiredMixin, generic.TemplateView):
    template_name = 'datacatalog/search_results.html'
    def post(self, request, *args, **kwargs):
        st = request.POST['srch_term']
        qs_ds = Dataset.objects.all()
        qs_ds =  qs_ds.filter(Q(ds_id__icontains=st) | 
                                Q(title__icontains=st) | 
                                Q(description__icontains=st) |
                                Q(comments__icontains=st)
                     ).filter(published=True
        )
        qs_dua = DataUseAgreement.objects.all()
        qs_dua = qs_dua.filter( Q(duaid__icontains=st) |
                                Q(title__icontains=st) |
                                Q(description__icontains=st) 
                      ).filter(published=True
        )
        qs_kw = Keyword.objects.all()
        qs_kw = qs_kw.filter( Q(keyword__icontains=st) |
                              Q(definition__icontains=st)  
        )
        qs_df = DataField.objects.all()
        qs_df = qs_df.filter( Q(name__icontains=st) |
                              Q(description__icontains=st)
        )
        context = { "search_str" : st,
                    "qs_ds": qs_ds,
                    "qs_dua": qs_dua,
                    "qs_kw": qs_kw,
                    "qs_df": qs_df,
        }
        return render(request, self.template_name, context)
        
############################
### Error handling views ###
############################
    
def handler403(request, exception, template_name="403.html"):
    """
    Error 403 = Forbidden 
    
    """
    response = render(request, "403.html")
    response.status_code = 403
    return response
    
def handler404(request, exception, template_name="404.html"):
    """
    Error 404 = Not found 
    
    """
    response = render(request, "404.html")
    response.status_code = 404
    return response
        