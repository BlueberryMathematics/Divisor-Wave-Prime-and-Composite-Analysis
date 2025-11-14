"""
Data Structure Reorganization Script
Creates a better organized directory structure for JSON files and mathematical data

This script:
1. Creates organized data directories
2. Moves and categorizes existing JSON files
3. Splits large JSON files into logical categories
4. Creates configuration and backup systems
5. Updates import paths in Python modules

Run with: python src/scripts/reorganize_data_structure.py [--dry-run]
"""

import os
import sys
import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
import argparse

# Add the core modules to path
core_dir = Path(__file__).parent.parent / "core"
sys.path.append(str(core_dir))

def create_directory_structure(base_path: Path, dry_run: bool = False) -> Dict[str, Path]:
    """Create the new organized directory structure"""
    
    structure = {
        "data": base_path / "data",
        "formulas": base_path / "data" / "formulas",
        "registry": base_path / "data" / "registry", 
        "config": base_path / "data" / "config",
        "cache": base_path / "data" / "cache",
        "backups": base_path / "data" / "backups",
        "exports": base_path / "data" / "exports",
        "latex_exports": base_path / "data" / "exports" / "latex_exports",
        "data_imports": base_path / "data" / "exports" / "data_imports"
    }
    
    print("🏗️  Creating new directory structure...")
    for name, path in structure.items():
        if not dry_run:
            path.mkdir(parents=True, exist_ok=True)
        print(f"   📁 {path}")
    
    return structure

def backup_existing_files(src_path: Path, backup_path: Path, dry_run: bool = False) -> None:
    """Create timestamped backup of existing JSON files"""
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = backup_path / f"backup_{timestamp}"
    
    json_files = list(src_path.glob("*.json"))
    
    if json_files:
        print(f"💾 Creating backup in: {backup_dir}")
        if not dry_run:
            backup_dir.mkdir(parents=True, exist_ok=True)
            
        for json_file in json_files:
            backup_file = backup_dir / json_file.name
            if not dry_run:
                shutil.copy2(json_file, backup_file)
            print(f"   📄 Backed up: {json_file.name}")

