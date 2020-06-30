#!/bin/python
import click
import requests
import pandas as pd


# API SERVER URL
API_SERVER_BASE_URL = 'http://localhost:8081/api'

def get_url(endpoint,query=''):
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

def get_environments():
    environments = get_request(endpoint='/environment/environments')
    return environments

def get_workers():
    workers = get_request(endpoint='/worker/workers')
    return workers

def get_actions():
    actions = get_request(endpoint='/environment/actions')
    return actions

def echo_as_table(data,headers):
    df = pd.DataFrame(data)
    print(df[headers].to_string(index=False,justify='left'))

@click.group()
def unacloud():
    pass

@unacloud.group()
def deployment():
    pass

@deployment.command(name='list')
def deployment_list():
    deployments = get_deployments()
    headers = ['id','environment_name','status','detail']
    echo_as_table(deployments,headers)

@unacloud.group()
def environment():
    pass

@environment.command(name='list')
def environment_list():
    environmets = get_environments()
    headers = [
        'id','name','provider','address','ssh_port',
        'cores','memory','status','worker_id'
    ]
    echo_as_table(environmets,headers)

@unacloud.group()
def worker():
    pass

@worker.command(name='list')
def worker_list():
    workers = get_workers()
    headers = ['id','address','cpus','memory','last_health_report_date']
    echo_as_table(workers,headers)

@unacloud.group()
def action():
    pass

@action.command(name='list')
def action_list():
    actions = get_actions()
    headers = ['id','action','environment_name','status','detail']
    echo_as_table(actions,headers)


if __name__ == '__main__':
    unacloud()