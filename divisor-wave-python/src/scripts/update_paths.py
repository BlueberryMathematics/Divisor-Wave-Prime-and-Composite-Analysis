"""
Simple Path Update Script
Updates key Python files to use the new data structure paths
"""

import os
from pathlib import Path

def update_file_paths():
    """Update the most important file paths"""
    
    # Define the files and their path updates
    updates = [
        {
            "file": "src/core/latex_function_builder.py",
            "replacements": [
                ('database_path: str = "custom_functions.json"', 'database_path: str = "../data/formulas/custom_functions.json"')
            ]
        },
        {
            "file": "src/core/function_registry.py", 
            "replacements": [
                ('Path(__file__).parent / "function_registry.json"', 'Path(__file__).parent / "../data/registry/function_registry.json"'),
                ('Path(__file__).parent / "divisor_wave_formulas.json"', 'Path(__file__).parent / "../data/formulas/core_functions.json"'),
                ('Path(__file__).parent / "custom_functions.json"', 'Path(__file__).parent / "../data/formulas/custom_functions.json"')
            ]
        },
        {
            "file": "src/core/mathematical_function_generator.py",
            "replacements": [
                ("'src/core/custom_functions.json'", "'src/data/formulas/custom_functions.json'"),
                ('"custom_functions.json not found"', '"src/data/formulas/custom_functions.json not found"')
            ]
        }
    ]
    
    base_path = Path(".")
    
    for update in updates:
        file_path = base_path / update["file"]
        if file_path.exists():
            print(f"📄 Updating: {update['file']}")
            
            # Read file
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Apply replacements
            for old_text, new_text in update["replacements"]:
                if old_text in content:
                    content = content.replace(old_text, new_text)
                    print(f"   ✅ Updated: {old_text[:50]}...")
            
            # Write back
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        else:
            print(f"⚠️  File not found: {update['file']}")

if __name__ == "__main__":
    print("🔄 Updating key file paths for new data structure...")
    update_file_paths()
    print("✅ Path updates complete!")