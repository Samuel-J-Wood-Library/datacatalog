from django.db import models

from django.urls import reverse

from django.contrib.auth.models import User

from dc_management.models import Person 

class Keyword(models.Model):
    """
    A collection of keywords or tags for mapping to other models (primarily Dataset)
    """
    # date the record was created
    record_creation = models.DateField(auto_now_add=True)
    
    # date the record was most recently modified
    record_update = models.DateField(auto_now=True)
    
    # the user who was signed in at time of record modification
    record_author = models.ForeignKey(User, on_delete=models.CASCADE)
 
    # keyword
    keyword = models.CharField(max_length=64)
    
    # definition / elaboration of keyword
    definition = models.TextField()

    def __str__(self):
        return "Keyword: {}".format(self.keyword,)

    def get_absolute_url(self):
        return reverse('datacatalog:keyword-view', kwargs={'pk': self.pk})

class DataProvider(models.Model):
    """
    This class defines data providers.
    """
    # date the record was created
    record_creation = models.DateField(auto_now_add=True)
    
    # date the record was most recently modified
    record_update = models.DateField(auto_now=True)
    
    # the user who was signed in at time of record modification
    record_author = models.ForeignKey(User, on_delete=models.CASCADE)
 
    # provider organization name
    name = models.CharField(max_length=256)
    
    # provider department
    dept = models.CharField(max_length=128, null=True, blank=True)
    
    # contact phone number
    phone = models.CharField(max_length=32, null=True, blank=True)
    
    # contact email 
    email = models.EmailField(null=True, blank=True)
    
    # provider country of origin
    country = models.CharField(max_length=64, null=True, blank=True)
    
    # provider affiliation: Academic, Hospital, Government, or Private
    ACADEMIC = 'AC'
    MEDICAL = 'ME'
    GOVERNMENT = 'GV'
    PRIVATE = 'PR'
    AFFILIATION_CHOICES = (
            (ACADEMIC, "Academic"),
            (MEDICAL, "Medical provider / Hospital"),
            (GOVERNMENT, "Government"),
            (PRIVATE, "Private institution"),
    )
    affiliation = models.CharField(
                        max_length=2,
                        choices = AFFILIATION_CHOICES,
                        default = GOVERNMENT,
    )

    def __str__(self):
        return "{}".format(self.name,)

    def get_absolute_url(self):
        return reverse('datacatalog:provider-view', kwargs={'pk': self.pk})

class DataAccess(models.Model):
    """
    This class defines the processes and information required in order to gain access 
    to a dataset. These instructions are generic, in as much as they define how anyone
    may gain access, and are not intended to only specify for a particular user/project. 
    """
    # date the record was created
    record_creation = models.DateField(auto_now_add=True)
    
    # date the record was most recently modified
    record_update = models.DateField(auto_now=True)
    
    # the user who was signed in at time of record modification
    record_author = models.ForeignKey(User, on_delete=models.CASCADE)
 
    # general name for identification of access models
    name = models.CharField(max_length=128)
        
    # is a DUA agreement required?
    dua_required = models.BooleanField(null=True, blank=True)
    
    # is a description of the project required?
    prj_desc_required = models.BooleanField(null=True, blank=True)
    
    # is a description of the storage and handling required?
    sys_desc_required = models.BooleanField(null=True, blank=True)
    
    # will other WCM people or departments be required in order to gain access?
    help_required = models.BooleanField(null=True, blank=True)
    
    # Charge for access (in US dollars, approximate, 0 for no cost)
    access_cost = models.IntegerField(null=True, blank=True)

    # publicly available
    public = models.BooleanField(null=True, blank=True)
    
    # typical time period from request to access of data
    time_required = models.DurationField(null=True, blank=True)

    def __str__(self):
        return "Access: {}".format(self.name)
            
    def get_absolute_url(self):
        return reverse('datacatalog:access-view', kwargs={'pk': self.pk})
    
    
