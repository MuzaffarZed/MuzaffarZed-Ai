import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\CatalogData.cs', 'r', encoding='utf-8') as f:
    text = f.read()

old_cats = """        public static readonly string[] ArtistCategories = new[]
        {
            "Barchasi",
            "🔥 Zamonaviy Xit",
            "🎤 Estrada & Pop",
            "🏛️ Mumtoz & Ustozlar",
            "💃 To'yona & Lazgi",
            "🌍 Jahon & Turk"
        };"""

new_cats = """        public static readonly string[] ArtistCategories = new[]
        {
            "Barchasi",
            "❤️ Sevimlilar",
            "🔥 Zamonaviy Xit",
            "🎤 Estrada & Pop",
            "🏛️ Mumtoz & Ustozlar",
            "💃 To'yona & Lazgi",
            "🌍 Jahon & Turk"
        };"""

assert old_cats in text, "old_cats not found in CatalogData.cs"
text = text.replace(old_cats, new_cats, 1)

with open(r'C:\Users\MuzaffarZed\ai_workspace\MusiqaMarkaziNative\CatalogData.cs', 'w', encoding='utf-8') as f:
    f.write(text)

print("CatalogData.cs updated with ❤️ Sevimlilar category!")
