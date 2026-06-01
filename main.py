import redis
import pickle
import time

class TaskBroker:
    """
    Distributed Asynchronous Task Broker
    Serializes functional tasks and pushes them to Redis list structures.
    """
    def __init__(self, host="localhost", port=6379):
        # Set up standard local connection (safely catches dry-runs)
        try:
            self.r = redis.Redis(host=host, port=port, socket_timeout=1)
        except Exception:
            self.r = None

    def push_task(self, task_name, args):
        payload = pickle.dumps((task_name, args))
        if self.r:
            self.r.rpush("task_queue", payload)
        print(f"Pushed task '{task_name}' to queue.")

    def run_worker(self):
        print("Starting task queue worker process...")
        if not self.r:
            print("Redis client offline. Simulating worker thread loop...")
            return
        
        while True:
            _, payload = self.r.blpop("task_queue")
            task_name, args = pickle.loads(payload)
            print(f"Executing task: {task_name} with arguments: {args}")

if __name__ == "__main__":
    broker = TaskBroker()
    broker.push_task("compute_pi", {"precision": 1000})
    broker.run_worker()
