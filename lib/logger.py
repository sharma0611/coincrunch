#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sharma0611
Module: Logger
Purpose: Provides interface to log print statements to log file
"""
import subprocess
import sys
import os 


class Logger(object):
    def __init__(self, fname):
        self.terminal = sys.stdout
        self.log = open(fname, "w")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def shutdown(self):
        self.log.close()
        sys.stdout = self.terminal

    def flush(self):
        pass

def start_printer(file_dir, file_name):
    if not os.path.isdir(file_dir):
        os.makedirs(file_dir)
    textfile = file_dir + '/' + file_name + '.txt'
    printer = Logger(textfile)
    sys.stdout = printer

def end_printer():
    sys.stdout.shutdown()

#if you want pdfs instead of text files, replace the end_printer fn with the one below & install the dependencies
#pdf dependencies:
    #Ghostscript
    #ps2pdf
    #enscript
    ## brew install these

#def end_printer(file_dir, file_name):
    #sys.stdout.shutdown()
    #textfile = file_dir + '/' + file_name + '.txt'
    #pdffile = file_dir + '/' + file_name + '.pdf'
    #bashcmd1 = "enscript -p " + file_dir + "/outputps.ps " + textfile
    #bashcmd2 = "ps2pdf " + file_dir + '/outputps.ps ' + pdffile
    #subprocess.call(bashcmd1, shell=True)
    #subprocess.call(bashcmd2, shell=True)

    #remove intermediate files
    #os.remove(textfile)
    #os.remove(file_dir + "/outputps.ps")

