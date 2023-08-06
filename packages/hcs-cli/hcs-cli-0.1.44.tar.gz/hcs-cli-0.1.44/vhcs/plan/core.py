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

import threading
import traceback
import typing
import inspect
import time
import re
from subprocess import CalledProcessError
from copy import deepcopy
import vhcs.common.util as util
from . import helper
from . import dag
from .helper import PlanException
from importlib import import_module

import logging
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

def _prepare_data(data: dict, additional_context: dict):
    if additional_context:
        common_items = util.get_common_items(additional_context.keys(), data.keys())
        if common_items:
            raise PlanException("blueprint and context have conflict keys: " + str(common_items))
        data.update(additional_context)
    blueprint, pending = helper.process_template(data)
    deployment_id = blueprint['deploymentId']
    state_file = deployment_id + '.state.yml'
    prev = _load_state(state_file)
    state = {'pending': pending}
    state.update(blueprint)
    state.update(prev)
    state['log']['deploy'] = []    # clear log
    
    return blueprint, state, state_file

def deploy(data: dict, resource_name: str = None, concurrency: int = 4, additional_context: dict = None):
    
    blueprint, state, state_file = _prepare_data(data, additional_context)

    def process_resource(name: str, res_data: dict):
        if name == 'defaults':
            return
        if res_data.get('type'):    #provider
            return
        
        _deploy_res(name, res_data, state)
        _resolve_pending_keys(blueprint, state, name)
        if resource_name and name == resource_name:
            return False

    try:
        dag.process_blueprint(blueprint, process_resource, concurrency)
    except CalledProcessError as e:
        raise PlanException(str(e))
    finally:
        util.save_data_file(state, state_file)

def _load_state(state_file):
    state = util.load_data_file(state_file, default={})
    if 'output' not in state:
        state['output'] = {}
    if 'destroy_output' not in state:
        state['destroy_output'] = {}
    if 'log' not in state:
        state['log'] = {}
    exec_log = state['log']
    if 'deploy' not in exec_log:
        exec_log['deploy'] = []
    if 'destroy' not in exec_log:
        exec_log['destroy'] = []
    return state

def _parse_statement_for(name, state) -> typing.Tuple[str, list]:
    # for: email in vars.userEmails
    res = state['resources'][name]
    for_statement = res.get('for')
    if not for_statement:
        return None, None
    pattern = r'(.+?)\s+in\s+(.+)'
    matcher = re.search(pattern, for_statement)

    def _raise_error(reason):
        raise PlanException(f"Invalid for statement: {reason}. Resource={name}, statement={for_statement}")
    
    if not matcher:
        _raise_error('Invalid syntax')
    var_name = matcher.group(1)
    values_name = matcher.group(2)
    values = _get_value_by_path(state, values_name, f"resources.{name}.for")
    if not isinstance(values, list):
        reason = 'The referencing value is not a list. Actual type=' + type(values).__name__
        _raise_error(reason)

    return var_name, values

def _get_value_by_path(state, var_name, required_by_attr_path):
    i = var_name.find('.')
    if i < 0:
        resource_name = var_name
    else:
        resource_name = var_name[:i]

    if resource_name in state['resources']:
        try:
            return util.deep_get_attr(state, "output." + var_name)
        except:
            raise PlanException(f"Plugin error: '{var_name}' does not exist in the output of resource '{resource_name}', which is required by '{required_by_attr_path}'")

    if resource_name in state:
        try:
            return util.deep_get_attr(state, var_name)
        except:
            raise PlanException(f"Plugin error: '{var_name}' does not exist in the output of resource '{resource_name}', which is required by '{required_by_attr_path}'")


def _deploy_res(name, res, state):
    def add_log(action: str, details: str = None):
        _add_log(state, 'deploy', res['kind'], name, action, details)

    def fn_deploy1(handler, res_data, res_state, fn_set_state):
        if res_state:
            add_log('skipped')
            return
        
        add_log('start')
        if _has_save_state(handler.deploy):
            new_state = handler.deploy(res_data, fn_set_state)
        else:
            new_state = handler.deploy(res_data)
        if new_state:
            fn_set_state(new_state)
        add_log('success')
    
    _handle_resource(name, res, state, True, add_log, fn_deploy1)

def _has_save_state(fn):
    signature = inspect.signature(fn)
    args = list(signature.parameters.keys())
    if len(args) < 2:
        return False
    name = args[1]
    if name == 'save_state':
        return True
    p = signature.parameters[args[1]]
    return p.annotation == typing.Callable
    
# def _convert_resource_path_to_readable_path(state, attr_path: str):
#     pattern = r'resources\[(\d+)\]\..+'
#     match = re.search(pattern, attr_path)
#     if match:
#         i = int(match.group(1))
#         name = state['resources'][i]['name']
#         n = attr_path.index(']')
#         readable_path = 'resources.' + name + attr_path[n + 1:]
#         return readable_path
#     return attr_path

def _resolve_pending_keys(blueprint, state, resource_name):
    prefix = resource_name + "."
    for attr_path, var_name in state['pending'].items():
        if not var_name.startswith(prefix) and var_name != resource_name:
            continue
        # found a key to solve
        
        # update that key
        expr = util.deep_get_attr(blueprint, attr_path)
        def _get_value(path):
            return _get_value_by_path(state, path, attr_path), True
        resolved_value, _pending_var = util.resolve_expression(expr, _get_value)

        log.debug('Resolved. %s: %s -> %s', attr_path, var_name, resolved_value)
        util.deep_set_attr(blueprint, attr_path, resolved_value)

