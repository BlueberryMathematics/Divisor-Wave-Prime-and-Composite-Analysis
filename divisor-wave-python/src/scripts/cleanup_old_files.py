"""
Cleanup Old JSON Files
Removes the old JSON files from src/core/ now that they've been reorganized
"""

import os
from pathlib import Path

def cleanup_old_files():
    """Remove old JSON files from src/core since they're now in src/data"""
    
    old_files = [
        "src/core/divisor_wave_formulas.json",
        "src/core/function_registry.json"
    ]
    
    # Note: custom_functions.json was already moved by our reorganization script
    
    base_path = Path(".")
    
    print("🧹 Cleaning up old JSON files from src/core/...")
    
    for file_path in old_files:
        full_path = base_path / file_path
        if full_path.exists():
            print(f"   🗑️  Removing: {file_path}")
            full_path.unlink()
        else:
            print(f"   ✅ Already removed: {file_path}")
    
    print("\n📁 New organized structure in src/data/:")
    data_path = base_path / "src/data"
    if data_path.exists():
        for root, dirs, files in os.walk(data_path):
            level = root.replace(str(data_path), '').count(os.sep)
            indent = ' ' * 2 * level
            print(f"{indent}{os.path.basename(root)}/")
            subindent = ' ' * 2 * (level + 1)
            for file in files:
                if not file.startswith('.'):
                    print(f"{subindent}{file}")

if __name__ == "__main__":
    cleanup_old_files()
    print("\n✅ Cleanup complete! Your data is now properly organized.")