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

import click
import vhcs.common.ctxp as ctxp
from vhcs.common.ctxp import panic, choose
from vhcs.plan.provider.azure import _az_facade
from vhcs.support.daas import infra
from vhcs.service import admin


@click.command()
def plan():
    """Interactive setup for shared infrastructure."""
    
    data = infra.all()

    _select_provider(data['provider'])
    _input_azure_sp(data['provider'])
    _select_vnet(data['network'])

    infra.save(data)



def _select_provider(data):
    providers = admin.provider.list(label='azure')
    if not providers:
        panic("No provider configured. Configure in HCS admin console first.")

    fn_provider_text = lambda p: f"{p['providerDetails']['data']['region']}, {p['name']}/{p['id']}"

    if len(providers) == 1:
        p = providers[0]
        click.echo("There's only one provider configured, and will be used: " + fn_provider_text(p))
    else:
        p = choose("Select region and provider", providers, fn_provider_text)
        if not p:
            return
    data['id'] = p['id']

def _input_azure_sp(data):
    data['applicationId'] = click.prompt("Input Azure service principle application ID:", default=data['applicationId'])
    data['applicationSecret'] = click.prompt("Input Azure service principle application secret:", default=data['applicationSecret'])

def _select_vnet(data):
    vnets = _az_facade.list_vnets()
    fn_get_text = lambda vnet: f"{vnet['name']} ({','.join(vnet['addressSpace']['addressPrefixes'])})"
    selected = choose("Select vNet:", vnets, fn_get_text)
    data['vNetId'] = selected['id']
    data['tenantCIDRs'] = ctxp.util.input_array("Tenant CIDRs", default=data['tenantCIDRs'])