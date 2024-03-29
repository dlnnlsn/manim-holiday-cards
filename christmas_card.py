from manim import *
import functools
import itertools
import random

GREETING = "To [Recipient]..."
SIGNOFF = "From [Sender]"
FONT = "Edwardian Script ITC"
FONT_SIZE = 1.5


class ChristmasCard(Scene):
    def construct(self):
        for _ in range(100):
            self.add(
                Snowflake(
                    point=np.random.uniform(-1, 1, 3)
                    * np.array([config.frame_x_radius, config.frame_y_radius, 0])
                )
            )

        tree = VGroup(
            Polygon(
                np.array([0, 2, 0]),
                np.array([-1.75, -2, 0]),
                np.array([1.75, -2, 0]),
                color=GREEN,
            )
        )
        trunk = VGroup(Rectangle(height=1.5, width=1, color=DARK_BROWN))
        tree.to_edge(RIGHT, buff=1)
        trunk.next_to(tree, DOWN, buff=0)
        self.play(Create(trunk), Create(tree))

        for _ in range(5):
            next_iter = next_sierpinski_iteration(tree)
            self.play(Transform(tree, next_iter))

        for _ in range(40):
            triangle = random.choice(tree.submobjects)
            weights = np.random.rand(len(triangle.get_vertices()))
            weights /= sum(weights)
            bauble_pt = weights.dot(np.array(triangle.get_vertices()))
            self.play(
                FadeIn(Dot(point=bauble_pt, color=random_bright_color(), radius=0.1)),
                run_time=0.1,
            )

        star = Tex("$\\star$", color=YELLOW)
        star.scale(2)
        star.next_to(tree, UP, buff=0)
        self.add(star)

        if GREETING:
            greeting = Text(GREETING, font=FONT).scale(FONT_SIZE)
            greeting.to_corner(UL)
            self.play(Write(greeting), run_time=3)

        message = Text("Merry Christmas", font=FONT).scale(FONT_SIZE)
        self.play(Write(message), run_time=3)
        self.wait()

        if SIGNOFF:
            signoff = Text(SIGNOFF, font=FONT).scale(FONT_SIZE)
            signoff.to_corner(DR)
            self.play(Write(signoff), run_time=3)


def divide_triangle(triangle):
    vertices = list(triangle.get_vertices())
    midpoints = list(
        itertools.starmap(
            lambda x, y: (x + y) / 2, zip(vertices, vertices[1:] + [vertices[0]])
        )
    )
    return itertools.starmap(
        functools.partial(Polygon, color=triangle.color),
        zip(vertices, midpoints, [midpoints[-1]] + midpoints),
    )


def next_sierpinski_iteration(triangles):
    return VGroup(*itertools.chain(*map(divide_triangle, triangles.submobjects)))


def drift_down(mobj, dt):
    mobj.shift(dt * DOWN)
    mobj.shift(random.gauss(0, 0.01) * RIGHT)
    if mobj.get_arc_center()[1] < -config.frame_y_radius:
        mobj.to_edge(UP)


class Snowflake(Dot):
    def __init__(self, *args, radius=0.04, **kwargs):
        super().__init__(*args, radius=radius, **kwargs)
        self.add_updater(drift_down)
