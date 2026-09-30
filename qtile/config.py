import subprocess
import os

from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.backend.wayland import InputConfig
from libqtile import hook



# ─────────────────────────────────────────────────────────────
# General
# ─────────────────────────────────────────────────────────────

mod = "mod4"
alt = "mod1"
terminal = "kitty"

groups = [Group(str(i)) for i in range(1, 10)] + [Group("0")]


# ─────────────────────────────────────────────────────────────
# Colors
# ─────────────────────────────────────────────────────────────

COLORS = {
    "bg": "#0b0b0f",
    "bg_alt": "#151419",
    "fg": "#d8d0d3",
    "muted": "#777176",
    "accent": "#c69aa5",
    "accent2": "#8f6874",
    "urgent": "#d06f7c",
    "black": "#000000",
    "white": "#ffffff",
}


# ─────────────────────────────────────────────────────────────
# PipeWire volume
# ─────────────────────────────────────────────────────────────

def get_volume():
    try:
        output = subprocess.check_output(
            ["wpctl", "get-volume", "@DEFAULT_AUDIO_SINK@"],
            text=True,
        ).strip()

        parts = output.split()
        volume = int(float(parts[1]) * 100)

        if "MUTED" in output:
            return "VOL MUTE"

        return f"VOL {volume}%"

    except Exception:
        return "VOL --"


# ─────────────────────────────────────────────────────────────
# Keybindings
# ─────────────────────────────────────────────────────────────

keys = [
    # Focus
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "k", lazy.layout.up()),
    Key([mod], "l", lazy.layout.right()),

    Key([mod], "Left", lazy.layout.left()),
    Key([mod], "Down", lazy.layout.down()),
    Key([mod], "Up", lazy.layout.up()),
    Key([mod], "Right", lazy.layout.right()),

    # Move windows
    Key([mod, "shift"], "h", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right()),

    Key([mod, "shift"], "Left", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "Right", lazy.layout.shuffle_right()),

    # Resize
    Key([mod, alt], "h", lazy.layout.grow_left()),
    Key([mod, alt], "j", lazy.layout.grow_down()),
    Key([mod, alt], "k", lazy.layout.grow_up()),
    Key([mod, alt], "l", lazy.layout.grow_right()),

    # Split
    Key([mod, alt], "space", lazy.layout.toggle_split()),

    # Applications
    Key([mod], "Return", lazy.spawn("kitty")),
    Key([mod], "w", lazy.spawn("firefox")),
    Key([mod], "e", lazy.spawn("dolphin")),
    Key(
        [mod, "shift"],
        "w",
        lazy.spawn("~/r/appimg/waterfox/waterfox"),
    ),

    # Rofi
    Key([mod], "d", lazy.spawn("rofi -show drun")),

    # Spawn command prompt
    Key([mod], "r", lazy.spawncmd()),

    # Window controls
    Key([mod], "q", lazy.window.kill()),
    Key([mod], "f", lazy.window.toggle_fullscreen()),
    Key([mod, "shift"], "space", lazy.window.toggle_floating()),

    # Layout
    Key([mod], "Tab", lazy.next_layout()),

    # Qtile
    Key([mod, "shift"], "c", lazy.reload_config()),
    Key([mod, "shift"], "r", lazy.reload_config()),
    Key([mod, "shift"], "e", lazy.shutdown()),

    # Volume
    Key(
        [],
        "XF86AudioMute",
        lazy.spawn(
            "wpctl set-mute @DEFAULT_AUDIO_SINK@ toggle"
        ),
    ),
    Key(
        [],
        "XF86AudioRaiseVolume",
        lazy.spawn(
            "wpctl set-volume -l 1 @DEFAULT_AUDIO_SINK@ 5%+"
        ),
    ),
    Key(
        [],
        "XF86AudioLowerVolume",
        lazy.spawn(
            "wpctl set-volume -l 1 @DEFAULT_AUDIO_SINK@ 5%-"
        ),
    ),

    # Media
    Key(
        [mod, "shift"],
        "p",
        lazy.spawn("playerctl play-pause"),
    ),
    Key(
        [mod, "shift"],
        "b",
        lazy.spawn("playerctl previous"),
    ),
    Key(
        [mod, "shift"],
        "n",
        lazy.spawn("playerctl next"),
    ),

    # Screenshots
    Key(
        [mod],
        "Print",
        lazy.spawn('grim -g "$(slurp)" - | wl-copy'),
    ),
    Key(
        [],
        "Print",
        lazy.spawn(
            'grim -g "$(slurp)" ~/Pictures/screenshot-$(date +%s).png'
        ),
    ),
    Key(
        ["shift"],
        "Print",
        lazy.spawn(
            'grim ~/Pictures/screenshot-$(date +%s).png'
        ),
    ),
]


# Workspace bindings
for group in groups:
    keys.extend([
        Key(
            [mod],
            group.name,
            lazy.group[group.name].toscreen(),
        ),
        Key(
            [mod, "shift"],
            group.name,
            lazy.window.togroup(
                group.name,
                switch_group=True,
            ),
        ),
    ])


