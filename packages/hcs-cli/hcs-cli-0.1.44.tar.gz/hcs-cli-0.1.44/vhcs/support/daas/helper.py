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
from vhcs.plan.provider.azure import _az_facade as az
from vhcs.service import admin
log = logging.getLogger(__file__)

def prep_az_cli(tenant_request):
    provider = tenant_request['provider']
    providerInstanceId = provider['providerInstanceId']
    print('Provider:', providerInstanceId)
    providerInstance = admin.provider.get('azure', providerInstanceId)
    subscription_id = providerInstance['providerDetails']['data']['subscriptionId']
    directory_id = providerInstance['providerDetails']['data']['directoryId']
    application_id = providerInstance['providerDetails']['data']['applicationId']
    region = providerInstance['providerDetails']['data']['region']
    print('Subscription:', subscription_id)
    print('Directory:', directory_id)
    print('ApplicationId:', application_id)
    print('Region:', region)
    if application_id != provider['applicationId']:
        log.warning("Configured application ID for CLI does not match application ID for provider.")
    
    az.login(provider['applicationId'], provider['applicationSecret'], directory_id)
    az.set_subscription(subscription_id)

