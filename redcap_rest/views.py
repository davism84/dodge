from http.client import HTTPSConnection
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json

from .models import LabResult

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