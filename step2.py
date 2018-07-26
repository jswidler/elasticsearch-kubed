#!/usr/bin/env python3

import os
import re
import subprocess
from base64 import b64encode
base64 = lambda s: b64encode(s.encode()).decode()
from jinja2 import Environment, FileSystemLoader
import shutil

dirname = os.path.dirname(__file__)
template_dir = os.path.join(dirname, 'templates')
clusters_dir = os.path.join(dirname, 'clusters')
jinja_env = Environment(loader=FileSystemLoader(template_dir))
jinja_env.filters['b64encode'] = base64

def prompt(msg, regex='.*', default=None):
    result = input(msg)
    if not result and default:
        return default
    if not re.match(regex, result):
        raise ValueError(f"expect response to match the regex '{regex}'.")
    return result

def check_cert_presence(cert_dir):
    files = ['ca.crt', 'ca.key', 'logstash.crt', 'logstash.key']
    for file in files:
        fname = os.path.join(cert_dir, file)
        if not os.path.isfile(fname):
            return False
    return True

def gen_logstash_certs(cert_dir):
    if not check_cert_presence(cert_dir):
        print("Setting up logstash with TLS authenication requires private keys and public certificates.")
        print("To generate the certificates, provide the following information: ")
        ca_name = prompt("Certificate Authority Name (default: 'Logstash CA'): ", default='Logstash CA')
        url = prompt("CN - Logstash Common Name (default: 'logstash.my-domain.com'): ",
            regex='^[a-zA-Z.-0-9]+$',
            default='logstash.my-domain.com'
        )
        country = prompt("C - Country Code (default: 'US'): ",
            regex='[A-Z]{1,4}',
            default='US'
        )
        state = prompt("ST - State (default: 'CA'): ",
            regex='[A-Z]{1,4}',
            default='CA'
        )
        loc = prompt("L - Loc / City (default: 'San Francisco'): ",
            regex='[A-Za-z 0-9-_.]+',
            default='San Francisco'
        )
        org = prompt("O - Org (default: 'Acme'): ",
            regex='[A-Za-z 0-9-_.]+',
            default='Acme'
        )
        org_unit = prompt("OU - Org Unit (default: 'Computers'): ",
            regex='[A-Za-z 0-9-_.]+',
            default='Computers'
        )
        try:
            os.makedirs(cert_dir)
        except FileExistsError:
            pass
        subprocess.run([
            os.path.join(dirname, 'templates', 'step2', 'ssl-gen.sh'),
            ca_name, url, country, state, loc, org, org_unit, cert_dir
        ], check=True)
        if not check_cert_presence(cert_dir):
            raise RuntimeError('certs failed to generate')

def prompt_for_user_vars():
    context = {}
    context['namespace'] = prompt('Enter the same namespace from step 1: ',
        '^[a-z][-a-z0-9]{1,19}$'')
    context['logstash_beats_port'] = '8751'
    cert_dir = os.path.join(clusters_dir, context['namespace'], "step2", "self-signed-certs")
    gen_logstash_certs(cert_dir)
    shutil.copytree(cert_dir, os.path.join(template_dir, 'secrets'))
    return context

def main():
    context = prompt_for_user_vars()
    cluster_dir = os.path.join(clusters_dir, context['namespace'])
    step_dir = os.path.join(cluster_dir, "step2")
    try:
        os.makedirs(step_dir)
    except FileExistsError:
        pass
    for template in jinja_env.list_templates(filter_func=(lambda x:re.match('^step2/[0-9][^/]+$', x))):
        output = jinja_env.get_template(template).render(context)
        with open(os.path.join(cluster_dir, template), 'w') as output_file:
            print(output, file=output_file)
    # The files are still in the clusters/namespace/step2/self-signed-certs directory
    # This removes a temporary copy in the template directory
    shutil.rmtree(os.path.join(template_dir, 'secrets'))
    print('\nSuccessfully generated cluster files.')
    print(f'kubeconfig files have been saved to {step_dir}')


if __name__ == "__main__":
    main()
