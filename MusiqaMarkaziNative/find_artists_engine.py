import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\StudioEngine.cs', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'(public static readonly List<ArtistItem>[^;]+;)', text, re.DOTALL)
if m:
    print("Found ArtistItem list, length:", len(m.group(1)))
    lines = m.group(1).splitlines()
    print("Total lines:", len(lines))
    for l in lines[:25]:
        print(l)

m2 = re.search(r'(public static readonly List<CollectionItem>[^;]+;)', text, re.DOTALL)
if m2:
    print("\nFound CollectionItem list, length:", len(m2.group(1)))
    lines2 = m2.group(1).splitlines()
    print("Total lines:", len(lines2))
    for l in lines2[:25]:
        print(l)
