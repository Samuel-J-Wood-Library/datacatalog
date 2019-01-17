from django.shortcuts import render

from django.views import generic

from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class IndexView(LoginRequiredMixin, generic.ListView):
    login_url='/login/'
    
    template_name = 'datacatalog/index.html'
    context_object_name = 'data_list'

    def get_queryset(self):
        # get the model that will be primarily indexed"""
        # return model
        return None
        
    def get_context_data(self, **kwargs):
        "get useful model objects here"
        context = super(IndexView, self).get_context_data(**kwargs)
        context.update({
                        # 'object_list'   : object_list,  
        })
        return context