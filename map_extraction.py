import os
from PIL import Image

def generate_settlement_map():
    input_filename = "map_regions.tga"
    txt_filename = "settlement_coordinates.txt"
    html_filename = "settlement_map.html"
    if not os.path.exists(input_filename):
        print(f"Error: {input_filename} not found.")
        return
    with Image.open(input_filename) as img:
        img = img.convert("RGB")
        width, height = img.size
        pixels = img.load()
        settlements = []
        for y in range(height):
            for x in range(width):
                r, g, b = pixels[x, y]
                if r == 0 and g == 0 and b == 0:
                    game_y = height - 1 - y
                    settlements.append((x, game_y))
    with open(txt_filename, "w") as f:
        for x, y in settlements:
            f.write(f"{x}, {y}\n")
    if not settlements:
        print("No settlements found in the image.")
        return
    scale = 4
    disp_width = width * scale
    disp_height = height * scale
    html_lines = [
        "<!DOCTYPE html>",
        "<html>",
        "<head>",
        '<meta charset="utf-8">',
        "<title>Settlement Map</title>",
        "<style>",
        "body { background-color: #ffffff; color: #000000; font-family: sans-serif; margin: 0; padding: 40px; }",
        f".container {{ max-width: {disp_width}px; margin: 0 auto; }}",
        f".map-canvas {{ position: relative; width: {disp_width}px; height: {disp_height}px; background-color: #ffffff; border: 1px solid #000000; }}",
        ".settlement { position: absolute; width: 6px; height: 6px; background-color: #000000; border-radius: 50%; transform: translate(-3px, 3px); cursor: pointer; }",
        ".settlement:hover { background-color: #ff0000; box-shadow: 0 0 8px #ff0000; z-index: 10; }",
        ".tooltip { visibility: hidden; background-color: #000000; color: #ffffff; padding: 4px 8px; border-radius: 4px; position: absolute; bottom: 12px; left: 50%; transform: translateX(-50%); white-space: nowrap; font-size: 11px; }",
        ".settlement:hover .tooltip { visibility: visible; }",
        "</style>",
        "</head>",
        "<body>",
        '<div class="container">',
        '<div class="map-canvas">'
    ]
    for idx, (x, y) in enumerate(settlements):
        left_pos = x * scale
        bottom_pos = y * scale
        html_lines.append(f'        <div class="settlement" style="left: {left_pos}px; bottom: {bottom_pos}px;">')
        html_lines.append(f'            <span class="tooltip">Settlement #{idx+1}<br>X: {x}, Y: {y}</span>')
        html_lines.append('        </div>')
    html_lines.extend([
        "    </div>",
        "</div>",
        "</body>",
        "</html>"
    ])
    with open(html_filename, "w") as f:
        f.write("\n".join(html_lines))
    print("Files successfully generated.")

if __name__ == "__main__":
    generate_settlement_map()
