# app.py
from core.context import ApplicationContext
from core.assistant import Assistant

if __name__ == "__main__":
    # Boot the application container environment
    context = ApplicationContext()
    context.initialize()
    
    # Start the main interaction loop
    assistant = Assistant(context)
    assistant.start()
    
    # Safely release resource chains
    context.shutdown()