import subprocess
import sys
import time

def main():
    try:
        # Start the web interface
        web_process = subprocess.Popen([sys.executable, 'web_interface.py'])
        print("Started web interface...")
        
        # Wait a bit for the web interface to initialize
        time.sleep(2)
        
        # Start the main program
        main_process = subprocess.Popen([sys.executable, 'main.py'])
        print("Started main program...")
        
        # Wait for both processes
        web_process.wait()
        main_process.wait()
        
    except KeyboardInterrupt:
        print("\nShutting down...")
        web_process.terminate()
        main_process.terminate()
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 