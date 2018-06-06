#!/usr/bin/env python
#coding:utf-8
#author: moorewqk@163.com
#date:
#以下代码可以实现ansible结果返回Json对象，便于数据处理。
# （可以配合前端勾选主机，随意组成Ansible动态主机），这样也可以通过setup模块加上自定义模块，来实现收集服务器硬件信息。

#import os, sys, time, datetime, commands

import json,sys,os
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory,Host,Group
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase
from ansible.executor.playbook_executor import PlaybookExecutor


class MyInventory(Inventory):
    def __init__(self, resource, loader, variable_manager):
        self.resource = resource
        self.inventory = Inventory(loader=loader, variable_manager=variable_manager, host_list=[])
        self.dynamic_inventory()

    def add_dynamic_group(self, hosts, groupname, groupvars=None):
        my_group = Group(name=groupname)
        if groupvars:
            for key, value in groupvars.iteritems():
                my_group.set_variable(key, value)
        for host in hosts:
            # set connection variables
            hostname = host.get("hostname")
            hostip = host.get('ip', hostname)
            hostport = host.get("port")
            username = host.get("username")
            password = host.get("password")
            ssh_key = host.get("ssh_key")
            my_host = Host(name=hostname, port=hostport)
            my_host.set_variable('ansible_ssh_host', hostip)
            my_host.set_variable('ansible_ssh_port', hostport)
            my_host.set_variable('ansible_ssh_user', username)
            my_host.set_variable('ansible_ssh_pass', password)
            my_host.set_variable('ansible_ssh_private_key_file', ssh_key)
            for key, value in host.iteritems():
                if key not in ["hostname", "port", "username", "password"]:
                    my_host.set_variable(key, value)
            my_group.add_host(my_host)

        self.inventory.add_group(my_group)

    def dynamic_inventory(self):
        if isinstance(self.resource, list):
            self.add_dynamic_group(self.resource, 'default_group')
        elif isinstance(self.resource, dict):
            for groupname, hosts_and_vars in self.resource.iteritems():
                print "bbbbbbbb",groupname,hosts_and_vars
                self.add_dynamic_group(hosts_and_vars.get("hosts"), groupname, hosts_and_vars.get("vars"))


class ModelResultsCollector(CallbackBase):

    def __init__(self, *args, **kwargs):
        super(ModelResultsCollector, self).__init__(*args, **kwargs)
        self.host_ok = {}
        self.host_unreachable = {}
        self.host_failed = {}

    def v2_runner_on_unreachable(self, result):
        self.host_unreachable[result._host.get_name()] = result

    def v2_runner_on_ok(self, result,  *args, **kwargs):
        self.host_ok[result._host.get_name()] = result

    def v2_runner_on_failed(self, result,  *args, **kwargs):
        self.host_failed[result._host.get_name()] = result

class PlayBookResultsCollector(CallbackBase):
    CALLBACK_VERSION = 2.0
    def __init__(self,taskList, *args, **kwargs):
        super(PlayBookResultsCollector, self).__init__(*args, **kwargs)
        self.task_ok = {}
        self.task_skipped = {}
        self.task_failed = {}
        self.task_status = {}
        self.task_unreachable = {}

    def v2_runner_on_ok(self, result, *args, **kwargs):
        if taskList.has_key(result._host.get_name()):
            data = {}
            data['task'] = str(result._task).replace("TASK: ","")
            taskList[result._host.get_name()].get('ok').append(data)
        self.task_ok[result._host.get_name()]  = taskList[result._host.get_name()]['ok']

    def v2_runner_on_failed(self, result, *args, **kwargs):
        if taskList.has_key(result._host.get_name()):
            data = {}
            data['task'] = str(result._task).replace("TASK: ","")
            msg = result._result.get('stderr')
            if msg is None:
                results = result._result.get('results')
                if result:
                    task_item = {}
                    for rs in results:
                        msg = rs.get('msg')
                        if msg:
                            task_item[rs.get('item')] = msg
                            data['msg'] = task_item
                    taskList[result._host.get_name()]['failed'].append(data)
                else:
                    msg = result._result.get('msg')
                    data['msg'] = msg
                    taskList[result._host.get_name()].get('failed').append(data)
        else:
            data = {}
            data['msg'] = msg
            taskList[result._host.get_name()].get('failed').append(data)
        self.task_failed[result._host.get_name()] = taskList[result._host.get_name()]['failed']

    def v2_runner_on_unreachable(self, result):
        self.task_unreachable[result._host.get_name()] = result

    def v2_runner_on_skipped(self, result):
        if taskList.has_key(result._host.get_name()):
            data = {}
            data['task'] = str(result._task).replace("TASK: ","")
            taskList[result._host.get_name()].get('skipped').append(data)
        self.task_ok[result._host.get_name()]  = taskList[result._host.get_name()]['skipped']

    def v2_playbook_on_stats(self, stats):
        hosts = sorted(stats.processed.keys())
        for h in hosts:
            t = stats.summarize(h)
            self.task_status[h] = {
                                       "ok":t['ok'],
                                       "changed" : t['changed'],
                                       "unreachable":t['unreachable'],
                                       "skipped":t['skipped'],
                                       "failed":t['failures']
                                   }

