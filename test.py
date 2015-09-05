from payload import Payload
from tasks import *
import gearman


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
sshtask.to_host = "192.168.1.13"
sshtask.command = "cd /etc/apt; ls"
payload.add_task(sshtask)

seril = payload.serilize()
completed_job_request = gm_client.submit_job("generic_worker", seril)

check_request_status(completed_job_request)

