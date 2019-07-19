from dal import autocomplete

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Fieldset

from django import forms

from django.utils.translation import gettext_lazy as _

from persons.models import Person
from .models import Dataset

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
                        css_class='col-xs-3',
                    ),
                    Div('period_end',
                        css_class='col-xs-3',
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
                    Fieldset('<div class="alert alert-info">Dataset Details</div>',
                            div_name,
                            'description',
                            'landing_url',
                            'publisher',
                            'keywords',
                            'expert',
                            style="font-weight: bold;",
                    ),
                    Fieldset('<div class="alert alert-info">Governance Details</div>',
                            div_dates,
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
                    'period_start', 
                    'period_end',
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
                    'expert' : autocomplete.ModelSelect2(
                                        url='persons:autocomplete-person'
                                        ),
                    'keywords' : autocomplete.ModelSelect2Multiple(
                                        url='datacatalog:autocomplete-keyword'
                                        ),  
                    'access_requirements' : autocomplete.ModelSelect2(
                                        url='datacatalog:autocomplete-access'
                                        ),                   
                    }
