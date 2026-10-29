import ext4

def inspect_apps():
    v = ext4.Volume(open(r"D:\T295_Studio_ROM_Build\system_raw.img", "rb"))
    
    for path in ["/system/app", "/system/priv-app", "/system/product/app", "/system/product/priv-app"]:
        try:
            d = v.inode_at(path)
            print(f"\n=== {path} ===")
            entries = []
            for entry, idx in d.opendir():
                if entry.name not in (b".", b".."):
                    entries.append(entry.name.decode("utf-8", errors="ignore"))
            entries.sort()
            for e in entries:
                print(f"  - {e}")
        except Exception as ex:
            print(f"Could not open {path}: {ex}")

if __name__ == "__main__":
    inspect_apps()
