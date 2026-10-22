import math
import random
import time
import turtle
from _engine import t, USE_SVG

# Enable RGB color tuples (0-255) so students can easily use the Google Color Picker
turtle.colormode(255)

# --- BASELINE EXAMPLES ---
def draw_bubble(x, y, radius):
    """
    Draws a single circular bubble using turtle commands.
    
    Args:
        x (int): The x-coordinate for the center of the bubble.
        y (int): The y-coordinate for the center of the bubble.
        radius (int): The size of the bubble.
        
    Returns:
        None
    """
    t.penup()
    t.color("#75D9F2")
    t.pensize(2)
    t.goto(x, y - radius)
    t.pendown()
    t.circle(radius)


def draw_seaweed(x, y, segments, color_name, sway_phase=0):
    """
    Draws a leafy sea plant with a curved stem and alternating fronds.
    
    Args:
        x (int): The starting x-coordinate for the seaweed.
        y (int): The starting y-coordinate (usually the tank floor).
        segments (int): How tall the seaweed should grow.
        color_name (str): The color of the seaweed.
        sway_phase (float): Animation phase controlling the seaweed's sway.
        
    Returns:
        None
    """
    palette = {
        "green": ("#236A42", "#34834D", "#63A95B"),
        "darkgreen": ("#174A37", "#246347", "#4D8B51"),
    }
    outline, leaf_color, highlight = palette.get(
        color_name, (color_name, color_name, color_name)
    )
    height = segments * 25
    sway = max(5, segments * 1.5)

    def stem_x(progress):
        return x + math.sin(progress * math.pi * 1.5 + sway_phase) * sway * progress

    def draw_blade(root, tip, side, blade_length):
        tip_x, tip_y = tip
        root_x, root_y = root
        width = blade_length * 0.23
        t.penup()
        t.goto(root_x, root_y)
        t.color(outline)
        t.fillcolor(leaf_color)
        t.begin_fill()
        t.pendown()
        for step in range(1, 13):
            amount = step / 12
            inverse = 1 - amount
            point = (
                inverse ** 3 * root_x
                + 3 * inverse ** 2 * amount * (root_x + side * width)
                + 3 * inverse * amount ** 2 * (tip_x + side * width)
                + amount ** 3 * tip_x,
                inverse ** 3 * root_y
                + 3 * inverse ** 2 * amount * (root_y + blade_length * 0.28)
                + 3 * inverse * amount ** 2 * (tip_y - blade_length * 0.28)
                + amount ** 3 * tip_y,
            )
            t.goto(*point)
        for step in range(1, 13):
            amount = step / 12
            inverse = 1 - amount
            point = (
                inverse ** 3 * tip_x
                + 3 * inverse ** 2 * amount * (tip_x - side * width)
                + 3 * inverse * amount ** 2 * (root_x - side * width * 0.3)
                + amount ** 3 * root_x,
                inverse ** 3 * tip_y
                + 3 * inverse ** 2 * amount * (tip_y - blade_length * 0.28)
                + 3 * inverse * amount ** 2 * (root_y + blade_length * 0.28)
                + amount ** 3 * root_y,
            )
            t.goto(*point)
        t.end_fill()

        t.penup()
        t.goto(root_x, root_y)
        t.color(highlight)
        t.pensize(max(1, segments * 0.16))
        t.pendown()
        t.goto(tip_x, tip_y)
        t.penup()

    # Draw the fronds behind the stem, alternating up both sides.
    for index in range(segments):
        progress = 0.18 + index * 0.72 / max(1, segments - 1)
        root_y = y + progress * height
        root = (stem_x(progress), root_y)
        side = -1 if index % 2 == 0 else 1
        blade_length = height * (0.2 - 0.045 * progress)
        tip = (
            root[0] + side * blade_length * 0.78,
            root_y + blade_length * 0.42,
        )
        draw_blade(root, tip, side, blade_length)

    t.penup()
    t.goto(stem_x(0), y)
    t.color(outline)
    t.pensize(max(2, segments * 0.38))
    t.setheading(90)
    t.pendown()
    for step in range(1, 25):
        progress = step / 24
        t.goto(stem_x(progress), y + progress * height)
    t.penup()
    t.color(highlight)
    t.pensize(max(1, segments * 0.12))
    t.goto(stem_x(0.02) + 1, y + height * 0.02)
    t.pendown()
    for step in range(1, 20):
        progress = 0.02 + step / 20 * 0.78
        t.goto(stem_x(progress) + 1, y + progress * height)
    t.penup()


