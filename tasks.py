

from abc import ABCMeta, abstractmethod
import os, re
import commands
import subprocess
import paramiko

ssh_command = "ssh "

class TaskInterface(object):
    __metaclass__ = ABCMeta
    
    status = False
    
    continue_on_fail = False
    name = __name__
    
    def say_hello(self):
        return 'hello'

    @abstractmethod
    def run(self): raise NotImplementedError
    
    def get_send_props(self):
        out = self.__dict__
        out['continue_on_fail'] = self.continue_on_fail
        return out
    
    
class BashTask(TaskInterface):
    
    command = ""
    
    def run(self):
        status, response = commands.getstatusoutput(self.command)
        self.status = status == 0
        return response
    
    
class PingTask(BashTask):
    
    host = ""
    
    def run(self):
        self.command = "ping -c 3 " + self.host
        return super(PingTask, self).run()


class ScpTask(TaskInterface):
    
    from_host = "local"
    to_host = "local"
    from_dir = "/"
    to_dir = "/"
    
    def run(self):
        pass

class SshTask(TaskInterface):
    
    to_host = ""
    command = ""
    
    def run(self):
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(self.to_host, username='kyle', password='')
        except paramiko.SSHException as e:
            self.status = False
            return e
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(self.command)
        ret = "".join(ssh_stdout.readlines()) + "   " + "".join(ssh_stderr.readlines())
        self.status = True
        return ret