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

import time
import threading
from graphlib import TopologicalSorter
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Callable
from vhcs.common import util

class Node:
    id: str
    dependencies: list[str] = []
    data: Any = None

class DAG:
    graph: dict[str, set[str]] = {}
    data: dict[str, Any] = {}

    def add(self, id: str, data: Any, dependencies = None):
        if id in self.data:
            raise Exception('Node already added to graph: ' + id)
        self.data[id] = data
        self.graph[id] = set(dependencies) if dependencies else set()


    def validate(self):
        all_keys = self.data.keys()
        for k, v in self.graph.items():
            for d in v:
                if d not in all_keys:
                    raise Exception(f"Blueprint error: target dpendency not found: from={k}, target={d}")
    
def process_blueprint(blueprint, fn_process_node: Callable, concurrency: int = 3):
    dag = _build_graph(blueprint)
    return _walkthrough(dag, fn_process_node, concurrency)

def reverse_traverse(blueprint, fn_process_node):
    # TODO: this is sequential so far
    dag = _build_graph(blueprint)
    dag.validate()

    topological_sorter = TopologicalSorter(dag.graph)
    sequence = list(topological_sorter.static_order())
    sequence.reverse()

    for node_name in sequence:
        stop = fn_process_node(node_name, dag.data[node_name])
        if stop == True:
            break

def _build_graph(blueprint):
    dag = DAG()

    def add_node(name, obj):
        data = obj.get('data')
        dependencies = set()
        if data:
            variables = util.deep_find_variables(data)
            for v in variables:
                i = v.find('.')
                resource_name = v if i < 0 else v[:i]
                dependencies.add(resource_name)
        after = obj.get('after')
        if after:
            def _add(t):
                if t in dependencies:
                    raise Exception("Invalid blueprint: statement after contains a dependency that is already implicitly created. This is not necessary. Key: " + t)
                dependencies.add(t)
            if isinstance(after, str):
                _add(after)
            else:
                for v in after:
                    _add(v)
        dag.add(name, obj, dependencies)
    
    for k,v in blueprint['resources'].items():
        add_node(k, v)
    defaults = blueprint.get('defaults')
    if defaults:
        add_node('defaults', defaults)
    providers = blueprint.get('providers')
    if providers:
        for p in providers:
            add_node(p['type'], p)
    return dag

def _walkthrough(dag: DAG, fn_process_node: Callable, concurrency: int):

    dag.validate()

    topological_sorter = TopologicalSorter(dag.graph)
    topological_sorter.prepare()
    lock = threading.Lock()

    flags = {
        'err': None,
        'stop': False
    }

    def process_node(node_id):
        err = None
        try:
            ret = fn_process_node(node_id, dag.data[node_id])
            if ret == False:
                flags['stop'] = True
        except Exception as e:
            err = e

        with lock:
            if err:
                flags['err'] = err
            else:
                topological_sorter.done(node_id)

    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        while topological_sorter.is_active():
            with lock:
                if flags['err'] or flags['stop']:
                    break
                read_nodes = topological_sorter.get_ready()
            if not len(read_nodes):
                time.sleep(1)
                continue
            for node in read_nodes:
                executor.submit(process_node, node)
        executor.shutdown(wait=True)
        if flags['err']:
            raise flags['err']

# dag = DAG()
# dag.add("b", "b")
# dag.add("a", "a", {"b", "c"})
# dag.add("c", "c")

# def fn_proc(id, data):
#     print("processing", id, data)
#     import time
#     import random
#     time.sleep(random.randint(0, 2))
#     raise Exception('demo error')

# _walkthrough(dag, fn_proc, 1)
# print('exit')