def draw_water_background():
    """Draws a smooth water gradient with light that fades toward the bottom."""
    color_stops = (
        (0.0, (7, 34, 54)),
        (0.35, (10, 57, 77)),
        (0.72, (18, 111, 132)),
        (1.0, (48, 151, 163)),
    )

    def water_color(level):
        for index in range(len(color_stops) - 1):
            start_level, start_color = color_stops[index]
            end_level, end_color = color_stops[index + 1]
            if level <= end_level:
                fraction = (level - start_level) / (end_level - start_level)
                channels = tuple(
                    round(start + (end - start) * fraction)
                    for start, end in zip(start_color, end_color)
                )
                return "#{:02X}{:02X}{:02X}".format(*channels)
        return "#{:02X}{:02X}{:02X}".format(*color_stops[-1][1])

    t.pensize(0)
    band_count = 112
    band_height = 560 / band_count
    for band in range(band_count):
        bottom = -280 + band * band_height
        top = bottom + band_height
        t.penup()
        t.goto(-380, bottom)
        t.color(water_color((bottom + 280) / 560))
        t.fillcolor(water_color((bottom + 280) / 560))
        t.begin_fill()
        t.pendown()
        t.goto(380, bottom)
        t.goto(380, top)
        t.goto(-380, top)
        t.goto(-380, bottom)
        t.end_fill()

    beams = (
        (-205, -95, -78, 68),
        (-45, 25, 82, 222),
        (115, 190, 226, 348),
    )
    light_color = (93, 177, 188)
    beam_slices = 64
    for top_left, top_right, bottom_left, bottom_right in beams:
        for band in range(beam_slices):
            start = band / beam_slices
            end = (band + 1) / beam_slices
            y_top = 280 - start * 535
            y_bottom = 280 - end * 535
            top_left_x = top_left + (bottom_left - top_left) * start
            top_right_x = top_right + (bottom_right - top_right) * start
            bottom_left_x = top_left + (bottom_left - top_left) * end
            bottom_right_x = top_right + (bottom_right - top_right) * end
            fade = (1 - (start + end) / 2) ** 2
            strength = 0.32 * fade
            base_color = water_color((y_top + 280) / 560)
            base_rgb = tuple(
                int(base_color[index:index + 2], 16)
                for index in (1, 3, 5)
            )
            beam_rgb = tuple(
                round(base + (light - base) * strength)
                for base, light in zip(base_rgb, light_color)
            )
            beam_color = "#{:02X}{:02X}{:02X}".format(*beam_rgb)
            points = (
                (top_left_x, y_top),
                (top_right_x, y_top),
                (bottom_right_x, y_bottom),
                (bottom_left_x, y_bottom),
            )
            t.penup()
            t.goto(points[0])
            t.color(beam_color)
            t.fillcolor(beam_color)
            t.begin_fill()
            t.pendown()
            for point in points[1:]:
                t.goto(point)
            t.goto(points[0])
            t.end_fill()

    # Gentle surface ripples catch the brightest light near the waterline.
    for ripple_x, ripple_y, ripple_width in (
        (-170, 248, 72), (-45, 262, 55), (80, 244, 88),
        (220, 260, 68), (310, 235, 48),
    ):
        t.penup()
        t.goto(ripple_x - ripple_width / 2, ripple_y)
        t.color("#70B6B5")
        t.pensize(2)
        t.pendown()
        for step in range(1, 13):
            progress = step / 12
            point_x = ripple_x - ripple_width / 2 + ripple_width * progress
            point_y = ripple_y + math.sin(progress * math.pi * 2) * 2
            t.goto(point_x, point_y)
        t.penup()
    t.penup()


