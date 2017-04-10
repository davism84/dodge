# dodge

Prerequisites
- Python 3.5.2
- Django 1.10.1	  (pip install django)
- Django Rest framework  (pip install djangorestframework)

REDCap

- Example bookmarks
	must setup a project bookmark with the following link and Link type set to __*Advanced Link*__:

	- http://localhost:8000/redcap_rest/authorize     - shows an authorization
	- http://localhost:8000/redcap_rest/mrns/		  - show list of mrns for a given patient
	- http://localhost:8000/redcap_rest/personinfo    - patient demographics (this can be a __Simple link__)
    - http://localhost:8000/redcap_rest/add/		  - adds a patient (__you must add new patient on redcap side first__)


__to run__

$ python manage.py runserver


__to add an admin user__

$ python manage.py createsuperuser
