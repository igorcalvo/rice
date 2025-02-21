home_path = "/home/calvo"
source_path = f"{home_path}/code/linux/dotfiles/colors.sh"

bspwm = {
    "active_border_color ": "primary",
    "normal_border_color ": "primary",
    "focused_border_color ": "secondary"
}

polybar = {
    "primary = ": "primary",
    "secondary = ": "secondary",
    "background = ": "background",
}

dunst = {
    "background = ": "background",
    "frame_color = ": "lighter",
    346: "primary",
    354: "darker",
}

cava = {
    "gradient_color_1 = ": "primary",
    "gradient_color_2 = ": "secondary"
}

paths_to_replace = {
    f"{home_path}/code/linux/dotfiles/.config/bspwm/bspwmrc": bspwm,
    f"{home_path}/code/linux/dotfiles/.config/polybar/config.ini": polybar,
    f"{home_path}/code/linux/dotfiles/.config/dunst/dunstrc": dunst,
    f"{home_path}/code/linux/dotfiles/.config/cava/config": cava
}

def strip_color_value(color_value: str) -> str:
    return color_value.replace("'", "").rstrip()

def read_colors(source_path: str) -> dict[str, dict[str | int, str]]:
    colors = {}
    lines = read_file(source_path)
    for line in lines:
        color_name, color_value = line.split('=')
        colors[color_name.replace('$', '')] = strip_color_value(color_value)
    return colors

def read_file(file_path: str) -> list[str]:
    result = ''
    with open(file_path, 'r') as file:
        result = file.readlines()
        file.close()
    return result

def replace_color(line: str, dict_color: str) -> str:
    old_color = line.split('#')[-1][:6]
    new_color = dict_color.replace('#', '')
    line = line.replace(old_color, new_color)
    return line

if __name__ == "__main__":
    colors = read_colors(source_path)
    for file_path in paths_to_replace.keys():
        replace_dict = paths_to_replace[file_path]
        lines = read_file(file_path)
        with open(file_path, 'w') as f:
            content = ''
            counter = 0
            for line_number, line in enumerate(lines):
                for key in replace_dict.keys():
                    if type(key) == type(1):
                        if key == line_number + 1:
                            dict_color = str(colors[replace_dict[key]])
                            line = replace_color(line, dict_color)
                            counter += 1
                            continue
                    else:
                        if str(key) in line and '.' not in line:
                            dict_color = str(colors[replace_dict[key]])
                            line = replace_color(line, dict_color)
                            counter += 1
                content += line
            f.write(content)
            f.close()
        print(f"{file_path.split('/')[-1]} updated {counter} lines")