def draw_sandy_bottom():
    """Draws a shallow sandy bed with scattered small stones."""
    t.penup()
    t.goto(-380, -251)
    t.color("#766747")
    t.fillcolor("#B9A477")
    t.begin_fill()
    t.pendown()
    for step in range(1, 33):
        x = -380 + step * (760 / 32)
        y = -248 + math.sin(step * 0.55) * 2.5 + math.sin(step * 0.19) * 1.5
        t.goto(x, y)
    t.goto(380, -280)
    t.goto(-380, -280)
    t.goto(-380, -251)
    t.end_fill()

    stones = (
        (-350, -267, 5, "#887C65"), (-320, -259, 3, "#D2C39A"),
        (-279, -270, 4, "#756D60"), (-241, -262, 6, "#9C8D6B"),
        (-198, -273, 3, "#D2C39A"), (-165, -258, 4, "#817966"),
        (-116, -269, 5, "#8E8065"), (-74, -261, 3, "#D2C39A"),
        (-33, -273, 4, "#716B5E"), (14, -260, 5, "#9C8D6B"),
        (58, -270, 3, "#D2C39A"), (103, -258, 4, "#817966"),
        (147, -272, 6, "#887C65"), (190, -262, 3, "#D2C39A"),
        (228, -270, 4, "#756D60"), (271, -258, 5, "#9C8D6B"),
        (314, -271, 3, "#D2C39A"), (352, -261, 4, "#817966"),
        (-300, -276, 2, "#E0D2AB"), (-92, -277, 2, "#E0D2AB"),
        (82, -277, 2, "#E0D2AB"), (250, -276, 2, "#E0D2AB"),
    )
    for stone_x, stone_y, radius, color in stones:
        t.penup()
        t.goto(stone_x, stone_y)
        t.dot(radius * 2, color)


def draw_fish_hideaway():
    """Draws an original stone shelter with an arched doorway and porthole."""
    center_x = 250
    base_y = -267
    silhouette = (
        (center_x - 52, base_y),
        (center_x - 49, -245),
        (center_x - 42, -229),
        (center_x - 29, -220),
        (center_x - 13, -216),
        (center_x + 2, -219),
        (center_x + 16, -214),
        (center_x + 34, -221),
        (center_x + 46, -237),
        (center_x + 51, -256),
        (center_x + 49, base_y),
    )
    t.penup()
    t.goto(silhouette[0])
    t.color("#37484A")
    t.fillcolor("#65716B")
    t.begin_fill()
    t.pendown()
    for point in silhouette[1:]:
        t.goto(point)
    t.goto(silhouette[0])
    t.end_fill()

    # Recessed rounded doorway.
    doorway_x = center_x - 12
    doorway_width = 19
    doorway_spring_y = -245
    t.penup()
    t.goto(doorway_x - doorway_width, base_y)
    t.color("#26383A")
    t.fillcolor("#102126")
    t.begin_fill()
    t.pendown()
    for step in range(25):
        angle = math.pi - math.pi * step / 24
        t.goto(
            doorway_x + math.cos(angle) * doorway_width,
            doorway_spring_y + math.sin(angle) * doorway_width,
        )
    t.goto(doorway_x + doorway_width, base_y)
    t.goto(doorway_x - doorway_width, base_y)
    t.end_fill()

    # Small round window and carved seams make the structure feel lived-in.
    t.penup()
    t.goto(center_x + 25, -242)
    t.color("#3B4B49")
    t.pensize(3)
    t.fillcolor("#8BC1BC")
    t.begin_fill()
    t.pendown()
    t.circle(7)
    t.end_fill()

    t.penup()
    t.goto(center_x - 43, -247)
    t.color("#8A9488")
    t.pensize(2)
    t.pendown()
    t.goto(center_x - 29, -250)
    t.goto(center_x - 24, -258)
    t.penup()
    t.goto(center_x + 12, -229)
    t.pendown()
    t.goto(center_x + 22, -233)
    t.goto(center_x + 31, -230)
    t.penup()


# --- STUDENT FUNCTIONS ---
def draw_tank(build_left, build_bottom, build_right, build_top):
    """
    Draws the 4 walls of the rectangular fish tank using the turtle.
    
    Args:
        build_left (bool): If True, draws the left wall.
        build_bottom (bool): If True, draws the floor of the tank.
        build_right (bool): If True, draws the right wall.
        build_top (bool): If True, draws the lid of the tank.
        
    Returns:
        None
    """
    draw_water_background()
    t.color("#23508C")
    t.pensize(4)
    t.penup()
    t.goto(-380, 280)
    t.setheading(270)
    
    for i in range(4):
        if i == 0:
            if build_left:
                t.pendown()
            else:
                t.penup()
        elif i == 1:
            if build_bottom:
                t.pendown()
            else:
                t.penup()
        elif i == 2:
            if build_right:
                t.pendown()
            else:
                t.penup()
        else:
            if build_top:
                t.pendown()
            else:
                t.penup()

        if i % 2 == 0:
            t.forward(560)
        else:
            t.forward(760)
        t.left(90)


