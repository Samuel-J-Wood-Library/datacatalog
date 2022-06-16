import datetime
from datetime import date

from django.db import models

from django.urls import reverse

from django.contrib.auth.models import User

from persons.models import Person, Department, Organization, Role 


def dictionary_directory_path(instance, filename):
    """
    This function specifies the filepath to save uploaded files to.
    """
    # file will be uploaded to MEDIA_ROOT/dataset<id>/<filename>
    return 'dset{0}/{1}'.format(instance.pk, filename)


def project_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/pi<id>/gov_type/<filename>
    return 'duas/{0}/{1}/{2}'.format(instance.pi, instance.governance_type.name, filename)

def multifile_directory_path(instance, filename):
    """
    This function specifies the filepath to save uploaded files for archiving.
    """
    # file will be uploaded to MEDIA_ROOT/to_archive/<pk>/<filename>
    return f'to_archive/DA{instance.pk}/{filename}'

def method_directory_path(instance, filename):
    """
    This function specifies the filepath to save uploaded data retention method files to.
    """
    # file will be uploaded to MEDIA_ROOT/methods/RR<pk>/<filename>
    return f'methods/RR{instance.pk}/{filename}'

def inventory_directory_path(instance, filename):
    """
    This function specifies the filepath to save uploaded inventory of archived files to.
    """
    # file will be uploaded to MEDIA_ROOT/inventory/RR<pk>/<filename>
    return f'inventory/RR{instance.pk}/{filename}'


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
                             help_text="""
                                       Descriptions of the scope of the data (eg. min, max, number of records, number
                                       of null values, number of unique values)
                                       """,
                             )
    
    def __str__(self):
        if self.scope:
            s = "{}...".format(self.scope[:20])
        else:
            s = "---"
        return "{} ({}...); {}".format(self.name,
                                       self.description[:20],
                                       s,
                                       )

    def get_absolute_url(self):
        return reverse('datacatalog:datafield-view', kwargs={'pk': self.pk})


class ConfidentialityImpact(models.Model):
    """
    A number of different standards define a confidentiality impact level, which can 
    mutually apply to any given dataset. This model will capture the standards and their 
    levels and definitions, allowing users to apply whatever relevant classification to 
    the dataset as needed.
    """
    # date the record was created
    record_creation = models.DateField(auto_now_add=True)
    
    # date the record was most recently modified
    record_update = models.DateField(auto_now=True)
    
    # the user who was signed in at time of record modification
    record_author = models.ForeignKey(User, on_delete=models.PROTECT)

    # the confidentiality impact level
    impact_level = models.CharField("Impact Level",
                                    max_length=32,
                                    unique=False,
                                    null=False,
                                    blank=False,
                                    help_text="Level as defined by the standard",
                                    )
    
    # for ranking the different scales, we include a separate rank field.
    # 1 is the highest risk level
    impact_rank = models.IntegerField(unique=False,
                                      null=False,
                                      blank=False,
                                      help_text="Rank of impact: 1 is highest risk",
                                      )
    
    # standard
    standard = models.CharField("Standard", 
                                max_length=32, 
                                unique=False, 
                                null=False, 
                                blank=False,
                                help_text="Standard defining the impact level",
                                )
    
    # definition
    definition = models.TextField(null=False, blank=False,)
    
    # url link to the relevant documentation 
    link = models.URLField(max_length=200,)

    def __str__(self):
        return "{}: {}".format(self.standard, self.impact_level)

    def get_absolute_url(self):
        return reverse('datacatalog:cil-view', kwargs={'pk': self.pk})
    

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
                        choices=AFFILIATION_CHOICES,
                        default=GOVERNMENT,
    )

    # this is set to true after being checked by the Data Catalog curation team
    curated = models.BooleanField(null=True, blank=True)

    # field to designate whether data should be published
    published = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return "{}".format(self.name,)

    def get_absolute_url(self):
        return reverse('datacatalog:provider-view', kwargs={'pk': self.pk})


class StorageType(models.Model):
    """
    This class defines the basic storage types and locations in which a set of digital
    objects might be found. This will allow the catalog to display the detailed location
    information for each type in a meaningful way, and ensure objects are only described
    from a single storage source. Creation of new storage types is not intended for end
    users, but only for administrators.
    """
    # date the record was created
    record_creation = models.DateField(auto_now_add=True)

    # date the record was most recently modified
    record_update = models.DateField(auto_now=True)

    # the user who was signed in at time of record modification
    record_author = models.ForeignKey(User, on_delete=models.PROTECT)

    # general name for identification of storage type
    name = models.CharField(max_length=128)

    # instructions for sysadmin archiving of files within the storage type
    archive_instructions = models.TextField(blank=True)

    def __str__(self):
        return "{}".format(self.name)


