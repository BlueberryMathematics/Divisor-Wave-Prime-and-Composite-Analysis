# LaTeX Setup Guide for Windows

## Step 1: Install MiKTeX (LaTeX Distribution)

1. Download MiKTeX from: https://miktex.org/download
2. Choose "Basic MiKTeX" installer for Windows
3. Run the installer with these recommended settings:
   - Install for all users (if admin) or current user
   - Set automatic package installation to "Yes"
   - Choose a local package repository

## Step 2: Verify Installation

After installation, open Command Prompt or PowerShell and verify:

```powershell
pdflatex --version
latexmk --version
biber --version
```

All commands should return version information.

## Step 3: Update PATH (if needed)

If commands aren't recognized, add MiKTeX to your PATH:
- Default installation path: `C:\Program Files\MiKTeX\miktex\bin\x64\`
- Add this to your system PATH environment variable

## Step 4: VS Code LaTeX Workshop Configuration

The repository includes a `.vscode/settings.json` file with optimal settings for LaTeX Workshop.

## Step 5: Building the Document

### Using VS Code LaTeX Workshop:
1. Open `docs/Divisor_Waves_and_their_Connection_to_the_Riemann_Hypothesis.tex`
2. Press `Ctrl+Alt+B` to build
3. Press `Ctrl+Alt+V` to view PDF

### Using Command Line:
```powershell
cd docs
latexmk -pdf -synctex=1 -interaction=nonstopmode Divisor_Waves_and_their_Connection_to_the_Riemann_Hypothesis.tex
```

## Troubleshooting

### Missing Packages
If you get "package not found" errors:
1. MiKTeX should auto-install missing packages
2. Or manually install via MiKTeX Console: `miktex-console`

### Bibliography Issues
Ensure biber/bibtex is working:
```powershell
biber Divisor_Waves_and_their_Connection_to_the_Riemann_Hypothesis
```

### Image/Graph Issues
- Check that all image files exist in the `graphs/` directory
- Images should be relative to the document location