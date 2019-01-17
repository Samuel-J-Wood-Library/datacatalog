from django.shortcuts import render

# Create your views here.
class IndexView(LoginRequiredMixin, generic.ListView):
    login_url='/login/'
    
    template_name = 'dc_management/index.html'
    context_object_name = 'project_list'

    def get_queryset(self):
        # get the model that will be primarily indexed"""
        # return model
    
    def get_context_data(self, **kwargs):
        # get useful model objects here
        context = super(IndexView, self).get_context_data(**kwargs)
        context.update({
                        # 'object_list'   : object_list,  
        })
        return context