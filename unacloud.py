#!/bin/python
import click
import requests


# API SERVER URL
API_SERVER_BASE_URL = 'http://localhost:8081/api'

def get_url(endpoint,query=''):
    endpoint = '/environment/deployments'
    url = API_SERVER_BASE_URL + endpoint + ''
    return url

def get_request(endpoint,query=''):
    url = get_url(endpoint=endpoint)
    data = None
    try:
        
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.ConnectionError as e:
        message = click.style(
            "API Server not available at: {}", fg="red"
        ).format(url)
        click.echo(message,err=True)

    return data

def get_deployments():
    deployments = get_request(endpoint='/environment/deployments')
    return deployments

def echo_as_table(data,*headers):
    lower_headers = list(map(lambda x:x.lower(),headers))
    header_format = "{:<20} " * len(lower_headers)
    header_str = header_format.format(*headers)

    # Print header
    click.echo(header_str)

    for datum in data:
        # Reordering data to match the headers positions
        reordered = {k: datum[k] for k in lower_headers}
        values = reordered.values()
        click.echo(header_format.format(*values))

@click.group()
def unacloud():
    pass

@unacloud.group()
def deployment():
    pass

@deployment.command(name='list')
def deployment_list():
    deployments = get_deployments()

    headers = ['ID','ENVIRONMENT_NAME','STATUS','DETAIL']
    echo_as_table(deployments,*headers)

@unacloud.command()
def environmet():
    pass

@unacloud.command()
def action():
    pass

if __name__ == '__main__':
    unacloud()