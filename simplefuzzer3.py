#!/usr/bin/python

file_list = ["2010820135318.xls",
             "tax__down_kyuyoido_rei.xls",
             "toku-kirikae.xls",
             "44hp.xls",
             "tool_1_3.xls"]

apps = ["/usr/bin/gnumeric"]

FuzzFactor = 250
num_tests = 10000

import math
import random
import string
import subprocess
import time

output = open("crashers3.list", 'wb')
output2 = open("real_crashers3.list", 'wb')
fuzz_output = "fuzz.xls"

num_crashes = 0
for i in range(num_tests):
    file_choice = random.choice(file_list)
    app = random.choice(apps)
    buf = bytearray(open(file_choice, 'rb').read())
    numwrites = random.randrange(math.ceil(float(len(buf)) / FuzzFactor)) + 1
    for j in range(numwrites):
        rbyte = random.randrange(256)
        rn = random.randrange(len(buf))
        buf[rn] = "%c" % rbyte
        
    f = open(fuzz_output, 'wb')
    f.write(buf)
    f.close()
    commandline = [app, fuzz_output]
    process = subprocess.Popen(commandline)

    time.sleep(3)
    crashed = process.poll()
    if not crashed:
        process.terminate()
    else:
        num_crashes += 1
        output.write("Crash# %d code %d: command %s\n" 
                     % (num_crashes, crashed, commandline))
        crashfname = "crasher3-%d.xls" % num_crashes
        fcrash = open(crashfname, 'wb')
        fcrash.write(buf)
        fcrash.close()

            
