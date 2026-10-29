import os
import pefile

target = os.path.join("D:\\", "KANPIYUTER O'YINLARI", "LOTR_Uzuklar_Hukmdori", "AllInOneLauncherSetup.exe")
pe = pefile.PE(target)
sections = [s.Name.decode(errors='ignore').strip('\x00') for s in pe.sections]
print("Sections:", sections)
is_dotnet = hasattr(pe, 'DIRECTORY_ENTRY_COM_DESCRIPTOR') or any('CLR' in s.Name.decode(errors='ignore') for s in pe.sections)
print("Is .NET:", is_dotnet)
if hasattr(pe, 'FileInfo'):
    for finfo in pe.FileInfo[0]:
        if finfo.Key.decode(errors='ignore') == 'StringFileInfo':
            for st in finfo.StringTable:
                for entry in st.entries.items():
                    print(entry[0].decode(errors='ignore'), ":", entry[1].decode(errors='ignore'))
