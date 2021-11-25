import csv
import os
from datetime import date
from mimetypes import guess_type

from dal import autocomplete
from django.contrib import messages
from django.http import HttpResponseRedirect, FileResponse, Http404, HttpResponse

from django.shortcuts import render, get_object_or_404

from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.db.models import Q

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required

from django.urls import reverse_lazy, reverse

from .models import Dataset, DataUseAgreement, DataAccess, Keyword, DataProvider
from .models import MediaSubType, DataField, ConfidentialityImpact, Project
from .models import RetentionRequest

from .forms import DatasetForm, DUAForm, ProjectForm, DataAccessForm, RetentionRequestForm
from .forms import RetentionWorkflowExistingProjectForm, RetentionWorkflowNewProjectForm
from .forms import RetentionWorkflowDataForm, RetentionWorkflowNewDataForm, RetentionWorkflowSummaryForm

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


class ProjectByUserAutocomplete(LoginRequiredMixin, autocomplete.Select2QuerySetView):
    """
    This autocomplete only offers Projects for which the selector is the record creator,
    the project pi, or the project admin.
    """
    def get_queryset(self):
        user = self.request.user
        qs = Project.objects.filter(
                            Q(record_author=user) |
                            Q(pi__cwid=user.username) |
                            Q(admin__cwid=user.username)
        )

        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs

class AccessByProjectAutocomplete(LoginRequiredMixin, autocomplete.Select2QuerySetView):
    def get_queryset(self):
        project = self.forwarded.get('project', None)
        qs = DataAccess.objects.filter(project=project)

        if self.q:
            qs =  qs.filter(
                Q(name__icontains=self.q) |
                Q(shareable_link__icontains=self.q) |
                Q(unique_id__icontains=self.q) |
                Q(filepaths__icontains=self.q)
            )
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


class IndexProjectByUserView(LoginRequiredMixin, generic.ListView):
    login_url = '/login/'

    template_name = 'datacatalog/index_projects.html'
    context_object_name = 'project_list'

    def get_queryset(self):
        user = self.request.user
        myprojects = Project.objects.filter(
            Q(record_author=user) |
            Q(pi__cwid=user.username) |
            Q(admin__cwid=user.username)
        ).distinct()
        return myprojects.order_by('record_creation',)

    def get_context_data(self, **kwargs):
        user = self.request.user

        retention_requests = RetentionRequest.objects.filter(
            Q(project__record_author=user) |
            Q(project__pi__cwid=user.username) |
            Q(project__admin__cwid=user.username) |
            Q(record_author=user)
        ).distinct()

        context = super(IndexProjectByUserView, self).get_context_data(**kwargs)
        context.update({
            'retention_requests': retention_requests,
        })
        return context

class IndexDataAccessView(PermissionRequiredMixin, generic.ListView):
    login_url='/login/'
    
    template_name = 'datacatalog/index_dataaccess.html'
    context_object_name = 'access_list'
    permission_required = 'datacatalog.view_dataaccess'

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

class IndexRetentionRequestView(PermissionRequiredMixin, generic.ListView):
    login_url = '/login/'

    template_name = 'datacatalog/index_retentionrequests.html'
    context_object_name = 'retention_requests'
    permission_required = 'datacatalog.view_retentionrequest'

    def get_queryset(self):
        qs = RetentionRequest.objects.order_by('record_update')
        return qs

    def get_context_data(self, **kwargs):
        context = super(IndexRetentionRequestView, self).get_context_data(**kwargs)
        context.update({
            'empty_list': [],
        })
        return context

class IndexActiveRetentionRequestView(PermissionRequiredMixin, generic.ListView):
    login_url = '/login/'

    template_name = 'datacatalog/index_retentionrequests_active.html'
    context_object_name = 'retention_requests'
    permission_required = 'datacatalog.view_retentionrequest'

    def get_queryset(self):
        qs = RetentionRequest.objects.filter(verified="False").order_by('record_update')
        return qs

    def get_context_data(self, **kwargs):
        context = super(IndexActiveRetentionRequestView, self).get_context_data(**kwargs)
        context.update({
            'empty_list': [],
        })
        return context

####################
### Detail views ###
####################

