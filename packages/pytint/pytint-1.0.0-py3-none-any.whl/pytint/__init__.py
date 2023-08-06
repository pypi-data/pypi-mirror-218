PRIMARY: list[str] = ["#00ff00", "#00FF00"]
SECONDARY: list[str] = ["#0000ff", "#0000FF"]
BACKGROUND: list[str] = ["#ff0000", "#FF0000"]
DETAIL: list[str] = ["#ffffff", "#FFFFFF"]
INVERSE_BG: list[str] = ["#000000"]

DEFAULTS: dict[str, str] = {
    "default": "#438de6",
    "accent": "#a4caee",
    "variant": "#f2f2f2",
    "alt": "#e5e5e5",
    "difference": "#1a1a1a",
}
SCHEMES: dict[str, dict[str, str]] = {
    "dark": {
        "variant": "#f2f2f2",
        "alt": "#e5e5e5",
        "difference": "#1a1a1a",
    },
    "light": {
        "variant": "#1a1a1a",
        "alt": "#262626",
        "difference": "#f2f2f2",
    },
}
INVERSE_SCHEMES: dict[str, dict[str, str]] = {
    "dark": {
        "variant": "#1a1a1a",
        "alt": "#262626",
        "difference": "#f2f2f2",
    },
    "light": {
        "variant": "#f2f2f2",
        "alt": "#e5e5e5",
        "difference": "#1a1a1a",
    },
}
COLORS: dict[str, dict[str, str]] = {
    "red": {"default": "#da4e4e", "accent": "#eea5aa"},
    "green": {"default": "#34b234", "accent": "#aaeea5"},
    "blue": {"default": "#438de6", "accent": "#a4caee"},
    "teal": {"default": "#139595", "accent": "#38dbd1"},
    "purple": {"default": "#7f54d4", "accent": "#bfb3e5"},
    "pink": {"default": "#ed5e8d", "accent": "#f4bed4"},
    "yellow": {"default": "#b2a400", "accent": "#f1e774"},
    "orange": {"default": "#c35622", "accent": "#f09e75"},
    "brown": {"default": "#6c4532", "accent": "#b78b7b"},
    "slate": {"default": "#6f8090", "accent": "#c7cbcc"},
}
