"""
Function Registry Migration Script
Demonstrates how to seamlessly upgrade the existing divisor wave system
to use the unified function registry without breaking changes

Usage:
    python migrate_to_registry.py [--dry-run] [--backup]

This script:
1. Backs up existing JSON files (optional)
2. Initializes the unified registry
3. Migrates all existing function data
4. Updates system components
5. Validates the migration

11/6/2025 - Migration utility for unified function management
"""

import argparse
import json
import shutil
from pathlib import Path
from datetime import datetime
import sys

# Add the core modules to path
core_dir = Path(__file__).parent
sys.path.append(str(core_dir))
sys.path.append(str(core_dir.parent))

try:
    from function_registry import FunctionRegistry, get_registry
    from registry_adapter import RegistryAdapter, integrate_with_existing_system
except ImportError:
    # Try alternative import paths
    try:
        from core.function_registry import FunctionRegistry, get_registry
        from core.registry_adapter import RegistryAdapter, integrate_with_existing_system
    except ImportError:
        print("Error: Could not import registry modules. Make sure you're in the correct directory.")
        sys.exit(1)

def backup_existing_files(backup_dir: Path):
    """Create backups of existing JSON files"""
    backup_dir.mkdir(exist_ok=True)
    
    files_to_backup = [
        'divisor_wave_formulas.json',
        'custom_functions.json'
    ]
    
    core_dir = Path(__file__).parent
    backed_up = []
    
    for filename in files_to_backup:
        source = core_dir / filename
        if source.exists():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"{filename}.backup_{timestamp}"
            backup_path = backup_dir / backup_name
            
            shutil.copy2(source, backup_path)
            backed_up.append(str(backup_path))
            print(f"✓ Backed up {filename} to {backup_name}")
    
    return backed_up

def analyze_existing_system():
    """Analyze the current system to understand what will be migrated"""
    analysis = {
        'files_found': [],
        'functions_count': {},
        'custom_functions': 0,
        'latex_formulas': 0,
        'issues': []
    }
    
    core_dir = Path(__file__).parent
    
    # Check divisor_wave_formulas.json
    formulas_file = core_dir / 'divisor_wave_formulas.json'
    if formulas_file.exists():
        analysis['files_found'].append('divisor_wave_formulas.json')
        try:
            with open(formulas_file) as f:
                formulas_data = json.load(f)
                formulas_count = len(formulas_data.get('formulas', {}))
                analysis['functions_count']['builtin'] = formulas_count
                analysis['latex_formulas'] = formulas_count
        except Exception as e:
            analysis['issues'].append(f"Error reading formulas file: {e}")
    
    # Check custom_functions.json  
    custom_file = core_dir / 'custom_functions.json'
    if custom_file.exists():
        analysis['files_found'].append('custom_functions.json')
        try:
            with open(custom_file) as f:
                custom_data = json.load(f)
                custom_count = len(custom_data.get('functions', {}))
                analysis['functions_count']['custom'] = custom_count
                analysis['custom_functions'] = custom_count
        except Exception as e:
            analysis['issues'].append(f"Error reading custom functions file: {e}")
    
    return analysis