def draw_mantaray(x, y, size, is_facing_left):
    """
    Draws a manta ray with a smooth body, broad wings, and a tapered tail.

    Args:
        x (int): Center x-coordinate.
        y (int): Center y-coordinate.
        size (int): Scale of the manta ray.
        is_facing_left (bool): Direction the manta ray faces.

    Returns:
        None
    """
    direction = -1 if is_facing_left else 1

    def move_to(point):
        t.goto(x + direction * point[0] * size, y + point[1] * size)

    def draw_curve(control_1, control_2, end):
        start = current_point[0], current_point[1]
        for step in range(1, 21):
            amount = step / 20
            inverse = 1 - amount
            point = (
                inverse ** 3 * start[0]
                + 3 * inverse ** 2 * amount * control_1[0]
                + 3 * inverse * amount ** 2 * control_2[0]
                + amount ** 3 * end[0],
                inverse ** 3 * start[1]
                + 3 * inverse ** 2 * amount * control_1[1]
                + 3 * inverse * amount ** 2 * control_2[1]
                + amount ** 3 * end[1],
            )
            move_to(point)
        current_point[0], current_point[1] = end

    def draw_detail_curve(start, control_1, control_2, end, color, width):
        t.penup()
        move_to(start)
        t.color(color)
        t.pensize(max(1, size * width))
        t.pendown()
        for step in range(1, 17):
            amount = step / 16
            inverse = 1 - amount
            point = (
                inverse ** 3 * start[0]
                + 3 * inverse ** 2 * amount * control_1[0]
                + 3 * inverse * amount ** 2 * control_2[0]
                + amount ** 3 * end[0],
                inverse ** 3 * start[1]
                + 3 * inverse ** 2 * amount * control_1[1]
                + 3 * inverse * amount ** 2 * control_2[1]
                + amount ** 3 * end[1],
            )
            move_to(point)
        t.penup()

    # Draw the tail first so it sits behind the body.
    t.penup()
    t.color("#1B292D")
    t.pensize(max(1, size * 0.045))
    move_to((-0.82, 0))
    t.pendown()
    current_point = [-0.82, 0]
    draw_curve((-1.25, -0.08), (-1.8, -0.2), (-2.45, -0.18))
    t.penup()

    t.pensize(1)
    t.color("#182629")
    t.fillcolor("#35494A")
    move_to((1.25, 0))
    t.begin_fill()
    t.pendown()
    current_point = [1.25, 0]
    draw_curve((1.12, 0.12), (1.42, 0.48), (1.05, 0.43))
    draw_curve((0.72, 0.76), (0.18, 0.94), (-0.28, 1.08))
    draw_curve((-0.9, 1.26), (-1.55, 1.72), (-1.95, 1.76))
    draw_curve((-1.62, 1.18), (-1.12, 0.53), (-0.72, 0.31))
    draw_curve((-0.43, 0.16), (-0.55, 0.04), (-0.95, 0))
    draw_curve((-0.55, -0.04), (-0.43, -0.16), (-0.72, -0.31))
    draw_curve((-1.12, -0.53), (-1.62, -1.18), (-1.95, -1.76))
    draw_curve((-1.55, -1.72), (-0.9, -1.26), (-0.28, -1.08))
    draw_curve((0.18, -0.94), (0.72, -0.76), (1.05, -0.43))
    draw_curve((1.42, -0.48), (1.12, -0.12), (1.25, 0))
    t.end_fill()

    # Small dorsal fin at the base of the tail.
    t.color("#182629")
    t.fillcolor("#293C3E")
    move_to((-0.72, 0.12))
    t.begin_fill()
    t.pendown()
    move_to((-0.82, 0.43))
    move_to((-1.12, 0.12))
    move_to((-0.72, 0.12))
    t.end_fill()
    t.penup()

    markings = (
        (-1.66, 1.52, 0.035, "#AEB9B1"),
        (-1.47, 1.35, 0.045, "#D2D6CC"),
        (-1.21, 1.43, 0.03, "#AEB9B1"),
        (-1.09, 1.18, 0.04, "#C6CEC5"),
        (-0.87, 1.23, 0.03, "#D2D6CC"),
        (-0.71, 1.01, 0.04, "#AEB9B1"),
        (-0.47, 0.91, 0.03, "#C6CEC5"),
        (-1.58, 1.03, 0.03, "#D2D6CC"),
        (-1.27, 0.98, 0.035, "#AEB9B1"),
        (-1.66, -1.52, 0.035, "#AEB9B1"),
        (-1.47, -1.35, 0.045, "#D2D6CC"),
        (-1.21, -1.43, 0.03, "#AEB9B1"),
        (-1.09, -1.18, 0.04, "#C6CEC5"),
        (-0.87, -1.23, 0.03, "#D2D6CC"),
        (-0.71, -1.01, 0.04, "#AEB9B1"),
        (-0.47, -0.91, 0.03, "#C6CEC5"),
        (-1.58, -1.03, 0.03, "#D2D6CC"),
        (-1.27, -0.98, 0.035, "#AEB9B1"),
        (0.24, 0.59, 0.025, "#AEB9B1"),
        (0.02, 0.72, 0.03, "#D2D6CC"),
        (-0.2, 0.84, 0.025, "#AEB9B1"),
        (0.24, -0.59, 0.025, "#AEB9B1"),
        (0.02, -0.72, 0.03, "#D2D6CC"),
        (-0.2, -0.84, 0.025, "#AEB9B1"),
    )
    for spot_x, spot_y, spot_size, spot_color in markings:
        move_to((spot_x, spot_y))
        t.dot(size * spot_size, spot_color)

    # Pale shoulder bars and subtle rays suggest the manta's natural markings.
    for side in (-1, 1):
        draw_detail_curve(
            (0.52, side * 0.48),
            (0.18, side * 0.62),
            (-0.06, side * 0.78),
            (-0.34, side * 0.91),
            "#B8C1B8",
            0.1,
        )
        draw_detail_curve(
            (0.46, side * 0.54),
            (0.16, side * 0.68),
            (-0.08, side * 0.82),
            (-0.32, side * 0.94),
            "#788985",
            0.035,
        )

    # Fine lines along the wings add structure without obscuring the spots.
    for side in (-1, 1):
        draw_detail_curve(
            (-0.32, side * 0.83),
            (-0.82, side * 1.03),
            (-1.28, side * 1.48),
            (-1.73, side * 1.63),
            "#536866",
            0.03,
        )
        draw_detail_curve(
            (-0.58, side * 0.51),
            (-0.94, side * 0.73),
            (-1.2, side * 1.04),
            (-1.45, side * 1.19),
            "#26383A",
            0.025,
        )

    # Five short gill slits sit on the underside behind the head.
    for gill_x in (0.22, 0.04, -0.14, -0.32, -0.5):
        draw_detail_curve(
            (gill_x, -0.36),
            (gill_x - 0.08, -0.44),
            (gill_x - 0.08, -0.56),
            (gill_x - 0.02, -0.63),
            "#172426",
            0.035,
        )

    # The paired cephalic fins and small mouth define the manta's face.
    for side in (-1, 1):
        draw_detail_curve(
            (0.78, side * 0.12),
            (0.94, side * 0.25),
            (1.12, side * 0.18),
            (1.21, side * 0.025),
            "#788985",
            0.055,
        )
    draw_detail_curve(
        (1.12, 0),
        (1.16, -0.018),
        (1.21, -0.018),
        (1.24, 0),
        "#172426",
        0.035,
    )

    # Eye sits near the front of the body, on the visible upper side.
    t.penup()
    for side in (-1, 1):
        move_to((0.78, side * 0.34))
        t.dot(size * 0.14, "#182629")
        move_to((0.78, side * 0.34))
        t.dot(size * 0.075, "#080F10")
        move_to((0.8, side * 0.37))
        t.dot(size * 0.022, "#D2D6CC")





