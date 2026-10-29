import sys
import os
import uiautomation as uia

def inspect():
    settings_win = uia.WindowControl(searchDepth=1, Name="Настройки")
    if not settings_win.Exists(3):
        print("Настройки window not found!")
        return

    print("Found Настройки window!")
    # Find all text and toggle controls
    for ctrl, depth in uia.WalkControl(settings_win, maxDepth=6):
        if ctrl.ControlType in [uia.ControlType.TextControl, uia.ControlType.ButtonControl, uia.ControlType.CheckBoxControl]:
            name = ctrl.Name.strip()
            if any(k in name.lower() for k in ["время", "часовой", "пояс", "автоматически", "tashkent", "utc", "ашхабад", "синхрон", "дата"]):
                print(f"[{ctrl.ControlTypeName}] {name} (Value: {ctrl.GetPattern(uia.PatternId.TogglePattern).ToggleState if ctrl.GetPattern(uia.PatternId.TogglePattern) else 'N/A'})")

if __name__ == '__main__':
    inspect()
