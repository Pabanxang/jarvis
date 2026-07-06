from core.context import ApplicationContext
from core.brain import Brain


class Assistant:
    """
    The main coordinator for JARVIS. 
    Handles user interaction loop, sends input to the Brain, and displays the output.
    """

    def __init__(self, context: ApplicationContext):
        self.context = context
        self.brain = Brain(context)

    def start(self) -> None:
        """Starts the main interaction loop."""
        self.context.logger.info("[ASSISTANT] Jarvis Assistant Loop Started.")
        print("\n=== JARVIS ASSISTANT ===")
        print("Type 'exit' or 'quit' to stop.\n")
        
        while True:
            try:
                user_input = input("User: ").strip()
                if not user_input:
                    continue

                if user_input.lower() in ["exit", "quit"]:
                    print("Jarvis: Goodbye!")
                    break
                
                # Send command to the brain for processing
                result = self.brain.process(user_input)
                
                # Display the result to the user
                if result.success:
                    print(f"Jarvis: {result.message}")
                else:
                    print(f"Jarvis (Error): {result.message}")
                    
            except KeyboardInterrupt:
                print("\nJarvis: Goodbye!")
                break
            except Exception as e:
                self.context.logger.error(f"[ASSISTANT] Unhandled exception: {e}")
                print("Jarvis: An unexpected error occurred.")