def split_divisor_wave_formulas(source_file: Path, formulas_dir: Path, dry_run: bool = False) -> None:
    """Split the large divisor_wave_formulas.json into categorized files"""
    
    if not source_file.exists():
        print(f"⚠️  Source file not found: {source_file}")
        return
    
    print("🔄 Splitting divisor_wave_formulas.json into categories...")
    
    with open(source_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Define categories and their functions
    categories = {
        "core_functions.json": {
            "description": "Core divisor wave functions and products",
            "functions": {}
        },
        "riesz_products.json": {
            "description": "Riesz product family functions",
            "functions": {}
        },
        "viete_products.json": {
            "description": "Viète product family functions", 
            "functions": {}
        },
        "special_products.json": {
            "description": "Other special mathematical products",
            "functions": {}
        }
    }
    
    # Categorize functions
    for func_name, func_data in data.get("formulas", {}).items():
        category = func_data.get("category", "Other")
        
        if "Riesz" in func_name or "Riesz" in category:
            categories["riesz_products.json"]["functions"][func_name] = func_data
        elif "Viete" in func_name or "Viète" in category:
            categories["viete_products.json"]["functions"][func_name] = func_data
        elif "product_of" in func_name or "Core" in category:
            categories["core_functions.json"]["functions"][func_name] = func_data
        else:
            categories["special_products.json"]["functions"][func_name] = func_data
    
    # Write categorized files
    for filename, category_data in categories.items():
        if category_data["functions"]:  # Only create file if it has functions
            output_file = formulas_dir / filename
            
            output_data = {
                "metadata": {
                    "description": category_data["description"],
                    "version": "1.0",
                    "created": datetime.now().isoformat(),
                    "source": "reorganized_from_divisor_wave_formulas.json",
                    "count": len(category_data["functions"])
                },
                "formulas": category_data["functions"],
                "normalization_info": data.get("normalization_info", {}),
                "coefficient_explanation": data.get("coefficient_explanation", {})
            }
            
            if not dry_run:
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(output_data, f, indent=2)
            
            print(f"   📄 Created: {filename} ({len(category_data['functions'])} functions)")

def create_registry_files(source_file: Path, registry_dir: Path, dry_run: bool = False) -> None:
    """Organize function registry into separate files"""
    
    if not source_file.exists():
        print(f"⚠️  Registry file not found: {source_file}")
        return
    
    print("🗂️  Organizing function registry...")
    
    with open(source_file, 'r', encoding='utf-8') as f:
        registry_data = json.load(f)
    
    # Main registry file (keep as is but cleaned up)
    main_registry = registry_dir / "function_registry.json"
    if not dry_run:
        shutil.copy2(source_file, main_registry)
    print(f"   📄 Moved: function_registry.json")
    
    # Extract categories into separate file
    categories = {}
    for func_id, func_data in registry_data.get("functions", {}).items():
        category = func_data.get("category", "Uncategorized")
        if category not in categories:
            categories[category] = {
                "description": f"Functions in the {category} category",
                "functions": []
            }
        categories[category]["functions"].append({
            "id": func_id,
            "name": func_data.get("name"),
            "display_name": func_data.get("display_name")
        })
    
    category_file = registry_dir / "category_definitions.json"
    category_data = {
        "metadata": {
            "description": "Function category definitions and organization",
            "version": "1.0", 
            "created": datetime.now().isoformat(),
            "total_categories": len(categories)
        },
        "categories": categories
    }
    
    if not dry_run:
        with open(category_file, 'w', encoding='utf-8') as f:
            json.dump(category_data, f, indent=2)
    print(f"   📄 Created: category_definitions.json ({len(categories)} categories)")
    
    # Create normalization modes file
    normalization_file = registry_dir / "normalization_modes.json"
    normalization_data = {
        "metadata": {
            "description": "Available normalization modes for mathematical functions",
            "version": "1.0",
            "created": datetime.now().isoformat()
        },
        "modes": {
            "N": {
                "name": "None",
                "description": "No normalization applied",
                "default": True
            },
            "Y": {
                "name": "Y-axis normalization", 
                "description": "Normalize along Y-axis"
            },
            "X": {
                "name": "X-axis normalization",
                "description": "Normalize along X-axis"  
            },
            "Z": {
                "name": "Z-axis normalization",
                "description": "Normalize along Z-axis"
            },
            "XYZ": {
                "name": "Combined normalization",
                "description": "Normalize across all axes"
            }
        }
    }
    
    if not dry_run:
        with open(normalization_file, 'w', encoding='utf-8') as f:
            json.dump(normalization_data, f, indent=2)
    print(f"   📄 Created: normalization_modes.json")

def create_config_files(config_dir: Path, dry_run: bool = False) -> None:
    """Create configuration files for system settings"""
    
    print("⚙️  Creating configuration files...")
    
    # Plotting defaults
    plotting_config = {
        "metadata": {
            "description": "Default plotting settings and parameters",
            "version": "1.0",
            "created": datetime.now().isoformat()
        },
        "defaults": {
            "2d_plots": {
                "x_range": [2, 28],
                "y_range": [-5, 5],
                "resolution": 200,
                "colormap": "viridis",
                "normalization": "N"
            },
            "3d_plots": {
                "x_range": [1.5, 18.5],
                "y_range": [-4.5, 4.5],
                "resolution": 100,
                "colormap": "viridis", 
                "normalization": "N",
                "elevation": 30,
                "azimuth": 45
            },
            "export": {
                "format": "png",
                "dpi": 300,
                "quality": 95
            }
        }
    }
    
    plotting_file = config_dir / "plotting_defaults.json"
    if not dry_run:
        with open(plotting_file, 'w', encoding='utf-8') as f:
            json.dump(plotting_config, f, indent=2)
    print(f"   📄 Created: plotting_defaults.json")
    
    # API configuration
    api_config = {
        "metadata": {
            "description": "API endpoint configuration and settings",
            "version": "1.0",
            "created": datetime.now().isoformat()
        },
        "server": {
            "host": "localhost",
            "port": 8000,
            "debug": False,
            "cors_origins": ["http://localhost:3000"]
        },
        "endpoints": {
            "functions": "/functions",
            "plotting": "/plot",
            "latex": "/latex",
            "registry": "/registry"
        },
        "limits": {
            "max_plot_resolution": 500,
            "max_computation_time": 30,
            "max_file_size": "10MB"
        }
    }
    
    api_file = config_dir / "api_endpoints.json"
    if not dry_run:
        with open(api_file, 'w', encoding='utf-8') as f:
            json.dump(api_config, f, indent=2)
    print(f"   📄 Created: api_endpoints.json")
    
    # System settings
    system_config = {
        "metadata": {
            "description": "System-wide settings and preferences",
            "version": "1.0",
            "created": datetime.now().isoformat()
        },
        "performance": {
            "enable_jit": True,
            "enable_gpu": True,
            "max_workers": 4,
            "cache_results": True
        },
        "data_paths": {
            "formulas_dir": "data/formulas",
            "registry_dir": "data/registry",
            "cache_dir": "data/cache",
            "backups_dir": "data/backups",
            "exports_dir": "data/exports"
        },
        "ai_discovery": {
            "enabled": True,
            "max_generations_per_session": 100,
            "evaluation_threshold": 0.7,
            "auto_save_interesting": True
        }
    }
    
    system_file = config_dir / "system_settings.json"
    if not dry_run:
        with open(system_file, 'w', encoding='utf-8') as f:
            json.dump(system_config, f, indent=2)
    print(f"   📄 Created: system_settings.json")

def create_ai_discovery_structure(formulas_dir: Path, dry_run: bool = False) -> None:
    """Create placeholder file for AI-generated functions"""
    
    print("🤖 Creating AI discovery structure...")
    
    ai_functions_file = formulas_dir / "ai_generated_functions.json"
    ai_data = {
        "metadata": {
            "description": "Functions discovered through AI mathematical generation",
            "version": "1.0",
            "created": datetime.now().isoformat(),
            "total_functions": 0,
            "last_discovery_session": None
        },
        "discovery_sessions": {
            "session_history": [],
            "interesting_functions": {},
            "archived_functions": {}
        },
        "functions": {},
        "evaluation_criteria": {
            "mathematical_interest": 0.25,
            "complexity": 0.15,
            "novelty": 0.20,
            "convergence": 0.15,
            "pattern_similarity": 0.15,
            "feasibility": 0.10
        }
    }
    
    if not dry_run:
        with open(ai_functions_file, 'w', encoding='utf-8') as f:
            json.dump(ai_data, f, indent=2)
    print(f"   📄 Created: ai_generated_functions.json")

def move_custom_functions(source_file: Path, formulas_dir: Path, dry_run: bool = False) -> None:
    """Move custom_functions.json to the formulas directory"""
    
    if source_file.exists():
        target_file = formulas_dir / "custom_functions.json"
        if not dry_run:
            shutil.move(str(source_file), str(target_file))
        print(f"   📄 Moved: custom_functions.json")
    else:
        print(f"⚠️  Custom functions file not found: {source_file}")

def update_import_paths(src_dir: Path, dry_run: bool = False) -> None:
    """Update Python files to use new data paths"""
    
    print("🔄 Updating import paths in Python modules...")
    
    # Files that need path updates
    python_files = [
        "core/special_functions_library.py",
        "core/plotting_methods.py", 
        "core/function_registry.py",
        "core/latex_function_builder.py",
        "api/main.py"
    ]
    
    # Path mappings (old -> new)
    path_mappings = {
        '"custom_functions.json"': '"../data/formulas/custom_functions.json"',
        '"divisor_wave_formulas.json"': '"../data/formulas/core_functions.json"',
        '"function_registry.json"': '"../data/registry/function_registry.json"',
        "'custom_functions.json'": "'../data/formulas/custom_functions.json'",
        "'divisor_wave_formulas.json'": "'../data/formulas/core_functions.json'",
        "'function_registry.json'": "'../data/registry/function_registry.json'"
    }
    
    for py_file in python_files:
        file_path = src_dir / py_file
        if file_path.exists():
            if not dry_run:
                # Read file
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Update paths
                updated = False
                for old_path, new_path in path_mappings.items():
                    if old_path in content:
                        content = content.replace(old_path, new_path)
                        updated = True
                
                # Write back if updated
                if updated:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"   📄 Updated: {py_file}")
            else:
                print(f"   📄 Would update: {py_file}")

