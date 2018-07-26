#!/usr/bin/env python3

import os
import re
from base64 import b64encode, urlsafe_b64encode
base64 = lambda s: b64encode(s.encode()).decode()
from jinja2 import Environment, FileSystemLoader

dirname = os.path.dirname(__file__)
template_dir = os.path.join(dirname, 'templates')
clusters_dir = os.path.join(dirname, 'clusters')
jinja_env = Environment(loader=FileSystemLoader(template_dir))
jinja_env.filters['b64encode'] = base64

def prompt(msg, regex='.*', default=None, readFile=False):
    result = input(msg)
    if not result and default:
        return default
    if not re.match(regex, result):
        raise ValueError(f"expect response to match the regex '{regex}'.")
    if readFile:
        with open(result, 'r') as file:
            data=file.read()
        return data
    else:
        return result

def prompt_for_user_vars():
    context = {}
    context['namespace'] = prompt('Enter the same namespace from step 1: ',
        '^[a-z][-a-z0-9]{1,19}$')
    context['github_org'] = prompt('Enter the GitHub org: ')
    context['github_team'] = prompt('Enter the GitHub team: ')
    context['oauth_client_id'] = prompt('Enter the OAuth Client ID: ')
    context['oauth_client_secret'] = prompt('Enter the OAuth Client Secret: ')
    context['oauth_cookie_name'] = '_ghoauth'
    context['oauth_cookie_secret'] = urlsafe_b64encode(os.urandom(16)).decode()

    context['ssl_crt'] = prompt('Enter the path to the SSL certificate: ', readFile=True)
    context['ssl_key'] = prompt('Enter the path to the SSL private key: ', readFile=True)

    return context

def main():
    context = prompt_for_user_vars()
    cluster_dir = os.path.join(clusters_dir, context['namespace'])
    step_dir = os.path.join(cluster_dir, "step3")
    try:
        os.makedirs(step_dir)
    except FileExistsError:
        pass
    for template in jinja_env.list_templates(filter_func=(lambda x:re.match('^step3/[0-9][^/]+$', x))):
        output = jinja_env.get_template(template).render(context)
        with open(os.path.join(cluster_dir, template), 'w') as output_file:
            print(output, file=output_file)
    print('\nSuccessfully generated cluster files.')
    print(f'kubeconfig files have been saved to {step_dir}')


if __name__ == "__main__":
    main()
