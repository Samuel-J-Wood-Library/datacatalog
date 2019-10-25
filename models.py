import datetime

from django.db import models

from django.urls import reverse

from django.contrib.auth.models import User

from persons.models import Person, Department, Organization, Role 

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

    # this is set to true after being checked by the Data Catalog curation team
    curated = models.BooleanField(null=True, blank=True)

    # field to designate whether data should be published
    published = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return "{}".format(self.keyword,)

    def get_absolute_url(self):
        return reverse('datacatalog:keyword-view', kwargs={'pk': self.pk})

class MediaSubType(models.Model):
    """
    This model holds values from www.iana.org media types (formally MIME types).
    """
    # description of the subtype
    name = models.CharField(max_length=256, 
                                unique=True,
    )
    
    # template indicates the type/subtype id
    template = models.CharField(max_length=256, 
                                unique=True,
                                null=True,
                                blank=True,
    )
    
    # iana reference
    reference = models.CharField(max_length=256, 
                                 null=True,
                                 blank=True,
    )
    
    # indicates now obsolete models
    obsolete = models.BinaryField(null=True, blank=True)
    
    def __str__(self):
        if self.template:
            n = self.template
        else:
            n = self.name
        return "{}".format(n)

class DataField(models.Model):
    # date the record was created
    record_creation = models.DateField(auto_now_add=True)
    
    # date the record was most recently modified
    record_update = models.DateField(auto_now=True)
    
    # the user who was signed in at time of record modification
    record_author = models.ForeignKey(User, on_delete=models.PROTECT)
    
    # field name
    name = models.CharField(max_length=256, 
                                help_text="The name of the field as it appears in schema",
    )
    
    # field description
    description = models.CharField(max_length=256, 
                                    help_text="Description of the field",
    )
    
    # descriptions defining scope of data
    scope = models.CharField(max_length=256, 
                            null=True,
                            blank=True,
                            help_text="Descriptions of the scope of the data (eg. min, max, number of records, number of null values, number of unique values)",
    )                                
    
    def __str__(self):
        if self.scope:
            s = "{}...".format(self.scope[:20])
        else:
            s = "---"
        return "{} ({}...); {}".format(  self.name, 
                                            self.description[:20],
                                            s,
                                            )

    def get_absolute_url(self):
        return reverse('datacatalog:datafield-view', kwargs={'pk': self.pk})
    
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

    # this is set to true after being checked by the Data Catalog curation team
    curated = models.BooleanField(null=True, blank=True)

    # field to designate whether data should be published
    published = models.BooleanField(null=True, blank=True)

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

    # this is set to true after being checked by the Data Catalog curation team
    curated = models.BooleanField(null=True, blank=True)

    # field to designate whether data should be published
    published = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return "{}".format(self.name)
            
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
    
    fields are mapped to BioCaddie DATS standard 2.2, from which the help_text has been
    drawn. 
    
    """
    # date the record was created
    record_creation = models.DateField(auto_now_add=True)
    
    # date the record was most recently modified
    record_update = models.DateField(auto_now=True)
    
    # the user who was signed in at time of record modification
    record_author = models.ForeignKey(User, on_delete=models.PROTECT)
    
    # dataset ID
    # http://schema.org/identifier
    ds_id = models.CharField(   "Dataset ID", 
                                max_length=128, 
                                unique=True, 
                                null=True, 
                                blank=True,
                                help_text="Unique identifer of the data set"
    )
    
    # dataset title/brief descriptor
    title = models.CharField(max_length=256, 
                                unique=True,
                                help_text="The name of the dataset, usually one sentence or short description of the dataset",
    )
    
    # description of dataset
    # https://schema.org/description
    description = models.TextField( null=True, 
                                    blank=True,
                                    help_text="Description of dataset, including purpose, scope, etc",
    )
    
    # a field to explicitly capture the fields present in a data model (if applicable)
    data_fields = models.ManyToManyField(DataField, 
                                         blank=True,
                                         help_text="List of all fields present in any schema",
    )
    
    # beginning of temporal coverage (time of earliest data record)
    # https://schema.org/Date
    period_start = models.DateField(null=True, 
                                    blank=True,
                                    help_text="Date of earliest data record",
    )
    
    # end of temporal coverage (time of latest data record) 
    # https://schema.org/Date
    period_end = models.DateField(  null=True, 
                                    blank=True,
                                    help_text="Date of latest data record"
    )
    
    # date the data set was published
    # https://schema.org/Date
    publication_date = models.DateField(null=True, 
                                        blank=True,
                                        help_text="Publication date of the dataset"
    )
    # dataset publisher 
    # https://schema.org/publisher
    publisher = models.ForeignKey(  DataProvider, 
                                    on_delete=models.PROTECT,
                                    related_name='dataset_publisher',
                                    help_text="Group responsible for publication of the data set",
    )
    
    # dataset source, which can be different to the publisher
    data_source = models.ForeignKey(DataProvider,
                                    null=True,
                                    blank=True, 
                                    on_delete=models.PROTECT,
                                    related_name='dataset_source',
                                    help_text="Group responsible for production of the data",
    )
    
    # keywords or topics related to the data
    # https://schema.org/codeValue
    keywords = models.ManyToManyField(  Keyword, 
                                        blank=True,
                                        help_text="Add keywords related to data set",
    )
    
    # URL of landing page to access data
    landing_url = models.URLField(  max_length=256,
                                    null=True, 
                                    blank=True,
                                    help_text="URL of page that allows access of data"
    )
    
    # notes or general comments
    comments = models.TextField(null=True, blank=True)
        
    # pointer to the generic instructions required for accessing this data
    access_requirements = models.ForeignKey(DataAccess, 
                                            null=True, 
                                            blank=True,
                                            on_delete=models.PROTECT,
                                            )    

    # local contact person who is an expert on this dataset
    expert = models.ForeignKey(Person,
                                null=True,
                                blank=True, 
                                on_delete=models.PROTECT,
                                help_text="A local contact who is an expert on the data"
                                )
    
    # media subtype (according to ontology at www.iana.org)
    media_subtype = models.ManyToManyField( MediaSubType,
                                            blank=True,
                                            help_text="The media types of all files in data set"
                                            
    )
    
    
    # this is set to true after being checked by the Data Catalog curation team
    curated = models.BooleanField(null=True, blank=True)

    # field to designate whether data should be published
    published = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return "{}".format(self.title)

    def get_absolute_url(self):
        return reverse('datacatalog:dataset-view', kwargs={'pk': self.pk})

class GovernanceType(models.Model):
    """
    The GovernanceType model stores and defines all the specific types of governance
    document that can be attributed to a dataset. This allows distinguishing between
    different governance documents that relate to a single dataset or project. For 
    example, Institutional Review Board approval, data publisher DUA, or Data Core
    User Agreement documentation. 
    """
    # date the record was created
    record_creation = models.DateField(auto_now_add=True)
    
    # date the record was most recently modified
    record_update = models.DateField(auto_now=True)
    
    # the user who was signed in at time of record modification
    record_author = models.ForeignKey(User, on_delete=models.CASCADE)

    # name of governance type (eg. "DUA", "WCM IRB", etc)
    name = models.CharField(max_length=128, unique=True)
    
    # brief description of type
    description = models.TextField(null=True, blank=True)

def project_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/prj<id>/<filename>
    return '{0}/{1}/{2}'.format(instance.pi, instance.governance_type.name, filename)
        
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
    
    # governance type
    governance_type = models.ForeignKey(GovernanceType, 
                                        null=True, 
                                        blank=True,
                                        on_delete=models.PROTECT, 
                                        )

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
    
    # specify a document that supersedes this DUA instance
    defers_to_doc = models.ForeignKey('self', 
                                        on_delete=models.PROTECT, 
                                        null=True, 
                                        blank=True,
                                        related_name='overrules')
    
    # specify a document that is superseded by this DUA instance 
    supersedes_doc = models.ForeignKey('self', 
                                        on_delete=models.PROTECT, 
                                        null=True, 
                                        blank=True,
                                        related_name='superseded_by')
        
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

    # description of types of experiments allowed under reuse terms
    reuse_scope = models.TextField(null=True, blank=True)
    
    # pointer to the generic instructions required for accessing this data
    access_requirements = models.ForeignKey(DataAccess, 
                                            null=True, 
                                            blank=True,
                                            on_delete=models.CASCADE)    

    # FileField stores a document for viewing (currently only by privileged users)
    documentation = models.FileField(
                            upload_to=project_directory_path, 
                            null=True,
                            blank=True,
    )

    # this is set to true after being checked by the Data Catalog curation team
    curated = models.BooleanField(null=True, blank=True)
    
    # this is set to true after when ready to be displayed on the website
    published = models.BooleanField(null=True, blank=True)
    
    # this is set to true if metadata is only to be visible to privileged users
    privileged = models.BooleanField(null=True, blank=True)
    
    def __str__(self):
        return "{}: {}".format(self.duaid, self.title)

    def get_absolute_url(self):
        return reverse('datacatalog:dua-view', kwargs={'pk': self.pk})

    def allowed_user_string(self):
        return  ", ".join([u.cwid for u in self.users.all()])

    def attention_required(self):
        """
        This function returns a bootstrap flag to indicate how close to the expiry date
        the DUA is.
        """
        td = self.end_date - datetime.date.today() 
        
        if td.days >  90:
            status = "safe"
        
        # if doc defers to another doc, then we need not pay attention to this one:
        elif self.defers_to_doc:
            status = "safe"
        elif len(DataUseAgreement.objects.filter(supersedes_doc=self)) > 0:
            status = "safe"
        
        # if not deferring, and not exempt:
        elif td.days <= 0:
            status = "danger"
        elif td.days <= 10:
            status = "warning"
        elif td.days <= 90:
            status = "primary"
        else:
            status = "danger"
        return status
    