@hook.subscribe.startup_once
def autostart():
    subprocess.Popen(["awww-daemon"])

    subprocess.Popen([
        "awww",
        "img",
        os.path.expanduser("~/.wallpapers/serene.png"),
    ])

# ─────────────────────────────────────────────────────────────
# Layouts
# ─────────────────────────────────────────────────────────────

layouts = [
    layout.Columns(
        border_width=0,
        border_focus=COLORS["white"],
        border_normal=COLORS["white"],
        margin=3,
    ),
    layout.Max(
        border_width=0,
        border_focus=COLORS["white"],
        border_normal=COLORS["white"],
        margin=3,
    ),
]


# ─────────────────────────────────────────────────────────────
# Floating windows
# ─────────────────────────────────────────────────────────────

floating_layout = layout.Floating(
    border_width=0,
    float_rules=[
        *layout.Floating.default_float_rules,

        Match(wm_class="confirmreset"),
        Match(wm_class="makebranch"),
        Match(wm_class="maketag"),
        Match(wm_class="ssh-askpass"),

        Match(title="branchdialog"),
        Match(title="pinentry"),
    ],
)


# ─────────────────────────────────────────────────────────────
# Mouse
# ─────────────────────────────────────────────────────────────

mouse = [
    Drag(
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [mod],
        "Button3",
        lazy.window.set_size_floating(),
        start=lazy.window.get_size(),
    ),
    Click(
        [mod],
        "Button2",
        lazy.window.bring_to_front(),
    ),
]


# ─────────────────────────────────────────────────────────────
# Widgets
# ─────────────────────────────────────────────────────────────

widget_defaults = dict(
    font="monospace",
    fontsize=10,
    padding=4,
)

extension_defaults = widget_defaults.copy()


# ─────────────────────────────────────────────────────────────
# Screen / Bar
# ─────────────────────────────────────────────────────────────

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(
                    active=COLORS["fg"],
                    inactive=COLORS["muted"],
                    this_current_screen_border=COLORS["accent"],
                    this_screen_border=COLORS["accent"],
                    other_current_screen_border=COLORS["accent2"],
                    other_screen_border=COLORS["accent2"],
                    urgent_alert_method="border",
                    urgent_border=COLORS["urgent"],
                    highlight_method="block",
                    block_highlight_text_color=COLORS["fg"],
                    padding=4,
                    margin_y=3,
                    margin_x=3,
                    borderwidth=2,
                    fontsize=10,
                ),

                widget.CurrentLayout(
                    foreground=COLORS["fg"],
                    padding=8,
                ),

                widget.Prompt(
                    prompt="Run: ",
                    foreground=COLORS["accent"],
                    cursor_color=COLORS["accent"],
                    padding=8,
                ),

                widget.Spacer(),

                widget.WindowName(
                    foreground=COLORS["fg"],
                    max_chars=60,
                    padding=8,
                ),

                widget.Spacer(),

                widget.CPU(
                    format="CPU {load_percent}%",
                    foreground=COLORS["fg"],
                    update_interval=2,
                    padding=8,
                ),

                widget.Memory(
                    format="RAM {MemPercent}%",
                    foreground=COLORS["fg"],
                    update_interval=2,
                    padding=8,
                ),

                widget.GenPollText(
                    func=lambda: subprocess.check_output(
                        [
                            "bash",
                            "-c",
                            "nmcli -t -f active,ssid dev wifi "
                            "| grep '^yes:' "
                            "| cut -d: -f2- "
                            "| head -1 "
                            "| sed 's/^/WiFi /'",
                        ],
                        text=True,
                    ).strip() or "WiFi --",
                    update_interval=5,
                    foreground=COLORS["fg"],
                    padding=8,
                ),

                widget.Net(
                    format="NET ↓{down} ↑{up}",
                    foreground=COLORS["fg"],
                    update_interval=2,
                    padding=8,
                ),

                widget.GenPollText(
                    func=get_volume,
                    update_interval=1,
                    foreground=COLORS["fg"],
                    padding=8,
                ),

                widget.Battery(
                    format="BAT {percent:2.0%}",
                    foreground=COLORS["fg"],
                    update_interval=30,
                    padding=8,
                ),

                widget.Systray(
                    icon_size=18,
                    padding=6,
                ),

                widget.TextBox(
                    text="│",
                    foreground=COLORS["muted"],
                    padding=4,
                ),

                widget.Clock(
                    format="%a %d %b  %H:%M",
                    foreground=COLORS["fg"],
                    padding=8,
                ),
            ],
            30,
            background="#0b0b0fcc",
            margin=[5, 8, 0, 8],
        ),
    ),
]


# ─────────────────────────────────────────────────────────────
# Qtile settings
# ─────────────────────────────────────────────────────────────

dgroups_key_binder = None
dgroups_app_rules = []

follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False

auto_fullscreen = True
focus_on_window_activation = "smart"
focus_previous_on_window_remove = False

reconfigure_screens = True

wmname = "LG3D"

wl_xcursor_theme = None
wl_xcursor_size = 24

wl_input_rules = {
    "type:touchpad": InputConfig(
        tap=True,
        tap_button_map="lrm",
    ),
}