class Dataset(models.Model):
    """
    Each instance of Dataset defines a single collection of data. The minimum unit of a
    dataset can be defined as the largest collection that can be uniformly and 
    accurately described using the fields of this model. Ie, if a collection requires
    two or more entries for a specific field to describe the collection, then the 
    collection should be subsetted and each subset defined with its own model instance. 
    
    While there is no minimum criteria for a dataset, it is recommended that each dataset
    be defined as the largest collection possible that can be defined within a single 
    instance.
    """
    # date the record was created
    record_creation = models.DateField(auto_now_add=True)
    
    # date the record was most recently modified
    record_update = models.DateField(auto_now=True)
    
    # the user who was signed in at time of record modification
    record_author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # dataset ID
    ds_id = models.CharField("Dataset ID", max_length=128, unique=True, 
                                null=True, blank=True)
    
    # dataset title/brief descriptor
    title = models.CharField(max_length=256, unique=True)
    
    # description of dataset
    description = models.TextField(null=True, blank=True)
    
    # beginning of temporal coverage (time of earliest data record)
    period_start = models.DateField(null=True, blank=True)
    
    # end of temporal coverage (time of latest data record)
    period_end = models.DateField(null=True, blank=True)
    
    # dataset publisher
    publisher = models.ForeignKey(DataProvider, on_delete=models.CASCADE)
    
    # keywords or topics related to the data
    keywords = models.ManyToManyField(Keyword, blank=True)
    
    # URL of landing page to access data
    landing_url = models.URLField(max_length=256,null=True, blank=True)
    
    # notes or general comments
    comments = models.TextField(null=True, blank=True)
        
    # pointer to the generic instructions required for accessing this data
    access_requirements = models.ForeignKey(DataAccess, 
                                            null=True, 
                                            blank=True,
                                            on_delete=models.CASCADE
                                            )    

    def __str__(self):
        return "Dataset {}: {}".format(self.ds_id, self.title)

    def get_absolute_url(self):
        return reverse('datacatalog:dataset-view', kwargs={'pk': self.pk})

        
class DataUseAgreement(models.Model):
    """
    The Datauseagreement model defines all the governance attributes of a single DUA 
    entered into by a specific set of users and a single data provider.
    The DUA will relate to a specific dataset as defined by a Dataset model instance. 
    """
    # date the record was created
    record_creation = models.DateField(auto_now_add=True)
    
    # date the record was most recently modified
    record_update = models.DateField(auto_now=True)
    
    # the user who was signed in at time of record modification
    record_author = models.ForeignKey(User, on_delete=models.CASCADE)

    # DUA ID
    duaid = models.CharField("DUA ID", max_length=128, unique=True)
    
    # name/title of DUA
    title = models.CharField(max_length=128, unique=True)
    
    # brief description of DUA
    description = models.TextField(null=True, blank=True)

    # dataset publisher
    publisher = models.ForeignKey(DataProvider, on_delete=models.CASCADE)
         
    # provider contact individual
    contact = models.ForeignKey(Person, 
                                related_name='contact_person',
                                on_delete=models.CASCADE
                                )
    
    # principal investigator
    pi = models.ForeignKey(Person, related_name='pi_person', on_delete=models.CASCADE)
    
    # all authorized individuals (may be irrelevant depending on level of auth.)
    users = models.ManyToManyField(Person,)
    
    # separate attestation form required for each user?
    separate_attestation = models.BooleanField(null=True)
    
    # level at which the project applies: User, PI, Project, Institutional
    USER = 'US'
    PI = 'PI'
    PROJECT = 'PJ'
    INSTITUTE = 'IN'
    SCOPE_CHOICES = (
            (USER, "User"),
            (PI, "Principle Investigator"),
            (PROJECT, "Project"),
            (INSTITUTE, "Institution"),
    )
    scope = models.CharField(
                        max_length=2,
                        choices = SCOPE_CHOICES,
                        default = USER,
    )
    
    # date DUA signed
    date_signed = models.DateField(null=True)
    
    # start date of DUA
    start_date = models.DateField(null=True)
    
    # end date of DUA
    end_date = models.DateField(null=True)
    
    # data destruction required at end?
    destruction_required = models.BooleanField(null=True)
    
    # mixing of other datasets with these allowed?
    mixing_allowed = models.BooleanField(null=True)
    
    # storage conditions specified
    storage_requirements = models.TextField(null=True, blank=True)
    
    # access conditions specified
    access_conditions = models.TextField(null=True, blank=True)
    
    # datasets included in governance terms
    datasets = models.ManyToManyField(Dataset,)

    # pointer to the generic instructions required for accessing this data
    access_requirements = models.ForeignKey(DataAccess, 
                                            null=True, 
                                            on_delete=models.CASCADE)    
    
    def __str__(self):
        return "DUA {}: {}".format(self.duaid, self.title)

    def get_absolute_url(self):
        return reverse('datacatalog:dua-view', kwargs={'pk': self.pk})
