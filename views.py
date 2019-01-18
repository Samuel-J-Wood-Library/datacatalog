from django.shortcuts import render

from django.views import generic

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Dataset, DataUseAgreement, DataAccess, Keyword

# Index views
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