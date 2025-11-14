#!/usr/bin/env python3
"""
Divisor Wave Analysis System Installer
Automated installation script for the mathematical function analysis platform

This installer:
- Creates and activates virtual environment
- Installs dependencies from requirements.txt
- Checks for package updates and resolves conflicts
- Verifies system installation
- Provides post-installation guidance

Usage:
    python install_system.py [--update] [--force] [--no-verify]
"""

import os
import sys
import subprocess
import argparse
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional

class SystemInstaller:
    """Automated installer for the divisor wave analysis system"""
    
    def __init__(self, project_dir: Path = None):
        self.project_dir = project_dir or Path(__file__).parent
        self.venv_dir = self.project_dir / "venv"
        self.requirements_file = self.project_dir / "requirements.txt"
        self.python_executable = self._get_python_executable()
        
    def _get_python_executable(self) -> str:
        """Get the appropriate Python executable path"""
        if os.name == 'nt':  # Windows
            if self.venv_dir.exists():
                return str(self.venv_dir / "Scripts" / "python.exe")
            return sys.executable
        else:  # Unix/Linux/Mac
            if self.venv_dir.exists():
                return str(self.venv_dir / "bin" / "python")
            return sys.executable
    
    def _run_command(self, command: List[str], capture_output: bool = True) -> subprocess.CompletedProcess:
        """Run a system command with proper error handling"""
        try:
            print(f"Running: {' '.join(command)}")
            result = subprocess.run(
                command,
                capture_output=capture_output,
                text=True,
                check=False
            )
            if result.returncode != 0 and not capture_output:
                print(f"Command failed with return code {result.returncode}")
                if result.stderr:
                    print(f"Error: {result.stderr}")
            return result
        except FileNotFoundError:
            print(f"Command not found: {command[0]}")
            return subprocess.CompletedProcess(command, 1, "", f"Command not found: {command[0]}")
    
    def check_python_version(self) -> bool:
        """Verify Python version compatibility"""
        print("Checking Python version...")
        
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 8):
            print(f"❌ Python {version.major}.{version.minor} is not supported")
            print("   Required: Python 3.8 or higher")
            return False
        
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} is supported")
        return True
    
    def create_virtual_environment(self) -> bool:
        """Create virtual environment if it doesn't exist"""
        if self.venv_dir.exists():
            print(f"✅ Virtual environment already exists at: {self.venv_dir}")
            return True
        
        print("Creating virtual environment...")
        result = self._run_command([sys.executable, "-m", "venv", str(self.venv_dir)])
        
        if result.returncode == 0:
            print(f"✅ Virtual environment created at: {self.venv_dir}")
            return True
        else:
            print(f"❌ Failed to create virtual environment: {result.stderr}")
            return False
    
    def activate_virtual_environment(self) -> bool:
        """Activate virtual environment and update Python executable path"""
        if not self.venv_dir.exists():
            print("❌ Virtual environment not found")
            return False
        
        # Update Python executable to use venv
        self.python_executable = self._get_python_executable()
        
        # Verify activation by checking Python path
        result = self._run_command([self.python_executable, "-c", "import sys; print(sys.executable)"])
        
        if result.returncode == 0:
            venv_python_path = result.stdout.strip()
            if str(self.venv_dir) in venv_python_path:
                print(f"✅ Virtual environment activated: {venv_python_path}")
                return True
        
        print("❌ Failed to activate virtual environment")
        return False
    
    def install_dependencies(self, update: bool = False, force: bool = False) -> bool:
        """Install dependencies from requirements.txt"""
        if not self.requirements_file.exists():
            print(f"❌ Requirements file not found: {self.requirements_file}")
            return False
        
        print("Installing dependencies...")
        
        # Upgrade pip first
        print("Upgrading pip...")
        pip_result = self._run_command([
            self.python_executable, "-m", "pip", "install", "--upgrade", "pip"
        ])
        
        if pip_result.returncode != 0:
            print(f"⚠️ Warning: Failed to upgrade pip: {pip_result.stderr}")
        
        # Install requirements
        install_cmd = [
            self.python_executable, "-m", "pip", "install"
        ]
        
        if update:
            install_cmd.append("--upgrade")
        
        if force:
            install_cmd.extend(["--force-reinstall", "--no-deps"])
        
        install_cmd.extend(["-r", str(self.requirements_file)])
        
        result = self._run_command(install_cmd, capture_output=False)
        
        if result.returncode == 0:
            print("✅ Dependencies installed successfully")
            return True
        else:
            print("❌ Failed to install dependencies")
            return False
    
    def check_package_updates(self) -> Dict[str, str]:
        """Check for available package updates"""
        print("Checking for package updates...")
        
        # Get list of outdated packages
        result = self._run_command([
            self.python_executable, "-m", "pip", "list", "--outdated", "--format=json"
        ])
        
        if result.returncode == 0:
            try:
                outdated_packages = json.loads(result.stdout)
                if outdated_packages:
                    print(f"📦 Found {len(outdated_packages)} package updates available:")
                    for pkg in outdated_packages:
                        print(f"   {pkg['name']}: {pkg['version']} -> {pkg['latest_version']}")
                    return {pkg['name']: pkg['latest_version'] for pkg in outdated_packages}
                else:
                    print("✅ All packages are up to date")
                    return {}
            except json.JSONDecodeError:
                print("⚠️ Could not parse package update information")
                return {}
        else:
            print("⚠️ Could not check for package updates")
            return {}
    
    def resolve_dependency_conflicts(self) -> bool:
        """Check and resolve dependency conflicts"""
        print("Checking for dependency conflicts...")
        
        result = self._run_command([
            self.python_executable, "-m", "pip", "check"
        ])
        
        if result.returncode == 0:
            print("✅ No dependency conflicts found")
            return True
        else:
            print("⚠️ Dependency conflicts detected:")
            print(result.stdout)
            
            # Attempt to resolve by reinstalling problematic packages
            print("Attempting to resolve conflicts...")
            resolve_result = self._run_command([
                self.python_executable, "-m", "pip", "install", "--force-reinstall", 
                "numpy", "scipy", "matplotlib", "sympy"
            ])
            
            if resolve_result.returncode == 0:
                print("✅ Conflicts resolved")
                return True
            else:
                print("❌ Could not resolve all conflicts automatically")
                return False
    
    def verify_installation(self) -> bool:
        """Run the verification script to ensure everything works"""
        verify_script = self.project_dir / "verify_installation.py"
        
        if not verify_script.exists():
            print("⚠️ Verification script not found, skipping verification")
            return True
        
        print("Running installation verification...")
        result = self._run_command([self.python_executable, str(verify_script)], capture_output=False)
        
        return result.returncode == 0
    
    def create_activation_script(self):
        """Create convenience script for activating the environment"""
        if os.name == 'nt':  # Windows
            script_content = f"""@echo off
REM Activate Divisor Wave Analysis Environment
cd /d "{self.project_dir}"
call "{self.venv_dir}\\Scripts\\activate.bat"
echo Virtual environment activated for Divisor Wave Analysis
echo Python: {self.python_executable}
echo Project: {self.project_dir}
cmd /k
"""
            script_path = self.project_dir / "activate_env.bat"
        else:  # Unix/Linux/Mac
            script_content = f"""#!/bin/bash
# Activate Divisor Wave Analysis Environment
cd "{self.project_dir}"
source "{self.venv_dir}/bin/activate"
echo "Virtual environment activated for Divisor Wave Analysis"
echo "Python: {self.python_executable}"
echo "Project: {self.project_dir}"
exec "$SHELL"
"""
            script_path = self.project_dir / "activate_env.sh"
        
        with open(script_path, 'w') as f:
            f.write(script_content)
        
        if not os.name == 'nt':
            os.chmod(script_path, 0o755)
        
        print(f"✅ Created activation script: {script_path}")
    
    def show_post_install_guidance(self):
        """Show post-installation instructions"""
        print("\n" + "=" * 60)
        print("INSTALLATION COMPLETE")
        print("=" * 60)
        
        if os.name == 'nt':
            activate_cmd = f"call {self.venv_dir}\\Scripts\\activate.bat"
            convenience_script = "activate_env.bat"
        else:
            activate_cmd = f"source {self.venv_dir}/bin/activate"
            convenience_script = "./activate_env.sh"
        
        print(f"\n📋 To use the system:")
        print(f"   1. Activate environment: {activate_cmd}")
        print(f"   2. Or use convenience script: {convenience_script}")
        print(f"   3. Start backend: python src/api/main.py")
        print(f"   4. Access API docs: http://localhost:8000/docs")
        
        print(f"\n🔬 System Features:")
        print(f"   - 37+ mathematical functions managed centrally")
        print(f"   - LaTeX ↔ NumPy conversion capabilities")
        print(f"   - Frontend function builder")
        print(f"   - GPU acceleration (if CUDA available)")
        print(f"   - RESTful API for integration")
        
        print(f"\n📁 Key Files:")
        print(f"   - Main API: src/api/main.py")
        print(f"   - Function Registry: src/core/function_registry.py")
        print(f"   - Verification: verify_installation.py")
        print(f"   - Documentation: docs/")
    
    def install(self, update: bool = False, force: bool = False, verify: bool = True) -> bool:
        """Main installation routine"""
        print("DIVISOR WAVE ANALYSIS SYSTEM INSTALLER")
        print("=" * 60)
        
        # Check Python version
        if not self.check_python_version():
            return False
        
        # Create virtual environment
        if not self.create_virtual_environment():
            return False
        
        # Activate virtual environment
        if not self.activate_virtual_environment():
            return False
        
        # Check for updates if requested
        if update:
            updates = self.check_package_updates()
            if updates:
                print(f"Updates will be installed for {len(updates)} packages")
        
        # Install dependencies
        if not self.install_dependencies(update=update, force=force):
            return False
        
        # Check and resolve conflicts
        if not self.resolve_dependency_conflicts():
            print("⚠️ Some dependency conflicts remain - system may still function")
        
        # Verify installation
        if verify:
            if not self.verify_installation():
                print("❌ Installation verification failed")
                return False
        
        # Create convenience scripts
        self.create_activation_script()
        
        # Show guidance
        self.show_post_install_guidance()
        
        return True

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Install Divisor Wave Analysis System")
    parser.add_argument("--update", action="store_true", 
                       help="Update packages to latest versions")
    parser.add_argument("--force", action="store_true", 
                       help="Force reinstall packages")
    parser.add_argument("--no-verify", action="store_true", 
                       help="Skip installation verification")
    
    args = parser.parse_args()
    
    # Get project directory
    project_dir = Path(__file__).parent
    
    # Initialize installer
    installer = SystemInstaller(project_dir)
    
    # Run installation
    success = installer.install(
        update=args.update,
        force=args.force,
        verify=not args.no_verify
    )
    
    if success:
        print("\n🎉 Installation completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Installation failed")
        sys.exit(1)

if __name__ == "__main__":
    main()