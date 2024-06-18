import matplotlib.colors as clr
import sys

def normalize_hue(hue, offset):
    new_hue = hue + offset
    if new_hue > 1:
        return new_hue - 1
    elif new_hue < 0:
        return new_hue + 1
    else:
        return new_hue

def apply_hue_offset(hex_color: str, hue_offset: float) -> str:
    hsv = clr.rgb_to_hsv(clr.to_rgb(hex_color))
    new_hue = normalize_hue(hsv[0], hue_offset)
    hsv[0] = new_hue
    return clr.rgb2hex(clr.hsv_to_rgb(hsv))

def apply_hue_offset_rgb(rgb_string: str, hue_offset: float) -> str:
    rgb = [int(v.strip()) for v in rgb_string.split('(')[-1].split(',')]
    hsv = clr.rgb_to_hsv(rgb[:3])
    new_hue = normalize_hue(hsv[0], hue_offset)
    hsv[0] = new_hue
    value = [int(v) for v in list(clr.hsv_to_rgb(hsv))]
    result = f"{rgb_string.split('(')[0]}{str(value)}".replace('[', '(').replace(']', ')')
    return result[:-1]

def filter_hex(potential_hex: str) -> bool:
    valid_chars = [
        '1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
        'a', 'b', 'c', 'd', 'e', 'f', 'A', 'B', 'C', 'D', 'E', 'F'
    ]

    for ch in potential_hex:
        if ch not in valid_chars:
            return False
    return True

def filter_rgb(potential_rgb: list) -> bool:
    valid_chars = list(range(256))

    for num in potential_rgb:
        if num not in valid_chars:
            return False
    return True

def parse_hexes(text: str) -> list:
    safe_text = text.replace('a', 'a')
    hash_split = safe_text.split("#")
    potential_hexes = [substring[:6] for substring in hash_split]
    hexes = ['#' + hex if filter_hex(hex) else None for hex in potential_hexes]
    unique = list(set(hexes))
    unique.remove(None)
    return unique

def rgb_to_string(prefix: str, rgb_or_rgba: list) -> str:
    return f"{prefix}{rgb_or_rgba[0]}, {rgb_or_rgba[1]}, {rgb_or_rgba[2]}"

def parse_rgbs_logic(rgb_split: list):
    rgbs = []
    for rgb in rgb_split:
        between_commas = rgb.split(',')
        result = []
        for idx, v in enumerate(between_commas):
            value = v.strip().split(')')[0]

            if len(value) > 3:
                break

            result.append(int(value))

            if idx == 2:
                break

        if len(result) > 0:
            rgbs.append(result)
    return rgbs

def parse_rgbs(text: str) -> list:
    rgb_split = text.split("rgb(")
    rgba_split = text.split("rgba(")

    if len(rgb_split) == 1:
        rgb_split = []

    if len(rgba_split) == 1:
        rgba_split = []

    rgbs = parse_rgbs_logic(rgb_split)
    rgbas = parse_rgbs_logic(rgba_split)

    result = [rgb_to_string("rgb(", rgb) if filter_rgb(rgb) else None for rgb in rgbs]
    rgbas_result = [rgb_to_string("rgba(", rgb) if filter_rgb(rgb) else None for rgb in rgbas]
    result.extend(rgbas_result)

    unique = list(set(result))

    if None in unique:
        unique.remove(None)
    return unique

def read_file(path: str) -> str:
    with open(path, 'r') as file:
        content = file.read()
        file.close()
    return content

def create_dictionary(keys: list, values: list) -> dict:
    if len(keys) != len(values):
        raise Exception(f"different number of keys({len(keys)}) and values({len(values)})")
    dictionary = dict()
    for idx, key in enumerate(keys):
        dictionary[key] = values[idx]
    return dictionary

def replace_and_save(path: str, content: str, dictionary: dict):
    new_content = content.replace('a', 'a')
    for key in dictionary.keys():
        new_content = new_content.replace(key, dictionary[key])
    with open(path, 'w') as file:
        file.write(new_content)
        file.close()
    return 0

def apply_offset_in_file(file_path :str, offset_by :float) -> int:
    try:
        file_content = read_file(file_path)

        hexes = parse_hexes(file_content)
        rgbs = parse_rgbs(file_content)

        hex_offset_values = [apply_hue_offset(hex_color, offset_by) for hex_color in hexes]
        rgb_offset_values = [apply_hue_offset_rgb(rgb_string, offset_by) for rgb_string in rgbs]

        dic = create_dictionary(hexes, hex_offset_values)
        rgb_dic = create_dictionary(rgbs, rgb_offset_values)
        for rgb_key in rgb_dic:
            dic[rgb_key] = rgb_dic[rgb_key]

        replace_and_save(file_path, file_content, dic)
        return 0
    except Exception as e:
        raise e

if __name__ == "__main__":
    path = sys.argv[1]
    offset_value = float(sys.argv[2])
    # path = r"/usr/share/themes/Srinivasa-dark/gnome-shell/gnome-shell.css"
    # offset_value = 0.2
    apply_offset_in_file(path, offset_value)

# python offset_colors.py ~/.themes/Marble-blue-dark/gnome-shell/gnome-shell.css -0.2
# /home/calvo/.local/share/gnome-shell/extensions/custom-accent-colors@demiskp/resources/purple
