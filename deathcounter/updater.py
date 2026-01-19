import sys, time, shutil, subprocess, os, stat

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
    # Get the DeathCounter folder path (parent of the exe)
    old_folder = os.path.dirname(old_exe)
    
    # Make new folder writable
    make_writable(new_folder)
    
    # Backup old folder
    backup = old_folder + ".bak"
    if os.path.exists(backup):
        make_writable(backup)
        shutil.rmtree(backup, ignore_errors=True)
    
    time.sleep(1)
    shutil.move(old_folder, backup)
    
    # Move new folder to replace old location
    shutil.move(new_folder, old_folder)
    
    # Run the updated exe
    new_exe = os.path.join(old_folder, os.path.basename(old_exe))
    subprocess.Popen([new_exe])
except Exception as e:
    print(f"Update failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
