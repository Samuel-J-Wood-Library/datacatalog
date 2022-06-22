import os
from datetime import datetime
from mimetypes import guess_type

from dal import autocomplete
from django.contrib import messages
from django.http import HttpResponseRedirect, FileResponse, Http404, HttpResponse

from django.shortcuts import render, get_object_or_404
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from django.views import generic
from django.views.generic.edit import CreateView, UpdateView
from django.db.models import Q

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required

from django.urls import reverse

from .models import Dataset, DataUseAgreement, DataAccess, Keyword, DataProvider
from .models import MediaSubType, DataField, ConfidentialityImpact, Project
from .models import RetentionRequest

from persons.models import Person

from .forms import DatasetForm, DUAForm, ProjectForm, DataAccessForm, RetentionRequestForm
from .forms import RetentionWorkflowExistingProjectForm, RetentionWorkflowNewProjectForm
from .forms import RetentionWorkflowDataForm, RetentionWorkflowNewDataForm, RetentionWorkflowMilestoneForm
from .forms import RetentionInventoryForm

# ################################## #
# #####  AUTOCOMPLETE  VIEWS   ##### #
# ################################## #


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
            qs = qs.filter(name__icontains=self.q)
        return qs


class AccessAutocomplete(LoginRequiredMixin, autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = DataAccess.objects.all()

        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs


class ProjectByUserAutocomplete(LoginRequiredMixin, autocomplete.Select2QuerySetView):
    """
    This autocomplete only offers Projects for which the selector is the record creator,
    the project pi, or the project admin.
    """
    def get_queryset(self):
        #user = self.request.user
        user = Person.objects.get(cwid=self.request.user.username)
        qs = Project.objects.filter(
                            Q(pi=user) |
                            Q(other_pis=user) |
                            Q(other_editors=user)
        ).distinct()

        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs


class AccessByProjectAutocomplete(LoginRequiredMixin, autocomplete.Select2QuerySetView):
    def get_queryset(self):
        project = self.forwarded.get('project', None)
        qs = DataAccess.objects.filter(project=project)

        if self.q:
            qs = qs.filter(
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
            qs = qs.filter(
                            Q(duaid__icontains=self.q) |
                            Q(title__icontains=self.q)
            )
        return qs


class KeywordAutocomplete(LoginRequiredMixin, autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Keyword.objects.all()

        if self.q:
            qs = qs.filter(
                            Q(keyword__icontains=self.q) |
                            Q(definition__icontains=self.q)
            )
        return qs


class DataFieldAutocomplete(LoginRequiredMixin, autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = DataField.objects.all()

        if self.q:
            qs = qs.filter(
                            Q(name__icontains=self.q) |
                            Q(description__icontains=self.q)
            )
        return qs


class MediaSubTypeAutocomplete(LoginRequiredMixin, autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = MediaSubType.objects.all()

        if self.q:
            qs = qs.filter(
                            Q(name__icontains=self.q) |
                            Q(template__istartswith=self.q)
            )
        return qs


class CILAutocomplete(LoginRequiredMixin, autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = ConfidentialityImpact.objects.all()

        if self.q:
            qs = qs.filter(
                            Q(impact_level__icontains=self.q) |
                            Q(standard__icontains=self.q) |
                            Q(definition_level__icontains=self.q)
            )
        return qs

# ################# #
# ## Index views ## #
# ################# #


class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'datacatalog/index.html'
    context_object_name = 'dataset_list'

    def get_queryset(self):
        ds = Dataset.objects.filter(published=True
                                    ).order_by('-record_update'
                                               )[:5]

        return ds

    def get_context_data(self, **kwargs):
        ds_count = Dataset.objects.filter(published=True).count()
        dua_count = DataUseAgreement.objects.filter(published=True).count()
        access_count = DataAccess.objects.filter(published=True).count()
        unlocked_requests = RetentionRequest.objects.exclude(locked=True).count()

        context = super(IndexView, self).get_context_data(**kwargs)
        context.update({'ds_count': ds_count,
                        'dua_count': dua_count,
                        'access_count': access_count,
                        'unlocked_requests': unlocked_requests,
                        })
        return context


class IndexDatasetView(LoginRequiredMixin, generic.ListView):
    template_name = 'datacatalog/index_datasets.html'
    context_object_name = 'dataset_list'

    def get_queryset(self):
        ds = Dataset.objects.filter(published=True)
        # ds.sort()
        return ds

    def get_context_data(self, **kwargs):
        context = super(IndexDatasetView, self).get_context_data(**kwargs)
        context.update({
                        'empty_list': [],
        })
        return context


class IndexDUAView(PermissionRequiredMixin, generic.ListView):
    template_name = 'datacatalog/index_duas.html'
    context_object_name = 'dua_list'
    permission_required = 'datacatalog.view_datauseagreement'

    def get_queryset(self):
        duas = DataUseAgreement.objects.filter(published=True)
        return duas

    def get_context_data(self, **kwargs):
        context = super(IndexDUAView, self).get_context_data(**kwargs)
        context.update({
                        'empty_list': [],
        })
        return context


class IndexKeywordView(LoginRequiredMixin, generic.ListView):
    template_name = 'datacatalog/index_keywords.html'
    context_object_name = 'keyword_list'

    def get_queryset(self):
        kws = Keyword.objects.filter(published=True)
        # kws.sort()
        return kws

    def get_context_data(self, **kwargs):
        context = super(IndexKeywordView, self).get_context_data(**kwargs)
        context.update({
                        'empty_list': [],
        })
        return context

class IndexProjectByUserView(LoginRequiredMixin, generic.ListView):
    template_name = 'datacatalog/index_projects.html'
    context_object_name = 'project_list'

    def get_queryset(self):
        try:
            user = Person.objects.get(cwid=self.request.user.username)
        except Person.DoesNotExist:
            user = -1

        myprojects = Project.objects.filter(
            Q(pi=user) |
            Q(other_pis=user) |
            Q(other_editors=user)
        ).distinct()
        return myprojects.order_by('record_creation',)

    def get_context_data(self, **kwargs):
        try:
            user = Person.objects.get(cwid=self.request.user.username)
        except Person.DoesNotExist:
            user = -1

        mypiprojects = Project.objects.filter(pi=user).distinct().order_by('record_creation',)
        myotherpisprojects = Project.objects.filter(other_pis=user).distinct().order_by('record_creation',)
        myothereditorsprojects = Project.objects.filter(other_editors=user).distinct().order_by('record_creation',)

        retention_requests = RetentionRequest.objects.filter(
            Q(project__pi=user) |
            Q(project__other_pis=user) |
            Q(project__other_editors=user)
        ).distinct()

        context = super(IndexProjectByUserView, self).get_context_data(**kwargs)
        context.update({
            'retention_requests': retention_requests,
            'mypiprojects':mypiprojects,
            'myotherpisprojects':myotherpisprojects,
            'myothereditorsprojects': myothereditorsprojects,
        })
        return context


class IndexDataAccessView(PermissionRequiredMixin, generic.ListView):
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
                        'empty_list': [],
        })
        return context


class IndexDataProviderView(LoginRequiredMixin, generic.ListView):
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
                        'empty_list': [],
        })
        return context


class IndexRetentionRequestView(PermissionRequiredMixin, generic.ListView):
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

# ################## #
# ## Detail views ## #
# ################## #


class ProjectDetailView(LoginRequiredMixin, generic.DetailView):
    model = Project
    template_name = 'datacatalog/detail_project.html'

    def get_context_data(self, **kwargs):
        # check permission to view project details:
        if self.object.viewing_is_permitted(self.request):
            access_permission = True
            metadata = Dataset.objects.filter(dataaccess__project=self.object).distinct()
            project = self.object
            pi = self.object.pi

        else:
            access_permission = False
            metadata = None
            project = self.object.name
            pi = self.object.pi

        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        context.update({'dataset_list': metadata,
                        'access_permission': access_permission,
                        'project': project,
                        'pi': pi,
                        })

        return context


class DatasetDetailView(LoginRequiredMixin, generic.DetailView):
    model = Dataset
    template_name = 'datacatalog/detail_dataset.html'

    def get_context_data(self, **kwargs):
        published_data = Dataset.objects.filter(published=True)
        published_duas = self.object.datauseagreement_set.filter(published=True)

        context = super(DatasetDetailView, self).get_context_data(**kwargs)
        context.update({'published_data': published_data,
                        'published_duas': published_duas,
                        })
        return context


class DataAccessDetailView(LoginRequiredMixin, generic.DetailView):
    model = DataAccess
    template_name = 'datacatalog/detail_access.html'

    def get_context_data(self, **kwargs):
        da_obj = self.object
        published_data = da_obj.metadata
        dua_list = DataUseAgreement.objects.filter(datasets__in=[ma.pk for ma in da_obj.metadata.all()]
                                                   ).distinct()
        context = super(DataAccessDetailView, self).get_context_data(**kwargs)
        context.update({'published_data': published_data,
                        'dua_list': dua_list,
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
        context.update({'published_data': published_data,
                        })
        return context


class KeywordDetailView(LoginRequiredMixin, generic.DetailView):
    model = Keyword
    template_name = 'datacatalog/detail_keyword.html'

    def get_context_data(self, **kwargs):
        kw_obj = self.object
        published_data = kw_obj.dataset_set.filter(published=True)
        context = super(KeywordDetailView, self).get_context_data(**kwargs)
        context.update({'published_data': published_data,
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
        context.update({'published_data': published_data,
                        })
        return context


class DataFieldDetailView(LoginRequiredMixin, generic.DetailView):
    model = DataField
    template_name = 'datacatalog/detail_datafield.html'

    def get_context_data(self, **kwargs):
        df_obj = self.object
        containing_datasets = df_obj.dataset_set.filter(published=True,)

        context = super(DataFieldDetailView, self).get_context_data(**kwargs)
        context.update({'containing_datasets': containing_datasets,
                        })
        return context


class RetentionDetailView(LoginRequiredMixin, generic.DetailView):
    model = RetentionRequest
    template_name = 'datacatalog/detail_retention.html'

    def get_context_data(self, **kwargs):
        if self.object.viewing_is_permitted(self.request):
            retentionpi = self.object.project.pi
            retentionadmin = self.object.project.admin
            retentionobject = self.object
            accessdenied = False
        else:
            retentionobject = None
            accessdenied = True
            retentionpi = None
            retentionadmin = None

        retention_request = self.object

        context = super(RetentionDetailView, self).get_context_data(**kwargs)
        context.update({'retentionrequest': retentionobject,
                        'retentionpi': retentionpi,
                        'retentionadmin': retentionadmin,
                        'accessdenied': accessdenied,
                        'form_inventory': RetentionInventoryForm(instance=retention_request),
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
            retention_request.archived = True
            retention_request.locked = True
            for da in retention_request.to_archive.all():
                da.data_retained = True
                da.save()

            messages.add_message(request, messages.SUCCESS,
                                 f"{retention_request.to_archive.count()} data locations marked as archived, request locked.")

        elif 'submitinventory' in request.POST:
            retention_request = get_object_or_404(RetentionRequest, pk=self.kwargs['pk'])

            rr_form = RetentionInventoryForm(instance=retention_request, data=request.POST, files=request.FILES)
            if rr_form.is_bound and rr_form.is_valid():
                retention_request = rr_form.save()
                messages.add_message(request,
                                     messages.SUCCESS,
                                     f"Data inventory added to {retention_request.name}.")
            else:
                messages.error(request, rr_form.errors)

        # return to detail view
        return HttpResponseRedirect(reverse('datacatalog:retention-view', kwargs={'pk': self.kwargs['pk']}))


def get_file_response(dd_file, content_type):
    try:
        with open(str(dd_file), 'rb') as fh:
            response = HttpResponse(fh.read(),
                                    content_type=content_type,
                                    )
            response['Content-Disposition'] = 'inline; filename={}'.format(
                                                        os.path.basename(str(dd_file))
                                                                            )
            return response

    except FileNotFoundError:
        raise Http404()


def file_view_response(model_file):
    """
    allows viewing or downloading of files
    """
    # check to see if file is associated:
    try:
        doc_file = model_file.file
        doc_name = model_file.name
    except ValueError:
        raise Http404()


    filename, extension_raw = os.path.splitext(doc_name)
    extension = extension_raw.lower()[1:]

    if extension == "pdf":
        try:
            return FileResponse(doc_file, content_type='application/pdf')
        except FileNotFoundError:
            raise Http404()
    elif extension == "docx":
        return get_file_response(doc_file, content_type="application/vnd.ms-word")
    elif extension == "xlsx":
        return get_file_response(doc_file, content_type="application/vnd.ms-excel")
    else:
        mime_type = guess_type(doc_name)
        with open(str(doc_file), 'rb') as fh:
            response = HttpResponse(fh.read(),
                                    content_type=mime_type,
                                    )
            response['Content-Disposition'] = f'attachment; filename={os.path.basename(str(doc_file))}'
            return response


@login_required()
def datadict_view(request, pk):
    model_instance = get_object_or_404(Dataset, pk=pk)
    response = file_view_response(model_file=model_instance.data_dictionary)
    return response


@login_required()
def methodfile_view(request, pk):
    model_instance = get_object_or_404(RetentionRequest, pk=pk)
    response = file_view_response(model_file=model_instance.methodfile)
    return response

@login_required()
def inventoryfile_view(request, pk):
    model_instance = get_object_or_404(RetentionRequest, pk=pk)
    response = file_view_response(model_file=model_instance.inventory)
    return response

@login_required()
def duadoc_view(request, pk):
    model_instance = get_object_or_404(DataUseAgreement, pk=pk)
    response = file_view_response(model_file=model_instance.documentation)
    return response


# ################## #
# ## Create views ## #
# ################## #
def check_or_create_user(user):
    """
    check if logged in user is in the persons database. If they are, return
    the user instance. If not, create a new person in the database, and then
    return the instance.
    """
    # 1st, check the user is in persons database:
    try:
        person = Person.objects.get(cwid=user.username)
    except Person.DoesNotExist:
        # if not in database, create new record
        person = Person(first_name=user.first_name,
                        last_name=user.last_name,
                        cwid=user.username,
                        )
        person.save()
    return person

def check_or_add_to_project(person, project):
    """
    if creator of a new project is not in any of the fields (pi, other pis, other editors),
    then add them to the other editors field.

    person: an instance from the persons.Person class
    project: an instance from the Project class
    """
    # add the record creator to the other_editors field if not already in the project people lists:
    if (person == project.pi or
            project.other_pis.filter(cwid=person.cwid).exists() or
            project.other_editors.filter(cwid=person.cwid).exists()
    ):

        return True
    else:
        project.other_editors.add(person)
        project.save()
        return False


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = "datacatalog/basic_crispy_form.html"

    def form_valid(self, form):
        self.object = form.save(commit=False)

        # update who last edited record
        user = self.request.user
        self.object.record_author = user

        self.object.save()

        # add record creator to other_editors field if not already added.
        # 1st, check the user is in persons database:
        person = check_or_create_user(user)

        # add the record creator to the other_editors field if not already in the project people lists:
        check_result = check_or_add_to_project(person, self.object)

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
        if self.object.public is True:
            self.object.published = True
        else:
            self.object.published = False

        self.object.save()
        return super(DatasetCreateView, self).form_valid(form)


class DataProviderCreateView(PermissionRequiredMixin, CreateView):
    model = DataProvider
    fields = ['name',
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

def save_multifiles(pk, filelist):
    "function to save multiple upload files and update the filepath field"
    storage_list = ""
    for f in filelist:
        print(f"FILE UPLOADED: {f.name}")
        # save file to media/to_archive
        file_path = default_storage.save(f'to_archive/DA{pk}/{f.name}', f)
        storage_list += f"\n{f.name}"
        print(file_path)
    return storage_list.strip()


class DataAccessCreateView(LoginRequiredMixin, CreateView):
    model = DataAccess
    form_class = DataAccessForm
    template_name = "datacatalog/basic_crispy_file_form.html"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        # update who last edited record
        self.object.record_author = self.request.user
        self.object.save()

        pk = self.object.pk

        # identify if multifiles has been populated and save accordingly
        if self.request.FILES:
            storage_list = save_multifiles(pk, self.request.FILES.getlist('multifiles'))
            self.object.fileupload_log = storage_list
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
    template_name = "datacatalog/basic_crispy_file_form.html"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        # update who last edited record
        self.object.record_author = self.request.user
        self.object.save()
        return super(RetentionRequestCreateView, self).form_valid(form)


# ################## #
# ## Update views ## #
# ################## #


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = "datacatalog/basic_crispy_form.html"


class DatasetUpdateView(LoginRequiredMixin, UpdateView):
    model = Dataset
    form_class = DatasetForm
    template_name = "datacatalog/basic_crispy_form.html"


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
    template_name = "datacatalog/basic_crispy_file_form.html"

# ############################# #
# ## RetentionWorkflow views ## #
# ############################# #

class RetentionWorkflowMilestoneView(generic.TemplateView):
    template_name = 'datacatalog/workflow_milestone.html'

    def get_context_data(self, **kwargs):

        context = super(RetentionWorkflowMilestoneView, self).get_context_data(**kwargs)
        context.update({
            'form': RetentionWorkflowMilestoneForm(),
        })
        return context

    def post(self, request, *args, **kwargs):
        # once the submit milestone button is clicked
        # create new retention request
        retention_request_form = RetentionWorkflowMilestoneForm(data=request.POST)
        if retention_request_form.is_bound and retention_request_form.is_valid():
            retention_request = retention_request_form.save(commit=False)
            retention_request.record_author = request.user
            retention_request.name = f"retention request {datetime.now()}"
            retention_request.save()
            messages.add_message(request, messages.SUCCESS,
                                 f"{retention_request.name}  created.")
        else:
            messages.error(request, retention_request_form.errors)

        return HttpResponseRedirect(reverse('datacatalog:wizard-project', kwargs={'pk': retention_request.pk}))

class RetentionWorkflowProjectView(generic.TemplateView):
    template_name = 'datacatalog/workflow_project.html'

    def get_context_data(self, **kwargs):
        retention_request = get_object_or_404(RetentionRequest, pk=self.kwargs['pk'])

        context = super(RetentionWorkflowProjectView, self).get_context_data(**kwargs)
        context.update({
            'retention_request': retention_request,
            'form_existing': RetentionWorkflowExistingProjectForm(instance=retention_request),
            'form_new': RetentionWorkflowNewProjectForm(),
        })
        return context

    def post(self, request, *args, **kwargs):
        # retrieve the primary key of the retention request from url
        rr_pk = self.kwargs['pk']

        # retrieve the RetentionRequest model instance based on pk
        retention_request = get_object_or_404(RetentionRequest, pk=rr_pk)

        # if the submit existing project button is pressed
        # create new retention request
        if 'submitexisting' in request.POST:
            retention_request_form = RetentionWorkflowExistingProjectForm(instance=retention_request, data=request.POST)
            if retention_request_form.is_bound and retention_request_form.is_valid():
                retention_request.save()
                messages.add_message(request, messages.SUCCESS,
                                     f"project added to {retention_request.name}.")
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
                new_project_form.save_m2m()

                # add record creator to other_editors field if not already added.
                person = check_or_create_user(request.user)
                check_result = check_or_add_to_project(person, new_project)

                project_pk = new_project.pk

                # connect  new project to existing retention request
                retention_request.project = new_project
                retention_request.save()

                messages.add_message(request, messages.SUCCESS,
                                     f"Project {new_project.pk} {new_project.name} created and added to request.")

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
            rr_form = RetentionWorkflowDataForm(instance=retention_request, data=request.POST, files=request.FILES)
            if rr_form.is_bound and rr_form.is_valid():
                retention_request = rr_form.save()
                messages.add_message(request,
                                     messages.SUCCESS,
                                     f"Data locations added to {retention_request.name}.")
            else:
                messages.error(request, rr_form.errors)
                return HttpResponseRedirect(reverse('datacatalog:wizard-data', kwargs={'pk': rr_pk}))

            # move to milestone details
            return HttpResponseRedirect(reverse('datacatalog:wizard-summary', kwargs={'pk': rr_pk}))

        # if the submit new data location button is pressed
        # save any updates to the existing data form that were made,
        # create new data access instance, then
        # add to existing retention request instance and return to same page.
        elif 'submitnew' in request.POST:
            # populate Data Access form with supplied details
            new_da_form = RetentionWorkflowNewDataForm(data=request.POST)
            if new_da_form.is_bound and new_da_form.is_valid():
                new_da = new_da_form.save(commit=False)
                new_da.record_author = request.user
                new_da.project = project
                new_da.save()
                da_pk = new_da.pk

                # identify if multifiles has been populated and save accordingly
                if request.FILES:
                    storage_list = save_multifiles(da_pk, request.FILES.getlist('multifiles'))
                    new_da.fileupload_log = storage_list
                    new_da.save()

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
    form_class = RetentionRequestForm
    template_name = "datacatalog/workflow_summary.html"


# ############################ #
# #####  SEARCH  VIEWS   ##### #
# ############################ #


class FullSearch(LoginRequiredMixin, generic.TemplateView):
    template_name = 'datacatalog/search_results.html'

    def post(self, request, *args, **kwargs):
        st = request.POST['srch_term']
        qs_ds = Dataset.objects.all()
        qs_ds = qs_ds.filter(Q(ds_id__icontains=st) |
                             Q(title__icontains=st) |
                             Q(description__icontains=st) |
                             Q(comments__icontains=st)
                             ).filter(published=True
                                      )
        qs_dua = DataUseAgreement.objects.all()
        qs_dua = qs_dua.filter(Q(duaid__icontains=st) |
                               Q(title__icontains=st) |
                               Q(description__icontains=st)
                               ).filter(published=True
                                        )
        qs_kw = Keyword.objects.all()
        qs_kw = qs_kw.filter(Q(keyword__icontains=st) |
                             Q(definition__icontains=st)
                             )
        qs_df = DataField.objects.all()
        qs_df = qs_df.filter(Q(name__icontains=st) |
                             Q(description__icontains=st)
                             )
        context = {"search_str": st,
                   "qs_ds": qs_ds,
                   "qs_dua": qs_dua,
                   "qs_kw": qs_kw,
                   "qs_df": qs_df,
                   }
        return render(request, self.template_name, context)

# ########################## #
# ## Error handling views ## #
# ########################## #


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
