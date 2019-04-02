import subprocess, os, psutil, sys, glob, shutil

pdflatex = 'pdflatex tesi'.split(' ')
biblatex = 'bibtex tesi'.split(' ')

compile_bib = len(sys.argv) > 1 and sys.argv[1] == "bib"

if "AcroRd32.exe" in (p.name() for p in psutil.process_iter()):
    os.system("TASKKILL /F /IM AcroRd32.exe")

if compile_bib:
    subprocess.call(pdflatex)
    subprocess.call(biblatex)
    subprocess.call(pdflatex)

subprocess.call(pdflatex)
subprocess.Popen(["AcroRd32.exe", 'tesi.pdf'])

for ext in ['*.aux', '*.log', '*.bbl', '*blg', '*.out', '*.log', '*.lof']:
    for file in glob.glob(ext):
        shutil.move(file, os.path.join('logs', file))
