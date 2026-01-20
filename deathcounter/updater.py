import sys, time, shutil, subprocess, os, stat

log_path = os.path.join(os.path.dirname(__file__), "updater.log")

def log(msg):
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"{time.ctime()} - {msg}\n")

def make_writable(path):
    """Make all files in a directory tree writable"""
    for root, dirs, files in os.walk(path):
        for d in dirs:
            try:
                os.chmod(os.path.join(root, d), stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
            except:
                pass
        for f in files:
            try:
                os.chmod(os.path.join(root, f), stat.S_IWRITE | stat.S_IREAD)
            except:
                pass

old_exe = sys.argv[1]
new_folder = sys.argv[2]

time.sleep(2)  # let main app exit

try:
    log("Updater started")
    # Get the DeathCounter folder path (parent of the exe)
    old_folder = os.path.dirname(old_exe)
    old_folder = os.path.dirname(old_folder)

    log("Making new folder writable")
    # Make new folder writable
    make_writable(new_folder)
    
    log("Moving old folder to backup")
    # Backup old folder
    backup = old_folder + ".bak"
    if os.path.exists(backup):
        make_writable(backup)
        shutil.rmtree(backup, ignore_errors=True)
    
    time.sleep(1)
    shutil.copytree(old_folder, backup)

    if os.path.exists(old_folder):
        make_writable(old_folder)
        shutil.rmtree(old_folder, ignore_errors=True)
    # Move new folder to replace old location
    time.sleep(1)
    shutil.copytree(new_folder, old_folder)
    
    log("Launching new exe")
    # Run the updated exe
    subprocess.Popen([old_exe])
except Exception as e:
    print(f"Update failed: {e}")
    log(f"Update failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
