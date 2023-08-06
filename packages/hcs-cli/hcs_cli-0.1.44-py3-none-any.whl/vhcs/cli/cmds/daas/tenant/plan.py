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

import yaml
import click
from vhcs.service import admin, ims_catalog
from vhcs.common.ctxp import choose, util as cli_util
from vhcs.common import util as data_util
from vhcs.support.daas import infra, template


_surfix = '.plan.yml'

@click.command()
@click.argument("name", type=str, required=True)
def plan(name: str):
    """Interactive command to request a DaaS tenant"""
    
    if name.endswith(_surfix):
        name = name[:-len(_surfix)]

    data = _load_data(name)
    
    vars = data['vars']
    _config_desktop(vars)
    _input_user_emails(vars)

    _save_plan(data)

def _save_plan(vars):
    deployment_id = vars['deploymentId']
    file_name = _get_file_name(deployment_id)
    blueprint_file = 'v1/tenant.blueprint.yml'
    blueprint = template.get(blueprint_file)
    text = "\n".join([
        yaml.safe_dump(vars, sort_keys=False),
        "",
        "# ----------------------------------",
        "# Blueprint: " + blueprint_file,
        "",
        yaml.safe_dump(blueprint, sort_keys=False)
    ])

    with open(file_name, "w") as file:
        file.write(text)

    print("Plan saved as file: " + file_name)
    print(f"To deploy the plan, use 'hcs plan deploy --file {file_name}'")

def _load_data(deployment_id):

    data = template.get('v1/tenant.vars.yml')
    if not data['deploymentId']:
        data['deploymentId'] = deployment_id
    data['vars']['orgId'] = _get_org_id()

    _apply_previous_input(data, deployment_id)

    # Add defaults from shared infra config, if anything missing
    data_util.deep_apply_defaults(data['vars'], infra.all())

    return data

def _apply_previous_input(data: dict, tenant_id: str):
    file_name = _get_file_name(tenant_id)
    prev = data_util.load_data_file(file_name)
    if not prev:
        return
    prev_vars = prev.get('vars')
    if not prev_vars:
        return
    
    data_util.deep_apply_defaults(data['vars'], prev_vars)

def _get_org_id():
    from vhcs.common.sglib import auth
    auth_info = auth.details(get_org_details=False)
    return auth_info.org.id

def _get_file_name(customer_id: str) -> str:
    return customer_id + '.plan.yml'


def _config_desktop(data):

    def _select_image_and_vm_sku(data):
        images = ims_catalog.helper.get_images_by_provider_instance_with_asset_details(data['provider']['id'])
        fn_get_text = lambda d: f"{d['name']}: {d['description']}"
        prev_selected_image = None
        if data['desktop']['streamId']:
            for i in images:
                if i['id'] == data['desktop']['streamId']:
                    prev_selected_image = i
                    break
        selected_image = choose("Select image:", images, fn_get_text, selected=prev_selected_image)
        data['desktop']['streamId'] = selected_image['id']

        fn_get_text = lambda m: f"{m['name']}"
        selected_marker = choose("Select marker:", selected_image['markers'], fn_get_text)
        data['desktop']['markerId'] = selected_marker['id']

        image_asset_details = selected_image['_assetDetails']['data']

        search = f"capabilities.HyperVGenerations $in {image_asset_details['generationType']}"
        vm_skus = admin.azure_infra.get_compute_vm_skus(data['provider']['id'], limit=200, search=search)
        prev_selected_vm_sku = None
        if data['desktop']['vmSkuName']:
            selected_vm_sku_name = data['desktop']['vmSkuName']
        else:
            selected_vm_sku_name = image_asset_details['vmSize']
        if selected_vm_sku_name:
            for sku in vm_skus:
                if sku['id'] == selected_vm_sku_name:
                    prev_selected_vm_sku = sku
                    break

        fn_get_text = lambda d: f"{d['data']['name']} (CPU: {d['data']['capabilities']['vCPUs']}, RAM: {d['data']['capabilities']['MemoryGB']})"

        selected = choose("Select VM size:", vm_skus, fn_get_text, selected=prev_selected_vm_sku)
        data['desktop']['vmSkuName'] = selected['data']['name']

    def _select_desktop_type(data):
        types = ['MULTI_SESSION', 'FLOATING']
        data['desktop']['templateType'] = choose("Desktop type:", types)


    _select_image_and_vm_sku(data)
    _select_desktop_type(data)

def _input_user_emails(data):
    data['userEmails'] = cli_util.input_array("User emails", default=data['userEmails'])
