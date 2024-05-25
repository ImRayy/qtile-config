from libqtile.config import EzKey as map
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal


class Command:
    clipboard = "rofi -modi 'clipboard:greenclip print' -show clipboard -run-command '{cmd}' -theme ~/.config/rofi/themes/default.rasi"
    powermenu = ["bash", "-c", "~/.config/rofi/powermenu.sh"]
    appmenu = "rofi -show drun -show-icons -theme ~/.config/rofi/themes/default.rasi"
    volume_up = ["bash", "-c", "~/.config/qtile/scripts/volume.sh volume_up"]
    volume_down = [
        "bash", "-c", "~/.config/qtile/scripts/volume.sh volume_down"
    ]


def keys():
    terminal = guess_terminal()
    return [
        # Window actions
        map("M-<space>", lazy.window.toggle_floating(),
            desc="Toggle floating"),
        map("M-f", lazy.window.toggle_fullscreen(), desc="Toggle fullscreen"),
        map("M-q", lazy.window.kill(), desc="Kill focused window"),
        map("M-S-q", lazy.shutdown(), desc="Shutdown Qtile"),
        map("M-t", lazy.toggle_split()),
        map("M-<tab>", lazy.next_layout(), desc="Toggle between layouts"),

        # General Actions
        map("M-r",
            lazy.spawncmd(),
            desc="Spawn a command using a prompt widget"),
        map("M-S-r", lazy.reload_config(), desc="Reload the config"),

        # Focus window
        map("M-h", lazy.layout.left()),
        map("M-l", lazy.layout.right()),
        map("M-j", lazy.layout.down()),
        map("M-k", lazy.layout.up()),

        # Move Window
        map("M-S-h", lazy.layout.shuffle_left()),
        map("M-S-l", lazy.layout.shuffle_right()),
        map("M-S-j", lazy.layout.shuffle_down()),
        map("M-S-k", lazy.layout.shuffle_up()),

        # Grow windows. If current window is on the edge of screen and direction
        # will be to screen edge - window would shrink.
        map("M-C-h", lazy.layout.grow_left()),
        map("M-C-l", lazy.layout.grow_right()),
        map("M-C-j", lazy.layout.grow_down()),
        map("M-C-k", lazy.layout.grow_up()),
        map("M-C-n", lazy.layout.normalize(), desc="Reset all window sizes"),

        # Launch Apps
        map("M-<Return>", lazy.spawn(terminal)),

        # Volume Control
        map("<XF86AudioRaiseVolume>", lazy.spawn(Command.volume_up)),
        map("<XF86AudioLowerVolume>", lazy.spawn(Command.volume_down)),

        # Rofi
        map("M-a", lazy.spawn(Command.appmenu), desc="App launcher"),
        map("M-x", lazy.spawn(Command.powermenu), desc="Powermenu"),
        map("M-v", lazy.spawn(Command.clipboard), desc="Clipboard manager"),
    ]