def create_readme_files(data_dir: Path, dry_run: bool = False) -> None:
    """Create README files explaining the new structure"""  
    
    print("📖 Creating documentation...")
    
    main_readme = data_dir / "README.md"
    readme_content = """# Mathematical Functions Data Directory

This directory contains all JSON data files for the Divisor Wave Analysis system, organized for better maintainability and functionality.

## Directory Structure

### 📁 `formulas/`
Mathematical function definitions organized by category:
- `core_functions.json` - Original divisor wave functions and core products
- `riesz_products.json` - Riesz product family functions  
- `viete_products.json` - Viète product family functions
- `special_products.json` - Other special mathematical products
- `custom_functions.json` - User-defined functions
- `ai_generated_functions.json` - AI-discovered functions

### 📁 `registry/`
Function registry and metadata:
- `function_registry.json` - Main unified function registry
- `category_definitions.json` - Function categories and organization  
- `normalization_modes.json` - Available normalization options

### 📁 `config/`
System configuration files:
- `plotting_defaults.json` - Default plotting settings and parameters
- `api_endpoints.json` - API configuration and limits
- `system_settings.json` - System-wide settings and preferences

### 📁 `cache/`
Temporary files and computation cache (auto-generated)

### 📁 `backups/`
Timestamped backups of data files

### 📁 `exports/`
Export/import staging area:
- `latex_exports/` - Generated LaTeX formula exports
- `data_imports/` - Import staging for new data

## Migration from Old Structure

This reorganization was performed to:
1. ✅ Separate data from code
2. ✅ Group similar functions together
3. ✅ Provide clear backup and versioning
4. ✅ Enable better import/export workflows  
5. ✅ Support AI mathematical discovery system
6. ✅ Make maintenance much easier

## Usage

The system automatically detects the new structure. All existing functionality remains unchanged - only the internal organization has improved.

For developers: Update any hardcoded paths to use the new `data/` structure.
"""
    
    if not dry_run:
        with open(main_readme, 'w', encoding='utf-8') as f:
            f.write(readme_content)
    print(f"   📄 Created: data/README.md")

