import subprocess

adb = r"C:\Users\MuzaffarZed\AppData\Local\Android\Sdk\platform-tools\adb.exe"

def sh(cmd):
    r = subprocess.run([adb, "shell", "su", "0", "sh", "-c", cmd], capture_output=True, text=True, timeout=5)
    return r.stdout.strip()

print("install-recovery:", sh("ls -la /system/bin/install-recovery.sh /vendor/bin/install-recovery.sh 2>/dev/null"))
print("init.rc includes:", sh("grep -rn 'import ' /init*.rc 2>/dev/null"))
print("local.prop:", sh("ls -la /data/local.prop 2>/dev/null"))
print("su version:", sh("su -v 2>/dev/null"))
print("daemonsu:", sh("ps -A | grep -i su 2>/dev/null"))
