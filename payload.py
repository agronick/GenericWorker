import json
from tasks import *
import pprint



class Payload:
    
    tasks = []
    pos = -1
    
    def add_task(self, task):
        self.tasks.append(task)
        
    def next(self):
        pos += 1
        if pos < len(tasks):
            return tasts[pos]
        else:
            return False
        
    def run(self):
        returns = []
        ret = {}
        try:
             i = 0
             for task in self.tasks:
                 ret = {
                     'name' : task.name,
                     'order' : str(i),
                 }
                 msg = task.run()
                 ret['status'] = task.status
                 ret['message'] = msg
                 returns.append(ret)
                 i += 1
                 if not task.status and not task.continue_on_fail:
                     return json.dumps(returns)
                 
        except Exception, e:
             ret['status'] = False
             ret['message'] = 'Exception:' + str(e)
             returns.append(ret)
             return json.dumps(returns)
        finally:
             return json.dumps(returns)
            
        
    def serilize(self):
        out = []
        for task in self.tasks:
            props = {}
            props['name'] = task.__class__.__name__
            props['class_props'] = task.get_send_props()
            out.append(props)
        return json.dumps(out)
        
    def deserilize(self, data):
        tasks = []
        data = json.loads(data)
        for item in data:
            constructor = globals()[item['name']]
            instance = constructor()
            instance.name = item['name']
 
            for key, value in item['class_props'].items():
                setattr(instance, key, value)
                
            tasks.append(instance)
        
        self.tasks = tasks
