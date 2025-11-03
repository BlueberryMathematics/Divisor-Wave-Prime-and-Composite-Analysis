@echo off
echo Building LaTeX document...

cd /d "%~dp0..\docs"

echo Step 1: First pdflatex run...
pdflatex -synctex=1 -interaction=nonstopmode "Divisor_Waves_and_their_Connection_to_the_Riemann_Hypothesis.tex"

echo Step 2: Running biber for bibliography...
biber "Divisor_Waves_and_their_Connection_to_the_Riemann_Hypothesis"

echo Step 3: Second pdflatex run...
pdflatex -synctex=1 -interaction=nonstopmode "Divisor_Waves_and_their_Connection_to_the_Riemann_Hypothesis.tex"

echo Step 4: Third pdflatex run...
pdflatex -synctex=1 -interaction=nonstopmode "Divisor_Waves_and_their_Connection_to_the_Riemann_Hypothesis.tex"

echo Build complete!
echo PDF should be available at: docs\Divisor_Waves_and_their_Connection_to_the_Riemann_Hypothesis.pdf

pause