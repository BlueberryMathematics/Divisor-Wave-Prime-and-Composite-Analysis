#!/usr/bin/env python3
"""
Complete launcher script for Divisor Wave System
Starts all 4 APIs: Python Backend, Neural Networks, AI Agents, and Next.js Frontend
"""

import subprocess
import time
import os
import sys
import signal
from pathlib import Path
from typing import List, Optional

class DivisorWaveSystemLauncher:
    """Complete system launcher with all 4 APIs"""
    
    def __init__(self):
        self.project_dir = Path(__file__).parent
        self.python_dir = self.project_dir / "divisor-wave-python"
        self.nextjs_dir = self.project_dir / "divisor-wave-nextjs"
        self.agent_dir = self.project_dir / "divisor-wave-agent"
        self.neural_dir = self.project_dir / "divisor-wave-neural-networks"
        
        self.running_processes: List[subprocess.Popen] = []
        
    def check_directories(self) -> bool:
        """Check if required directories exist"""
        required_dirs = [self.python_dir, self.nextjs_dir]
        
        for dir_path in required_dirs:
            if not dir_path.exists():
                print(f"❌ Required directory not found: {dir_path}")
                return False
        
        return True
    
    def start_process(self, name: str, working_dir: Path, executable: str, 
                     args: List[str], port: int, required: bool = True) -> Optional[subprocess.Popen]:
        """Start a server process and track it"""
        try:
            print(f"🚀 Starting {name} on port {port}...")
            
            process = subprocess.Popen(
                [executable] + args,
                cwd=working_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            if process:
                self.running_processes.append(process)
                print(f"✅ {name} started successfully on http://localhost:{port}")
                return process
            else:
                print(f"❌ Failed to start {name}")
                return None
                
        except Exception as e:
            print(f"❌ Error starting {name}: {e}")
            if required:
                raise
            return None
    
    def cleanup_processes(self):
        """Stop all running processes"""
        print("\n🛑 Shutting down all services...")
        for process in self.running_processes:
            if process.poll() is None:  # Process is still running
                try:
                    process.terminate()
                    # Give it a moment to shut down gracefully
                    try:
                        process.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        process.kill()
                except Exception as e:
                    print(f"   Error stopping process: {e}")
        
        print("✅ All services stopped")
    
    def signal_handler(self, signum, frame):
        """Handle Ctrl+C gracefully"""
        print("\n🛑 Received interrupt signal...")
        self.cleanup_processes()
        sys.exit(0)
    
    def run(self, skip_neural: bool = False, skip_agents: bool = False):
        """Run the complete system"""
        # Set up signal handler for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        
        print("🌊 Starting Complete Divisor Wave System")
        print("=" * 50)
        print(f"📂 Project Directory: {self.project_dir}")
        
        # Check directories
        if not self.check_directories():
            return
        
        try:
            # 1. Start Python Mathematical Backend (Required)
            print("\n1️⃣ Starting Python Mathematical Backend...")
            venv_python = self.python_dir / "venv" / "Scripts" / "python.exe"
            
            if not venv_python.exists():
                print("❌ Virtual environment not found!")
                print("💡 Please run these commands first:")
                print(f"   cd {self.python_dir}")
                print("   python -m venv venv")
                print("   venv\\Scripts\\Activate.ps1")
                print("   pip install -r requirements.txt")
                return
            
            python_process = self.start_process(
                "Python Mathematical Backend",
                self.python_dir,
                str(venv_python),
                ["-m", "uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"],
                8000,
                required=True
            )
            time.sleep(3)
            
            # 2. Start Neural Network API (Optional)
            print("\n2️⃣ Starting Neural Network API...")
            neural_server = self.nextjs_dir / "neural-api-server.py"
            if not skip_neural and neural_server.exists():
                neural_process = self.start_process(
                    "Neural Network API",
                    self.nextjs_dir,
                    "python",
                    ["neural-api-server.py"],
                    8001,
                    required=False
                )
                time.sleep(2)
            else:
                print("⏩ Neural Network API skipped")
            
            # 3. Start AI Agent API (Optional)
            print("\n3️⃣ Starting AI Agent API...")
            agent_server = self.nextjs_dir / "agent-api-server.py"
            if not skip_agents and agent_server.exists():
                agent_process = self.start_process(
                    "AI Agent API",
                    self.nextjs_dir,
                    "python",
                    ["agent-api-server.py"],
                    8002,
                    required=False
                )
                time.sleep(2)
            else:
                print("⏩ AI Agent API skipped")
            
            # 4. Show status summary
            print("\n📊 System Status Summary:")
            print("==========================")
            running_count = sum(1 for p in self.running_processes if p.poll() is None)
            print(f"   ✅ Running services: {running_count}")
            
            print("\n🌐 Available Endpoints:")
            print("   • Python Backend:     http://localhost:8000")
            print("   • API Documentation:  http://localhost:8000/docs")
            print("   • Neural Networks:    http://localhost:8001")
            print("   • AI Agents:          http://localhost:8002")
            print("   • Next.js Frontend:   http://localhost:3000")
            
            # 5. Start Next.js Frontend (Blocking)
            print("\n4️⃣ Starting Next.js Frontend...")
            os.chdir(self.nextjs_dir)
            
            # Check if node_modules exists
            if not (self.nextjs_dir / "node_modules").exists():
                print("� Installing Node.js dependencies...")
                subprocess.run(["npm", "install"])
            
            print("\n🎯 Complete Divisor Wave System Ready!")
            print("=======================================")
            print("⚛️  Starting Next.js Frontend...")
            print("🚀 Frontend will be available at http://localhost:3000")
            print("\n⚠️  Keep this terminal open to maintain all services")
            print("   Press Ctrl+C to stop all servers")
            print("=======================================")
            
            # Start Next.js development server (blocking)
            subprocess.run(["npm", "run", "dev"])
            
        except KeyboardInterrupt:
            self.cleanup_processes()
        except Exception as e:
            print(f"\n❌ Error during startup: {e}")
            self.cleanup_processes()


def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Complete Divisor Wave System Launcher')
    parser.add_argument('--skip-neural', action='store_true', 
                       help='Skip neural network API')
    parser.add_argument('--skip-agents', action='store_true',
                       help='Skip AI agent API')
    
    args = parser.parse_args()
    
    if len(sys.argv) == 1:
        print("🌊 Divisor Wave Complete System Launcher")
        print("========================================")
        print("")
        print("Starting all 4 APIs:")
        print("  • Python Mathematical Backend:  http://localhost:8000")
        print("  • Neural Network API:           http://localhost:8001")
        print("  • AI Agent API:                 http://localhost:8002")
        print("  • Next.js Frontend:             http://localhost:3000")
        print("")
        print("Use --help for more options")
        print("")
    
    launcher = DivisorWaveSystemLauncher()
    launcher.run(
        skip_neural=args.skip_neural,
        skip_agents=args.skip_agents
    )


if __name__ == "__main__":
    main()