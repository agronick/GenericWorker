from payload import Payload
from tasks import *
import gearman
from pprint import pprint


gm_client = gearman.GearmanClient(['localhost:4730'])

def check_request_status(job_request):
    if job_request.complete:
        print "Job %s finished!  Result: %s - %s" % (job_request.job.unique, job_request.state, job_request.result)
    elif job_request.timed_out:
        print "Job %s timed out!" % job_request.unique
    elif job_request.state == JOB_UNKNOWN:
        print "Job %s connection failed!" % job_request.unique

payload = Payload()

pingtask = PingTask()
pingtask.host = "google.com"
payload.add_task(pingtask)

bashtask = BashTask()
bashtask.command = "ls"
payload.add_task(bashtask)

sshtask = SshTask()
sshtask.to_host = ""
sshtask.command = "cd /srv/www/htdocs; ls"
sshtask.username = ""
sshtask.password = ""
payload.add_task(sshtask)

scptask = ScpPutTask()
scptask.to_host = "localhost"
scptask.username = ""
scptask.password = ""
scptask.from_dir = "/tmp/foo1"
scptask.to_dir = "/tmp/foo2"
payload.add_task(scptask)


scptask = ScpGetTask()
scptask.to_host = ""
scptask.username = ""
scptask.password = ""
scptask.from_dir = "/tmp/foo3"
scptask.to_dir = "/tmp/foo4"
payload.add_task(scptask)

seril = payload.serilize()
completed_job_request = gm_client.submit_job("generic_worker", seril)

check_request_status(completed_job_request)

