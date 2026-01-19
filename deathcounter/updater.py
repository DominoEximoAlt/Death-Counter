import sys, time, shutil, subprocess

old_exe = sys.argv[1]
new_exe = sys.argv[2]

time.sleep(1)  # let main app exit

backup = old_exe + ".bak"
shutil.move(old_exe, backup)
shutil.move(new_exe, old_exe)

subprocess.Popen([old_exe])