class ProjectDetailView(LoginRequiredMixin, generic.DetailView):
    model = Project
    template_name = 'datacatalog/detail_project.html'

    def get_context_data(self, **kwargs):
        metadata = Dataset.objects.filter(dataaccess__project=self.object).distinct()

        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        context.update({'dataset_list': metadata,
                        })
        return context

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
        published_data = da_obj.metadata
        dua_list = DataUseAgreement.objects.filter(datasets__in=[ ma.pk for ma in da_obj.metadata.all()]
                                          ).distinct()
        context = super(DataAccessDetailView, self).get_context_data(**kwargs)
        context.update({'published_data' : published_data,
                        'dua_list':dua_list,
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

class RetentionDetailView(LoginRequiredMixin, generic.DetailView):
    model = RetentionRequest
    template_name = 'datacatalog/detail_retention.html'

    def get_context_data(self, **kwargs):
        if self.object.viewing_is_permitted:
            retentionpi = self.object.project.pi
            retentionadmin = self.object.project.admin
            retentionobject = self.object
            accessdenied = False
        else:
            retentionobject = None
            accessdenied = True
            retentionpi = None
            retentionadmin = None

        context = super(RetentionDetailView, self).get_context_data(**kwargs)
        context.update({'retentionrequest': retentionobject,
                        'retentionpi': retentionpi,
                        'retentionadmin': retentionadmin,
                        'accessdenied': accessdenied,
                        })
        return context

    def post(self, request, *args, **kwargs):
        """
        this is to handle single button actions available on the details page, to update boolean fields in the model.
        """
        # if the Lock Request button is pressed
        # update model locked field to True
        if 'marklocked' in request.POST:
            retention_request = get_object_or_404(RetentionRequest, pk=self.kwargs['pk'])
            retention_request.locked = True
            retention_request.save()

            messages.add_message(request, messages.SUCCESS,
                                     f"{retention_request.name} locked.")

        # if the Lock Request button is pressed
        # update model locked field to True
        if 'markunlocked' in request.POST:
            retention_request = get_object_or_404(RetentionRequest, pk=self.kwargs['pk'])
            retention_request.locked = False
            retention_request.save()

            messages.add_message(request, messages.SUCCESS,
                                 f"{retention_request.name} unlocked.")

        # if the Mark as verified button is pressed
        # update model locked field to True
        elif 'markverified' in request.POST:
            retention_request = get_object_or_404(RetentionRequest, pk=self.kwargs['pk'])
            retention_request.verified = True
            retention_request.save()

            messages.add_message(request, messages.SUCCESS,
                                 f"{retention_request.name} verified.")

        # if the Mark as archived button is pressed
        # update each data access model data_retained field to True
        elif 'markarchived' in request.POST:
            retention_request = get_object_or_404(RetentionRequest, pk=self.kwargs['pk'])
            for da in retention_request.to_archive.all():
                da.data_retained = True
                da.save()

            messages.add_message(request, messages.SUCCESS,
                                 f"{retention_request.to_archive.count()} data locations marked as archived.")

        # return to detail view
        return HttpResponseRedirect(reverse('datacatalog:retention-view', kwargs={'pk': self.kwargs['pk']}))

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
        
    if dd_extension.lower() == "pdf":
        try:
            return FileResponse(dd_file, content_type='application/pdf')
        except FileNotFoundError:
            raise Http404()

    elif dd_extension.lower() == "csv":
        try:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

            writer = csv.writer(response)
            with open(str(dd_file), 'rb') as fh:
                for line in fh:
                    writer.writerow(line.split(','))
            return response
        except (FileNotFoundError, ValueError):
            raise Http404()
            
    elif dd_extension.lower() == "docx":
        get_file_response(dd_file, content_type="application/vnd.ms-word")
    elif dd_extension.lower() == "xlsx":
        get_file_response(dd_file, content_type="application/vnd.ms-excel")
    else:
        mime_type = guess_type(dd_name)
        with open(str(dd_file), 'r') as fh:
            response = HttpResponse(fh.read(),
                                    content_type=mime_type,
                                    )
            response['Content-Disposition'] = f'attachment; filename={os.path.basename(str(dd_file))}'
            return response

####################
### Create views ###
####################

class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = "datacatalog/basic_crispy_form.html"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        # update who last edited record
        self.object.record_author = self.request.user

        self.object.save()
        return super(ProjectCreateView, self).form_valid(form)

class DatasetCreateView(LoginRequiredMixin, CreateView):
    model = Dataset
    form_class = DatasetForm
    template_name = "datacatalog/basic_crispy_form.html"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        # update who last edited record
        self.object.record_author = self.request.user

        # publish immediately if user checks the public field
        if self.object.public == True:
            self.object.published = True
        else:
            self.object.published = False

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

    def form_valid(self, form):
        self.object = form.save(commit=False)
        # update who last edited record
        self.object.record_author = self.request.user
        self.object.published = True
        self.object.save()
        return super(DataProviderCreateView, self).form_valid(form)

class DataAccessCreateView(LoginRequiredMixin, CreateView):
    model = DataAccess
    form_class = DataAccessForm
    template_name = "datacatalog/basic_crispy_form.html"
    
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

    def form_valid(self, form):
        self.object = form.save(commit=False)
        # update who last edited record
        self.object.record_author = self.request.user
        self.object.published = True
        self.object.save()
        return super(KeywordCreateView, self).form_valid(form)

class DataFieldCreateView(LoginRequiredMixin, CreateView):
    model = DataField
    fields = ['name', 'description','scope' ]
    template_name = "datacatalog/basic_form.html"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        # update who last edited record
        self.object.record_author = self.request.user
        self.object.save()
        return super(DataFieldCreateView, self).form_valid(form)

class RetentionRequestCreateView(LoginRequiredMixin, CreateView):
    model = RetentionRequest
    form_class = RetentionRequestForm
    template_name = "datacatalog/basic_crispy_form.html"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        # update who last edited record
        self.object.record_author = self.request.user
        self.object.save()
        return super(RetentionRequestCreateView, self).form_valid(form)



####################
### Update views ###
####################

class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = "datacatalog/basic_crispy_form.html"

class DatasetUpdateView(PermissionRequiredMixin, UpdateView):
    model = Dataset
    form_class = DatasetForm
    template_name = "datacatalog/basic_crispy_form.html"
    permission_required = 'datacatalog.change_dataset'

class DataAccessUpdateView(LoginRequiredMixin, UpdateView):
    model = DataAccess
    form_class = DataAccessForm
    template_name = "datacatalog/basic_crispy_form.html"


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

class RetentionUpdateView(LoginRequiredMixin, UpdateView):
    model = RetentionRequest
    form_class = RetentionRequestForm
    template_name = "datacatalog/basic_crispy_form.html"

###############################
### RetentionWorkflow views ###
###############################

class RetentionWorkflowProjectView(generic.TemplateView):
    template_name = 'datacatalog/workflow_project.html'

    def get_context_data(self, **kwargs):
        context = super(RetentionWorkflowProjectView, self).get_context_data(**kwargs)
        context.update({
            'form_existing': RetentionWorkflowExistingProjectForm(),
            'form_new': RetentionWorkflowNewProjectForm(),
        })
        return context

    def post(self, request, *args, **kwargs):

        def validate_new_retention_request(retention_request):
            if retention_request.is_bound and retention_request.is_valid():
                retention_request.record_author = request.user
                retention_request.name = f"retention for project {retention_request.project} {date.today()}"
                retention_request.save()
                messages.add_message(request, messages.SUCCESS,
                                     f"{retention_request.pk} {retention_request.name} {retention_request.project} saved")
            else:
                messages.error(request, retention_request.errors)

        # if the submit existing project button is pressed
        # create new retention request
        if 'submitexisting' in request.POST:
            retention_request_form = RetentionWorkflowExistingProjectForm(data=request.POST)
            if retention_request_form.is_bound and retention_request_form.is_valid():
                retention_request=retention_request_form.save(commit=False)
                retention_request.record_author = request.user
                retention_request.name = f"retention for project {retention_request.project} {date.today()}"
                retention_request.save()
                messages.add_message(request, messages.SUCCESS,
                                     f"{retention_request.name}  created.")
            else:
                messages.error(request, retention_request_form.errors)

        # if the submit new project button is pressed
        # create new project instance, then
        # create new retention request instance and append new project to it.
        elif 'submitnew' in request.POST:
            new_project_form = RetentionWorkflowNewProjectForm(data=request.POST)
            if new_project_form.is_bound and new_project_form.is_valid():
                new_project = new_project_form.save(commit=False)
                new_project.record_author = request.user
                new_project.save()
                project_pk = new_project.pk
                messages.add_message(request, messages.SUCCESS,
                                     f"Project {new_project.pk} {new_project.name} created.")

                # create new data retention request, and connect to new project.
                retention_name = f"retention for project {project_pk} {date.today()}"
                retention_request = RetentionRequest(project=new_project,
                                                     record_author=request.user,
                                                     name=retention_name,
                                                     )
                retention_request.save()

                messages.add_message(request, messages.SUCCESS,
                                         f"{retention_request.name} started.")

            else:
                messages.error(request, new_project_form.errors)

        return HttpResponseRedirect(reverse('datacatalog:wizard-data', kwargs={'pk': retention_request.pk}))

class RetentionWorkflowDataView(generic.TemplateView):
    template_name = 'datacatalog/workflow_data.html'

    def get_context_data(self, **kwargs):
        context = super(RetentionWorkflowDataView, self).get_context_data(**kwargs)
        retention_request = get_object_or_404(RetentionRequest, pk=self.kwargs['pk'])

        context.update({
            'retention_request': retention_request,
            'form_existing': RetentionWorkflowDataForm(instance=retention_request),
            'form_new': RetentionWorkflowNewDataForm(),
        })

        return context

    def post(self, request, *args, **kwargs):
        # retrieve the primary key from url
        rr_pk = self.kwargs['pk']

        # retrieve the RetentionRequest model instance based on pk
        retention_request = get_object_or_404(RetentionRequest, pk=rr_pk)
        project = retention_request.project


        # if the add existing data locations button is pressed
        # update existing retention request, and
        # continue to summary page.
        if 'submitexisting' in request.POST:
            # create a PersonForm based on person and form data
            rr_form = RetentionWorkflowDataForm(instance=retention_request, data=request.POST)
            if rr_form.is_bound and rr_form.is_valid():
                retention_request = rr_form.save()
                messages.add_message(request, messages.SUCCESS,
                                     f"Data locations added to {retention_request.name}.")
            else:
                messages.error(request, rr_form.errors)

            # move to update summary
            return HttpResponseRedirect(reverse('datacatalog:wizard-milestone', kwargs={'pk': rr_pk}))

        # if the submit new project button is pressed
        # save any updates to the existing data form that were made,
        # create new data access instance, then
        # add to existing retention request instance and return to same page.
        elif 'submitnew' in request.POST:
            new_da_form = RetentionWorkflowNewDataForm(data=request.POST)
            if new_da_form.is_bound and new_da_form.is_valid():
                new_da = new_da_form.save(commit=False)
                new_da.record_author = request.user
                new_da.project = project
                new_da.save()
                da_pk = new_da.pk

                # update retention request by appending new data access to existing in to_archive
                retention_request.to_archive.add(new_da)

                # add banner message to highlight to user that data location has been created.
                messages.add_message(request, messages.SUCCESS,
                                         f"Data location {new_da.name} appended to request")

                # return to same page to allow additional datasets to be added
                return HttpResponseRedirect(reverse('datacatalog:wizard-data', kwargs={'pk': rr_pk}))

            else:
                messages.error(request, new_da_form.errors)

        # this response is only accessed if there is an error in the form
        return HttpResponseRedirect(reverse('datacatalog:wizard-data', kwargs={'pk': rr_pk}))

class RetentionWorkflowSummaryView(LoginRequiredMixin, UpdateView):
    model = RetentionRequest
    form_class = RetentionWorkflowSummaryForm
    template_name = "datacatalog/workflow_summary.html"
    initial = { 'milestone':"",
                'milestone_pointer':"",
                'milestone_date':"",
                }

    def form_valid(self, form):
        instance = form.save()
        self.success_url = reverse('datacatalog:retention-update', kwargs={'pk': instance.pk})
        return super(RetentionWorkflowSummaryView, self).form_valid(form)


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
        