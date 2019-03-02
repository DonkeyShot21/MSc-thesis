#!/usr/bin/python
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess, os, psutil, sys, glob, shutil


class Handler(FileSystemEventHandler):
    last_mod_time = ''

    def on_modified(self, event):

        if not any(x in event.src_path for x in ['.tex', '.bib']):
            return

        current_mod_time = os.path.getmtime(event.src_path)
        if self.last_mod_time == current_mod_time:
            return
        else:
            self.last_mod_time = current_mod_time

        self.close_reader()
        self.pdflatex()

        if '.bib' in event.src_path:
            self.biblatex()
            self.pdflatex()
            self.pdflatex()

        self.open_reader()
        print('\nLatexmon waiting for changes...')

    def pdflatex(self):
        subprocess.call('pdflatex tesi'.split(' '))

    def biblatex(self):
        subprocess.call('bibtex tesi'.split(' '))

    def open_reader(self):
        subprocess.Popen(["AcroRd32.exe", 'tesi.pdf'])

    def close_reader(self):
        if "AcroRd32.exe" in (p.name() for p in psutil.process_iter()):
            os.system("TASKKILL /F /IM AcroRd32.exe")

    def clean(self):
        for ext in ['*.aux', '*.log', '*.bbl', '*blg', '*.out', '*.log']:
            for file in glob.glob(ext):
                shutil.move(file, os.path.join('logs', file))


if __name__ == "__main__":
    event_handler = Handler()
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
