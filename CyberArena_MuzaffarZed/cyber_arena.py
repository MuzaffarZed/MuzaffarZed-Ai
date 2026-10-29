import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import sys
import os
import math
import random
import time
import pygame
import numpy as np

# Adjust path and encoding
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from sound_effects import SoundFX

# =============================================================================
# CONSTANTS & PALETTES
# =============================================================================
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
TITLE = "CYBER ARENA: ZERO DEFECT (DUAL GAMEPAD ULTIMATE)"
AUTHOR = "MuzaffarZed"

# Cyberpunk Palette
COLOR_BG = (10, 14, 22)
COLOR_GRID = (20, 32, 50)
COLOR_CYAN = (0, 229, 255)
COLOR_EMERALD = (0, 230, 118)
COLOR_GOLD = (255, 215, 0)
COLOR_RED = (255, 82, 82)
COLOR_PURPLE = (179, 136, 255)
COLOR_WHITE = (240, 246, 252)
COLOR_DARK_PANEL = (18, 24, 36)

# =============================================================================
# PARTICLE & EFFECT SYSTEM
# =============================================================================
class Particle:
    def __init__(self, x, y, vx, vy, color, size, life, decay=0.96):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.size = size
        self.max_life = life
        self.life = life
        self.decay = decay

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vx *= self.decay
        self.vy *= self.decay
        self.life -= 1
        return self.life > 0

    def draw(self, surface):
        alpha = max(0, min(255, int(255 * (self.life / self.max_life))))
        s = pygame.Surface((int(self.size * 2), int(self.size * 2)), pygame.SRCALPHA)
        col = (*self.color[:3], alpha)
        pygame.draw.circle(s, col, (int(self.size), int(self.size)), int(self.size))
        surface.blit(s, (self.x - self.size, self.y - self.size))

class Shockwave:
    def __init__(self, x, y, color, max_radius=80, speed=5):
        self.x = x
        self.y = y
        self.color = color
        self.radius = 4
        self.max_radius = max_radius
        self.speed = speed

    def update(self):
        self.radius += self.speed
        return self.radius < self.max_radius

    def draw(self, surface):
        alpha = max(0, min(255, int(255 * (1.0 - (self.radius / self.max_radius)))))
        s = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(s, (*self.color[:3], alpha), (self.radius, self.radius), int(self.radius), 3)
        surface.blit(s, (self.x - self.radius, self.y - self.radius))

