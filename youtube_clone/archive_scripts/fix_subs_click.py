with open(r'C:\Users\MuzaffarZed\ai_workspace\youtube_clone\app.js', 'r', encoding='utf-8') as f:
    code = f.read()

target = "this.filterSubscriptions();"
idx = code.find(target)
if idx != -1:
    print("Found this.filterSubscriptions() at:", idx)
    print(repr(code[idx-80:idx+60]))

    old_block = """          else if (targetNav === 'subscriptions') {
            this.switchView('home');
            this.filterSubscriptions();
          }"""
    new_block = """          else if (targetNav === 'subscriptions') {
            this.openSubscriptionsView();
          }"""
    if old_block in code:
        code = code.replace(old_block, new_block, 1)
        print("Replaced old_block successfully!")
    else:
        # replace manually
        pos_start = code.rfind("else if (targetNav === 'subscriptions')", 0, idx)
        pos_end = code.find("}", idx) + 1
        code = code[:pos_start] + "else if (targetNav === 'subscriptions') {\n            this.openSubscriptionsView();\n          }" + code[pos_end:]
        print("Replaced with range slice!")

with open(r'C:\Users\MuzaffarZed\ai_workspace\youtube_clone\app.js', 'w', encoding='utf-8') as f:
    f.write(code)

print("Saved app.js!")