def _assert_all_vars_resolved(data, name):
    def fn_on_value(path, value):
        if isinstance(value, str) and value.find('${') >= 0:
            raise PlanException(f"Unresolved variable '{path}' for plugin '{name}'. Value={value}")
        return value
    util.deep_update_object_value(data, fn_on_value)

_providers = {}
_provider_lock = threading.Lock()
def _get_resource_handler(kind: str, state: dict):
    provider_type, res_handler_type = kind.split('/')
    res_handler_type = res_handler_type.replace('-', '_')
    # Ensure provider initialized
    with _provider_lock:
        if not provider_type in _providers:
            provider = import_module("vhcs.plan.provider." + provider_type)
            # Get provider data
            filter_by_type = lambda m: m['type'] == provider_type
            providers = state.get('providers', {})
            meta = next(filter(filter_by_type, providers), None)
            data = meta.get('data') if meta else None
            if data:
                _assert_all_vars_resolved(data, provider_type)
            log.info("[init] Provider: %s", provider_type)
            state['output'][provider_type] = provider.prepare(data)
            log.info("[ok  ] Provider: %s", provider_type)
            _providers[provider_type] = 1

    module_name = f"vhcs.plan.provider.{provider_type}.{res_handler_type}"
    return import_module(module_name)

def get_common_items(iter1, iter2):
    return set(iter1).intersection(set(iter2))

def _handle_resource(name, res, state, vars_must_resolve: bool, add_log: typing.Callable, fn_process: typing.Callable):
    try:
        kind = res['kind']
        data = res.get('data', {})
        if data:
            if vars_must_resolve:
                _assert_all_vars_resolved(data, name)

        handler = _get_resource_handler(kind, state)
        def _handle_resource_1(resource_data, resource_state, fn_set_state):
            if _is_runtime(kind):   # runtime has no refresh
                pass
            else:
                new_state = handler.refresh(resource_data, resource_state)
                if new_state:
                    fn_set_state(new_state)
                    resource_state = new_state

            fn_process(handler, resource_data, resource_state, fn_set_state)

        for_var_name, values = _parse_statement_for(name, state)
        if for_var_name:
            if for_var_name in data:
                raise PlanException(f"Invalid blueprint: variable name defined in for-statement already exists in data declaration. Resource: {name}. Conflicting names: {common}")
            
            size = len(values)
            # ensure output array placeholder
            output = state['output'].setdefault(name, [])
            while len(output) < size:
                output.append(None)
            for i in range(size):
                v = values[i]
                resource_state = output[i]
                def _fn_set_state(o):
                    output[i] = deepcopy(o)
                resource_data = deepcopy(data)
                resource_data[for_var_name] = v
                _handle_resource_1(resource_data, resource_state, _fn_set_state)
        else:
            resource_state = state['output'].get(name)
            def _fn_set_state(o):
                state['output'][name] = deepcopy(o)
            resource_data = deepcopy(data)
            _handle_resource_1(resource_data, resource_state, _fn_set_state)
    except Exception as e:
        add_log('error', e)
        raise

    
def _add_log(state: dict, mode: str, kind: str, name: str, action: str, details = None):
    if mode == 'deploy':
        labels = {
            'start':   '[creating]',
            'success': '[created ]',
            'skipped': '[skipped ]',
            'error':   '[error   ]'
        }
    elif mode == 'destroy':
        labels = {
            'start':   '[deleting]',
            'success': '[deleted ]',
            'skipped': '[skipped ]',
            'error':   '[error   ]'
        }
    else:
        raise PlanException("Invalid log mode: " + mode)
    log.info(f'{labels[action]} {kind}:{name}')
    entry = {
        'name': name,
        'time': time.time(),
        'action': action
    }
    if details:
        if isinstance(details, Exception):
            if isinstance(details, PlanException):
                pass
            else:
                e = details
                traceback.print_exception(type(e), e, e.__traceback__)
            details = details.__class__.__name__ + ': ' + str(details)
        else:
            details = str(details)
        entry['details'] = details
    state['log'][mode].append(entry)
    if action == 'error':
        log.warning('Plugin "%s:%s" failed: %s', kind, name, details)


def _destroy_res(name, res, state, force):
    def add_log(action: str, details: str = None):
        _add_log(state, 'destroy', res['kind'], name, action, details)

    def fn_destroy1(handler, res_data, res_state, fn_set_state):
        if not res_state:
            add_log('skipped', 'Not found')
            return
        
        add_log('start')
        try:
            ret = handler.destroy(res_data, res_state)
            state['destroy_output'][name] = deepcopy(ret)
            fn_set_state(None)
            add_log('success', 'Deleted')
        except Exception as e:
            if force:
                add_log('error', e)
                pass
            else:
                # add_log('error', e) will be handled by framework.
                raise

    _handle_resource(name, res, state, False, add_log, fn_destroy1)

def _is_runtime(kind: str):
    return kind.startswith('runtime/')

def destroy(data, force: bool, resource_name: str = None, concurrency: int = 4, additional_context: dict = None):
    
    blueprint, state, state_file = _prepare_data(data, additional_context)

    def destroy_resource(node_name, node):
        # skip provider
        if 'type' in node:  
            return
        kind = node.get('kind')
        # skip non-resources, e.g. 'defaults'
        if not kind:
            return
        # skip runtime
        if kind.startswith('runtime/'):
            return
        
        res = state['resources'].get(node_name)
        if not res:
            res = blueprint['resources'][node_name]
        _destroy_res(node_name, res, state, force)
        if resource_name and resource_name == node_name:
            return True

    try:
        dag.reverse_traverse(blueprint, destroy_resource)
    except CalledProcessError as e:
        raise PlanException(str(e))
    finally:
        util.save_data_file(state, state_file)

