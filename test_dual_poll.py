import pygame
import time

pygame.init()
pygame.joystick.init()

count = pygame.joystick.get_count()
print(f"Pygame Joysticks: {count}")

j0 = pygame.joystick.Joystick(0)
j0.init()

j1 = pygame.joystick.Joystick(1)
j1.init()

print(f"J0 Name: {j0.get_name()}, Buttons: {j0.get_numbuttons()}, Axes: {j0.get_numaxes()}, Hats: {j0.get_numhats()}")
print(f"J1 Name: {j1.get_name()}, Buttons: {j1.get_numbuttons()}, Axes: {j1.get_numaxes()}, Hats: {j1.get_numhats()}")

# Poll events
for _ in range(5):
    pygame.event.pump()
    axes0 = [round(j0.get_axis(i), 2) for i in range(j0.get_numaxes())]
    buttons0 = [j0.get_button(i) for i in range(j0.get_numbuttons())]
    hat0 = j0.get_hat(0) if j0.get_numhats() > 0 else (0,0)

    axes1 = [round(j1.get_axis(i), 2) for i in range(j1.get_numaxes())]
    buttons1 = [j1.get_button(i) for i in range(j1.get_numbuttons())]
    hat1 = j1.get_hat(0) if j1.get_numhats() > 0 else (0,0)

    print(f"J0: Axes={axes0}, Buttons={buttons0}, Hat={hat0}")
    print(f"J1: Axes={axes1}, Buttons={buttons1}, Hat={hat1}")
    time.sleep(0.1)

pygame.quit()