class FloatingText:
    def __init__(self, x, y, text, color, font, duration=45):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.font = font
        self.life = duration
        self.max_life = duration

    def update(self):
        self.y -= 1.2
        self.life -= 1
        return self.life > 0

    def draw(self, surface):
        alpha = max(0, min(255, int(255 * (self.life / self.max_life))))
        surf = self.font.render(self.text, True, self.color)
        surf.set_alpha(alpha)
        surface.blit(surf, (self.x - surf.get_width() // 2, self.y))

# =============================================================================
# PROJECTILE CLASSES
# =============================================================================
class Projectile:
    def __init__(self, x, y, angle, speed, damage, color, owner, p_type="laser"):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = speed
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.damage = damage
        self.color = color
        self.owner = owner
        self.type = p_type
        self.life = 120
        self.radius = 5 if p_type == "laser" else 8
        self.trail_timer = 0

    def update(self, particles, arena_rect):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1

        self.trail_timer += 1
        if self.trail_timer % 2 == 0:
            particles.append(Particle(self.x, self.y, -self.vx * 0.1, -self.vy * 0.1, self.color, 3, 15))

        # Check arena bounds bounce or destroy
        if not arena_rect.collidepoint(self.x, self.y):
            return False
        return self.life > 0

    def draw(self, surface):
        if self.type == "laser":
            end_x = self.x - math.cos(self.angle) * 14
            end_y = self.y - math.sin(self.angle) * 14
            pygame.draw.line(surface, self.color, (self.x, self.y), (end_x, end_y), 4)
            pygame.draw.circle(surface, COLOR_WHITE, (int(self.x), int(self.y)), 3)
        elif self.type == "plasma":
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)
            pygame.draw.circle(surface, COLOR_WHITE, (int(self.x), int(self.y)), self.radius // 2)
        elif self.type == "missile":
            pygame.draw.circle(surface, COLOR_GOLD, (int(self.x), int(self.y)), 5)

# =============================================================================
# POWERUP CRATES
# =============================================================================
class Powerup:
    TYPES = [
        ("shield", "SH", "SHIELD (+50)", COLOR_CYAN),
        ("speed", "TB", "TURBO (2X)", COLOR_GOLD),
        ("plasma", "PL", "PLASMA CANNON", COLOR_PURPLE),
        ("heal", "HP", "REPAIR (+35)", COLOR_EMERALD),
        ("nuke", "EMP", "EMP NUKE (-30)", COLOR_RED)
    ]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type_info = random.choice(self.TYPES)
        self.type = self.type_info[0]
        self.short_tag = self.type_info[1]
        self.label = self.type_info[2]
        self.color = self.type_info[3]
        self.radius = 16
        self.pulse = 0.0

    def update(self):
        self.pulse += 0.08

    def draw(self, surface, font):
        r = self.radius + math.sin(self.pulse) * 3
        # Outer glow
        s = pygame.Surface((int(r * 4), int(r * 4)), pygame.SRCALPHA)
        pygame.draw.circle(s, (*self.color, 45), (int(r * 2), int(r * 2)), int(r * 1.6))
        pygame.draw.circle(s, self.color, (int(r * 2), int(r * 2)), int(r), 2)
        surface.blit(s, (self.x - r * 2, self.y - r * 2))

        # Short tag rendered cleanly
        txt = font.render(self.short_tag, True, COLOR_WHITE)
        surface.blit(txt, (self.x - txt.get_width() // 2, self.y - txt.get_height() // 2))

# =============================================================================
# PLAYER / SHIP CLASS
# =============================================================================
class Player:
    SHIP_PRESETS = {
        "VIPER": {"speed": 5.8, "max_hp": 100, "fire_rate": 8, "dash_cd": 60, "name": "Viper (Speed)"},
        "TITAN": {"speed": 4.2, "max_hp": 140, "fire_rate": 14, "dash_cd": 90, "name": "Titan (Armor)"},
        "SPECTRE": {"speed": 5.0, "max_hp": 115, "fire_rate": 10, "dash_cd": 70, "name": "Spectre (Tactical)"}
    }

    def __init__(self, p_id, x, y, color, ship_type="VIPER", joystick=None):
        self.p_id = p_id
        self.start_x = x
        self.start_y = y
        self.x = x
        self.y = y
        self.color = color
        self.ship_type = ship_type
        self.joystick = joystick

        preset = self.SHIP_PRESETS[ship_type]
        self.base_speed = preset["speed"]
        self.speed = self.base_speed
        self.max_hp = preset["max_hp"]
        self.hp = self.max_hp
        self.shield = 0
        self.fire_rate = preset["fire_rate"]
        self.dash_cd_max = preset["dash_cd"]
        self.dash_cd = 0
        self.stamina = 100.0

        self.angle = 0.0 if p_id == 1 else math.pi
        self.radius = 20
        self.cooldown = 0
        self.secondary_cd = 0
        self.kills = 0
        self.rounds_won = 0

        # Powerup modifiers
        self.speed_boost_timer = 0
        self.plasma_buff_timer = 0
        self.dash_trail = []

    def reset_position(self):
        self.x = self.start_x
        self.y = self.start_y
        self.hp = self.max_hp
        self.shield = 0
        self.stamina = 100.0
        self.cooldown = 0
        self.dash_cd = 0
        self.speed = self.base_speed
        self.angle = 0.0 if self.p_id == 1 else math.pi

    def handle_input(self, keys, sfx, projectiles, particles):
        dx = 0.0
        dy = 0.0
        shoot = False
        dash = False
        secondary = False

        # 1. GAMEPAD INPUT
        if self.joystick:
            try:
                num_axes = self.joystick.get_numaxes()
                # Left Analog Stick
                if num_axes >= 2:
                    jx = self.joystick.get_axis(0)
                    jy = self.joystick.get_axis(1)
                    if abs(jx) > 0.2:
                        dx += jx
                    if abs(jy) > 0.2:
                        dy += jy

                # D-Pad fallback
                if self.joystick.get_numhats() > 0:
                    hx, hy = self.joystick.get_hat(0)
                    if hx != 0:
                        dx += hx
                    if hy != 0:
                        dy -= hy # Invert Y for screen coords

                # Buttons
                # Button 2: Cross / A (Fire)
                # Button 0: Triangle / Y (Dash)
                # Button 1: Circle / B (Secondary / Missile)
                # Button 3: Square / X (Secondary)
                num_btns = self.joystick.get_numbuttons()
                if num_btns > 2 and self.joystick.get_button(2):
                    shoot = True
                if num_btns > 0 and self.joystick.get_button(0):
                    dash = True
                if num_btns > 1 and (self.joystick.get_button(1) or (num_btns > 3 and self.joystick.get_button(3))):
                    secondary = True
                if num_btns > 5 and (self.joystick.get_button(4) or self.joystick.get_button(5)):
                    shoot = True
            except Exception:
                pass

        # 2. KEYBOARD INPUT (Fallback / Co-op)
        if self.p_id == 1 and not self.joystick:
            if keys[pygame.K_w]: dy -= 1.0
            if keys[pygame.K_s]: dy += 1.0
            if keys[pygame.K_a]: dx -= 1.0
            if keys[pygame.K_d]: dx += 1.0
            if keys[pygame.K_SPACE]: shoot = True
            if keys[pygame.K_LSHIFT]: dash = True
            if keys[pygame.K_e]: secondary = True
        elif self.p_id == 2 and not self.joystick:
            if keys[pygame.K_UP]: dy -= 1.0
            if keys[pygame.K_DOWN]: dy += 1.0
            if keys[pygame.K_LEFT]: dx -= 1.0
            if keys[pygame.K_RIGHT]: dx += 1.0
            if keys[pygame.K_RETURN] or keys[pygame.K_KP0]: shoot = True
            if keys[pygame.K_RCTRL] or keys[pygame.K_KP_PERIOD]: dash = True
            if keys[pygame.K_KP1]: secondary = True

        # Process Movement & Heading
        mag = math.hypot(dx, dy)
        if mag > 0.1:
            dx /= mag
            dy /= mag
            self.angle = math.atan2(dy, dx)
            current_spd = self.speed * (1.5 if self.speed_boost_timer > 0 else 1.0)
            self.x += dx * current_spd
            self.y += dy * current_spd

            # Thruster Particles
            tail_x = self.x - math.cos(self.angle) * 18
            tail_y = self.y - math.sin(self.angle) * 18
            flame_col = COLOR_GOLD if self.speed_boost_timer > 0 else self.color
            particles.append(Particle(tail_x, tail_y, -dx * 2 + random.uniform(-1, 1), -dy * 2 + random.uniform(-1, 1), flame_col, 4, 16))

        # Stamina recharge
        if self.stamina < 100.0:
            self.stamina = min(100.0, self.stamina + 0.35)

        # Dash execution
        if dash and self.dash_cd <= 0 and self.stamina >= 35.0:
            self.dash_cd = self.dash_cd_max
            self.stamina -= 35.0
            dash_dist = 90
            self.x += math.cos(self.angle) * dash_dist
            self.y += math.sin(self.angle) * dash_dist
            sfx.play('dash')
            for _ in range(16):
                particles.append(Particle(self.x, self.y, random.uniform(-4, 4), random.uniform(-4, 4), COLOR_WHITE, 5, 20))

        if self.dash_cd > 0:
            self.dash_cd -= 1

        # Shooting execution
        if self.cooldown > 0:
            self.cooldown -= 1

        if shoot and self.cooldown <= 0:
            p_type = "plasma" if self.plasma_buff_timer > 0 else "laser"
            dmg = 24 if p_type == "plasma" else 15
            spd = 12 if p_type == "plasma" else 15

            # Fire from nose
            nose_x = self.x + math.cos(self.angle) * 22
            nose_y = self.y + math.sin(self.angle) * 22

            if self.ship_type == "VIPER":
                # Twin cannons
                offset = 7
                ox = -math.sin(self.angle) * offset
                oy = math.cos(self.angle) * offset
                projectiles.append(Projectile(nose_x + ox, nose_y + oy, self.angle, spd, dmg, self.color, self.p_id, p_type))
                projectiles.append(Projectile(nose_x - ox, nose_y - oy, self.angle, spd, dmg, self.color, self.p_id, p_type))
            else:
                projectiles.append(Projectile(nose_x, nose_y, self.angle, spd, dmg, self.color, self.p_id, p_type))

            sfx.play('plasma' if p_type == "plasma" else 'laser')
            self.cooldown = self.fire_rate

        # Secondary Weapon (Homing Missile / Shockwave)
        if self.secondary_cd > 0:
            self.secondary_cd -= 1

        if secondary and self.secondary_cd <= 0 and self.stamina >= 40.0:
            self.secondary_cd = 90
            self.stamina -= 40.0
            nose_x = self.x + math.cos(self.angle) * 20
            nose_y = self.y + math.sin(self.angle) * 20
            projectiles.append(Projectile(nose_x, nose_y, self.angle, 10, 30, COLOR_GOLD, self.p_id, "missile"))
            sfx.play('missile')

        # Powerup Timers
        if self.speed_boost_timer > 0: self.speed_boost_timer -= 1
        if self.plasma_buff_timer > 0: self.plasma_buff_timer -= 1

    def clamp_to_arena(self, rect):
        self.x = max(rect.left + self.radius, min(rect.right - self.radius, self.x))
        self.y = max(rect.top + self.radius, min(rect.bottom - self.radius, self.y))

    def take_damage(self, amount, sfx, floating_texts, font):
        if self.shield > 0:
            absorbed = min(self.shield, amount)
            self.shield -= absorbed
            amount -= absorbed
            sfx.play('shield')
            floating_texts.append(FloatingText(self.x, self.y - 20, f"SHIELD -{absorbed}", COLOR_CYAN, font))

        if amount > 0:
            self.hp = max(0, self.hp - amount)
            floating_texts.append(FloatingText(self.x, self.y - 35, f"-{amount}", COLOR_RED, font))
            return self.hp <= 0
        return False

    def draw(self, surface):
        # 1. Shield Aura
        if self.shield > 0:
            s_rad = int(self.radius * 1.5)
            s_surf = pygame.Surface((s_rad * 2, s_rad * 2), pygame.SRCALPHA)
            pygame.draw.circle(s_surf, (*COLOR_CYAN, 80), (s_rad, s_rad), s_rad, 3)
            surface.blit(s_surf, (self.x - s_rad, self.y - s_rad))

        # 2. Ship Polygon Body
        cos_a = math.cos(self.angle)
        sin_a = math.sin(self.angle)

        nose = (self.x + cos_a * 22, self.y + sin_a * 22)
        wing_l = (self.x - cos_a * 14 - sin_a * 16, self.y - sin_a * 14 + cos_a * 16)
        wing_r = (self.x - cos_a * 14 + sin_a * 16, self.y - sin_a * 14 - cos_a * 16)
        back_center = (self.x - cos_a * 8, self.y - sin_a * 8)

        pts = [nose, wing_l, back_center, wing_r]
        pygame.draw.polygon(surface, self.color, pts)
        pygame.draw.polygon(surface, COLOR_WHITE, pts, 2)

        # Cockpit glass
        cockpit = (self.x + cos_a * 6, self.y + sin_a * 6)
        pygame.draw.circle(surface, COLOR_WHITE, (int(cockpit[0]), int(cockpit[1])), 4)

        # Player Tag Header
        tag = f"P{self.p_id}"
        # Small indicator

# =============================================================================
# MAIN GAME CONTROLLER & SCENE MANAGER
# =============================================================================
class CyberArenaGame:
    def __init__(self):
        pygame.init()
        pygame.joystick.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(f"{TITLE} - by {AUTHOR}")
        self.clock = pygame.time.Clock()

        self.font_huge = pygame.font.SysFont("Segoe UI", 48, bold=True)
        self.font_large = pygame.font.SysFont("Segoe UI", 28, bold=True)
        self.font_mid = pygame.font.SysFont("Segoe UI", 18, bold=True)
        self.font_small = pygame.font.SysFont("Segoe UI", 12)

        self.sfx = SoundFX()

        # Arena bounds (centered combat pitch)
        self.arena_rect = pygame.Rect(60, 80, SCREEN_WIDTH - 120, SCREEN_HEIGHT - 130)

        # Auto-detect Dual Joysticks
        self.joysticks = []
        self.scan_joysticks()

        # Game State
        self.state = "MENU" # MENU, CHAR_SELECT, PLAYING, ROUND_OVER, MATCH_OVER, PAUSE
        self.mode = "1v1" # 1v1, VS_AI, COOP

        # Players
        j0 = self.joysticks[0] if len(self.joysticks) > 0 else None
        j1 = self.joysticks[1] if len(self.joysticks) > 1 else None

        self.p1 = Player(1, self.arena_rect.left + 150, self.arena_rect.centery, COLOR_CYAN, "VIPER", j0)
        self.p2 = Player(2, self.arena_rect.right - 150, self.arena_rect.centery, COLOR_EMERALD, "TITAN", j1)

        self.projectiles = []
        self.particles = []
        self.shockwaves = []
        self.floating_texts = []
        self.powerups = []
        self.powerup_timer = 300

        self.round_num = 1
        self.max_rounds = 3
        self.round_timer = 90 * FPS
        self.round_winner = None
        self.match_winner = None
        self.shake_intensity = 0.0

        # Background grid wave simulation
        self.grid_nodes = []
        self.init_grid()

    def scan_joysticks(self):
        pygame.joystick.quit()
        pygame.joystick.init()
        self.joysticks = []
        for i in range(pygame.joystick.get_count()):
            try:
                j = pygame.joystick.Joystick(i)
                j.init()
                self.joysticks.append(j)
            except Exception:
                pass
        print(f"[+] Active joysticks bound: {len(self.joysticks)}")

    def init_grid(self):
        self.grid_nodes = []
        for x in range(self.arena_rect.left, self.arena_rect.right + 40, 50):
            for y in range(self.arena_rect.top, self.arena_rect.bottom + 40, 50):
                self.grid_nodes.append([x, y, 0.0]) # base_x, base_y, ripple_offset

    def trigger_shake(self, amount):
        self.shake_intensity = min(20.0, self.shake_intensity + amount)

    def spawn_powerup(self):
        px = random.randint(self.arena_rect.left + 60, self.arena_rect.right - 60)
        py = random.randint(self.arena_rect.top + 60, self.arena_rect.bottom - 60)
        self.powerups.append(Powerup(px, py))
        self.shockwaves.append(Shockwave(px, py, COLOR_GOLD, 50, 4))

    def reset_round(self):
        self.p1.reset_position()
        self.p2.reset_position()
        self.projectiles.clear()
        self.powerups.clear()
        self.round_timer = 90 * FPS

    # =========================================================================
    # UPDATE & DRAW
    # =========================================================================
    def update(self):
        keys = pygame.key.get_pressed()

        if self.state == "PLAYING":
            # 1. Update Players
            self.p1.handle_input(keys, self.sfx, self.projectiles, self.particles)
            self.p1.clamp_to_arena(self.arena_rect)

            if self.mode == "VS_AI" and not self.p2.joystick:
                self.update_ai()
            else:
                self.p2.handle_input(keys, self.sfx, self.projectiles, self.particles)
            self.p2.clamp_to_arena(self.arena_rect)

            # 2. Projectiles vs Players
            for proj in self.projectiles[:]:
                active = proj.update(self.particles, self.arena_rect)
                if not active:
                    self.projectiles.remove(proj)
                    continue

                # Check hit P1
                if proj.owner != 1 and math.hypot(proj.x - self.p1.x, proj.y - self.p1.y) < (proj.radius + self.p1.radius):
                    dead = self.p1.take_damage(proj.damage, self.sfx, self.floating_texts, self.font_small)
                    self.trigger_shake(6)
                    self.shockwaves.append(Shockwave(proj.x, proj.y, self.p1.color, 40))
                    for _ in range(12):
                        self.particles.append(Particle(proj.x, proj.y, random.uniform(-4, 4), random.uniform(-4, 4), self.p1.color, 4, 20))
                    if proj in self.projectiles:
                        self.projectiles.remove(proj)
                    if dead:
                        self.handle_round_end(winner=2)
                        break

                # Check hit P2
                elif proj.owner != 2 and math.hypot(proj.x - self.p2.x, proj.y - self.p2.y) < (proj.radius + self.p2.radius):
                    dead = self.p2.take_damage(proj.damage, self.sfx, self.floating_texts, self.font_small)
                    self.trigger_shake(6)
                    self.shockwaves.append(Shockwave(proj.x, proj.y, self.p2.color, 40))
                    for _ in range(12):
                        self.particles.append(Particle(proj.x, proj.y, random.uniform(-4, 4), random.uniform(-4, 4), self.p2.color, 4, 20))
                    if proj in self.projectiles:
                        self.projectiles.remove(proj)
                    if dead:
                        self.handle_round_end(winner=1)
                        break

            # 3. Powerups Pickup
            for pw in self.powerups[:]:
                pw.update()
                for p in [self.p1, self.p2]:
                    if math.hypot(p.x - pw.x, p.y - pw.y) < (p.radius + pw.radius):
                        self.apply_powerup(p, pw.type)
                        self.sfx.play('powerup')
                        self.floating_texts.append(FloatingText(pw.x, pw.y, pw.label, pw.color, self.font_mid))
                        self.shockwaves.append(Shockwave(pw.x, pw.y, pw.color, 60))
                        if pw in self.powerups:
                            self.powerups.remove(pw)
                        break

            # 4. Powerup Spawner
            self.powerup_timer -= 1
            if self.powerup_timer <= 0:
                self.spawn_powerup()
                self.powerup_timer = random.randint(400, 700)

            # 5. Round Timer
            self.round_timer -= 1
            if self.round_timer <= 0:
                # Time out -> Highest HP wins
                win = 1 if self.p1.hp >= self.p2.hp else 2
                self.handle_round_end(winner=win)

        # Decay shake
        if self.shake_intensity > 0:
            self.shake_intensity = max(0.0, self.shake_intensity * 0.9)

        # Update Visual FX
        self.particles = [p for p in self.particles if p.update()]
        self.shockwaves = [s for s in self.shockwaves if s.update()]
        self.floating_texts = [t for t in self.floating_texts if t.update()]

    def update_ai(self):
        # Intelligent Bot for Solo Play
        dx = self.p1.x - self.p2.x
        dy = self.p1.y - self.p2.y
        dist = math.hypot(dx, dy)
        target_angle = math.atan2(dy, dx)
        self.p2.angle = target_angle

        # Strafe around P1
        if dist > 260:
            self.p2.x += math.cos(target_angle) * self.p2.speed
            self.p2.y += math.sin(target_angle) * self.p2.speed
        else:
            strafe = target_angle + math.pi / 2
            self.p2.x += math.cos(strafe) * self.p2.speed * 0.8
            self.p2.y += math.sin(strafe) * self.p2.speed * 0.8

        # AI Shooting
        if self.p2.cooldown <= 0 and random.random() < 0.6:
            nose_x = self.p2.x + math.cos(self.p2.angle) * 20
            nose_y = self.p2.y + math.sin(self.p2.angle) * 20
            self.projectiles.append(Projectile(nose_x, nose_y, self.p2.angle, 14, 15, self.p2.color, 2, "laser"))
            self.sfx.play('laser')
            self.p2.cooldown = self.p2.fire_rate + 2

    def apply_powerup(self, player, p_type):
        if p_type == "shield":
            player.shield = 50
        elif p_type == "speed":
            player.speed_boost_timer = 300
        elif p_type == "plasma":
            player.plasma_buff_timer = 300
        elif p_type == "heal":
            player.hp = min(player.max_hp, player.hp + 35)
        elif p_type == "nuke":
            # EMP Nuke deals 30 damage to opponent and clears projectiles
            opponent = self.p2 if player.p_id == 1 else self.p1
            opponent.take_damage(30, self.sfx, self.floating_texts, self.font_mid)
            self.projectiles.clear()
            self.trigger_shake(15)
            self.sfx.play('explosion')

    def handle_round_end(self, winner):
        self.round_winner = winner
        self.sfx.play('ko')
        self.trigger_shake(12)

        if winner == 1:
            self.p1.rounds_won += 1
        else:
            self.p2.rounds_won += 1

        # Check if match won
        rounds_to_win = (self.max_rounds // 2) + 1
        if self.p1.rounds_won >= rounds_to_win:
            self.match_winner = 1
            self.state = "MATCH_OVER"
        elif self.p2.rounds_won >= rounds_to_win:
            self.match_winner = 2
            self.state = "MATCH_OVER"
        else:
            self.state = "ROUND_OVER"
            self.round_over_timer = 120 # 2 seconds

    def draw(self):
        # 1. Apply Screen Shake
        ox = random.uniform(-self.shake_intensity, self.shake_intensity) if self.shake_intensity > 0 else 0
        oy = random.uniform(-self.shake_intensity, self.shake_intensity) if self.shake_intensity > 0 else 0

        self.screen.fill(COLOR_BG)

        # 2. Draw Arena Grid
        pygame.draw.rect(self.screen, COLOR_DARK_PANEL, self.arena_rect)
        pygame.draw.rect(self.screen, COLOR_CYAN, self.arena_rect, 2)

        for x in range(self.arena_rect.left, self.arena_rect.right + 20, 50):
            pygame.draw.line(self.screen, COLOR_GRID, (x + ox, self.arena_rect.top), (x + ox, self.arena_rect.bottom))
        for y in range(self.arena_rect.top, self.arena_rect.bottom + 20, 50):
            pygame.draw.line(self.screen, COLOR_GRID, (self.arena_rect.left, y + oy), (self.arena_rect.right, y + oy))

        # Center Arena Ring
        pygame.draw.circle(self.screen, COLOR_GRID, self.arena_rect.center, 90, 1)

        # 3. Draw Game Objects
        for pw in self.powerups:
            pw.draw(self.screen, self.font_small)

        for proj in self.projectiles:
            proj.draw(self.screen)

        for p in self.particles:
            p.draw(self.screen)

        for s in self.shockwaves:
            s.draw(self.screen)

        if self.state in ["PLAYING", "ROUND_OVER", "MATCH_OVER"]:
            self.p1.draw(self.screen)
            self.p2.draw(self.screen)

        for txt in self.floating_texts:
            txt.draw(self.screen)

        # 4. Top Header & HUD
        self.draw_hud()

        # 5. Overlays for Menus / KO
        if self.state == "MENU":
            self.draw_menu()
        elif self.state == "CHAR_SELECT":
            self.draw_char_select()
        elif self.state == "ROUND_OVER":
            self.draw_round_banner()
        elif self.state == "MATCH_OVER":
            self.draw_match_over()
        elif self.state == "PAUSE":
            self.draw_pause()

        pygame.display.flip()

    def draw_hud(self):
        # 1. Top Header Bar (Combat Metrics)
        hdr_rect = pygame.Rect(0, 0, SCREEN_WIDTH, 70)
        pygame.draw.rect(self.screen, (14, 18, 28), hdr_rect)
        pygame.draw.line(self.screen, (30, 42, 60), (0, 70), (SCREEN_WIDTH, 70), 1)

        # Player 1 HUD (Left)
        p1_title = self.font_mid.render(f"P1: {self.p1.ship_type} (Cyan)", True, COLOR_CYAN)
        self.screen.blit(p1_title, (50, 8))
        # P1 Health Bar
        self.draw_bar(50, 30, 240, 16, self.p1.hp, self.p1.max_hp, COLOR_CYAN, self.p1.shield)
        # P1 Stamina / Dash
        self.draw_bar(50, 48, 240, 6, self.p1.stamina, 100.0, COLOR_GOLD)
        # P1 Score Stars
        for i in range(2):
            star_col = COLOR_GOLD if i < self.p1.rounds_won else (40, 50, 70)
            pygame.draw.circle(self.screen, star_col, (305 + i * 18, 38), 6)

        # Round & Timer Display (Center)
        t_sec = max(0, self.round_timer // FPS)
        timer_lbl = self.font_large.render(f"{t_sec:02d}", True, COLOR_WHITE)
        self.screen.blit(timer_lbl, (SCREEN_WIDTH // 2 - timer_lbl.get_width() // 2, 8))
        round_lbl = self.font_small.render(f"ROUND {self.round_num} / {self.max_rounds}", True, COLOR_GOLD)
        self.screen.blit(round_lbl, (SCREEN_WIDTH // 2 - round_lbl.get_width() // 2, 42))

        # Player 2 HUD (Right)
        p2_title = self.font_mid.render(f"P2: {self.p2.ship_type} (Emerald)", True, COLOR_EMERALD)
        self.screen.blit(p2_title, (SCREEN_WIDTH - 50 - 240, 8))
        # P2 Health Bar
        self.draw_bar(SCREEN_WIDTH - 50 - 240, 30, 240, 16, self.p2.hp, self.p2.max_hp, COLOR_EMERALD, self.p2.shield)
        # P2 Stamina / Dash
        self.draw_bar(SCREEN_WIDTH - 50 - 240, 48, 240, 6, self.p2.stamina, 100.0, COLOR_GOLD)
        # P2 Score Stars
        for i in range(2):
            star_col = COLOR_GOLD if i < self.p2.rounds_won else (40, 50, 70)
            pygame.draw.circle(self.screen, star_col, (SCREEN_WIDTH - 305 - i * 18, 38), 6)

        # 2. Dedicated Bottom Footer Bar (Status & Watermark)
        ftr_y = SCREEN_HEIGHT - 38
        ftr_rect = pygame.Rect(0, ftr_y, SCREEN_WIDTH, 38)
        pygame.draw.rect(self.screen, (12, 16, 24), ftr_rect)
        pygame.draw.line(self.screen, (30, 42, 60), (0, ftr_y), (SCREEN_WIDTH, ftr_y), 1)

        # Left: Gamepad Status
        j_cnt = len(self.joysticks)
        j_col = COLOR_EMERALD if j_cnt >= 2 else (COLOR_GOLD if j_cnt == 1 else COLOR_CYAN)
        j_str = f"[JOSTIK] {j_cnt}/2 Ulangan (Faol)" if j_cnt > 0 else "[KLAVIATURA] 2x Rejim (W/A/S/D & O'qlar)"
        j_lbl = self.font_small.render(j_str, True, j_col)
        self.screen.blit(j_lbl, (30, ftr_y + 11))

        # Center: Quick Control Guide
        guide_str = "Boshqaruv: [A / Cross] Otish | [Y / Triangle] Dash | [B / Circle] Raketa | [START] Menyu"
        guide_lbl = self.font_small.render(guide_str, True, (160, 180, 205))
        self.screen.blit(guide_lbl, (SCREEN_WIDTH // 2 - guide_lbl.get_width() // 2, ftr_y + 11))

        # Right: Author Signature Watermark (Rule 7)
        auth = self.font_small.render(f"Dasturchi: {AUTHOR} | Zero-Defect Studio", True, (110, 135, 170))
        self.screen.blit(auth, (SCREEN_WIDTH - auth.get_width() - 30, ftr_y + 11))

    def draw_bar(self, x, y, w, h, val, max_val, color, shield=0):
        pygame.draw.rect(self.screen, (25, 30, 45), (x, y, w, h))
        pct = max(0.0, min(1.0, val / max_val))
        pygame.draw.rect(self.screen, color, (x, y, int(w * pct), h))
        if shield > 0:
            sh_pct = min(1.0, shield / 50.0)
            pygame.draw.rect(self.screen, (255, 255, 255, 120), (x, y, int(w * sh_pct), h), 2)
        pygame.draw.rect(self.screen, (60, 75, 100), (x, y, w, h), 1)

    def draw_menu(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((10, 14, 22, 230))
        self.screen.blit(overlay, (0, 0))

        # Title
        t1 = self.font_huge.render("CYBER ARENA: 2x JOSTIK", True, COLOR_CYAN)
        t2 = self.font_large.render("MUKAMMAL 2-KISHILIK O'YIN", True, COLOR_GOLD)
        self.screen.blit(t1, (SCREEN_WIDTH // 2 - t1.get_width() // 2, 130))
        self.screen.blit(t2, (SCREEN_WIDTH // 2 - t2.get_width() // 2, 190))

        # Buttons / Menu Options
        opts = [
            ("1. 2 O'YINCHI 1v1 (Jostik 1 vs Jostik 2)", "1v1", COLOR_CYAN),
            ("2. 1 O'YINCHI (AI Botga Qarshi Sinov)", "VS_AI", COLOR_EMERALD),
            ("3. CHIQISH", "EXIT", COLOR_RED)
        ]

        cy = 310
        for text, mode, col in opts:
            box = pygame.Rect(SCREEN_WIDTH // 2 - 240, cy, 480, 50)
            pygame.draw.rect(self.screen, COLOR_DARK_PANEL, box)
            pygame.draw.rect(self.screen, col, box, 2)
            lbl = self.font_mid.render(text, True, COLOR_WHITE)
            self.screen.blit(lbl, (box.centerx - lbl.get_width() // 2, box.centery - lbl.get_height() // 2))
            cy += 70

        # Controls Hint
        hint = self.font_small.render("Tugmalar: [A / Cross] = Otish  |  [Triangle / Y] = Dash  |  [B / Circle] = Raketa  |  [START] = Boshlash", True, (160, 180, 210))
        self.screen.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, SCREEN_HEIGHT - 60))

    def draw_char_select(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((10, 14, 22, 230))
        self.screen.blit(overlay, (0, 0))

        title = self.font_large.render("KEMA VA QAHRAMONNI TANLANG", True, COLOR_GOLD)
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))

        # 3 Ships Cards
        ships = [
            ("VIPER", "Tezkor Qiruvchi", "Tezlik: ★★★★★ | Zirh: ★★★☆☆ | Qurol: Ikkitalik Plazma", COLOR_CYAN),
            ("TITAN", "Og'ir Zirhli", "Tezlik: ★★★☆☆ | Zirh: ★★★★★ | Qurol: Og'ir Zarbador To'p", COLOR_EMERALD),
            ("SPECTRE", "Taktik Qidiruvchi", "Tezlik: ★★★★☆ | Zirh: ★★★★☆ | Qurol: O'zi Qidiruvchi Raketa", COLOR_PURPLE)
        ]

        cx = 160
        for name, sub, desc, col in ships:
            card = pygame.Rect(cx, 200, 280, 320)
            pygame.draw.rect(self.screen, COLOR_DARK_PANEL, card)
            pygame.draw.rect(self.screen, col, card, 2)

            nl = self.font_large.render(name, True, col)
            sl = self.font_mid.render(sub, True, COLOR_WHITE)
            dl = self.font_small.render(desc.split('|')[0], True, (160, 175, 200))
            dl2 = self.font_small.render(desc.split('|')[1], True, (160, 175, 200))
            dl3 = self.font_small.render(desc.split('|')[2], True, (160, 175, 200))

            self.screen.blit(nl, (card.centerx - nl.get_width() // 2, card.top + 30))
            self.screen.blit(sl, (card.centerx - sl.get_width() // 2, card.top + 70))
            self.screen.blit(dl, (card.centerx - dl.get_width() // 2, card.top + 140))
            self.screen.blit(dl2, (card.centerx - dl2.get_width() // 2, card.top + 170))
            self.screen.blit(dl3, (card.centerx - dl3.get_width() // 2, card.top + 200))

            btn = self.font_mid.render("TANLASH (A / Space)", True, col)
            pygame.draw.rect(self.screen, (25, 35, 50), (card.left + 20, card.bottom - 60, 240, 40))
            pygame.draw.rect(self.screen, col, (card.left + 20, card.bottom - 60, 240, 40), 1)
            self.screen.blit(btn, (card.centerx - btn.get_width() // 2, card.bottom - 50))

            cx += 340

    def draw_round_banner(self):
        w_col = COLOR_CYAN if self.round_winner == 1 else COLOR_EMERALD
        w_text = f"ROUND {self.round_num} G'OLIBI: {self.round_winner}-O'YINCHI!"
        lbl = self.font_huge.render(w_text, True, w_col)
        self.screen.blit(lbl, (SCREEN_WIDTH // 2 - lbl.get_width() // 2, SCREEN_HEIGHT // 2 - 40))

    def draw_match_over(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((10, 14, 22, 220))
        self.screen.blit(overlay, (0, 0))

        w_col = COLOR_CYAN if self.match_winner == 1 else COLOR_EMERALD
        w_text = f"CHEMPION: {self.match_winner}-O'YINCHI! 🏆"
        lbl = self.font_huge.render(w_text, True, w_col)
        sub = self.font_large.render("Qayta o'ynash uchun [START] yoki [SPACE] bosing", True, COLOR_GOLD)
        self.screen.blit(lbl, (SCREEN_WIDTH // 2 - lbl.get_width() // 2, SCREEN_HEIGHT // 2 - 60))
        self.screen.blit(sub, (SCREEN_WIDTH // 2 - sub.get_width() // 2, SCREEN_HEIGHT // 2 + 30))

    def draw_pause(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((10, 14, 22, 180))
        self.screen.blit(overlay, (0, 0))

        p_lbl = self.font_huge.render("PAUZA (TO'XTATILDI)", True, COLOR_GOLD)
        sub = self.font_mid.render("Davom etish uchun [START] yoki [ESC] bosing", True, COLOR_WHITE)
        self.screen.blit(p_lbl, (SCREEN_WIDTH // 2 - p_lbl.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(sub, (SCREEN_WIDTH // 2 - sub.get_width() // 2, SCREEN_HEIGHT // 2 + 20))

    # =========================================================================
    # EVENT LOOP & SCENE TRANSITIONS
    # =========================================================================
    def run(self):
        running = True
        while running:
            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # Keyboard Controls
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.state == "PLAYING":
                            self.state = "PAUSE"
                        elif self.state == "PAUSE":
                            self.state = "PLAYING"
                        elif self.state in ["CHAR_SELECT", "ROUND_OVER", "MATCH_OVER"]:
                            self.state = "MENU"

                    if self.state == "MENU":
                        if event.key in [pygame.K_1, pygame.K_RETURN, pygame.K_SPACE]:
                            self.mode = "1v1"
                            self.state = "CHAR_SELECT"
                            self.sfx.play('beep')
                        elif event.key == pygame.K_2:
                            self.mode = "VS_AI"
                            self.state = "CHAR_SELECT"
                            self.sfx.play('beep')

                    elif self.state == "CHAR_SELECT":
                        if event.key in [pygame.K_RETURN, pygame.K_SPACE, pygame.K_1]:
                            self.p1.ship_type = "VIPER"
                            self.p2.ship_type = "TITAN"
                            self.reset_match()
                            self.state = "PLAYING"
                            self.sfx.play('beep')

                    elif self.state == "MATCH_OVER":
                        if event.key in [pygame.K_SPACE, pygame.K_RETURN]:
                            self.reset_match()
                            self.state = "PLAYING"

                # Gamepad START / Cross Buttons in Menus
                elif event.type == pygame.JOYBUTTONDOWN:
                    btn = event.button
                    if btn == 9: # START
                        if self.state == "MENU":
                            self.mode = "1v1"
                            self.state = "CHAR_SELECT"
                            self.sfx.play('beep')
                        elif self.state == "PLAYING":
                            self.state = "PAUSE"
                        elif self.state == "PAUSE":
                            self.state = "PLAYING"
                        elif self.state == "MATCH_OVER":
                            self.reset_match()
                            self.state = "PLAYING"
                    elif btn == 2: # A / Cross (Select)
                        if self.state == "MENU":
                            self.mode = "1v1"
                            self.state = "CHAR_SELECT"
                            self.sfx.play('beep')
                        elif self.state == "CHAR_SELECT":
                            self.reset_match()
                            self.state = "PLAYING"
                            self.sfx.play('beep')

            # State-specific timing
            if self.state == "ROUND_OVER":
                self.round_over_timer -= 1
                if self.round_over_timer <= 0:
                    self.round_num += 1
                    self.reset_round()
                    self.state = "PLAYING"

            self.update()
            self.draw()

        pygame.quit()

    def reset_match(self):
        self.round_num = 1
        self.p1.rounds_won = 0
        self.p2.rounds_won = 0
        self.match_winner = None
        self.round_winner = None
        self.reset_round()

if __name__ == '__main__':
    game = CyberArenaGame()
    game.run()
