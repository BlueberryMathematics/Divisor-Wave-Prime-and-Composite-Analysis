# Start all API servers for full Next.js integration
# This script starts all backend services needed for complete integration

import subprocess
import sys
import time
import os
from pathlib import Path

def start_server(script_name, port, description):
    """Start a server script in a separate process"""
    print(f"🚀 Starting {description} on port {port}...")
    try:
        process = subprocess.Popen([
            sys.executable, script_name
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Give the server a moment to start
        time.sleep(2)
        
        # Check if process is still running
        if process.poll() is None:
            print(f"✅ {description} started successfully on port {port}")
            return process
        else:
            stdout, stderr = process.communicate()
            print(f"❌ Failed to start {description}")
            print(f"Error: {stderr}")
            return None
    except Exception as e:
        print(f"❌ Error starting {description}: {e}")
        return None

def main():
    """Start all API servers for complete divisor-wave integration"""
    print("🌊 Divisor Wave Complete Integration Startup")
    print("=" * 50)
    
    servers = []
    
    # Check if we're in the right directory
    if not Path("neural-api-server.py").exists():
        print("❌ Error: Please run this script from the divisor-wave-nextjs directory")
        return
    
    # Start Python backend (divisor-wave-python integration)
    print("\n1️⃣ Starting Python Backend...")
    python_backend_path = "../divisor-wave-python/src/api/main.py"
    if Path(python_backend_path).exists():
        python_process = start_server(python_backend_path, 8000, "Python Mathematical Backend")
        if python_process:
            servers.append(("Python Backend", python_process))
    else:
        print("⚠️  Python backend not found - some features will be limited")
    
    # Start Neural Network API
    print("\n2️⃣ Starting Neural Network API...")
    neural_process = start_server("neural-api-server.py", 8001, "Neural Network API")
    if neural_process:
        servers.append(("Neural Network API", neural_process))
    
    # Start AI Agent API
    print("\n3️⃣ Starting AI Agent API...")
    agent_process = start_server("agent-api-server.py", 8002, "AI Agent API")
    if agent_process:
        servers.append(("AI Agent API", agent_process))
    
    # Summary
    print("\n" + "=" * 50)
    print("🎯 Integration Status Summary:")
    print(f"✅ Running servers: {len(servers)}")
    for name, _ in servers:
        print(f"   • {name}")
    
    print("\n📊 API Endpoints Available:")
    print("   • Python Backend:     http://localhost:8000")
    print("   • Neural Networks:    http://localhost:8001") 
    print("   • AI Agents:          http://localhost:8002")
    print("   • Next.js Frontend:   http://localhost:3000")
    
    if len(servers) > 0:
        print("\n🚀 Ready! You can now use the complete AI-integrated frontend:")
        print("   1. Start the Next.js frontend: npm run dev")
        print("   2. Open http://localhost:3000")
        print("   3. Click 'AI LaTeX Builder' or 'Neural Dashboard'")
        print("   4. Enjoy AI-powered mathematical discovery!")
        
        print("\n⚠️  Keep this terminal open to maintain all services")
        print("   Press Ctrl+C to stop all servers")
        
        try:
            # Keep the script running and monitor servers
            while True:
                time.sleep(5)
                # Check if any servers have died
                for name, process in servers[:]:
                    if process.poll() is not None:
                        print(f"❌ {name} has stopped unexpectedly")
                        servers.remove((name, process))
                
                if len(servers) == 0:
                    print("❌ All servers have stopped")
                    break
                    
        except KeyboardInterrupt:
            print("\n🛑 Shutting down all servers...")
            for name, process in servers:
                print(f"   Stopping {name}...")
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
            print("✅ All servers stopped")
    else:
        print("\n❌ No servers started successfully")
        print("   Please check the error messages above")

if __name__ == "__main__":
    main()