class ANSRunner(object):
    def __init__(self,resource,*args, **kwargs):
        self.resource = resource
        self.inventory = None
        self.variable_manager = None
        self.loader = None
        self.options = None
        self.passwords = None
        self.callback = None
        self.__initializeData()
        self.results_raw = {}

    def __initializeData(self):
        Options = namedtuple('Options', ['connection','module_path', 'forks', 'timeout',  'remote_user',
                'ask_pass', 'private_key_file', 'ssh_common_args', 'ssh_extra_args', 'sftp_extra_args',
                'scp_extra_args', 'become', 'become_method', 'become_user', 'ask_value_pass', 'verbosity',
                'check', 'listhosts', 'listtasks', 'listtags', 'syntax'])

        self.variable_manager = VariableManager()
        self.loader = DataLoader()
        self.options = Options(connection='smart', module_path=None, forks=100, timeout=10,
                remote_user='root', ask_pass=False, private_key_file=None, ssh_common_args=None, ssh_extra_args=None,
                sftp_extra_args=None, scp_extra_args=None, become=None, become_method=None,
                become_user='root', ask_value_pass=False, verbosity=None, check=False, listhosts=False,
                listtasks=False, listtags=False, syntax=False)

        self.passwords = dict(sshpass=None, becomepass=None)
        print "aaaaaa",self.resource
        self.inventory = MyInventory(self.resource, self.loader, self.variable_manager).inventory
        print self.inventory
        self.variable_manager.set_inventory(self.inventory)

    def run_model(self, host_list, module_name, module_args):
        """
        run module from andible ad-hoc.
        module_name: ansible module_name
        module_args: ansible module args
        """
        play_source = dict(
                name="Ansible Play",
                hosts=host_list,
                gather_facts='no',
                tasks=[dict(action=dict(module=module_name, args=module_args))]
        )
        play = Play().load(play_source, variable_manager=self.variable_manager, loader=self.loader)
        tqm = None
        self.callback = ModelResultsCollector()
        try:
            tqm = TaskQueueManager(
                    inventory=self.inventory,
                    variable_manager=self.variable_manager,
                    loader=self.loader,
                    options=self.options,
                    passwords=self.passwords,
            )
            tqm._stdout_callback = self.callback
            result = tqm.run(play)
        finally:
            if tqm is not None:
                tqm.cleanup()

    def run_playbook(self, host_list=None, playbook_path=None,extra_vars=None):
        """
        run ansible palybook
        """
        print "ccccc",host_list,playbook_path
        global taskList
        taskList = {}
    
        for host in host_list:
            taskList[host] = {}
            taskList[host]['ok'] = []
            taskList[host]['failed'] = []
            taskList[host]['skppied'] = []
        try:
            self.callback = PlayBookResultsCollector(taskList)
            self.variable_manager.extra_vars=extra_vars
            executor = PlaybookExecutor(
                playbooks=[playbook_path], inventory=self.inventory, variable_manager=self.variable_manager, loader=self.loader,
                options=self.options, passwords=self.passwords,
            )
            executor._tqm._stdout_callback = self.callback
            executor.run()
        except Exception as e:
            print e
            return False

    def get_model_result(self):
        self.results_raw = {'success':{}, 'failed':{}, 'unreachable':{}}
        for host, result in self.callback.host_ok.items():
            self.results_raw['success'][host] = result._result

        for host, result in self.callback.host_failed.items():
            self.results_raw['failed'][host] = result._result

        for host, result in self.callback.host_unreachable.items():
            self.results_raw['unreachable'][host]= result._result
        return json.dumps(self.results_raw)

    def get_playbook_result(self):
        self.results_raw = {'skipped':{}, 'failed':{}, 'ok':{},"status":{},'unreachable':{}}
        #print "dddd",self.callback.task_ok.items()
        for host, result in self.callback.task_ok.items():
            self.results_raw['ok'][host] = result

        for host, result in self.callback.task_failed.items():
            self.results_raw['failed'][host] = result

        for host, result in self.callback.task_status.items():
            self.results_raw['status'][host] = result

        for host, result in self.callback.task_skipped.items():
            self.results_raw['skipped'][host] = result

        for host, result in self.callback.task_unreachable.items():
            self.results_raw['unreachable'][host] = result
        return json.dumps(self.results_raw)



if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf8')
    #resource = [
    #             {"hostname": "192.168.100.4", "port": "22", "username": "root", "password": "pw"},
    #             {"hostname": "192.168.100.5", "port": "22", "username": "root", "password": "pw"},
    #                 {"hostname": "192.168.1.1", "port": "22", "username": "root", "password": "pw"}
    #             ]
    # resource =  {
    #                 "dynamic_host": {  #定义的动态主机名，需要跟playbook里面的hosts对应
    #                     "hosts": [
    #                                 {"hostname": "192.168.1.34", "port": "22", "username": "root", "password": "pw"},
    #                                 {"hostname": "192.168.1.130", "port": "22", "username": "root", "password": "pw"},
    #                                 {"hostname": "192.168.1.1", "port": "22", "username": "root", "password": "pw"}
    #                               ],
    #                     "vars": {
    #                              "var1":"ansible",
    #                              "var2":"saltstack"
    #                              }
    #                 }
    #             }
    resource =  {
                    "test": {  #定义的动态主机名，需要跟playbook里面的hosts对应
                        "hosts": [
                                    {"hostname": "10.211.55.3","username":"root"},
                                  ],
                        "vars": {
                            "host":"10.211.55.3"
                        }
                    }
                }
    

    rbt = ANSRunner(resource)  #resource可以是列表或者字典形式，如果做了ssh-key认证，就不会通过账户密码方式认证
    # rbt.run_model(host_list=["10.211.55.3"],module_name='fetch',module_args="src=/tmp/OpsPlayBookExe.py dest=/tmp")
    # data = rbt.get_model_result()
    rbt.run_playbook (host_list=["test"], playbook_path='fetch_test.yml', extra_vars={"host": "10.211.55.3"})
    data = rbt.get_playbook_result()
    print json.dumps(data,indent=4)