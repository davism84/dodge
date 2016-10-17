from http.client import HTTPSConnection
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, get_list_or_404
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json

from .models import LabResult, Identity, Mrn
from .forms import IdentityForm

# general method for formating a multipart message
def encode_multipart_formdata(fields, files):
    """
    fields is a sequence of (name, value) elements for regular form fields.
    files is a sequence of (name, filename, value) elements for data to be uploaded as files
    Return (content_type, body) ready for httplib.HTTP instance
    """
    BOUNDARY = '---011000010111000001101001'
    CRLF = '\r\n'
    L = []
    for (key, value) in fields.items():
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="%s"' % key)
        L.append('')
        L.append(value)
    for (key, filename, value) in files:
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename))
        L.append('Content-Type: %s' % get_content_type(filename))
        L.append('')
        L.append(value)
    L.append('--' + BOUNDARY + '--')
    L.append('')
    body = CRLF.join(L)
    #content_type = 'content-type: multipart/form-data; boundary=%s' % BOUNDARY
    content_type = {
		'content-type': "multipart/form-data; boundary=---011000010111000001101001",
    	'cache-control': "no-cache"
    }

    return content_type, body

def results(request, record_id):
    labresult = get_object_or_404(LabResult, pk=record_id)
    return render(request, 'redcap_rest/results.html', {'lab': labresult})	

def detail(request):
	record_id = request.GET.get('record')
	labresult = get_object_or_404(LabResult, pk=record_id)
	return render(request, 'redcap_rest/results.html', {'lab': labresult})

# endpoint for authorizing REDCap User
@api_view(['POST'])
def authorize(request):
	if request.method == 'POST':
		data=request.data
		# grab the auth key from redcap
		authkey = request.data.get('authkey')

		# resend this back to redcap to get full auth info
		#return Response(data, status=status.HTTP_201_CREATED)
		REDCAP = getattr(settings, 'REDCAP', '')
		token = REDCAP['token']
		host = REDCAP['host']
		endpoint = REDCAP['endpoint']
	
		# this will all the desired fields to the payload, encode_multipart_formdata
		fields = {'authkey': authkey, 'format':'json'}
		files = []
		content, body = encode_multipart_formdata(fields, files)

    	# connect to host and send request
		conn = HTTPSConnection(host)

		conn.request("POST", endpoint, body, content)

		res = conn.getresponse()
		# read the content from the response, type is <byte>
		data = res.read()
		#print(type(data))
		print(data)
		
		# decode the data body content from <byte> using utf-8 to a string
		decoded = data.decode("utf-8")
		# convert the string to a json object
		user = json.loads(decoded)
		#print(user['username'])
		# simple check against the internal user auth table
		try:
			m = User.objects.get(username=user['username'])
			print(m)
		except ValueError:
			return Response('User not authorized', status=status.HTTP_404_NOT_FOUND)
		return Response('User is authorized')
	return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def getforms(request):
	
	REDCAP = getattr(settings, 'REDCAP', '')
	token = REDCAP['token']
	host = REDCAP['host']
	endpoint = REDCAP['endpoint']
	
	# payload fields for redcap
	fields = {'token': token, 'format':'json', 'content':'instrument'}
	files = []
	content, body = encode_multipart_formdata(fields, files)
	#print(content)
	print(body)

	headers = {
	'content-type': "multipart/form-data; boundary=---011000010111000001101001",
    'cache-control': "no-cache"
    }
	conn = HTTPSConnection(host)
	conn.request("POST", endpoint, body, headers)

	res = conn.getresponse()

	data = res.read()
	print(data)
	return JsonResponse(data.decode("utf-8"), safe=False)

# displays person info
def personinfo(request):
	# get the record id
	record_id = request.GET.get('record')
	# grab the identity of the person
	pid = get_object_or_404(Identity, record_id=record_id)
	return render(request, 'redcap_rest/person.html', {'pid': pid})	

