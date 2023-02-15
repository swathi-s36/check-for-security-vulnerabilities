import subprocess

def cewl_generate(url):
	process = subprocess.Popen(['cewl','-w','cewl_wordlists.txt',url])
	stderr, stdout = process.communicate()
	return process.returncode

#if __name__ == "__main__":
#	cewl_generate(input("Enter URL to test: "))
