from django.shortcuts import render

from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.db.models import Q

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from django.urls import reverse_lazy, reverse

from .models import Dataset, DataUseAgreement, DataAccess, Keyword, DataProvider


###################
### Index views ###
###################

class IndexView(PermissionRequiredMixin, generic.ListView):
    login_url='/login/'
    
    template_name = 'datacatalog/index.html'
    context_object_name = 'dataset_list'
    permission_required = 'datacatalog.view_dataset'

    def get_queryset(self):
        ds = Dataset.objects.all()
        # ds.sort()
        return ds
        
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context.update({
                        'empty_list'    : [],  
        })
        return context

class IndexDatasetView(PermissionRequiredMixin, generic.ListView):
    login_url='/login/'
    
    template_name = 'datacatalog/index_datasets.html'
    context_object_name = 'dataset_list'
    permission_required = 'datacatalog.view_dataset'

    def get_queryset(self):
        ds = Dataset.objects.all()
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
        duas = DataUseAgreement.objects.all()
        # duas.sort()
        return duas
        
    def get_context_data(self, **kwargs):
        context = super(IndexDUAView, self).get_context_data(**kwargs)
        context.update({
                        'empty_list'    : [],  
        })
        return context
        
class IndexKeywordView(PermissionRequiredMixin, generic.ListView):
    login_url='/login/'
    
    template_name = 'datacatalog/index_keywords.html'
    context_object_name = 'keyword_list'
    permission_required = 'datacatalog.view_keyword'

    def get_queryset(self):
        kws = Keyword.objects.all()
        # kws.sort()
        return kws
        
    def get_context_data(self, **kwargs):
        context = super(IndexKeywordView, self).get_context_data(**kwargs)
        context.update({
                        'empty_list'    : [],  
        })
        return context
        
class IndexDataAccessView(PermissionRequiredMixin, generic.ListView):
    login_url='/login/'
    
    template_name = 'datacatalog/index_dataaccess.html'
    context_object_name = 'access_list'
    permission_required = 'datacatalog.view_dataaccess'

    def get_queryset(self):
        ins = DataAccess.objects.all()
        # ins.sort()
        return ins
        
    def get_context_data(self, **kwargs):
        context = super(IndexDataAccessView, self).get_context_data(**kwargs)
        context.update({
                        'empty_list'    : [],  
        })
        return context
        
class IndexDataProviderView(PermissionRequiredMixin, generic.ListView):
    login_url='/login/'
    
    template_name = 'datacatalog/index_dataproviders.html'
    context_object_name = 'provider_list'
    permission_required = 'datacatalog.view_dataprovider'

    def get_queryset(self):
        pvs = DataProvider.objects.all()
        # pvs.sort()
        return pvs
        
    def get_context_data(self, **kwargs):
        context = super(IndexDataProviderView, self).get_context_data(**kwargs)
        context.update({
                        'empty_list'    : [],  
        })
        return context
        
####################
### Detail views ###
####################

class DatasetDetailView(PermissionRequiredMixin, generic.DetailView):
    model = Dataset
    template_name = 'datacatalog/detail_dataset.html'
    permission_required = 'datacatalog.view_dataset'
    
class DataAccessDetailView(PermissionRequiredMixin, generic.DetailView):
    model = DataAccess
    template_name = 'datacatalog/detail_access.html'
    permission_required = 'datacatalog.view_dataaccess'

class DataUseAgreementDetailView(PermissionRequiredMixin, generic.DetailView):
    model = DataUseAgreement
    template_name = 'datacatalog/detail_dua.html'
    permission_required = 'datacatalog.view_datauseagreement'

class KeywordDetailView(PermissionRequiredMixin, generic.DetailView):
    model = Keyword
    template_name = 'datacatalog/detail_keyword.html'
    permission_required = 'datacatalog.view_keyword'

