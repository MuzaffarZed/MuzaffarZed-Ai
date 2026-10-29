"""
Pro-Cinema Engine: Manim 3D Mathematical & Physical Simulation Suite
Author: MuzaffarZed
Standards:
- 3D spatial simulation scenes (No flat 2D cards)
- Dynamic camera tracking & mathematical curves
"""

from manim import *
import numpy as np

class CosmicSpaceTimeCurvature(ThreeDScene):
    """
    Simulates gravitational spacetime curvature around a massive singularity
    using a 3D parametric surface, geodesic grid lines, and orbiting particles.
    """
    def construct(self):
        # 1. Setup 3D Camera
        self.set_camera_orientation(phi=65 * DEGREES, theta=-55 * DEGREES)

        # 2. Spacetime Grid Surface (Warped Funnel)
        def spacetime_funnel(u, v):
            # u: radius, v: angle
            r = u
            theta = v
            x = r * np.cos(theta)
            y = r * np.sin(theta)
            # Gravitational well depth
            z = -2.5 / (r + 0.35)
            return np.array([x, y, z])

        grid_surface = Surface(
            spacetime_funnel,
            u_range=[0.4, 3.8],
            v_range=[0, TAU],
            resolution=(24, 48),
            fill_opacity=0.35,
            checkerboard_colors=[BLUE_E, PURPLE_E],
            stroke_color=TEAL_A,
            stroke_width=0.8
        )

        # 3. Central Singularity Sphere
        singularity = Sphere(radius=0.45, color=GOLD_A)
        singularity.set_fill(BLACK, opacity=1.0)
        singularity.move_to([0, 0, -2.5 / (0.45 + 0.35)])

        # 4. Title & Mathematical Equation
        title = Text("FAZO-VAQT EGRI CHIZIG'I", font="Inter", weight="BOLD", font_size=28)
        title.to_corner(UL)
        self.add_fixed_in_frame_mobjects(title)

        formula = Text("G_μν + Λg_μν = (8πG/c⁴) T_μν", font="Inter", font_size=24, color=YELLOW)
        formula.to_corner(UR)
        self.add_fixed_in_frame_mobjects(formula)

        # Watermark (Rule 7)
        watermark = Text("Dasturchi: MuzaffarZed", font="Inter", font_size=18, color=GRAY_B)
        watermark.to_corner(DR)
        self.add_fixed_in_frame_mobjects(watermark)

        # 5. Animations
        self.play(Create(grid_surface), run_time=2.0)
        self.play(FadeIn(singularity), Write(title), Write(formula), run_time=1.5)

        # 6. Smooth Cinematic Camera Orbit
        self.begin_ambient_camera_rotation(rate=0.25)
        self.wait(2.5)
        self.stop_ambient_camera_rotation()

        self.play(FadeOut(grid_surface), FadeOut(singularity), FadeOut(title), FadeOut(formula), run_time=1.0)
