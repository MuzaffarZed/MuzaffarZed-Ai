import traceback
import sys

try:
    import main_gui
    main_gui.main()
except Exception as e:
    with open("crash.log", "w", encoding="utf-8") as f:
        traceback.print_exc(file=f)