def draw_pufferfish(x, y, size, is_facing_left):
    """
    Draws a round pufferfish with natural coloring, markings, fins, and spines.

    Args:
        x (int): The x-coordinate of the fish.
        y (int): The y-coordinate of the fish.
        size (int): Radius of the pufferfish body.
        is_facing_left (bool): Direction the fish faces.

    Returns:
        None
    """
    direction = -1 if is_facing_left else 1

    def move_to(point):
        t.goto(x + direction * point[0] * size, y + point[1] * size)

    def draw_fin(points, fill_color):
        t.penup()
        move_to(points[0])
        t.color("#66502E")
        t.fillcolor(fill_color)
        t.begin_fill()
        t.pendown()
        for point in points[1:]:
            move_to(point)
        move_to(points[0])
        t.end_fill()
        t.penup()

    # Draw the tail and fins first so their roots sit behind the body.
    draw_fin(((-0.82, 0.08), (-1.3, 0.34), (-1.24, 0), (-1.3, -0.34), (-0.82, -0.08)), "#967A43")
    draw_fin(((-0.28, 0.78), (-0.02, 1.18), (0.18, 0.78)), "#A9853F")
    draw_fin(((-0.35, -0.78), (-0.08, -1.12), (0.18, -0.78)), "#A9853F")

    # Short, tapered spines around the body.
    t.penup()
    t.color("#66502E")
    t.pensize(max(1, size * 0.035))
    for index in range(16):
        angle = math.radians(11.25 + index * 22.5)
        inner_x = math.cos(angle) * 0.92
        inner_y = math.sin(angle) * 0.92
        outer_x = math.cos(angle) * 1.2
        outer_y = math.sin(angle) * 1.2
        move_to((inner_x, inner_y))
        t.setheading(90 + direction * (math.degrees(angle) - 90))
        t.pendown()
        t.forward(size * 0.27)
        t.penup()

    # Rounded golden-olive body.
    t.penup()
    t.setheading(0)
    t.goto(x, y - size)
    t.color("#66502E")
    t.pensize(max(1, size * 0.045))
    t.fillcolor("#B99A52")
    t.pendown()
    t.begin_fill()
    t.circle(size)
    t.end_fill()

    # Pale underside, shaped to follow the round belly.
    t.penup()
    t.color("#8A7448")
    t.fillcolor("#D8C99B")
    move_to((-0.86, 0.02))
    t.begin_fill()
    t.pendown()
    for step in range(1, 25):
        fraction = step / 24
        belly_x = -0.86 + 1.72 * fraction
        belly_y = 0.02 - 0.58 * math.sin(math.pi * fraction)
        move_to((belly_x, belly_y))
    move_to((-0.86, 0.02))
    t.end_fill()
    t.penup()

    # Irregular dark spots across the back.
    spots = (
        (-0.7, 0.42, 0.14), (-0.48, 0.68, 0.12), (-0.16, 0.51, 0.17),
        (0.13, 0.72, 0.13), (0.48, 0.51, 0.16), (0.7, 0.26, 0.12),
        (-0.68, -0.02, 0.1), (-0.33, 0.25, 0.12), (0.06, 0.28, 0.1),
        (0.39, 0.2, 0.11),
    )
    for spot_x, spot_y, spot_size in spots:
        move_to((spot_x, spot_y))
        t.dot(size * spot_size, "#756039")

    # Subtle pectoral fin and gill detail on the visible side.
    draw_fin(((-0.58, 0.08), (-0.94, 0.22), (-0.86, -0.14), (-0.56, -0.2)), "#A18A50")
    t.color("#776442")
    t.pensize(max(1, size * 0.025))
    for gill_offset in (0, 1, 2):
        start = (-0.45 - gill_offset * 0.08, 0.12)
        move_to(start)
        t.setheading(90 + direction * (-70 - 90))
        t.pendown()
        t.forward(size * 0.16)
        t.penup()

    # Small beak-like mouth and a glossy eye near the front.
    move_to((0.9, 0.02))
    t.dot(size * 0.09, "#55462F")
    move_to((0.55, 0.32))
    t.dot(size * 0.21, "#E9DFC2")
    move_to((0.57, 0.32))
    t.dot(size * 0.13, "#171716")
    move_to((0.59, 0.36))
    t.dot(size * 0.04, "white")
    

