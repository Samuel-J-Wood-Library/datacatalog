# Data Catalog
__A django app for cataloging institutional research datasets__

```
Peter Oxley
Weill Cornell Medicine
Samuel J. Wood Library and C.V. Starr Biomedical Information Center
1300 York Ave
New York, NY 10065
pro2004@med.cornell.edu
```

## Scope
The Data Catalog is an internal catalog of research datasets available to members of an institution. The catalog does not contain the data, but rather contains descriptions and metadata of each dataset. The catalog allows researchers to make their own datasets discoverable to others at the institution, and allows researchers to identify biomedical or health data that are not readily accessible elsewhere. 
The catalog provides the ability to search for datasets based on their title, description, data elements, keywords, or data governance.
Researchers can also submit new datasets for display in the catalog. After new submissions have been reviewed by the curatorial team, they are then made available for discovery in the catalog.

## Structure of the catalog
The catalog consists of 5 primary tables of information:
1. Datasets - metadata regarding a specific data repository/file/database
2. Data Providers - either the data source for a dataset, or a publisher of the data
3. Data Use Agreements - specific terms of use for a specific set of users, for a delimited period of time
4. Data Access Conditions - requirements for hosting the dataset (as specified by the publisher). Includes whether data must be secured, can be mixed with other data, and must be destroyed at end of project.
5. Keywords - a customizable dictionary of terms that can be used to tag related datasets.


## Setup
This app will need to be installed into an existing Django project.

1. Download latest code from https://github.com/oxpeter/datacatalog/archive/master.zip 
1. Copy `datacatalog` directory into the Django project directory
2. Add `datacatalog.apps.DatacatalogConfig` to INSTALLED_APPS in settings.py
3. From the project directory, run `python manage.py migrate datacatalog`
4. Go to the Django admin page
5. Under AUTHENTICATION AND AUTHORIZATION select Add Group
6. Create the following groups: 
    1. datacatalog_editor - give view/add/delete/change permissions to datacatalog tables
    2. dua_viewing_privileges - give view permissions to datacatalog tables

## app permissions
### Viewing data use agreements
Data Use Agreements are by default hidden from your users, unless they are added to the dua_viewing_privileges group. 

### Editing items
Regular users have the ability to submit new entries for all catalog types. These entries will not be marked curated or published, and thus will not be immediately visible in the catalog. Instead, users in the datacatalog_editor group have the ability to view and modify the entries, and inside the admin site, can change the items to curated (to indicate they have been quality checked), and also set to published (to make them visible on the website). To assist with large-scale curation or publication, you can select multiple entries in the admin table and use the actions box to mark all selected items as published/unpublished/curated. 



## Dependencies
This app was developed and tested with Django 2.1. While it should work on all versions ≥2.0, we cannot guarantee performance on other versions.

You will also require the following apps:
* django-autocomplete-light yourlabs/django-autocomplete-light
* django-crispy-forms django-crispy-forms/django-crispy-forms
* django-bootstrap4 zostera/django-bootstrap4
* persons oxpeter/persons

You will also require the following python packages:
* numpy
* psycopg2
