from django.shortcuts import render

from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView

from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse_lazy, reverse

from .models import Dataset, DataUseAgreement, DataAccess, Keyword, DataProvider

###################
### Index views ###
###################

class IndexDatasetView(LoginRequiredMixin, generic.ListView):
    login_url='/login/'
    
    template_name = 'datacatalog/index_datasets.html'
    context_object_name = 'dataset_list'

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
        
class IndexDUAView(LoginRequiredMixin, generic.ListView):
    login_url='/login/'
    
    template_name = 'datacatalog/index_duas.html'
    context_object_name = 'dua_list'

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
        
class IndexKeywordView(LoginRequiredMixin, generic.ListView):
    login_url='/login/'
    
    template_name = 'datacatalog/index_keywords.html'
    context_object_name = 'keyword_list'

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
        
class IndexDataAccessView(LoginRequiredMixin, generic.ListView):
    login_url='/login/'
    
    template_name = 'datacatalog/index_dataaccess.html'
    context_object_name = 'instructions_list'

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
        
class IndexDataProviderView(LoginRequiredMixin, generic.ListView):
    login_url='/login/'
    
    template_name = 'datacatalog/index_dataproviders.html'
    context_object_name = 'provider_list'

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

class DatasetDetailView(LoginRequiredMixin, generic.DetailView):
    model = Dataset
    template_name = 'dc_management/detail_dataset.html'

class DataAccessDetailView(LoginRequiredMixin, generic.DetailView):
    model = DataAccess
    template_name = 'dc_management/detail_access.html'

class DataUseAgreementDetailView(LoginRequiredMixin, generic.DetailView):
    model = DataUseAgreement
    template_name = 'dc_management/detail_dua.html'

class KeywordDetailView(LoginRequiredMixin, generic.DetailView):
    model = Keyword
    template_name = 'dc_management/detail_keyword.html'

class DataProviderDetailView(LoginRequiredMixin, generic.DetailView):
    model = DataProvider
    template_name = 'dc_management/detail_provider.html'

###############################
### Create and Update views ###
###############################

class DatasetCreateView(LoginRequiredMixin, CreateView):
    model = Dataset
    fields = [  'ds_id',
                'title',
                'description',
                'period_start',
                'period_end',
                'keywords',
                'landing_url',
                'comments',
                'access_requirements',
    ]
    template_name = "datacatalog/basic_crispy_form.html"
    # default success_url should be to the object page defined in model.
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return super(DatasetCreateView, self).form_valid(form)

class DataProviderCreateView(LoginRequiredMixin, CreateView):
    model = DataProvider
    fields = [  'name',
                'dept',
                'phone',
                'email',
                'country',
                'affiliation',
    ]
    template_name = "datacatalog/basic_crispy_form.html"
    # default success_url should be to the object page defined in model.
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
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
    template_name = "datacatalog/basic_crispy_form.html"
    # default success_url should be to the object page defined in model.
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return super(DataAccessCreateView, self).form_valid(form)

class DataUseAgreementCreateView(LoginRequiredMixin, CreateView):
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
    template_name = "datacatalog/basic_crispy_form.html"
    # default success_url should be to the object page defined in model.
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return super(DataUseAgreementCreateView, self).form_valid(form)

class KeywordCreateView(LoginRequiredMixin, CreateView):
    model = Keyword
    fields = ['keyword', 'definition', ]
    template_name = "datacatalog/basic_crispy_form.html"
    # default success_url should be to the object page defined in model.
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return super(KeywordCreateView, self).form_valid(form)

class DatasetUpdateView(LoginRequiredMixin, UpdateView):
    model = Dataset
    fields = [  'ds_id',
                'title',
                'description',
                'period_start',
                'period_end',
                'keywords',
                'landing_url',
                'comments',
                'access_requirements',
    ]

class DataAccessUpdateView(LoginRequiredMixin, UpdateView):
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

class DataProviderUpdateView(LoginRequiredMixin, UpdateView):
    model = DataProvider
    fields = [  'name',
                'dept',
                'phone',
                'email',
                'country',
                'affiliation',
    ]
  
class DataUseAgreementUpdateView(LoginRequiredMixin, UpdateView):
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
    
class KeywordUpdateView(LoginRequiredMixin, UpdateView):
    model = Keyword
    fields = ['keyword', 'definition', ]               
 
 
##############################
######  SEARCH  VIEWS   ######
##############################

class FullSearch(LoginRequiredMixin, generic.TemplateView):
    template_name = 'dc_management/search_results.html'
    def post(self, request, *args, **kwargs):
        st = request.POST['srch_term']
        qs_prj = Project.objects.all()
        qs_prj =  qs_prj.filter(Q(dc_prj_id__icontains=st) | 
                                Q(title__icontains=st) | 
                                Q(nickname__icontains=st) |
                                Q(comments__icontains=st)
        )
        qs_usr = Person.objects.all()
        qs_usr = qs_usr.filter( Q(first_name__icontains=st) |
                                Q(last_name__icontains=st) |
                                Q(cwid__icontains=st) |
                                Q(comments__icontains=st)
        )
        qs_gov = Governance_Doc.objects.all()
        qs_gov = qs_gov.filter( Q(doc_id__icontains=st) |
                                Q(governance_type=st) |
                                Q(comments__icontains=st)
        )
        context = { "search_str" : st,
                    "qs_prj": qs_prj,
                    "qs_usr": qs_usr,
                    "qs_gov": qs_gov,
        }
        return render(request, self.template_name, context)
        
    