def draw_creature(creature_type, x, y, size, is_facing_left):
    """
    Dispatcher function to draw different creatures based on parameters.
    
    Args:
        creature_type (str): The type of creature to draw (e.g., "fish").
        x (int): The x-coordinate for the creature.
        y (int): The y-coordinate for the creature.
        size (int): The scale or radius of the creature.
        is_facing_left (bool): If True, draws the creature facing left. 
                               If False, draws it facing right.
        
    Returns:
        None
    """
    if creature_type == "mantaray" and is_facing_left:
        draw_mantaray(x, y, size, True)
    elif creature_type == "mantaray" and not is_facing_left:
        draw_mantaray(x, y, size, False)
    elif creature_type == "pufferfish" and is_facing_left:
        draw_pufferfish(x, y, size, True)
    elif creature_type == "pufferfish" and not is_facing_left:
        draw_pufferfish(x, y, size, False)
    else:
        draw_mantaray(x, y, size, is_facing_left)


def draw_environment(include_seaweed=True, include_bubbles=True):
    """
    Draws the background elements of the tank, including sand, bubbles, and seaweed.
    
    Args:
        include_seaweed (bool): If False, leave plants for the animation layer.
        include_bubbles (bool): If False, leave bubbles for the animation layer.
        
    Returns:
        None
    """
    draw_sandy_bottom()

    if include_bubbles:
        y = -200
        while y <= 280:
            random_x = random.randint(-230, -170)
            draw_bubble(random_x, y, 10)
            y += 60

    draw_fish_hideaway()

    if include_seaweed:
        for x, segments, color_name in SEAWEED_PLANTS:
            draw_seaweed(x, -270, segments, color_name)


