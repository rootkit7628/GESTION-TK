'''

	RABEZANAHARY LUCIE VOARY

'''
import os

try:
	os.system('python ./ident/identify.py')
except:
	os.system('py ./ident/identify.py')
	try:
		os.system('python3 ./ident/identify.py')
	except Exception as e:
		print('[ Erreur ] : ', e, 'Python is not installed in your computer')
