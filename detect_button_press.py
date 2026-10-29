import pygame
import time

pygame.init()
pygame.joystick.init()

count = pygame.joystick.get_count()
print(f"Connected joysticks: {count}")
joysticks = [pygame.joystick.Joystick(i) for i in range(count)]
for j in joysticks:
    j.init()

print("Listening for any button press or stick movement for 5 seconds...")
start = time.time()
events_caught = []

while time.time() - start < 5.0:
    for event in pygame.event.get():
        if event.type == pygame.JOYBUTTONDOWN:
            events_caught.append(f"Joy {event.joy} Button {event.button} PRESSED!")
        elif event.type == pygame.JOYAXISMOTION:
            if abs(event.value) > 0.3:
                events_caught.append(f"Joy {event.joy} Axis {event.axis} MOVED: {event.value:.2f}")
        elif event.type == pygame.JOYHATMOTION:
            if event.value != (0, 0):
                events_caught.append(f"Joy {event.joy} Hat MOVED: {event.value}")
    time.sleep(0.02)

print(f"Total events caught: {len(events_caught)}")
for e in events_caught[:20]:
    print("  ->", e)

pygame.quit()
