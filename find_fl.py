import psutil

print("Searching processes:")
for p in psutil.process_iter(['pid', 'name', 'exe', 'cmdline']):
    try:
        name = p.info['name'] or ''
        exe = p.info['exe'] or ''
        cmdline = ' '.join(p.info['cmdline'] or [])
        if any(k in name.lower() or k in exe.lower() or k in cmdline.lower() for k in ['fl', 'image-line', 'fl64']):
            print(f"PID: {p.pid} | Name: {name} | Exe: {exe} | Cmd: {cmdline}")
    except Exception as e:
        pass
