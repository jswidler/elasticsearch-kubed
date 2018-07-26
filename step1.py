#!/usr/bin/env python3

import os
import re
from jinja2 import Environment, FileSystemLoader

dirname = os.path.dirname(__file__)
template_dir = os.path.join(dirname, 'templates')
clusters_dir = os.path.join(dirname, 'clusters')
jinja_env = Environment(loader=FileSystemLoader(template_dir))

data_node_configs = {
    'minikube': {
        'replicas': '2',
        'storage_class': 'standard',
        'heap_size': '512m',
        'memory_limit': '1Gi'
    },
    '4cpu X 3': {
        'replicas': '3',
        'storage_class': 'ssd',
        'heap_size': '4g',
        'memory_limit': '8Gi'
    },
    '8cpu X 3': {
        'replicas': '3',
        'storage_class': 'ssd',
        'heap_size': '8g',
        'memory_limit': '16Gi'
    },
    '16cpu X 3': {
        'replicas': '3',
        'storage_class': 'ssd',
        'heap_size': '20g',
        'memory_limit': '40Gi'
    }
}

def prompt(msg, regex):
    result = input(msg)
    if not re.match(regex, result):
        raise ValueError(f"expect response to match the regex '{regex}'.")
    return result

def prompt_for_user_vars():
    context = {}
    context['namespace'] = prompt(
        'Enter a namespace for the elasticsearch cluster: ',
        '^[a-z][-a-z0-9]{1,19}$'
    )
    print('Select the node size: ')
    for i, key in enumerate(data_node_configs):
        print(f'{i+1}: {key}')
    config_count = len(data_node_configs)
    node_size_choice = int(prompt(
        f'[1-{config_count}]: ',
        f'^[1-{config_count}]$'
    ))
    context['data_node'] = data_node_configs[list(data_node_configs.keys())[node_size_choice-1]]
    context['data_node']['volume_size'] = prompt(
        'Enter the data volume size in GB [10-9999]: ',
        '^[1-9][0-9]{1,3}$'
    )
    return context

def main():
    print('These scripts will create kubeconfig files to set up an elasticsearch cluster in Kubernetes.')

    context = prompt_for_user_vars()
    cluster_dir = os.path.join(clusters_dir, context['namespace'])
    step_dir = os.path.join(cluster_dir, "step1")
    try:
        os.makedirs(step_dir)
    except FileExistsError:
        pass
    for template in jinja_env.list_templates(filter_func=(lambda x:re.match('^step1/[0-9][^/]+$', x))):
        output = jinja_env.get_template(template).render(context)
        with open(os.path.join(cluster_dir, template), 'w') as output_file:
            print(output, file=output_file)
    print('\nSuccessfully generated cluster files.')
    print(f'kubeconfig files have been saved to {step_dir}')


if __name__ == "__main__":
    main()