# displays a list of mrns for a patient
@api_view(['POST'])
def mrns(request):
	if request.method == 'POST':
		data=request.data
		# grab the auth key from redcap
		authkey = request.data.get('authkey')

		# resend this back to redcap to get full auth info
		#return Response(data, status=status.HTTP_201_CREATED)
		REDCAP = getattr(settings, 'REDCAP', '')
		token = REDCAP['token']
		host = REDCAP['host']
		endpoint = REDCAP['endpoint']
	
		# this will all the desired fields to the payload, encode_multipart_formdata
		fields = {'authkey': authkey, 'format':'json'}
		files = []
		content, body = encode_multipart_formdata(fields, files)

    	# connect to host and send request
		conn = HTTPSConnection(host)

		conn.request("POST", endpoint, body, content)

		res = conn.getresponse()
		# read the content from the response, type is <byte>
		data = res.read()
		#print(type(data))
		print(data)
		
		# decode the data body content from <byte> using utf-8 to a string
		decoded = data.decode("utf-8")
		# convert the string to a json object
		response = json.loads(decoded)
		#print(user['username'])
		# simple check against the internal user auth table
		try:
			m = User.objects.get(username=response['username'])
			print(m)

			# get the record id
			record_id = request.GET.get('record')
			print(record_id)

			# grab the identity of the person
			pid = get_object_or_404(Identity, pk=record_id)

			# get all the persons mrns
			mrns = get_list_or_404(Mrn, identity = pid)

			print(mrns)

		except ValueError:
			return Response('User not authorized', status=status.HTTP_404_NOT_FOUND)
		return render(request, 'redcap_rest/identity.html', {'mrns': mrns, 'pid':pid})
	return Response(status=status.HTTP_404_NOT_FOUND)

# add method for displaying a identity form
@api_view(['POST'])
def add(request):
	validresponse = validate(request)
	if validresponse:
		record_id = request.GET.get('record')
		print(record_id)
		project_id = validresponse['project_id']
		if record_id != "":
			print('record is not empty')
			form = IdentityForm(initial={'record_id':record_id, 'project_id':project_id})
		else:
			form = IdentityForm()
		return render(request, 'redcap_rest/edit_ident.html', {'form': form})
	else:
		Response('User not authorized', status=status.HTTP_404_NOT_FOUND)	

# Action method for saving a new identity
@api_view(['POST'])
def save(request):
	if request.method == "POST":
		form = IdentityForm(request.POST)
		if form.is_valid():
			form.save()
		return render(request, 'redcap_rest/save.html')	

# general method for validation process from REDCap
def validate(request):
	if request.method == 'POST':
		data=request.data
		# grab the auth key from redcap
		authkey = request.data.get('authkey')

		# resend this back to redcap to get full auth info
		#return Response(data, status=status.HTTP_201_CREATED)
		REDCAP = getattr(settings, 'REDCAP', '')
		token = REDCAP['token']
		host = REDCAP['host']
		endpoint = REDCAP['endpoint']
	
		# this will all the desired fields to the payload, encode_multipart_formdata
		fields = {'authkey': authkey, 'format':'json'}
		files = []
		content, body = encode_multipart_formdata(fields, files)

    	# connect to host and send request
		conn = HTTPSConnection(host)

		conn.request("POST", endpoint, body, content)

		res = conn.getresponse()
		# read the content from the response, type is <byte>
		data = res.read()
		#print(type(data))
		print(data)
		
		# decode the data body content from <byte> using utf-8 to a string
		decoded = data.decode("utf-8")
		# convert the string to a json object
		response = json.loads(decoded)
		#print(user['username'])
		# simple check against the internal user auth table
		try:
			m = User.objects.get(username=response['username'])
			print(m)

			# get the record id
			record_id = request.GET.get('record')
			print(record_id)

		except ValueError:
			return ''
		return response
	return ''
