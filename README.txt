Requirements
	Python 2.7
	Django 1.6+
	MySQL (PostgreSQL not supported)

1 - Install:
	Django
	South (optional)
	reportlab
	Privateoffice
2 - Add root url in url.py to Privateoffece
	url(r'^', include('privateoffice.urls')),
3 - Coolect static
3 - Load fixtures
	$ python2.7 manage.py loaddata country.json
	$ python2.7 manage.py loaddata town.json
	$ python2.7 manage.py loaddata hotel.json
=============
