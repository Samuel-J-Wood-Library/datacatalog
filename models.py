from django.db import models

from django.contrib.auth.models import User

from dc_management import Individual 

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

class DataProvider(models.Model):
    """
    This class defines data providers.
    """
    # provider organization name
    name = models.CharField(max_length=256)
    
    # provider department
    name = models.CharField(max_length=128)
    
    # contact phone number
    name = models.CharField(max_length=32)
    
    # contact email 
    email = models.EmailField()
    
    # provider country of origin
    country = models.CharField(max_length=64)
    
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
    ds_id = models.CharField("Dataset ID", max_length=128, unique=True, null=True)
    
    # dataset title/brief descriptor
    title = models.CharField(max_length=256, unique=True)
    
    # description of dataset
    description = models.TextField(null=True, blank=True)
    
    # beginning of temporal coverage (time of earliest data record)
    period_start = models.DateField(null=True)
    
    # end of temporal coverage (time of latest data record)
    period_end = models.DateField(null=True)
    
    # keywords or topics related to the data
    keywords = models.ManyToManyField(Keyword,null=True)
    
    # URL of landing page to access data
    landing_url = models.URLField(max_length=256,null=True)
    
    # typical time period from request to access of data
    request_time = models.DurationField(null=True)
    
    # publicly available
    public = models.BooleanField(null=True)
    
    # DUA required for access
    dua_required = models.BooleanField(null=True)
    
    # Charge for access (in US dollars, approximate, 0 for no cost)
    access_cost = models.IntegerField(null=True)
    
    # notes or general comments
    comments = models.TextField(null=True)
        
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
    
    # data provider / publisher
    publisher = models.ForeignKeyField(DataProvider)
    
    # provider contact individual
    contact = models.ForeignKeyField(Individual, related_name='contact_individual')
    
    # principal investigator
    contact = models.ForeignKeyField(Individual, related_name='pi_individual')
    
    # all authorized individuals (may be irrelevant depending on level of auth.)
    contact = models.ManyToManyField(Individual,)
    
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
    
    def __str__(self):
        return "DUA {}: {}".format(self.duaid, self.title)

