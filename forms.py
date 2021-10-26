from dal import autocomplete

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Fieldset, HTML

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
div_access = Div(
                    Div('publisher',
                        css_class='col-6',
                    ),
                    Div('access_requirements',
                        css_class='col-6',
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
    
class DatasetForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DatasetForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['cil'].label = "Cofidentiality Impact Level"
        self.helper.form_id = 'datasetForm'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))
        self.helper.layout = Layout(
                    Fieldset('<div class="alert alert-info">Dataset Detail Form</div>',
                            div_name,
                            'description',
                            'data_dictionary',
                            'keywords',
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
                    }

div_choose_add_dset = Div(
                            Div('metadata',
                                css_class='col-10'
                            ),
                            HTML("""
                                    <a  href="{% url 'datacatalog:dataset-add' %}"
                                        target="_blank" 
                                        type="button" 
                                        class="btn btn-success">
                                            Create new dataset record
                                    </a>
                                """
                            ),
                            css_class="row",
)

class DataAccessForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DataAccessForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['name'].label = "Short Description"
        self.fields['steward_email'].label = "Contact email"
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
                  'metadata',
                  'project',
                  'steward_email',
                  'access_instructions',
                  'public',
                  ]

        widgets = {'metadata': autocomplete.ModelSelect2(
                                url='datacatalog:autocomplete-dataset'
                                ),
                   'project': autocomplete.ModelSelect2(
                                url='datacatalog:autocomplete-project-byuser'
                                ),
        }

class ProjectForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
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
                     layout_two_equal('pi', 'admin'),
                     layout_two_equal('sponsor', 'funding_id'),
                     'completion',
                     style="font-weight: normal;",
                     ),
        )

    class Meta:
        model = Project
        fields = ['name',
                  'description',
                  'pi',
                  'admin',
                  'sponsor',
                  'funding_id',
                  'completion',
                  ]

        widgets = {'pi': autocomplete.ModelSelect2(
            url='persons:autocomplete-person'
        ),
            'admin': autocomplete.ModelSelect2(
                url='persons:autocomplete-person'
            ),
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
div_dua_dates =  Div(
                    Div('date_signed',
                        css_class='col-4',
                    ),
                    Div('start_date',
                        css_class='col-4',
                    ),
                    Div('end_date',
                        css_class='col-4',
                    ),
                    css_class="row"
)

div_attestation =  Div(
                        Div('separate_attestation',
                            css_class='col-6',
                        ),
                        Div('scope',
                            css_class='col-6',
                        ),
                        css_class="row"
)
div_handling = Div(
                        Div('destruction_required',
                            css_class='col-6',
                        ),
                        Div('mixing_allowed',
                            css_class='col-6',
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
                    Fieldset('<div class="alert alert-info">DUA Form</div>',
                            div_duaname,
                            'description',
                            div_provider_details,
                            'datasets',
                            'pi',
                            'users',
                            div_attestation,
                            div_dua_dates,
                            style="font-weight: bold;",
                    ),
                    Fieldset('<div class="alert alert-info">Data handling conditions</div>',
                            div_handling,
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
                    }

class RetentionRequestForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RetentionRequestForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'retentionRequestForm'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))
        self.helper.layout = Layout(
            Fieldset('<div class="alert alert-info">Request for Data Retention</div>',
                     'name',
                     'project',
                     'milestone',
                     'to_archive',
                     'comments',
                     style="font-weight: normal;",
                     ),
        )

    class Meta:
        model = RetentionRequest
        fields = ['name',
                  'project',
                  'milestone',
                  'to_archive',
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
        }