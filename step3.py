#!/usr/bin/env python3

from util import prompt, base64, random_token
import os
import re
from jinja2 import Environment, FileSystemLoader

dirname = os.path.dirname(__file__)
template_dir = os.path.join(dirname, 'templates')
clusters_dir = os.path.join(dirname, 'clusters')
jinja_env = Environment(loader=FileSystemLoader(template_dir))
jinja_env.filters['b64encode'] = base64

def prompt_for_user_vars():
    context = {}
    context['namespace'] = prompt('Enter the same namespace from step 1',
        '^[a-z][-a-z0-9]{1,19}$',
        'my-es-cluster')
    context['github_org'] = prompt('Enter the GitHub org')
    context['github_team'] = prompt('Enter the GitHub team')
    context['oauth_client_id'] = prompt('Enter the OAuth Client ID')
    context['oauth_client_secret'] = prompt('Enter the OAuth Client Secret')
    context['oauth_cookie_name'] = '_ghoauth'
    context['oauth_cookie_secret'] = random_token()

    context['ssl_crt'] = prompt('Enter the path to the SSL certificate', readFile=True)
    context['ssl_key'] = prompt('Enter the path to the SSL private key', readFile=True)

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
