from django.db import models

from django.contrib.auth.models import User

from dc_management import DC_User 

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
    # definition / elaboration of keyword

class Dataprovider(models.Model):
    """
    This class defines data providers.
    """
    # provider organization name
    # provider department
    # contact phone number
    # contact email 
    # provider country of origin
    # provider affiliation: Academic, Hospital, Government, Private
    
    
class Datauseagreement(models.Model):
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
    # name/title of DUA
    # brief description of DUA
    # data provider / publisher
    # provider contact individual
    # principal investigator
    # separate attestation form required for each user?
    # level at which the project applies: User, PI, Project, Institutional
    # date DUA signed
    # start date of DUA
    # end date of DUA
    # data destruction required at end?
    # mixing of other datasets with these allowed?
    # storage conditions specified
    # access conditions specified
    # datasets included in governance terms
    
    
    def __str__(self):
        return "DUA {}: {}".format(self.id, self.title)

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
    
    # dataset title/brief descriptor
    # description of dataset
    # beginning of temporal coverage (time of earliest data record)
    # end of temporal coverage (time of latest data record)
    # keywords
    # URL of landing page to access data
    # typical time period from request to access of data
    # publicly available
    # DUA required for access
    # Charge for access
    # notes or general comments