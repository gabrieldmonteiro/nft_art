from PIL import Image, ImageDraw, ImageChops
import os
import random
import colorsys


def random_point(image_size_px: int, padding: int):
    return random.randint(padding, image_size_px - padding)


def random_color():  # HSV
    h = random.random()
    s = 1
    v = 1
    float_rbg = colorsys.hsv_to_rgb(h, s, v)

    # Return RGB
    return (
        int(float_rbg[0] * 255),
        int(float_rbg[1] * 255),
        int(float_rbg[2] * 255),
    )


def interpolate(start_color, end_color, k: float):
    new_color_rgb = []
    for i in range(3):
        new_color_value = k * end_color[i] + (1 - k) * start_color[i]
        new_color_rgb.append(int(new_color_value))
    return tuple(new_color_rgb)


def generate_art(collection: str, name: str):
    output_dir = os.path.join("output", collection)
    image_path = os.path.join(output_dir, f"{name}.png")

    # Size
    rescale = 2
    image_size_px = 128 * rescale
    padding = 12 * rescale

    # Dir + BG
    os.makedirs(output_dir, exist_ok=True)

    bg_color = (30, 30, 30)
    image = Image.new("RGB", (image_size_px, image_size_px), bg_color)

    # Num of lines
    num_lines = 10
    points = []

    # Colors.
    start_color = random_color()
    end_color = random_color()

    # Points
    for _ in range(num_lines):
        point = (
            random_point(image_size_px, padding),
            random_point(image_size_px, padding),
        )
        points.append(point)

    # Center image

    min_x = min([p[0] for p in points])
    max_x = max([p[0] for p in points])
    min_y = min([p[1] for p in points])
    max_y = max([p[1] for p in points])

    x_offset = (min_x - padding) - (image_size_px - padding - max_x)
    y_offset = (min_y - padding) - (image_size_px - padding - max_y)

    for i, point in enumerate(points):
        points[i] = (point[0] - x_offset // 2, point[1] - y_offset // 2)

    # Draw
    current_thickness = 1 * rescale
    n_points = len(points) - 1
    for i, point in enumerate(points):

        overlay_image = Image.new("RGB", (image_size_px, image_size_px), (0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay_image)

        if i == n_points:
            next_point = points[0]
        else:
            next_point = points[i + 1]

        # Color
        factor = i / n_points
        line_color = interpolate(start_color, end_color, k=factor)

        # Draw the line.
        overlay_draw.line([point, next_point], fill=line_color, width=current_thickness)
        current_thickness += rescale
        image = ImageChops.add(image, overlay_image)

    image = image.resize(
        (image_size_px // rescale, image_size_px // rescale), resample=Image.ANTIALIAS
    )

    # Saving
    image.save(image_path)
