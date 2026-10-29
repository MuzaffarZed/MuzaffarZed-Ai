import pygame

pygame.init()
pygame.joystick.init()

count = pygame.joystick.get_count()
print(f"Pygame detected {count} joysticks:")

for i in range(count):
    j = pygame.joystick.Joystick(i)
    j.init()
    print(f"\n--- Joystick {i} ---")
    print(f"Name: {j.get_name()}")
    print(f"GUID: {j.get_guid()}")
    print(f"Axes: {j.get_numaxes()}")
    print(f"Buttons: {j.get_numbuttons()}")
    print(f"Hats (D-Pad): {j.get_numhats()}")
    print(f"Power level: {j.get_power_level()}")