class Dataset(models.Model):
    """
    Each instance of Dataset defines a single collection of data. The minimum unit of a
    dataset can be defined as the largest collection that can be uniformly and 
    accurately described using the fields of this model. Ie, if a collection requires
    two or more entries for a specific field to describe the collection, then the 
    collection should be subsetted and each subset defined with its own model instance. 

    Related subsets can be linked together with a master dataset record, and the linked_data
    field.

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
    ds_id = models.CharField("Dataset ID",
                             max_length=128,
                             unique=True,
                             null=True,
                             blank=True,
                             help_text="Unique identifer of the data set"
                             )
    
    # dataset title/brief descriptor
    title = models.CharField(max_length=256, 
                             unique=True,
                             help_text="""
                                       The name of the dataset, usually one sentence or short description of the dataset
                                       """,
                             )
    
    # description of dataset
    # https://schema.org/description
    description = models.TextField(null=True,
                                   blank=True,
                                   help_text="Description of dataset, including purpose, scope, etc",
                                   )
    
    # a field to explicitly capture the fields present in a data model (if applicable)
    # Deprecated: to be replaced by the Data Dictionary fileField,
    # which will subsequently be set to parse the dictionary to metadata.
    data_fields = models.ManyToManyField(DataField, 
                                         blank=True,
                                         help_text="List of all fields present in any schema",
                                         )
    
    # data dictionary (to have specified format for parsing to metadata, but otherwise
    # will allow upload of any file as a record.)
    data_dictionary = models.FileField(
                            upload_to=dictionary_directory_path, 
                            null=True,
                            blank=True,
                            help_text="CSV or TSV file of each data field and its description.",
    )
    
    # beginning of temporal coverage (time of earliest data record)
    # https://schema.org/Date
    period_start = models.DateField(null=True, 
                                    blank=True,
                                    help_text="Date of earliest data record",
                                    )
    
    # end of temporal coverage (time of latest data record) 
    # https://schema.org/Date
    period_end = models.DateField(null=True,
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
    publisher = models.ForeignKey(DataProvider,
                                  blank=True,
                                  null=True,
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
    keywords = models.ManyToManyField(Keyword,
                                      blank=True,
                                      help_text="Add keywords related to data set",
                                      )
    
    # confidentiality impact level
    cil = models.ManyToManyField(ConfidentialityImpact,
                                 blank=True,
                                 help_text="Select an impact level based on data risk",
                                 )
    
    # field to indicate the size of the dataset in terms of number of records
    num_records = models.IntegerField("Number of records", blank=True, null=True,
                                      help_text="sample size of the dataset"
                                      )
    
    # indicate scale of the dataset based on the number of records
    UNITS = 'UN'
    TENS = 'TE'
    HUNDREDS = 'HU'
    THOUSANDS = 'TH'
    TENTHOUSANDS = 'TT'
    HUNDREDTHOUSANDS = 'HT' 
    MILLIONS = 'MI'
    SCALE_CHOICES = (
            (UNITS, "< 10"),
            (TENS, "10s"),
            (HUNDREDS, "100s"),
            (THOUSANDS, "1,000s"),
            (TENTHOUSANDS, "10,000s"),
            (HUNDREDTHOUSANDS, "100,000s"),
            (MILLIONS, "1,000,000s"),
    )

    record_scale = models.CharField(
                        max_length=2,
                        choices=SCALE_CHOICES,
                        blank=True,
                        null=True,
                        help_text="indicate the scale, based on the number of records"
    )
    
    # URL of landing page to access data
    landing_url = models.URLField(max_length=256,
                                  null=True,
                                  blank=True,
                                  help_text="URL of page that allows access of data"
                                  )
    
    # notes or general comments
    comments = models.TextField(null=True, blank=True)
        
    # pointer to the generic instructions required for accessing this data
    # access_requirements = models.ManyToManyField(DataAccess, blank=True,)

    # local contact person who is an expert on this dataset
    expert = models.ForeignKey(Person,
                               null=True,
                               blank=True,
                               on_delete=models.PROTECT,
                               help_text="A local contact who is an expert on the data"
                               )
    
    # media subtype (according to ontology at www.iana.org)
    media_subtype = models.ManyToManyField(MediaSubType,
                                           blank=True,
                                           help_text="The media types of all files in data set"
                                           )

    # this is set to true after being checked by the Data Catalog curation team
    curated = models.BooleanField(null=True, blank=True)

    # field to designate whether data should be published
    published = models.BooleanField(null=True, blank=True)

    # flag as publicly visible.
    public = models.BooleanField(null=True,
                                 blank=True,
                                 default=True,
                                 help_text="Whether to make this record visible in the Data Catalog",
                                 )

    # specify the users who have access. If none specified, then all users have
    # access to view
    restricted = models.ManyToManyField(Person, related_name='restricted_dataset', blank=True)

    # provide a direct link between related datasets, allowing for smart subsetting of projects or data models
    linked_data = models.ManyToManyField("self")

    def viewing_is_permitted(self, request):
        """
        checks viewing permission of instance against restricted field, and the logged in user via requests
        and returns True if the model instance is viewable by the user.
        """
        if self.public:
            return True
        elif len(self.restricted) == 0:
            return True

        user = getattr(request, 'user', None)
        if self.restricted.filter(id=user.id).exists():
            return True
        else:
            return False

    def __str__(self):
        return "{}".format(self.title)

    def get_absolute_url(self):
        return reverse('datacatalog:dataset-view', kwargs={'pk': self.pk})


class Project(models.Model):
    """
    The Project model allows aggregation of multiple datasets together under a common
    goal, providing common attributes related to the datasets' management, including
    PI, funding, and expected project completion.
    """
    # date the record was created
    record_creation = models.DateField(auto_now_add=True)

    # date the record was most recently modified
    record_update = models.DateField(auto_now=True)

    # the user who was signed in at time of record modification
    record_author = models.ForeignKey(User, on_delete=models.PROTECT, related_name='record_author')

    # name of project
    name = models.CharField(max_length=128, unique=True)

    # brief description of project
    description = models.TextField(null=True, blank=True)

    # principle investigator
    pi = models.ForeignKey(Person,
                           on_delete=models.PROTECT,
                           verbose_name='PI',
                           related_name='pi_project_person'
                           )

    # additional PIs to have access to the project record
    other_pis = models.ManyToManyField(Person,
                                       related_name='other_pis',
                                       blank=True,
                                       verbose_name='Other PIs',
                                       help_text="additional PIs related to the project",
                                       )

    # DEPRECATED: project administrator. This field will be dropped in a future update.
    admin = models.ForeignKey(Person, on_delete=models.PROTECT, related_name='admin_person', null=True, blank=True,)

    # list of all other people who are to have access to the project record
    other_editors = models.ManyToManyField(Person,
                                           related_name='other_editors',
                                           blank=True,
                                           help_text="additional people to give access to edit the project",
                                           )

    # project sponsor
    sponsor = models.CharField(max_length=128, null=True, blank=True)

    # sponsored project identifier
    funding_id = models.CharField(max_length=64, null=True, blank=True, help_text="WRG project ID",)

    # expected date of project completion
    completion = models.DateField(null=True, blank=True, help_text="expected completion date of project",)

    def viewing_is_permitted(self, request):
        """
        checks viewing permission of instance against restricted field, and the logged in user via requests
        and returns True if the model instance is viewable by the user.
        """
        user = getattr(request, 'user', None)
        if user.has_perm('datacatalog.view_project'):
            return True
        elif user.username == self.pi.cwid:
            return True
        elif self.other_pis.filter(cwid=user.username).exists():
            return True
        elif self.other_editors.filter(cwid=user.username).exists():
            return True
        else:
            return False

    def __str__(self):
        return "{}".format(self.name)

    def get_absolute_url(self):
        return reverse('datacatalog:project-view', kwargs={'pk': self.pk})


class DataAccess(models.Model):
    """
    This class defines the processes and information required in order to gain access
    to a dataset. These instructions are generic, in as much as they define how anyone
    may gain access, and are not intended to only specify for a particular user/project.
    These instructions are specific, in as much as they pertain to a particular set of
    digital objects associated with a described dataset.
    """
    # date the record was created
    record_creation = models.DateField(auto_now_add=True)

    # date the record was most recently modified
    record_update = models.DateField(auto_now=True)

    # the user who was signed in at time of record modification
    record_author = models.ForeignKey(User, on_delete=models.CASCADE)

    # general name for identification of access object
    name = models.CharField(max_length=128, blank=True, null=True)

    # the storage type classification for the digital objects
    storage_type = models.ForeignKey(StorageType,
                                     blank=True,
                                     null=True,
                                     on_delete=models.PROTECT,
                                     help_text="Select the system storing the data",
                                     )

    # unique identifier of digital objects collection (eg LabArchives notebook ID)
    unique_id = models.CharField("Unique ID",
                                 max_length=256,
                                 blank=True,
                                 null=True,
                                 help_text="system-generated unique identifier for e.g. Starfish",
                                 )

    # shareable link that gives access to the digital objects/collection
    shareable_link = models.URLField("Link to your data location",
                                     blank=True,
                                     null=True,
                                     max_length=1024,
                                     help_text="system-generated shareable link to the data, e.g. OneDrive, LabArchives",
                                     )

    # description of digital object locations - as filepaths
    filepaths = models.TextField(blank=True,
                                 null=True,
                                 help_text="describe the full path to all directories and/or files, e.g. libsrv.med.cornell.edu/my_lab/myfolder/data.csv",
                                 )

    # form for uploading multiple files directly through Django
    multifiles = models.FileField(upload_to=multifile_directory_path,
                                  blank=True,
                                  null=True,
                                  help_text="upload files directly for archiving",
                                  )

    # field to record all files uploaded via multifiles field
    fileupload_log = models.TextField(blank=True,
                                      null=True,
                                      default="",
                                      )

    # points to the dataset object that describes this set of data files
    metadata = models.ManyToManyField(Dataset,
                                      blank=True,
                                      help_text="link this dataset to selected Data Catalog record(s)",
                                      )

    # project that the data are associated with
    project = models.ForeignKey(Project, blank=True, null=True, on_delete=models.PROTECT)

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

    # whether the digital objects are publicly available
    public_data = models.BooleanField(null=True, blank=True, default=False,
                                      help_text="Choose yes to make this information publicly visible"
                                      )

    # email for others to request access to the digital objects
    steward_email = models.EmailField(null=True, blank=True,
                                      help_text="Person to contact for data access"
                                      )

    # details for gaining access to the dataset
    access_instructions = models.TextField(blank=True, null=True,
                                           help_text="Any additional instructions for accessing the data")

    # whether this record is to be publicly available
    public = models.BooleanField(null=True, blank=True, default=False)

    # typical time period from request to access of data
    time_required = models.DurationField(null=True, blank=True)

    # mark whether a request for archiving has been made
    retention_requested = models.BooleanField(null=True, blank=True)

    # mark whether the data have been archived
    data_retained = models.BooleanField(null=True, blank=True)

    # this is set to true after being checked by the Data Catalog curation team
    curated = models.BooleanField(null=True, blank=True, default=False)

    # field to designate whether data should be published
    published = models.BooleanField(null=True, blank=True, default=True)

    # specify the users who have access. If none specified, then all users have
    # access to view
    restricted = models.ManyToManyField(Person, related_name='restricted_access', )

    def __str__(self):
        return "{}".format(self.name)

    def get_absolute_url(self):
        return reverse('datacatalog:access-view', kwargs={'pk': self.pk})

    def viewing_is_permitted(self, request):
        """
        checks viewing permission of instance against restricted field, and the logged in user via requests
        and returns True if the model instance is viewable by the user.
        """
        user = getattr(request, 'user', None)
        if user.has_perm('datacatalog.view_dataaccess'):
            return True
        elif user.username == self.project.pi.cwid:
            return True
        elif self.project.other_pis.filter(cwid=user.username).exists():
            return True
        elif self.project.other_editors.filter(cwid=user.username).exists():
            return True
        elif self.public:
            return True
        elif self.restricted.filter(cwid=user.username).exists():
            return True
        else:
            return False

    def is_requested(self):
        if self.retention_requests.count() > 0:
            return True
        else:
            return False


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

    def __str__(self):
        return "{}".format(self.name)
       

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
            (PI, "Principal Investigator"),
            (PROJECT, "Project"),
            (INSTITUTE, "Institution"),
    )
    scope = models.CharField(
                        max_length=2,
                        choices=SCOPE_CHOICES,
                        default=USER,
    )
    
    # date DUA signed
    date_signed = models.DateField(null=True, blank=True)
    
    # start date of DUA
    start_date = models.DateField(null=True, blank=True)
    
    # end date of DUA
    end_date = models.DateField(null=True, blank=True)
    
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
    datasets = models.ManyToManyField(Dataset, blank=True)

    # description of types of experiments allowed under reuse terms
    reuse_scope = models.TextField(null=True, blank=True)
    
    # pointer to the generic instructions required for accessing this data
    # access_requirements = models.ManyToManyField(DataAccess, blank=True,)

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

    # flag as publicly visible.
    public = models.BooleanField(null=True, blank=True)

    # specify the users who have access. If none specified, then all users have
    # access to view
    restricted = models.ManyToManyField(Person, related_name='restricted_dua')
    
    def __str__(self):
        return "{}: {}".format(self.duaid, self.title)

    def get_absolute_url(self):
        return reverse('datacatalog:dua-view', kwargs={'pk': self.pk})

    def allowed_user_string(self):
        return ", ".join([u.cwid for u in self.users.all()])

    def attention_required(self):
        """
        This function returns a bootstrap flag to indicate how close to the expiry date
        the DUA is.
        """
        td = self.end_date - datetime.date.today() 
        
        if td.days > 90:
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

    def viewing_is_permitted(self, request):
        """
        checks viewing permission of instance against restricted field, and the logged in user via requests
        and returns True if the model instance is viewable by the user.
        """
        if self.public:
            return True
        elif len(self.restricted) == 0:
            return True

        user = getattr(request, 'user', None)
        if self.restricted.filter(id=user.id).exists():
            return True
        else:
            return False


class RetentionRequest(models.Model):
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
    record_author = models.ForeignKey(User, on_delete=models.PROTECT)

    # short description of the request
    name = models.CharField("Short description",
                            max_length=256,
                            help_text="enter a name to identify this request",
                            )

    # project associated with the milestone
    project = models.ForeignKey(Project,
                                on_delete=models.PROTECT,
                                null=True,
                                blank=True,
                                help_text="Select from your available projects",
                                )

    # Milestone that defines the reason for data retention
    PUBLICATION = 'PU'
    COMPLETION = 'CO'
    TRANSFER = 'TR'
    PRIVATE = 'PR'
    OTHER = 'OT'
    MILESTONE_CHOICES = (
        ("", "--- choose one ---"),
        (PUBLICATION, "Publication"),
        (COMPLETION, "Project/Grant completion"),
        (TRANSFER, "Leaving Weill Cornell Medicine"),
    )
    milestone = models.CharField(
        max_length=2,
        choices=MILESTONE_CHOICES,
        default=COMPLETION,
    )

    # date in which the milestone itself is completed
    milestone_date = models.DateField(default=date.today,
                                      help_text="expected completion date of milestone",
                                      )

    # unambiguous pointer to milestone record
    milestone_pointer = models.CharField(max_length=64,
                                         help_text="DOI of published article, WRG project ID, or HR offboarding form ID",
                                         )

    # digital objects for archiving
    to_archive = models.ManyToManyField(DataAccess,
                                        related_name='retention_requests',
                                        help_text="select all data for retention from the project chosen above",
                                        )

    # methods documentation linking source files and results files
    methodfile = models.FileField("Methods file",
                            upload_to=method_directory_path,
                            null=True,
                            help_text="""
                                      upload a document describing steps required to produce output data from raw data 
                                      """,
                            )

    # for additional information necessary for archiving
    comments = models.TextField(null=True, blank=True)

    # ITS ticket ID
    ticket = models.CharField(max_length=32, null=True, blank=True)

    # set record to locked to prevent users from altering after data retention has occurred
    locked = models.BooleanField(null=True, blank=True, default=False)

    # set to True once the researcher has validated the retention contents
    verified = models.BooleanField(null=True, blank=True, default=False)

    # set to True once the researcher has validated the retention contents
    archived = models.BooleanField(null=True, blank=True, default=False)

    inventory = models.FileField(
                        upload_to=inventory_directory_path,
                        null=True,
                        help_text="""Document list of all files archived""",
                        )

    def __str__(self):
        return "{}: {}".format(self.record_creation, self.name)

    def get_absolute_url(self):
        return reverse('datacatalog:retention-view', kwargs={'pk': self.pk})

    def viewing_is_permitted(self, request):
        """
        checks viewing permission of instance against restricted fields, and the logged in user via requests
        and returns True if the model instance is viewable by the user.
        """
        user = getattr(request, 'user', None)

        if user.has_perm('datacatalog.view_retentionrequest'):
            return True
        elif user.username == self.project.pi.cwid:
            return True
        elif self.project.other_pis.filter(cwid=user.username).exists():
            return True
        elif self.project.other_editors.filter(cwid=user.username).exists():
            return True
        else:
            return False