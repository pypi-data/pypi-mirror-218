"""
Copyright 2023-2023 VMware Inc.
SPDX-License-Identifier: Apache-2.0

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import subprocess
import json
import logging

log = logging.getLogger(__name__)

def _az(command: str, check=True) -> dict:
    log.debug(command)
    args = command.split(' ')
    try:
        completed_process = subprocess.run(args, stdout=subprocess.PIPE, timeout=None, check=check)
        output = completed_process.stdout
        if output and completed_process.returncode == 0:
            try:
                return json.loads(output)
            except Exception as e:
                log.error("Fail parsing response %s", e)
                log.warning("Payload: %s", output)
    except subprocess.CalledProcessError as e:
        raise

def login(username: str, password: str, tenant_id: str):
    return _az(f"az login --service-principal -u {username} -p {password} --tenant {tenant_id}")

def _formalize_tags(tags: list[str]) -> str:
    if not tags:
        tags = []
    tags.append('managed-by=titan-lite')
    return ' '.join(tags)

def set_subscription(id: str):
    return _az(f"az account set --subscription {id}")

def list_vnets():
    return _az("az network vnet list")

def create_resource_group(name: str, location: str, tags: list = None):
    tags_str = _formalize_tags(tags)
    return _az(f"az group create --location {location} --name {name} --tags {tags_str}")

def delete_resource_group(name: str):
    exists = _az(f"az group exists --name {name}")
    if exists:
        _az(f"az group delete --name {name} --yes")
        return True
    return False

class _aad_group:
    @staticmethod
    def create(display_name: str, mail_nickname: str, description: str = None):
        cmd = f"az ad group create --display-name {display_name} --mail-nickname {mail_nickname}"
        if description:
            cmd += f" --description {description}"
        return _az(cmd)

    @staticmethod
    def get(id_or_display_name: str):
        return _az(f"az ad group show --group {id_or_display_name}", check=False)

    @staticmethod
    def delete(id_or_display_name: str):
        return _az(f"az ad group delete --group {id_or_display_name}")

    @staticmethod
    def list_members():
        pass

    @staticmethod
    def add_member(id_or_display_name: str, member_id: str):
        return _az(f"az ad group member add --group {id_or_display_name} --member-id {member_id}")

class _aad_user:
    @staticmethod
    def create(display_name: str, password: str, principal_name: str):
        return _az(f"az ad user create --display-name {display_name} --password {password} --user-principal-name {principal_name}")
    
    @staticmethod
    def get(id_or_principal_name: str):
        return _az(f"az ad user show --id {id_or_principal_name}", check=False)

    @staticmethod
    def delete(id: str):
        return _az(f"az ad user delete --id {id}")


class aad:
    group = _aad_group
    user = _aad_user
    




def get_vnet(id: str):
    return _az(f"az network vnet show --ids {id}")

def create_nsg(rg_name: str, name: str, location: str, tags: list[str] = None):
    tags_str = _formalize_tags(tags)
    return _az(f"az network nsg create -g {rg_name} -n {name} --location {location} --tags {tags_str}")

def delete_nsg_by_id(id: str):
    return _az(f"az network nsg delete --ids {id}")

def delete_nsg(rg_name: str, name: str):
    return _az(f"az network nsg delete -g {rg_name} -n {name}")

def create_subnet(rg_name: str, vnet_name: str, name: str, cidr: str, nsg_name: str):
    return _az(f"az network vnet subnet create -g {rg_name} --vnet-name {vnet_name} -n {name} --address-prefixes {cidr} --network-security-group {nsg_name}")

def delete_subnet_by_id(id: str):
    return _az(f"az network vnet subnet delete --ids {id}")

def delete_subnet(rg_name: str, vnet_name: str, name: str):
    return _az(f"az network vnet subnet delete -g {rg_name} --vnet-name {vnet_name} -n {name}")