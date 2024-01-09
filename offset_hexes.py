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

def filter_hex(potential_hex: str) -> bool:
    valid_chars = [
        '1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
        'a', 'b', 'c', 'd', 'e', 'f', 'A', 'B', 'C', 'D', 'E', 'F'
    ]

    for ch in potential_hex:
        if ch not in valid_chars:
            return False
    return True

def parse_hexes(text: str) -> list:
    hash_split = text.split("#")
    potential_hexes = [substring[:6] for substring in hash_split]
    hexes = ['#' + hex if filter_hex(hex) else None for hex in potential_hexes]
    unique = list(set(hexes))
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

def apply_offset_to_hexes_in_file(file_path :str, offset_by :float) -> int:
    try:
        file_content = read_file(file_path)
        hexes = parse_hexes(file_content)
        offset_value = [apply_hue_offset(hex_color, offset_by) for hex_color in hexes]
        dictionary = create_dictionary(hexes, offset_value)
        return replace_and_save(file_path, file_content, dictionary)
    except Exception as e:
        raise e

if __name__ == "__main__":
    path = sys.argv[1]
    offset_value = float(sys.argv[2])
    apply_offset_to_hexes_in_file(path, offset_value)

# offset_by = -0.3
# path = r"/usr/share/themes/Midnight-Green/gnome-shell/gnome-shell.css"

# python3 Code/Rice/offset_hexes.py /usr/share/themes/Midnight-Green/gnome-shell/gnome-shell.css -0.3

