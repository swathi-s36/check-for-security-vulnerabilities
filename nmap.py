from termcolor import colored
import subprocess
import re

def main(url):

	if url.startswith("http://"):
		str_list = url.split("http://")
	elif url.startswith("https://"):
		str_list = url.split("https://")

	target = "".join(str_list)
#	print (target)
	target = target.replace('/','')
#	print (target)

	process = subprocess.Popen(['nmap','--script','ssl-cert','-p','443,80',target,'-oN','nmap_result.txt'])
	out , err = process.communicate()

	if process.returncode == 0:
		with open('nmap_result.txt','r') as file:
			content = file.read()

		if 'ssl certificate' not in content:
			print (colored(f'{target} does not contain valid ssl certificate', 'red', attrs=["bold"]))


#main("http://testphp.vulnweb.com/")
