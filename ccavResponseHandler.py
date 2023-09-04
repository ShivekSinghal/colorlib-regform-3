#!/usr/bin/python

from ccavutil import encrypt, decrypt
from string import Template


def res(encResp):
    '''
    Please put in the 32 bit alphanumeric key in quotes provided by CCAvenues.
    '''
    workingKey = '1ED377C8D4316E3330503FC2188622A1	'
    decResp = decrypt(encResp, workingKey)
    data = '<table border=1 cellspacing=2 cellpadding=2><tr><td>'
    data = data + decResp.replace('=', '</td><td>')
    data = data.replace('&', '</td></tr><tr><td>')
    data = data + '</td></tr></table>'

    html = '''\
	<html>
		<head>
			<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
			<title>Response Handler</title>
		</head>
		<body>
			<center>
				<font size="4" color="blue"><b>Response Page</b></font>
				<br>
				$response
			</center>
			<br>

		</body>
	</html>
	'''

    fin = Template(html).safe_substitute(response=data)
    return fin
