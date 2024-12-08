def color(text, spec: dict[str, int]):
    # List of ANSI color codes
    colors = [
        "\033[90m",  # Black
        "\033[97m",  # White
        "\033[31m",  # Red
        "\033[32m",  # Green
        "\033[33m",  # Yellow
        "\033[34m",  # Blue
        "\033[35m",  # Magenta
        "\033[36m",  # Cyan
        "\033[91m",  # Bright Red
        "\033[92m",  # Bright Green
        "\033[93m",  # Bright Yellow
        "\033[94m",  # Bright Blue
        "\033[95m",  # Bright Magenta
        "\033[96m",  # Bright Cyan
    ]

    # Dictionary to store character-color mappings
    char_colors = {}
    for k, v in spec.items():
        char_colors[k] = colors[v]

    for k, v in spec.items():
        colors = colors[:v] + colors[v + 1 :]

    # Reset code
    reset = "\033[0m"

    # Assign colors to unique characters
    color_index = 0
    result = ""

    for char in text:
        if char not in char_colors:
            char_colors[char] = colors[color_index % len(colors)]
            color_index += 1

        result += char_colors[char] + char + reset

    return result
