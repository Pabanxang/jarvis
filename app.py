# app.py
from core.context import ApplicationContext

if __name__ == "__main__":
    # Boot the application environment registry
    context = ApplicationContext()
    context.initialize()
    
    print("\n==================================================")
    print("  JARVIS FRAMEWORK RUNTIME INTERACTIVE SHELL INTERFACE  ")
    print("  Type your commands below. Enter 'exit' to terminate.  ")
    print("==================================================\n")
    
    try:
        while True:
            # Captures keyboard string strings directly from user terminal stdout
            user_input = input("JARVIS > ")
            if user_input.strip().lower() == "exit":
                print("\nInitiating system shutdown sequence...")
                break
                
            if not user_input.strip():
                continue
                
            # Process intent tokens through our central brain router
            result = context.brain.process_input(user_input)
            
            # Print execution payloads depending on output metrics
            if result.is_ok:
                print(f"\n[SUCCESS]\n{result.value}\n")
            else:
                print(f"\n[EXECUTION FAILURE] {result.error_message}\n")
                
    except KeyboardInterrupt:
        print("\nAbrupt termination signal intercepted.")
    finally:
        # Guarantee safe context disposal cleanup operations
        context.shutdown()