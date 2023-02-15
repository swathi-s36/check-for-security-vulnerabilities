"""
	Project: Dragline - Strengthening web applications
	Authors: Swathi Sankaranarayanan, Sriram Nanda Kumar, Tanzila Hasan Pinky
	Dates: 30th January 2023 - 2nd February 2023
"""

import gen_cewl
from cross_site import scan_xss
from termcolor import colored
import hsts
import subprocess
import re
import nmap
import nikto
import time

def execute_functions(url ,level='beginner'):

	result = test_sql_injection(url, level)
	time.sleep(2)
	result = test_xss(url, level)
	time.sleep(2)
	result = test_hsts(url)
	time.sleep(2)
	result = test_components_certificate(url, level)

#Retrieve only the URLs from the results of dirb
def get_urls():

	with open('dirb_results.txt','r') as file:
		text = file.read()
	urls = re.findall('(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-?=%.]+', text)
#	print (urls)
	return urls

#Run dirb on common wordlist and generated wordlist
def run_dirb(url):

	print ()
	print ("="*90)
	print ("*	        	GENERATING NAVIGATABLE DIRECTORY LIST FOR THE WEBSITE		*")
	print ("="*90)
	print ()

	result = gen_cewl.cewl_generate(url)
	if result == 0:
		print ("Successfully generated wordlist from website!")
	else:
		print ("Failed to generate wordlist from website! Using predefind wordlist!")

	process = subprocess.Popen(['dirb',url,'/usr/share/dirb/wordlists/common.txt,cewl_wordlists.txt','-o','dirb_results.txt'])
	stderr, stdout = process.communicate()
	if result == 0:
		print ("Successfully generated wordlist from website!")
	else:
		print ("Failed to generate wordlist from website! Using predefind wordlist!")

	return process.returncode


#Tests for sql injection vulnerability
def test_sql_injection(url, level='beginner'):

	print ()
	print ("="*90)
	print ("*				TESTING FOR SQL INJECTION VULNERABILITY			*")
	print ("="*90)
	print ()

	answers = 'quit=Y,follow=Y,threads=1,exploit=Y,store=N,test=Y,normalize=Y,existence=N'

	if level == 'beginner':
		process = subprocess.Popen(['sqlmap','-u',url,'--answer',answers,'-crawl','2'])
		stdout, stderr = process.communicate()
		return process.returncode
	elif level == 'intermediate':
		process = subprocess.Popen(['sqlmap','-u',url,'--answer',answers,'-crawl','3','-dbs'])
		stdout, stderr = process.communicate()
		return process.returncode
	elif level == 'expert':
		run_query = input("Do you want to run additional sql query? (y/n)? ")
		if run_query == 'y':
			query = input("Type query you want to execute on the server: ")
		else:
			query = ''
		process = subprocess.Popen(['sqlmap','-u',url,'--answer',answers,'-crawl','3','--sql-query',query])
		stdout, stderr = process.communicate()
		return process.returncode

	#print (f"Status of SQLmap: {process.returncode}")


#Runs cross-site scripting test
def test_xss(url, level='beginner'):

	print ()
	print ("="*90)
	print ("*			TESTING FOR CROSS_SITE SCRIPTING VULNERABILITY			*")
	print ("="*90)
	print ()

	if level == 'beginner':
		vulnerable = scan_xss(url)
		if vulnerable == True:
			print (colored(f'\n{url} is vulnerable to Cross-site scripting attack','red',attrs=["bold"]))
	elif level == 'intermediate' or level == 'expert':
		run_dirb(url)
		urls = get_urls()
		checked_links = []
		for link in urls:
			if link.startswith('http') == True:
				if link not in checked_links:
					vulnerable = scan_xss(link)
					checked_links.append(link)
					if vulnerable == True:
						print (colored(f'\n{link} is vulnerable to Cross-site scripting attack','red', attrs=["bold"]))
					#else:
					#	print (colored(f'\n{link} is not vulnerable to Cross-site scripting attack','green'))


#Checks if the website can be downgraded to HTTP from HTTPS
def test_hsts(url):

	print ()
	print ("="*90)
	print ("*			TESTING FOR HTTP STRICT-TRANSPORT-POLICY VULNERABILITY		*")
	print ("="*90)
	print ()

	hsts.main(url)


#Checks for any outdated components and valid SSL certificates for HTTPS sites
def test_components_certificate(url, level='beginner'):

	print ()
	print ("="*90)
	print ("*			TESTING FOR OUTDATED COMPONENTS AND SSL CERTIFICATION		 *")
	print ("="*90)
	print ()

	print ("======================= CHECKING FOR VULNERABILITIES USING NIKTO =========================")

	if level == 'beginner':
		result = nikto.main(url)

	elif level == 'intermediate':
		result = nikto.main(url)

	elif level == 'expert':
		result = nikto.main(url)

	print ("="*90)
	print ()

	print ("======================= CHECKING FOR SSL CERTIFICATES USING NMAP =========================")

	if level == 'beginner':
		result = nmap.main(url)
	elif level == 'intermediate':
		result = nmap.main(url)
	elif level == 'expert':
		result = nmap.main(url)

	print ("="*90)
	print ()


if __name__ == "__main__":

	print ()
	print ("="*90)
	print ("*				Welcome to Dragline					 *")
	print ("*	This tool checks for SQL Injection vulnerability in your web application!	 *")
	print ("*	In addition we also offer testing for cross-site scripting for all forms	 *")
	print ("*	available in the application. Furthermore, we help you identify if your  	 *")
	print ("*	website could be downgraded to HTTP from HTTPS connection by checking for	 *")
	print ("*	the HSTS header in your website! Further to make your application even more	 *")
	print ("*	secure we check for valid ssl certificates and other plausible attack sites.	 *")
	print ("*											 *")
	print ("*											 *")
	print ("*											 *")
	print ("			=================================			  	  ")
	print ("			||	      MENU	       ||				  ")
	print ("			=================================			  	  ")
	print ("*			1) You are a Beginner/Novice user 				 *")
	print ("*			2) You are an Intermediary user					 *")
	print ("*			3) You are an expert user				  	 *")
	print ("*											 *")
	print ("*		   Select your level to see the tests performed	 			 *")
	print ("="*90)

	choice = int(input("Enter the level to begin testing: "))
	match choice:
		case 1:
			filename = "beginner.txt"
			execute = "beginner"
		case 2:
			filename = "intermediate.txt"
			execute = "intermediate"
		case 3:
			filename = "expert.txt"
			execute = "expert"
		case _:
			print (colored(f"\nInvalid level selected!\n",'yellow'))
			exit()

	with open(filename,'r') as file:

		print ()
		print (file.read())
		print ()

	match execute:
		case 'beginner':
				print (colored(f"Executing Beginner level tests!",'magenta', attrs=["bold"]))
				url = input("Enter url of website to continue: ")
				execute_functions(url, execute)
		case 'intermediate':
				print (colored(f"Executing Intermediate level tests!",'magenta', attrs=["bold"]))
				url = input("Enter url of website to continue: ")
				execute_functions(url, execute)
		case 'expert':
				print (colored(f"Executing Expert level tests!",'magenta', attrs=["bold"]))
				url = input("Enter url of website to continue: ")
				execute_functions(url, execute)
