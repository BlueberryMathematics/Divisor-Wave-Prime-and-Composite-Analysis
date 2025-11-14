# Mathematical Functions Data Directory

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