SEAWEED_PLANTS = (
    (-310, 4, "darkgreen"),
    (-235, 6, "green"),
    (-155, 3, "darkgreen"),
    (-80, 5, "green"),
    (10, 7, "darkgreen"),
    (105, 4, "green"),
    (195, 6, "darkgreen"),
    (300, 3, "green"),
)

BUBBLES = (
    (-230, -200, 7, 36),
    (-190, -80, 10, 29),
    (-215, 40, 6, 43),
    (-175, 170, 9, 32),
    (-120, -140, 5, 39),
    (65, -230, 8, 31),
    (130, -20, 6, 42),
    (210, 120, 9, 30),
    (275, -100, 5, 38),
)


def main():
    """
    Main execution function to assemble the fish tank.
    
    Args:
        None
        
    Returns:
        None
    """
    draw_tank(True, True, True, True)
    draw_environment()

    for i in range(6):
        x = -250 + i * 110
        y = 90 - (i % 3) * 30
        draw_creature("mantaray", x, y, 22, i % 2 == 0)
        draw_creature("pufferfish", x + 30, -100 + (i % 2) * 25, 14, i % 2 == 1)


def animate_aquarium():
    """Animates swaying seaweed, swimming fish, and rising bubbles."""
    global t

    screen = t.getscreen()
    screen.tracer(0, 0)
    draw_tank(True, True, True, True)
    draw_environment(include_seaweed=False, include_bubbles=False)
    screen.update()

    static_turtle = t
    animation_turtle = turtle.Turtle()
    animation_turtle.speed(0)
    animation_turtle.hideturtle()
    start_time = time.monotonic()

    def animate_frame():
        global t

        animation_turtle.clear()
        t = animation_turtle
        elapsed = time.monotonic() - start_time

        for index, (x, start_y, radius, rise_speed) in enumerate(BUBBLES):
            y = -280 + ((start_y + elapsed * rise_speed + 280) % 560)
            bubble_x = x + math.sin(elapsed * 1.4 + index) * 4
            draw_bubble(bubble_x, y, radius)

        for index, (x, segments, color_name) in enumerate(SEAWEED_PLANTS):
            draw_seaweed(x, -270, segments, color_name, elapsed * 1.4 - index * 0.55)

        for index in range(6):
            base_x = -250 + index * 110
            manta_phase = elapsed + index * 0.9
            manta_x = base_x + math.sin(manta_phase) * 18
            manta_y = 90 - (index % 3) * 30 + math.sin(manta_phase * 1.7) * 5
            manta_facing_left = math.cos(manta_phase) < 0
            draw_creature("mantaray", manta_x, manta_y, 22, manta_facing_left)

            puffer_phase = elapsed * 0.75 + index * 1.1
            puffer_x = base_x + 30 + math.sin(puffer_phase) * 14
            puffer_y = -100 + (index % 2) * 25 + math.sin(puffer_phase * 1.5) * 4
            puffer_facing_left = math.cos(puffer_phase) < 0
            draw_creature("pufferfish", puffer_x, puffer_y, 14, puffer_facing_left)

        t = static_turtle
        screen.update()
        screen.ontimer(animate_frame, 30)

    animate_frame()


if __name__ == "__main__":
    if USE_SVG:
        main()
        t.save_as('my_fishtank.svg')
        print("Successfully saved my_fishtank.svg")
    else:
        animate_aquarium()
        turtle.done()