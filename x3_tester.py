import pygame
import sys
import time

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

def main():
    pygame.init()
    pygame.joystick.init()
    
    if pygame.joystick.get_count() == 0:
        print("Hech qanday geympad topilmadi!")
        return
        
    js = pygame.joystick.Joystick(0)
    js.init()
    print(f"Geympad ulandi: {js.get_name()}")
    print("Stiklar va tugmalarni bosing (To'xtatish uchun Ctrl+C bosing)...\n")
    
    try:
        while True:
            pygame.event.pump()
            
            # Stiklar (Chap stik: 0, 1; O'ng stik: 2, 3 yoki 3, 4)
            axes = [round(js.get_axis(i), 2) for i in range(js.get_numaxes())]
            
            # Bosilgan tugmalar
            buttons = [i for i in range(js.get_numbuttons()) if js.get_button(i)]
            
            # Faqat o'zgarish bo'lsa yoki harakat bo'lsa chiqarish
            active_axes = {i: val for i, val in enumerate(axes) if abs(val) > 0.15}
            
            if active_axes or buttons:
                sys.stdout.write(f"\rStiklar: {active_axes} | Bosilgan tugmalar: {buttons}         ")
                sys.stdout.flush()
                
            time.sleep(0.05)
    except KeyboardInterrupt:
        print("\nTest yakunlandi.")

if __name__ == "__main__":
    main()