def migrate_system(dry_run=False):
    """Perform the actual migration to unified registry"""
    print("🚀 Starting migration to unified function registry...")
    
    # Analyze current system
    analysis = analyze_existing_system()
    print(f"\n📊 Current System Analysis:")
    print(f"   Files found: {', '.join(analysis['files_found'])}")
    print(f"   Builtin functions: {analysis['functions_count'].get('builtin', 0)}")
    print(f"   Custom functions: {analysis['functions_count'].get('custom', 0)}")
    print(f"   Total LaTeX formulas: {analysis['latex_formulas']}")
    
    if analysis['issues']:
        print(f"   ⚠ Issues found: {', '.join(analysis['issues'])}")
    
    if dry_run:
        print("\n🔍 DRY RUN MODE - No changes will be made")
        return True
    
    try:
        # Initialize the unified registry (automatically imports legacy data)
        print("\n🔄 Initializing unified registry...")
        registry = get_registry()
        
        # Create adapter for system integration
        adapter = RegistryAdapter()
        
        # Generate updated files
        print("📝 Generating updated configuration files...")
        registry.sync_legacy_files()
        
        # Create registry file
        registry.save_registry()
        
        # Validate migration
        validation = adapter.validate_system_consistency()
        
        print(f"\n✅ Migration completed successfully!")
        print(f"   📁 Registry file created: function_registry.json")
        print(f"   🔗 Legacy files synchronized")
        print(f"   📈 Total functions managed: {validation['total_functions']}")
        
        # Show function distribution
        for source, count in validation['function_count_by_source'].items():
            print(f"   📊 {source.title()} functions: {count}")
        
        if not validation['valid']:
            print(f"   ⚠ Validation issues found:")
            for issue in validation['issues']:
                print(f"     - {issue}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        return False

def update_main_py_example():
    """Generate example code for updating main.py"""
    example_code = '''
# Example: How to update your main.py to use the unified registry

# BEFORE (scattered function management):
# special_functions = SpecialFunctionsLibrary()
# plotter_2d = PlottingMethods("2D")
# plotter_3d = PlottingMethods("3D")

# AFTER (unified registry):
from core.registry_adapter import integrate_with_existing_system

special_functions = SpecialFunctionsLibrary()
plotter_2d = PlottingMethods("2D")
plotter_3d = PlottingMethods("3D")

# Single line to upgrade entire system to unified registry
adapter = integrate_with_existing_system(
    special_functions=special_functions,
    plotting_methods=plotter_2d,
    api_app=app
)

# Now all function mappings are managed centrally!
# - No more scattered JSON files to maintain
# - Automatic consistency across all components  
# - Easy addition of new functions
# - Built-in validation and documentation

# Optional: Access the registry directly
registry = adapter.registry

# Add a new custom function
new_func_id = registry.add_custom_function(
    name="my_custom_function",
    latex_formula="f(z) = z^3 + 1", 
    description="My custom mathematical function",
    category="User Functions"
)

# Search functions
prime_functions = registry.search_functions("prime")
riemann_functions = registry.search_functions("riemann", filters={'category': 'Prime Indicators'})

# Get comprehensive documentation
docs = adapter.create_function_documentation()
'''
    
    example_file = Path(__file__).parent / "migration_example.py"
    with open(example_file, 'w') as f:
        f.write(example_code)
    
    print(f"📄 Integration example saved to: {example_file}")

def main():
    parser = argparse.ArgumentParser(
        description="Migrate divisor wave system to unified function registry"
    )
    parser.add_argument(
        '--dry-run', 
        action='store_true',
        help='Show what would be migrated without making changes'
    )
    parser.add_argument(
        '--backup',
        action='store_true', 
        help='Create backups of existing files before migration'
    )
    parser.add_argument(
        '--example',
        action='store_true',
        help='Generate example integration code for main.py'
    )
    
    args = parser.parse_args()
    
    print("🌊 Divisor Wave Function Registry Migration Tool")
    print("=" * 50)
    
    if args.example:
        update_main_py_example()
        return
    
    # Create backups if requested
    if args.backup and not args.dry_run:
        backup_dir = Path(__file__).parent / "backups"
        backed_up = backup_existing_files(backup_dir)
        print(f"💾 Created {len(backed_up)} backup files")
    
    # Perform migration
    success = migrate_system(dry_run=args.dry_run)
    
    if success:
        print("\n🎉 Migration completed successfully!")
        print("\nNext steps:")
        print("1. Update your main.py using the integration example")
        print("2. Test the system to ensure everything works")
        print("3. Add new functions using the unified registry")
        print("\nRun with --example to see integration code")
    else:
        print("\n💥 Migration failed! Check the error messages above")
        if args.backup:
            print("Your original files have been backed up")

if __name__ == "__main__":
    main()