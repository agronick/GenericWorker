import gearman
from payload import Payload
import pprint

gm_worker = gearman.GearmanWorker(['localhost:4730'])

payload = Payload()
def do_work(gearman_worker, gearman_job):
    payload.deserilize(gearman_job.data)
    return payload.run()

gm_worker.register_task('generic_worker', do_work)

# Enter our work loop and call gm_worker.after_poll() after each time we timeout/see socket activity
gm_worker.work()