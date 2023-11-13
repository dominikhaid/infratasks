# Infratasks

Infratasks is a python package that contains operations and deploys for pyinfra.

## Projekt Structure 

### Inventories 
- Inventories are specific servers or devices groups
- See the example folder for more informations

### Deploys
- Deploys include serval operations

## Operations
- Operations are groud by package managers (apt, npm, ect.)

#### Debugging
- pyinfra INVENTORY debug-inventoy
- pyinfra INVENTORY server.user pyinfra home=/home/pyinfra

## Vairables  & Env

### Inventories
[
{server1:
     ops: {container: True}
     deploy: {dev_env : True}
  }
},
{server2:
  {
     deploy: wsl : True
  },
  {docker},
  {vagrant}
}
]  

### Groupe_vars
- pyinfra.config runs for each inventory such as ssh users
- variables accessible trough pyinfra.host.data

## TODOS
- Clean up Dotfiles and TODOS
- List deploys in CLI
- List operations in CLI
- @docker Connector
- Write tests
- Document Code

## Quickstart

Install pyinfra with [`pipx`](https://pipxproject.github.io/pipx/) (recommended) or `pip`:

### Install

```sh
python3 -m venv .venv
source .venv/bin/activate
## Build
python3 -m pip install .
## Test
pyinfra @local exec -- echo "hello world"
pyinfra @docker/ubuntu exec -- echo "Hello world"

## Uninstall
python3 setup.py clean --all
python3 -m pip uninstall infratasks
# install pyinfra systemwide pipx install pyinfra
```

```sh
# Only execute against @zshlocal
pyinfra inventory.py deploy.py --limit @local

# Only execute against hosts in the `app_servers` grouo
pyinfra inventory.py deploy.py --limit app_servers

# Only execute against hosts with names matching db*
pyinfra inventory.py deploy.py --limit "db*"

# Combine multiple limits
pyinfra inventory.py deploy.py --limit app_servers --limit db-1.net
```
