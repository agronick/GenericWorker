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
        for task in self.tasks:
            msg = task.run()
            ret = {
                'status' : task.status,
                'message' : msg
            }
            returns.append(ret)
            if not task.status and not task.continue_on_fail:
                return json.dumps(returns)
            
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
 
            for key, value in item['class_props'].items():
                setattr(instance, key, value)
                
            tasks.append(instance)
        
        self.tasks = tasks