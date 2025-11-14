#!/usr/bin/env python3
"""
Launcher script for AI Mathematical Discovery
Handles proper path setup and import resolution
"""

import sys
import os
from pathlib import Path

# Get the project root directory
project_root = Path(__file__).parent.parent
divisor_wave_python = project_root / 'divisor-wave-python'

# Ensure the divisor-wave-python directory is in the Python path
if str(divisor_wave_python) not in sys.path:
    sys.path.insert(0, str(divisor_wave_python))

# Change to the divisor-wave-python directory to resolve relative imports
original_cwd = os.getcwd()
os.chdir(str(divisor_wave_python))

try:
    # Now import and run the AI discovery workflow
    from divisor_wave_agent.src.workflows.ai_mathematical_discovery import AIDiscoveryWorkflow
    import asyncio
    
    async def main():
        print("🚀 Launching AI Mathematical Discovery System")
        print("=" * 60)
        print(f"Project root: {project_root}")
        print(f"Python module path: {divisor_wave_python}")
        print(f"Current working directory: {os.getcwd()}")
        
        workflow = AIDiscoveryWorkflow()
        await workflow.run_discovery_session()
    
    if __name__ == "__main__":
        asyncio.run(main())

finally:
    # Restore original working directory
    os.chdir(original_cwd)