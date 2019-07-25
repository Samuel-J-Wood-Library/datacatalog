from dal import autocomplete

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Fieldset, HTML

from django import forms

from django.utils.translation import gettext_lazy as _

from persons.models import Person
from .models import Dataset, MediaSubType, DataField

div_datafields = Div(
                    Div('data_fields',
                        css_class='col-xs-10'
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
                    css_class='col-xs-3',
                ),
                Div('title',
                    css_class='col-xs-9',
                ),
                css_class="row"
)
div_dates = Div(
                    Div('period_start',
                        css_class='col-xs-4',
                    ),
                    Div('period_end',
                        css_class='col-xs-4',
                    ),
                    Div('publication_date',
                        css_class='col-xs-4',
                    ),
                    css_class="row"
)
div_access = Div(
                    Div('publisher',
                        css_class='col-xs-6',
                    ),
                    Div('access_requirements',
                        css_class='col-xs-6',
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