def main():
    parser = argparse.ArgumentParser(description="Reorganize JSON data structure")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done without making changes")
    args = parser.parse_args()
    
    # Define paths
    script_dir = Path(__file__).parent
    src_dir = script_dir.parent
    core_dir = src_dir / "core"
    
    print("🏗️  MATHEMATICAL DATA STRUCTURE REORGANIZATION")
    print("=" * 60)
    
    if args.dry_run:
        print("🔍 DRY RUN MODE - No files will be modified")
        print("=" * 60)
    
    try:
        # 1. Create new directory structure
        directories = create_directory_structure(src_dir, args.dry_run)
        
        # 2. Backup existing files
        backup_existing_files(core_dir, directories["backups"], args.dry_run)
        
        # 3. Split and reorganize JSON files
        split_divisor_wave_formulas(
            core_dir / "divisor_wave_formulas.json", 
            directories["formulas"], 
            args.dry_run
        )
        
        create_registry_files(
            core_dir / "function_registry.json",
            directories["registry"],
            args.dry_run
        )
        
        move_custom_functions(
            core_dir / "custom_functions.json",
            directories["formulas"], 
            args.dry_run
        )
        
        # 4. Create new organizational files
        create_config_files(directories["config"], args.dry_run)
        create_ai_discovery_structure(directories["formulas"], args.dry_run)
        
        # 5. Create documentation
        create_readme_files(directories["data"], args.dry_run)
        
        # 6. Update Python import paths
        update_import_paths(src_dir, args.dry_run)
        
        print("\n" + "=" * 60)
        if args.dry_run:
            print("✅ DRY RUN COMPLETE - Review the planned changes above")
            print("📋 To apply changes, run: python src/scripts/reorganize_data_structure.py")
        else:
            print("✅ DATA REORGANIZATION COMPLETE!")
            print("📁 New structure created in: src/data/")
            print("💾 Backups saved to: src/data/backups/")
            print("📖 Documentation: src/data/README.md")
            print("\n🔄 Next steps:")
            print("   1. Test system functionality")
            print("   2. Update any custom scripts with new paths")  
            print("   3. Remove old JSON files from src/core/ if everything works")
    
    except Exception as e:
        print(f"\n❌ Error during reorganization: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()