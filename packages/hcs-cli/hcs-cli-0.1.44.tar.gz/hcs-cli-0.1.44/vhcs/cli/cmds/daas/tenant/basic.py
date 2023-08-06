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
from vhcs.support.daas import tenant

@click.command("list")
def list_tenants():
    """List tenant configurations"""
    return tenant.list()

@click.command()
@click.argument("text")
def find(text: str):
    """Get tenant by ID or customer name"""
    t = tenant.get(text)
    if t:
        return t
    return tenant.find_by_customer_name(text)


