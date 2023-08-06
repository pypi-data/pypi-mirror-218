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
import logging
import vhcs.service.admin as admin
from vhcs.plan.provider.azure import _az_facade as az
from vhcs.plan import PlanException

log = logging.getLogger(__name__)

def deploy(data: dict) -> dict:
    provider = data['provider']
    providerInstanceId = provider['providerInstanceId']
    log.info('Provider: %s', providerInstanceId)
    providerInstance = admin.provider.get('azure', providerInstanceId)
    if not providerInstance:
        raise PlanException('Provider not found: ' + providerInstanceId)
    subscription_id = providerInstance['providerDetails']['data']['subscriptionId']
    directory_id = providerInstance['providerDetails']['data']['directoryId']
    application_id = providerInstance['providerDetails']['data']['applicationId']
    region = providerInstance['providerDetails']['data']['region']
    log.info('Subscription: %s', subscription_id)
    log.info('Directory: %s', directory_id)
    log.info('ApplicationId: %s', application_id)
    log.info('Region: %s', region)

    return {
        'location': 'westus2',
        'cidr': _calculate_cidr(),
        'vNet': az.get_vnet(data['network']['vNetId']),
        'providerInstance': providerInstance
    }

def _calculate_cidr():
    #TODO
    cidr = "10.200.1.0/24"
    return cidr

def destroy(data: dict, prev: dict):
    return