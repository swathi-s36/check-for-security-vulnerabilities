import requests
from termcolor import colored

def check_hsts(domain):
    try:
        response = requests.get(f'https://{domain}', verify=False)
        return 'yes' if 'strict-transport-security' in response.headers else 'no'
    except Exception as e:
        return 'no'
#        return f"Error: {e}"

def main(domain):
#    domains = input("Enter one or more domains separated by spaces: ").split()
#    for domain in domains:
    result = check_hsts(domain)
    print (f'Checking whether {domain} supports HSTS.....')

    if result == 'yes':
        print (colored(f'\n{domain} supports HSTS!','green', attrs=["bold"]))
    else:
        print (colored(f'\n{domain} does not support HSTS!','red', attrs=["bold"]))

#if __name__ == '__main__':
#    main()
