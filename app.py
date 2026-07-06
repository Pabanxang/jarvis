# app.py
import time
from core.context import ApplicationContext

if __name__ == "__main__":
    # Boot the application container environment
    context = ApplicationContext()
    context.initialize()
    
    print("\n--- Simulating Live System Events ---\n")
    
    # Broadcast an independent system event into the pipeline
    context.event_bus.publish("system.heartbeat", {"sender": "KernelScheduler"})
    
    time.sleep(0.5)
    
    # Safely release resource chains
    context.shutdown()