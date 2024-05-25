import os
import subprocess
from libqtile import bar, layout, qtile, widget
from libqtile import hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
import keybindings

mod = "mod4"
keys = keybindings.keys()

groups = [Group(f"{i+1}", label=" ") for i in range(5)]

for i in groups:
    keys.extend([
        Key(
            [mod],
            i.name,
            lazy.group[i.name].toscreen(),
            desc="Switch to group {}".format(i.name),
        ),
        Key(
            [mod, "shift"],
            i.name,
            lazy.window.togroup(i.name, switch_group=True),
            desc="Switch to & move focused window to group {}".format(i.name),
        ),
    ])

layouts = [
    layout.MonadTall(border_width=3, margin=4, border_focus="#b4befe"),
    layout.Bsp(),
    layout.Tile(),
    layout.TreeTab(),
]

borderwidth = 3

widget_defaults = dict(
    font="sans",
    fontsize=12,
    padding=3,
)

extension_defaults = widget_defaults.copy()

font_family = "CommitMono"
font_size = 14
fmt = "<b>{}</b>"

screens = [
    Screen(
        top=bar.Bar(
            [
                # OS icon
                widget.TextBox(" ", fontsize=16, foreground="#74c7ec"),
                widget.Sep(padding=10, linewidth=2, foreground="#45475a"),

                # Workspaces
                widget.GroupBox(
                    fontsize=14,
                    highlight_method="block",
                    active="#cdd6f4",
                    block_highlight_text_color="#a6e3a1",
                    highlight_color="#4B427E",
                    this_current_screen_border="#1e1e2e",
                    urgent_border="#f38ba8",
                    rounded=False,
                    disable_drag=True,
                ),
                widget.Sep(padding=10, linewidth=2, foreground="#45475a"),

                # CPU
                widget.TextBox(" ", fontsize=16, foreground="#cba6f7"),
                widget.CPU(
                    font=font_family,
                    fontsize=font_size,
                    fmt=fmt,
                    foreground="#cba6f7",
                    format="CPU {load_percent}%",
                ),

                # Memory
                widget.TextBox(" ", fontsize=16, foreground="#b4befe"),
                widget.Memory(
                    font=font_family,
                    fontsize=font_size,
                    fmt=fmt,
                    foreground="#b4befe",
                    format="{MemUsed: .0f}{mm} /{MemTotal: .0f}{mm}",
                ),
                widget.Spacer(),
                widget.Mpris2(
                    font=font_family,
                    fontsize=font_size,
                    format="{xesam:artist} - {xesam:title}",
                    no_metadata_text="Player paused",
                    paused_text="󰏤 <b><i>paused:</i> {track}</b>",
                    playing_text=" <b>{track}</b>",
                    scroll=False,
                ),
                widget.Spacer(),

                # Current Layout Name
                widget.TextBox("󱂬 ", fontsize=18, foreground="#f2cdcd"),
                widget.CurrentLayout(font=font_family,
                                     fontsize=font_size,
                                     fmt=fmt,
                                     foreground="#f2cdcd"),
                widget.Sep(padding=10, linewidth=2, foreground="#45475a"),

                # Network
                widget.Net(
                    format="{down:.0f}{down_suffix} ↓↑ {up:.0f}{up_suffix}",
                    font=font_family,
                    fontsize=font_size,
                    fmt=fmt,
                    foreground="#74c7ec",
                ),
                widget.Sep(padding=10, linewidth=2, foreground="#45475a"),

                # Volume
                widget.TextBox(
                    " ",
                    fontsize=14,
                    foreground="#a6e3a1",
                ),
                widget.Volume(font=font_family,
                              fontsize=font_size,
                              fmt=fmt,
                              foreground="#a6e3a1"),
                widget.Sep(padding=10, linewidth=2, foreground="#45475a"),

                # Time & Date
                widget.Clock(
                    font=font_family,
                    fontsize=font_size,
                    fmt=fmt,
                    format="󰥔 %H:%M  󰃭 %A %d",
                    foreground="#fab387",
                ),
                widget.Sep(padding=10, linewidth=2, foreground="#45475a"),
                widget.TextBox(" ", fontsize=16, foreground="#f38ba8"),
            ],
            24,
            border_width=6,
            border_color="#1e1e2e",
            background="#1e1e2e",
        ), ),
]

# Drag floating layouts.
mouse = [
    Drag(
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag([mod],
         "Button3",
         lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class="confirmreset"),  # gitk
    Match(wm_class="makebranch"),  # gitk
    Match(wm_class="maketag"),  # gitk
    Match(wm_class="ssh-askpass"),  # ssh-askpass
    Match(title="branchdialog"),  # gitk
    Match(title="pinentry"),  # GPG key password entry
])
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None


@hook.subscribe.startup_once
def autostart():
    from datetime import datetime

    home = os.path.expanduser("~/.config/qtile/scripts/startup.sh")
    try:
        subprocess.Popen([home])
    except Exception as error:
        with open("qtile_log", "a+") as f:
            f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " +
                    str(error))


# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "Qtile"
