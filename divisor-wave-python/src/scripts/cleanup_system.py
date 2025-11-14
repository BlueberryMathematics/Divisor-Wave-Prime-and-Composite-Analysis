"""
Safe System Cleanup Script
Removes redundant files after successful registry migration
Creates backups and archives legacy files for reference

Run with: python cleanup_system.py [--dry-run]
"""

import os
import shutil
from pathlib import Path
import argparse
from datetime import datetime

def create_backup_archive():
    """Create backup of files before deletion"""
    backup_dir = Path("cleanup_backup_" + datetime.now().strftime("%Y%m%d_%H%M%S"))
    backup_dir.mkdir(exist_ok=True)
    
    print(f"📦 Creating backup archive: {backup_dir}")
    return backup_dir

def cleanup_redundant_files(dry_run=False):
    """Remove files that are now redundant after registry migration"""
    
    # Files to remove (now redundant with registry)
    redundant_files = [
        "src/core/python_to_latex_converter.py",
        "src/core/latex_to_numpy_converter.py", 
        "src/core/latex_function_builder.py"
    ]
    
    # Files to archive (keep for reference)
    archive_files = [
        "src/core/migrate_to_registry.py",
        "src/core/migration_example.py",
        "src/core/redundancy_elimination_summary.md"
    ]
    
    # Create docs directories
    docs_dirs = [
        "docs/utilities",
        "docs/examples", 
        "docs/legacy",
        "docs/cleanup"
    ]
    
    print(f"🧹 System Cleanup {'(DRY RUN)' if dry_run else '(LIVE)'}")
    print("=" * 50)
    
    if not dry_run:
        backup_dir = create_backup_archive()
    
    # Create docs structure
    for doc_dir in docs_dirs:
        doc_path = Path(doc_dir)
        if not dry_run:
            doc_path.mkdir(parents=True, exist_ok=True)
        print(f"📁 {'Would create' if dry_run else 'Created'} directory: {doc_dir}")
    
    # Remove redundant files
    print("\\n🗑️ Removing redundant files:")
    for file_path in redundant_files:
        path = Path(file_path)
        if path.exists():
            if not dry_run:
                # Backup before removal
                shutil.copy2(path, backup_dir / path.name)
                path.unlink()
            print(f"   ❌ {'Would remove' if dry_run else 'Removed'}: {file_path}")
        else:
            print(f"   ⚠️ Not found: {file_path}")
    
    # Archive documentation files  
    print("\\n📚 Archiving documentation files:")
    archive_mapping = {
        "src/core/migrate_to_registry.py": "docs/utilities/migrate_to_registry.py",
        "src/core/migration_example.py": "docs/examples/migration_example.py",
        "src/core/redundancy_elimination_summary.md": "docs/redundancy_elimination_summary.md"
    }
    
    for source, dest in archive_mapping.items():
        source_path = Path(source)
        dest_path = Path(dest)
        
        if source_path.exists():
            if not dry_run:
                shutil.move(source_path, dest_path)
            print(f"   📁 {'Would move' if dry_run else 'Moved'}: {source} → {dest}")
        else:
            print(f"   ⚠️ Not found: {source}")
    
    # Archive legacy files
    print("\\n📦 Archiving legacy files:")
    legacy_source = Path("src/original_legacy_files")
    legacy_dest = Path("docs/legacy/original_legacy_files")
    
    if legacy_source.exists():
        if not dry_run:
            shutil.move(legacy_source, legacy_dest)
        print(f"   📁 {'Would move' if dry_run else 'Moved'}: {legacy_source} → {legacy_dest}")
    else:
        print(f"   ⚠️ Not found: {legacy_source}")
    
    # Clean cache files
    print("\\n🧽 Cleaning cache files:")
    cache_cleaned = 0
    for root, dirs, files in os.walk("src"):
        for dir_name in dirs[:]:  # Create a copy to safely modify during iteration
            if dir_name == "__pycache__":
                cache_path = Path(root) / dir_name
                if not dry_run:
                    shutil.rmtree(cache_path)
                print(f"   🗑️ {'Would remove' if dry_run else 'Removed'}: {cache_path}")
                cache_cleaned += 1
                dirs.remove(dir_name)  # Don't traverse into deleted directory
    
    print(f"\\n✅ Cleanup Summary:")
    print(f"   📊 Redundant files: {len([f for f in redundant_files if Path(f).exists()])}")
    print(f"   📚 Archived files: {len([f for f, _ in archive_mapping.items() if Path(f).exists()])}")
    print(f"   🧽 Cache directories: {cache_cleaned}")
    
    if not dry_run:
        print(f"   💾 Backup created: {backup_dir}")

def verify_core_system():
    """Verify that essential core files are present"""
    essential_files = [
        "src/core/function_registry.py",
        "src/core/registry_adapter.py", 
        "src/core/special_functions_library.py",
        "src/core/plotting_methods.py",
        "src/api/main.py"
    ]
    
    print("\\n✅ Verifying essential core files:")
    all_present = True
    
    for file_path in essential_files:
        path = Path(file_path)
        if path.exists():
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ MISSING: {file_path}")
            all_present = False
    
    return all_present

def main():
    parser = argparse.ArgumentParser(description="Clean up redundant files after registry migration")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be cleaned without making changes")
    
    args = parser.parse_args()
    
    print("🌊 Divisor Wave System Cleanup Tool")
    print("=" * 40)
    
    # Verify essential files first
    if not verify_core_system():
        print("\\n❌ Essential files missing! Cleanup aborted.")
        return
    
    # Perform cleanup
    cleanup_redundant_files(dry_run=args.dry_run)
    
    if args.dry_run:
        print("\\n💡 Run without --dry-run to perform actual cleanup")
    else:
        print("\\n🎉 System cleanup completed successfully!")
        print("\\n📊 Final core file count:")
        core_files = list(Path("src/core").glob("*.py"))
        print(f"   Core Python files: {len(core_files)}")
        for file in sorted(core_files):
            print(f"     - {file.name}")

if __name__ == "__main__":
    main()