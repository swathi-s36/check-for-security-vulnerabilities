"""
Using 'Subprocess' capture the standard output and standard error of the NIKTO process,
and also obtain the return code of the process after it has completed.
"""

import subprocess
from termcolor import colored

issues = ['X-XSS-Protection ', 'SQL injection', 'Cross-site scripting (XSS)', 
	'Cross-site request forgery (CSRF)', 'Remote code execution', 'Directory traversal', 
         'Broken authentication and session management', 'Broken access control', 'Insecure', 'cryptographic storage', 'Injection flaws', 'anti-clickjacking', 'SSL']

def run_nikto_scan(target_url, tuning, output_file):

    cmd = f"nikto -h {target_url} -Tuning {tuning} -output {output_file}"

    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return_code = process.returncode

    if return_code != 0:
        print(f"NIKTO scan failed with return code {return_code}")
        print("Standard error output:")
        print(stderr.decode())
    else:
        print("NIKTO scan completed successfully")


def check_for_vulnerabilities(output_file,target_url):

    with open(output_file, "r") as f:
        nikto_output = f.read()
    for issue in issues:
        if issue in nikto_output:
            print(colored(f"\n{target_url} could be attacked by {issue}",'red', attrs=["bold"]))


def main(target_url):

#    target_url = "http://testphp.vulnweb.com/"
    tuning = 61
    output_file = "nikto_output.txt"


    run_nikto_scan(target_url, tuning, output_file)
    check_for_vulnerabilities(output_file,target_url)

#if __name__ == "__main__":
#    main()
