from dal import autocomplete

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Fieldset, HTML

from django import forms

from django.utils.translation import gettext_lazy as _

from persons.models import Person
from .models import Dataset, MediaSubType, DataField, DataUseAgreement

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

class DatasetForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DatasetForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'datasetForm'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))
        self.helper.layout = Layout(
                    Fieldset('<div class="alert alert-info">Dataset Detail Form</div>',
                            div_name,
                            'description',
                            div_datafields,
                            'keywords',
                            style="font-weight: bold;",
                    ),
                    Fieldset('<div class="alert alert-info">Data Details</div>',
                            'data_source',
                            'media_subtype',
                            div_dates,
                            style="font-weight: bold;",
                    ),
                    Fieldset('<div class="alert alert-info">Access Details</div>',
                            'landing_url',
                            div_access,
                            'expert',
                            style="font-weight: bold;"
                    ), 
                    Fieldset('<div class="alert alert-info">Comments</div>',
                            'comments',
                            style="font-weight: bold;"
                    ),        
        )
    
    class Meta:
        model = Dataset
        fields = [  'ds_id',
                    'title',
                    'description',
                    'media_subtype',
                    'data_fields',
                    'publication_date', 
                    'period_start', 
                    'period_end',
                    'data_source',
                    'publisher', 
                    'keywords',
                    'landing_url', 
                    'comments', 
                    'access_requirements',
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
                    'access_requirements' : autocomplete.ModelSelect2(
                                        url='datacatalog:autocomplete-access'
                                        ),   
                    'data_fields' : autocomplete.ModelSelect2Multiple(
                                        url='datacatalog:autocomplete-datafield'
                                        ),  
                    'media_subtype' : autocomplete.ModelSelect2Multiple(
                                        url='datacatalog:autocomplete-mediatype'
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
                            'access_requirements',
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
                    'access_requirements',
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
                    'access_requirements' : autocomplete.ModelSelect2(
                                        url='datacatalog:autocomplete-access'
                                        ),   
                    'datasets' : autocomplete.ModelSelect2Multiple(
                                        url='datacatalog:autocomplete-dataset'
                                        ),                                      
                    }
