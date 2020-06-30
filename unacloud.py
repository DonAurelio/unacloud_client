#!/bin/python
import click
import requests
import os
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

def post_request(data,endpoint,query=''):
    url = get_url(endpoint=endpoint)

    try:
        response = requests.post(url,json=data)
        response.raise_for_status()
        data = response.json()
        message = data.get('message')
        click.echo(message)
    except requests.exceptions.ConnectionError as e:
        message = click.style(
            "API Server not available at: {}", fg="red"
        ).format(url)
        click.echo(message,err=True)

    except Exception as e:
        message = click.style(str(e),fg="red")
        click.echo(message,err=True)

def create_environment(name,provider,cpus,memory):
    data = {
        'name': name,
        'provider': provider,
        'cpus': cpus,
        'memory': memory
    }
    post_request(data=data,endpoint='/environment/create/')

def start_environment(name):
    data = {
        'environment_name': name,
        'action': 'start',
    }
    post_request(data=data,endpoint='/environment/action/')

def stop_environment(name):
    data = {
        'environment_name': name,
        'action': 'stop',
    }
    post_request(data=data,endpoint='/environment/action/')

def reset_environment(name):
    data = {
        'environment_name': name,
        'action': 'reset',
    }
    post_request(data=data,endpoint='/environment/action/')

def delete_environment(name):
    data = {
        'environment_name': name,
        'action': 'delete',
    }
    post_request(data=data,endpoint='/environment/action/')

def ssh_environment(name):
    endpoint = '/environment/environments/?name=%s' % name
    environment = get_request(endpoint=endpoint)

    if environment:
        address = environment[0].get('address')
        port = environment[0].get('ssh_port')

        if address and port:
            command = 'ssh -p %s unacloud@%s' % (address,port)
            os.system(command)
        else:
            click.echo("the environment does not have 'address' and 'port to ssh'")
            click.echo("probable the environment is not deployed yet")

    else:
        click.echo("environment '%s' not found !!" % name)

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

@environment.command(name='create')
@click.argument('name')
@click.option('--provider', default='virtualbox', help='environment virtualization provider')
@click.option('--cpus', default=2, help='number of cpus for the environment')
@click.option('--memory', default=2048, help='RAM memory in MB')
def environment_create(name,provider,cpus,memory):
    create_environment(name,provider,cpus,memory)

@environment.command(name='start')
@click.argument('name')
def environment_start(name):
    start_environment(name)

@environment.command(name='stop')
def environment_stop(name):
    stop_environment(name)

@environment.command(name='reset')
def environment_reset(name):
    stop_environment(name)

@environment.command(name='delete')
def environment_delete(name):
    delete_environment(name)

@environment.command(name='ssh')
def environment_ssh():
    ssh_environment(name)

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