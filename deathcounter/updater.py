import sys, time, shutil, subprocess, os

old_exe = sys.argv[1]
new_folder = sys.argv[2]

time.sleep(1)  # let main app exit

# Get the DeathCounter folder path (parent of the exe)
old_folder = os.path.dirname(old_exe)

# Backup old folder
backup = old_folder + ".bak"
if os.path.exists(backup):
    shutil.rmtree(backup)
shutil.move(old_folder, backup)

# Move new folder to replace old location
shutil.move(new_folder, old_folder)

# Run the updated exe
new_exe = os.path.join(old_folder, os.path.basename(old_exe))
subprocess.Popen([new_exe])