class DataProviderDetailView(PermissionRequiredMixin, generic.DetailView):
    model = DataProvider
    template_name = 'datacatalog/detail_dataprovider.html'
    permission_required = 'datacatalog.view_dataprovider'

####################
### Create views ###
####################

class DatasetCreateView(PermissionRequiredMixin, CreateView):
    model = Dataset
    fields = [  'ds_id',
                'title',
                'description',
                'publisher',
                'period_start',
                'period_end',
                'keywords',
                'landing_url',
                'comments',
                'access_requirements',
    ]
    template_name = "datacatalog/basic_form.html"
    permission_required = 'datacatalog.add_dataset'
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

class DataAccessCreateView(PermissionRequiredMixin, CreateView):
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
    permission_required = 'datacatalog.add_dataaccess'
    # default success_url should be to the object page defined in model.
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        # update who last edited record
        self.object.record_author = self.request.user
        self.object.save()
        return super(DataAccessCreateView, self).form_valid(form)

class DataUseAgreementCreateView(PermissionRequiredMixin, CreateView):
    model = DataUseAgreement
    fields = [  'duaid',
                'title',
                'description',
                'publisher',
                'contact',
                'pi',
                'users',
                'separate_attestation',
                'scope',
                'date_signed',
                'start_date',
                'end_date',
                'destruction_required',
                'mixing_allowed',
                'storage_requirements',
                'access_conditions',
                'datasets',
                'access_requirements',
    ]
    template_name = "datacatalog/basic_form.html"
    permission_required = 'datacatalog.add_datauseagreement'
    # default success_url should be to the object page defined in model.
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        # update who last edited record
        self.object.record_author = self.request.user
        self.object.save()
        return super(DataUseAgreementCreateView, self).form_valid(form)

class KeywordCreateView(PermissionRequiredMixin, CreateView):
    model = Keyword
    fields = ['keyword', 'definition', ]
    template_name = "datacatalog/basic_form.html"
    permission_required = 'datacatalog.add_keyword'
    # default success_url should be to the object page defined in model.
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        # update who last edited record
        self.object.record_author = self.request.user
        self.object.save()
        return super(KeywordCreateView, self).form_valid(form)

####################
### Update views ###
####################

class DatasetUpdateView(PermissionRequiredMixin, UpdateView):
    model = Dataset
    template_name = "datacatalog/basic_form.html"
    fields = [  'ds_id',
                'title',
                'description',
                'publisher',
                'period_start',
                'period_end',
                'keywords',
                'landing_url',
                'comments',
                'access_requirements',
    ]
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
    template_name = "datacatalog/basic_form.html"
    fields = [  'duaid',
                'title',
                'description',
                'publisher',
                'contact',
                'pi',
                'users',
                'separate_attestation',
                'scope',
                'date_signed',
                'start_date',
                'end_date',
                'destruction_required',
                'mixing_allowed',
                'storage_requirements',
                'access_conditions',
                'datasets',
                'access_requirements',
                'reuse_scope',
    ]
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
        )
        qs_dua = DataUseAgreement.objects.all()
        qs_dua = qs_dua.filter( Q(duaid__icontains=st) |
                                Q(title__icontains=st) |
                                Q(description__icontains=st) 
        )
        qs_kw = Keyword.objects.all()
        qs_kw = qs_kw.filter( Q(keyword__icontains=st) |
                              Q(definition__icontains=st)  
        )
        context = { "search_str" : st,
                    "qs_ds": qs_ds,
                    "qs_dua": qs_dua,
                    "qs_kw": qs_kw,
        }
        return render(request, self.template_name, context)
        
############################
### Error handling views ###
############################
    
def handler403(request, exception, template_name="403.html"):
    """
    Error 403 = Forbidden 
    
    """
    response = render_to_response("403.html")
    response.status_code = 403
    return response
    
def handler404(request, exception, template_name="404.html"):
    """
    Error 404 = Not found 
    
    """
    response = render_to_response("404.html")
    response.status_code = 404
    return response
        