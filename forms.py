import re

from dal import autocomplete

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Fieldset, HTML, Field

from django import forms

from .models import Dataset, DataAccess, Project, DataUseAgreement, RetentionRequest

div_datafields = Div(
                    Div('data_fields',
                        css_class='col-10'
                    ),
                    HTML("""
                            <a  href="{% url 'datacatalog:datafield-add' %}"
                                type="button" 
                                class="btn btn-success">
                                    Create new field
                            </a>
                        """
                    ),
                    css_class="row",
)
div_name = Div(
                Div('ds_id',
                    css_class='col-3',
                ),
                Div('title',
                    css_class='col-9',
                ),
                css_class="row"
)
div_dates = Div(
                    Div('period_start',
                        css_class='col-4',
                    ),
                    Div('period_end',
                        css_class='col-4',
                    ),
                    Div('publication_date',
                        css_class='col-4',
                    ),
                    css_class="row"
)


def layout_two_equal(field1, field2):
    form = Div(
                Div(field1,
                    css_class='col-6',
                ),
                Div(field2,
                    css_class='col-6',
                ),
                css_class="row"
            )    
    return form

def layout_three_equal(field1, field2, field3):
    form = Div(
                Div(field1,
                    css_class='col-44',
                ),
                Div(field2,
                    css_class='col-4',
                ),
                Div(field3,
                css_class='col-4',
                ),
                css_class="row"
            )
    return form

class DateInput(forms.DateInput):
    input_type = 'date'

class DatasetForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DatasetForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['cil'].label = "Cofidentiality Impact Level"
        self.fields['data_source'].label = "Data Source / Data Creator"
        self.fields['publisher'].label = "Data Publisher / Data Provider"
        self.helper.form_id = 'datasetForm'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))
        self.helper.layout = Layout(
                    Fieldset('<div class="alert alert-info">Dataset Detail Form (Data Catalog Entry)</div>',
                            div_name,
                            'description',
                            'data_dictionary',
                            'keywords',
                            'public',
                            style="font-weight: normal;",
                    ),
                    Fieldset('<div class="alert alert-info">Data Details</div>',
                            'data_source',
                            'media_subtype',
                            layout_two_equal('cil', 'num_records'),
                            div_dates,
                            style="font-weight: normal;",
                    ),
                    Fieldset('<div class="alert alert-info">Access Details</div>',
                            'landing_url',
                            'publisher',
                            'expert',
                            style="font-weight: normal;"
                    ), 
                    Fieldset('<div class="alert alert-info">Comments</div>',
                            'comments',
                            style="font-weight: normal;"
                    ),        
        )
    
    class Meta:
        model = Dataset
        fields = [  'ds_id',
                    'title',
                    'description',
                    'data_dictionary',
                    'media_subtype',
                    'cil', 
                    'num_records',
                    'data_fields',
                    'publication_date', 
                    'period_start', 
                    'period_end',
                    'data_source',
                    'publisher', 
                    'keywords',
                    'landing_url', 
                    'comments', 
                    'expert',
                    'public',
                ]

        widgets =  {'publisher' : autocomplete.ModelSelect2(
                                        url='datacatalog:autocomplete-publisher'
                                        ),
                    'data_source' : autocomplete.ModelSelect2(
                                        url='datacatalog:autocomplete-publisher'
                                        ),
                    'expert' : autocomplete.ModelSelect2(
                                        url='persons:autocomplete-person'
                                        ),
                    'keywords' : autocomplete.ModelSelect2Multiple(
                                        url='datacatalog:autocomplete-keyword'
                                        ),
                    'data_fields' : autocomplete.ModelSelect2Multiple(
                                        url='datacatalog:autocomplete-datafield'
                                        ),  
                    'media_subtype' : autocomplete.ModelSelect2Multiple(
                                        url='datacatalog:autocomplete-mediatype'
                                        ),  
                    'cil' :  autocomplete.ModelSelect2Multiple(
                                        url='datacatalog:autocomplete-cil'
                                        ),
                    'publication_date': DateInput(),
                    'period_end': DateInput(),
                    'period_start': DateInput(),
                    }

div_choose_add_dset = Div(
                            Div('metadata',
                                css_class='col-10'
                            ),
                            HTML("""<div class="col-2">
                                    <a  href="{% url 'datacatalog:dataset-add' %}"
                                        target="_blank" 
                                        type="button" 
                                        class="btn btn-success">
                                            Create new entry
                                    </a>
                                    </div>
                                """,
                            ),
                            css_class="row",
)

def clean_tooltip(text):
    "remove multiple whitespace and carriage returns introduced by python string format"
    text = re.sub("\s+", " ", text)
    text = re.sub("\n", "", text)
    return text

class DataAccessForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DataAccessForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['name'].label = "Descriptive dataset name"
        self.fields['steward_email'].label = "Contact email"
        multifile_tooltip = """Click and drag files into the field below, or click the 'browse' 
                               button. If you have folders and/or subfolders that need 
                               to be saved, we recommend
                               using the OneDrive or Starfish storage types, or you can
                               first zip all files and folders together, then upload the zipped
                               file."""
        self.fields['multifiles'].label = f"""Directly upload multiple files from a single folder<div 
                                           data-toggle="tooltip" 
                                           data-html="true"
                                           data-trigger="click"
                                           data-placement="left"
                                           data-container="body"
                                           title="{clean_tooltip(multifile_tooltip)}"> 
                                            <img src="/static/img/information.svg" 
                                            height="20" 
                                            width="20">
                                           </div>
                                            """.replace('\n','')
        self.fields['metadata'].label = "Data Catalog record of dataset"
        self.fields['public'].label = "Add public link for data sharing to catalog:"
        self.helper.form_id = 'dataaccessForm'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))
        self.helper.layout = Layout(
            Fieldset('<div class="alert alert-info">Create New Record for Data Access</div>',
                     'name',
                     'project',
                     'storage_type',
                     layout_two_equal('unique_id', 'shareable_link'),
                     'filepaths',
                     'multifiles',
                     style="font-weight: normal;",
                     ),
            Fieldset('<div class="alert alert-info">Discover and Access</div>',
                     div_choose_add_dset,
                     'steward_email',
                     'access_instructions',
                     'public',
                     style="font-weight: normal;",
                     ),
        )

    class Meta:
        model = DataAccess
        fields = ['name',
                  'storage_type',
                  'unique_id',
                  'shareable_link',
                  'filepaths',
                  'multifiles',
                  'metadata',
                  'project',
                  'steward_email',
                  'access_instructions',
                  'public',
                  ]

        widgets = {'metadata': autocomplete.ModelSelect2Multiple(
                                url='datacatalog:autocomplete-dataset'
                                ),
                   'project': autocomplete.ModelSelect2(
                                url='datacatalog:autocomplete-project-byuser'
                                ),
                   'multifiles': forms.ClearableFileInput(attrs={'multiple':True,}),

        }

class ProjectForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.fields['funding_id'].label = "WRG ID"
        self.helper = FormHelper()
        self.helper.form_id = 'projectForm'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))
        self.helper.layout = Layout(
            Fieldset('<div class="alert alert-info">Create New Project</div>',
                     'name',
                     'description',
                     style="font-weight: normal;",
                     ),
            Fieldset('<div class="alert alert-info">Project Details</div>',
                     layout_two_equal('pi', 'other_pis'),
                     'other_editors',
                     layout_two_equal('funding_id', 'completion'),
                     style="font-weight: normal;",
                     ),
        )

    class Meta:
        model = Project
        fields = ['name',
                  'description',
                  'pi',
                  'other_pis',
                  'other_editors',
                  'admin',
                  'funding_id',
                  'completion',
                  ]

        widgets = {'pi': autocomplete.ModelSelect2(
                url='persons:autocomplete-person'
            ),
            'other_pis': autocomplete.ModelSelect2Multiple(
                url='persons:autocomplete-person'
            ),
            'other_editors': autocomplete.ModelSelect2Multiple(
                url='persons:autocomplete-person'
            ),
            'completion': DateInput(),
        }


div_duaname = Div(
                Div('duaid',
                    css_class='col-3',
                ),
                Div('title',
                    css_class='col-9',
                ),
                css_class="row"
)
div_provider_details = Div(
                            Div('publisher',
                                css_class='col-8',
                            ),
                            Div('contact',
                                css_class='col-4',
                            ),
                            css_class="row"
)

class DUAForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DUAForm, self).__init__(*args, **kwargs)
        self.fields['publisher'].label = "DUA publisher"
        self.fields['contact'].label = "DUA contact"
        self.fields['pi'].label = "PI"
        self.fields['separate_attestation'].label = "Individual attestation required"
        self.fields['scope'].label = "DUA authorization level"
        self.helper = FormHelper()
        self.helper.form_id = 'duaForm'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))
        self.helper.layout = Layout(
                    Fieldset('<div class="alert alert-info">Data Use Agreement Details</div>',
                            div_duaname,
                            'documentation',
                            'description',
                            div_provider_details,
                            'datasets',
                            'pi',
                            'users',
                            layout_two_equal('separate_attestation', 'scope'),
                            layout_three_equal('date_signed', 'start_date', 'end_date'),
                            style="font-weight: bold;",
                    ),
                    Fieldset('<div class="alert alert-info">Data handling conditions</div>',
                            layout_two_equal('destruction_required', 'mixing_allowed'),
                            'storage_requirements',
                            'access_conditions', 
                            'reuse_scope',                           
                            style="font-weight: bold;",
                    ),
        )
    
    class Meta:
        model = DataUseAgreement
        fields = [  'duaid',
                    'title',
                    'documentation',
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
                    'reuse_scope',
                ]

        widgets =  {'publisher' : autocomplete.ModelSelect2(
                                        url='datacatalog:autocomplete-publisher'
                                        ),
                    'data_source' : autocomplete.ModelSelect2(
                                        url='datacatalog:autocomplete-publisher'
                                        ),
                    'contact' : autocomplete.ModelSelect2(
                                        url='persons:autocomplete-person'
                                        ),
                    'users' : autocomplete.ModelSelect2Multiple(
                                        url='persons:autocomplete-person'
                                        ),  
                    'pi' : autocomplete.ModelSelect2(
                                        url='persons:autocomplete-person'
                                        ),
                    'datasets' : autocomplete.ModelSelect2Multiple(
                                        url='datacatalog:autocomplete-dataset'
                                        ),
                    'start_date' :  DateInput(),
                    'end_date': DateInput(),
                    'date_signed': DateInput(),
                    }

class RetentionRequestForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RetentionRequestForm, self).__init__(*args, **kwargs)

        if self.instance.milestone_pointer == "Enter reference here":
            print("Statement is TRUE")
            self.instance.milestone_pointer = ""
        kwargs['instance'] = self.instance
        super(RetentionRequestForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_id = 'retentionRequestForm'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit retention request'))
        self.helper.layout = Layout(
            Fieldset('<div class="alert alert-info">Request for Data Retention</div>',
                     'name',
                     layout_two_equal('milestone','project'),
                     layout_two_equal('milestone_pointer', 'milestone_date'),
                     'to_archive',
                     'methodfile',
                     'comments',
                     style="font-weight: normal;",
                     ),
        )

    class Meta:
        model = RetentionRequest
        fields = ['name',
                  'project',
                  'milestone',
                  'milestone_date',
                  'milestone_pointer',
                  'to_archive',
                  'methodfile',
                  'comments',
                  ]

        widgets = {
            'project':autocomplete.ModelSelect2(
                    url='datacatalog:autocomplete-project-byuser'
            ),
            'to_archive': autocomplete.ModelSelect2Multiple(
                    url='datacatalog:autocomplete-access-byproject',
                    forward=['project',],
            ),
            'milestone_date': DateInput(),
        }

# The following forms work together to create the Data Retention Request Wizard
class RetentionWorkflowExistingProjectForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RetentionWorkflowExistingProjectForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'retentionWorkflowExistingProjectForm'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submitexisting', 'Select and continue'))
        self.helper.layout = Layout(
            Fieldset("",
                     'project',
                     style="font-weight: normal;",
                     ),
        )

    class Meta:
        model = RetentionRequest
        fields = [
                  'project',
                  ]

        widgets = {
            'project':autocomplete.ModelSelect2(
                    url='datacatalog:autocomplete-project-byuser'
            ),
        }

class RetentionWorkflowNewProjectForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RetentionWorkflowNewProjectForm, self).__init__(*args, **kwargs)
        self.fields['pi'].label = "PI"
        self.fields['funding_id'].label = "WRG ID"
        self.helper = FormHelper()
        self.helper.form_id = 'retentionWorkflowNewProjectForm'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submitnew', 'Save and continue'))
        self.helper.layout = Layout(
            Fieldset("",
                     'name',
                     'description',
                     style="font-weight: normal;",
                     ),
            Fieldset('<div class="alert alert-info">Project Details</div>',
                     'pi',
                     'other_pis',
                     'other_editors',
                     layout_two_equal('funding_id', 'completion'),
                     style="font-weight: normal;",
                     ),
        )

    class Meta:
        model = Project
        fields = ['name',
                  'description',
                  'pi',
                  'other_pis',
                  'other_editors',
                  'admin',
                  'funding_id',
                  'completion',
                  ]

        widgets = {'pi': autocomplete.ModelSelect2(
                url='persons:autocomplete-person'
            ),
            'other_pis': autocomplete.ModelSelect2Multiple(
                url='persons:autocomplete-person'
            ),
            'other_editors': autocomplete.ModelSelect2Multiple(
                url='persons:autocomplete-person'
            ),
            'completion': DateInput(),
        }

class RetentionInventoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RetentionInventoryForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'retentionInventoryForm'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submitinventory', 'Upload inventory'))
        self.helper.layout = Layout(
            Fieldset("",
                     'inventory',
                     style="font-weight: normal;",
                     ),
        )

    class Meta:
        model = RetentionRequest
        fields = [
                  'inventory',
                  ]

class RetentionWorkflowDataForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RetentionWorkflowDataForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['to_archive'].label = "List of all data locations"
        self.fields['methodfile'].label = '''Methods file (<a href="https://medcornell.sharepoint.com/:x:/s/DataCore/ESDrN8oHNbFAgKAkQ3Ot2KcBfRy1y7B0MCW3on9Ib_P7Yw?e=AU2e1e" target="_blank">download template here</a>)'''

        self.fields['to_archive'].help_text = "Select all data from the project that needs to be archived"
        self.helper.form_id = 'retentionWorkflowDataForm'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submitexisting', 'Continue to summary'))
        self.helper.layout = Layout(
            Fieldset("",
                     'project',
                     'to_archive',
                     'methodfile',
                     style="font-weight: normal;",
                     ),
        )

    class Meta:
        model = RetentionRequest
        fields = [
                  'project',
                  'to_archive',
                  'methodfile',
                  ]

        widgets = {
            'project':forms.HiddenInput(),
            'to_archive': autocomplete.ModelSelect2Multiple(
                    url='datacatalog:autocomplete-access-byproject',
                    forward=['project',],
            ),
        }

class RetentionWorkflowNewDataForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RetentionWorkflowNewDataForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['name'].label = "Descriptive dataset name"
        self.fields['steward_email'].label = "Contact email"
        multifile_tooltip = """Click and drag files into the field below, or click the 'browse' 
                               button. If you have folders and/or subfolders that need 
                               to be saved, we recommend
                               using the OneDrive or Starfish storage types, or you can
                               first zip all files and folders together, then upload the zipped
                               file.""".replace('\n','')
        self.fields['multifiles'].label = f"""Directly upload multiple files from a single folder
                                            <div data-toggle="tooltip" 
                                           data-html="true"
                                           data-trigger="click"
                                           data-placement="left"
                                           data-container="body"
                                           title="{clean_tooltip(multifile_tooltip)}">
                                            <img src="{{% static 'img/information.svg' %}}" height="20" width="20">
                                            </div>
                                            """
        self.fields['metadata'].label = "Data Catalog record of dataset"
        self.fields['public'].label = "Add public link for data sharing to catalog:"
        self.helper.form_id = 'retentionWorkflowNewDataForm'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submitnew', 'Create and add to project'))
        self.helper.layout = Layout(
            Fieldset("",
                     'name',
                     'storage_type',
                     style="font-weight: normal;",
                     ),
            Fieldset('<div class="alert alert-info"><h4>Data location</h4><h6>Enter details in at least one of the following fields:</h6></div>',
                     'multifiles',
                     'unique_id',
                     'shareable_link',
                     'filepaths',
                     style="font-weight: normal;",
                     ),
            Fieldset('<div class="alert alert-info"><h4>Discovery and Access</h4><h6>OPTIONAL. If you would like to make your data findable and accessible to other researchers at WCM through the Data Catalog, fill in the fields below.</h6></div>',
                     div_choose_add_dset,
                     'access_instructions',
                     'steward_email',
                     'public',
                     style="font-weight: normal;",
                     ),
        )

    class Meta:
        model = DataAccess
        fields = ['name',
                  'storage_type',
                  'unique_id',
                  'shareable_link',
                  'multifiles',
                  'filepaths',
                  'metadata',
                  'steward_email',
                  'access_instructions',
                  'public',
                  ]

        widgets = {'metadata': autocomplete.ModelSelect2Multiple(
                                url='datacatalog:autocomplete-dataset'
                                ),
                   'project': autocomplete.ModelSelect2(
                                url='datacatalog:autocomplete-project-byuser'
                                ),
                   'multifiles': forms.ClearableFileInput(attrs={'multiple': True}),
        }

class RetentionWorkflowMilestoneForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RetentionWorkflowMilestoneForm, self).__init__(*args, **kwargs)
        self.fields['milestone'].initial = ""
        self.fields['milestone'].label = "Milestone"
        self.helper = FormHelper()
        self.helper.form_id = 'retentionWorkflowSummaryForm'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Continue to project details'))
        self.helper.layout = Layout(
            Fieldset('',
                     'milestone',
                     layout_two_equal(Field('milestone_pointer', placeholder="enter reference here"), 'milestone_date'),
                     'comments',
                     style="font-weight: normal;",
                     ),
        )

    class Meta:
        model = RetentionRequest
        fields = [
                  'milestone',
                  'milestone_date',
                  'milestone_pointer',
                  'comments',
                  ]

        widgets = {
            'milestone_date': DateInput(),
        }
