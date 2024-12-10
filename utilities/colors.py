def get_colors():
    # List of ANSI color codes
    return [
        "\033[38;2;0;0;0m",  # Black
        "\033[38;2;100;100;100m",  # Dark gray
        "\033[38;2;130;60;60m",  # Muted red
        "\033[38;2;130;95;60m",  # Muted orange
        "\033[38;2;130;130;60m",  # Muted yellow
        "\033[38;2;95;130;60m",  # Muted light green
        "\033[38;2;60;130;60m",  # Muted green
        "\033[38;2;60;130;95m",  # Muted spring green
        "\033[38;2;60;130;130m",  # Muted cyan
        "\033[38;2;60;95;130m",  # Muted light blue
        "\033[38;2;60;60;130m",  # Muted blue
        "\033[38;2;95;60;130m",  # Muted purple
        "\033[38;2;130;60;130m",  # Muted magenta
        "\033[38;2;255;255;255m",  # White
    ]


def color(text, spec: dict[str, int]):
    colors = get_colors()

    # Dictionary to store character-color mappings
    char_colors = {}
    for k, v in spec.items():
        char_colors[k] = colors[v]

    for k, v in spec.items():
        colors = colors[:v] + colors[v + 1 :]

    # Reset code
    reset = "\033[0m"

    # Assign colors to unique characters
    result = ""

    for char in text:
        result += char_colors.get(char, colors[0]) + char + reset

    return result


# def colors_with_default(text, spec: dict[str, int]):
#     colors = get_colors()

#     # Dictionary to store character-color mappings
#     char_colors = {}
#     for k, v in spec.items():
#         char_colors[k] = colors[v]

#     for k, v in spec.items():
#         colors = colors[:v] + colors[v + 1 :]

#     # Reset code
#     reset = "\033[0m"

#     # Assign colors to unique characters
#     color_index = 0
#     result = ""

#     for char in text:
#         if char not in char_colors:
#             char_colors[char] = colors[color_index % len(colors)]
#             color_index += 1

#         result += char_colors[char] + char + reset

#     return result
