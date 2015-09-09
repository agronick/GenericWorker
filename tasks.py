

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
    times = 3
    
    def run(self):
        self.command = "ping -c " + str(self.times) + "  " + self.host
        return super(PingTask, self).run()


class ScpTask(TaskInterface):
    
    to_host = "local"
    from_dir = "/"
    to_dir = "/"
    username = "root"
    password = None
    
    def do_run(self):
        ssh = get_ssh_client()
        try:
            ssh.connect(self.to_host, username = self.username, password=self.password, look_for_keys=True)
            sftp = ssh.open_sftp()
            if self.mode == 'p':
                sftp.put(self.from_dir, self.to_dir)
            elif self.mode == 'g':
                sftp.get(self.from_dir, self.to_dir)
            else:
                self.status = False
                return "error"
            self.status = True
            return self.from_dir + " : " + self.to_dir 
        except paramiko.SSHException as e:
            self.status = False
            return e
        
class ScpPutTask(ScpTask):
    
    mode = 'p'
    
    def run(self):
        return super(ScpPutTask, self).do_run()
    

class ScpGetTask(ScpTask):
    
    mode = 'g'
    
    def run(self):
        return super(ScpGetTask, self).do_run()

class SshTask(TaskInterface):
    
    to_host = ""
    command = ""
    username = "root"
    password = None
    
    def run(self):
        ssh = get_ssh_client()
        try:
            ssh.connect(self.to_host, username = self.username, password=self.password, look_for_keys=True)
        except paramiko.SSHException as e:
            self.status = False
            return e
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(self.command)
        ret = "".join(ssh_stdout.readlines()) + "   " + "".join(ssh_stderr.readlines())
        self.status = True
        return ret
    
def get_ssh_client():
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    return ssh
