# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile import hook
import os
import subprocess
from qtile_extras import widget
from libqtile.utils import guess_terminal
run = "dmenu_run -g 4 -o 76  -nb '#1e2030'  -sb '#8aadf4' -p DMENU: -fn 'Jet Brains Mono Nerd Font' -sf '#FFF' -nf '#FFF'"
mod = "mod4"
wallpaper = "bash ~/.config/qtile/wallpaper.sh"
terminal = "kitty"


def move_current_window_to_screen(qtile, Screen):
    screen_id = [2, 0, 1]
    group = qtile.screens[screen_id[screen]].group
    qtile.current_window.togroup(group.name)


keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(),
        desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(),
        desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(),
        desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(),
        desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(),
        desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "t", lazy.window.toggle_floating(), desc="toggle floating"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    Key([mod, "shift"], "w",
        lazy.function(move_current_window_to_screen),
        desc='random wallpaper'
        ),

    Key([mod], "p", lazy.spawn(run), desc="dmenu"),
]


def window_to_previous_screen(qtile, switch_group=False, switch_screen=False):
    i = qtile.screens.index(qtile.current_screen)
    if i != 0:
        group = qtile.screens[i - 1].group.name
        qtile.current_window.togroup(group, switch_group=switch_group)
        if switch_screen == True:
            qtile.cmd_to_screen(i - 1)


def window_to_next_screen(qtile, switch_group=False, switch_screen=False):
    i = qtile.screens.index(qtile.current_screen)
    if i + 1 != len(qtile.screens):
        group = qtile.screens[i + 1].group.name
        qtile.current_window.togroup(group, switch_group=switch_group)
        if switch_screen == True:
            qtile.cmd_to_screen(i + 1)


keys.extend([
    Key([mod, "shift"],  "left",  lazy.function(window_to_next_screen)),
    Key([mod, "shift"],  "period", lazy.function(window_to_previous_screen)),
    Key([mod, "control"], "comma",  lazy.function(
        window_to_next_screen, switch_screen=True)),
    Key([mod, "control"], "period", lazy.function(
        window_to_previous_screen, switch_screen=True)),
])
groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(
                    i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )


def init_layout_theme():
    return {"margin": 12,
            "border_focus": "#ed8796",
            "border_normal": "#7dc4e4",
            }

#this is my qtile config. YAYAY
layout_theme = init_layout_theme()
layouts = [
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    layout.MonadTall(**layout_theme),
    layout.MonadWide(),
    layout.RatioTile(**layout_theme),
    layout.Tile(**layout_theme),
    layout.TreeTab(**layout_theme),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="JetBrainsMono Nerd Font",
    padding=3,
    fontsize=14,
)

extension_defaults = widget_defaults.copy()

window_name = widget.WindowName()

screens = [
    Screen(
        top=bar.Bar([

            widget.Wallpaper(background='#363a4f', directory='~/Pictures/Wallpapers/',
                             label=' 󰣇 ', random_selection='True', fontsize='24', foreground='#cad3f5'),
            widget.GroupBox(background="#363a4f", highlight_method="block", active="#FFF", this_current_screen_border="#ed8796",
                            foreground="#ed8796", inactive="#b7bdf8", other_current_screen_border="#eed49f", this_screen_border="#8bd5ca"),
            widget.TextBox("", fontsize="50",
                           foreground="#363a4f", ),
            window_name,
            widget.TextBox("", fontsize="250",
                           foreground="#8aadf4", width=19),
            widget.CPU(background="#8aadf4", foreground="#181926",
                       format=' {freq_current}GHz {load_percent}%'),
            widget.TextBox("", fontsize="250",
                           foreground="#b7bdf8", background="#8aadf4", width=19),
            widget.OpenWeather(app_key="b8d241d5e318d53d05e4311bee5b5cb3", location="Harrisburg", metric=False,
                               format='󰖐 {main_temp}F, {weather_details}', background="#b7bdf8", foreground="#181926"),             widget.TextBox("", fontsize="250",
                                                                                                                                                    background="#b7bdf8", foreground="#939ab7", width=19),
            widget.CurrentLayoutIcon(scale=0.7, background="#939ab7"),
            widget.TextBox("", fontsize="250",
                           foreground="#6e738d", background="#939ab7", width=19),
            widget.Net(format=' {up}  {down}',
                       background="#6e738d", foreground="#cad3f5"),
            widget.TextBox("", fontsize="250",
                           foreground="#363a4f", background="#6e738d", width=19),
            widget.TextBox(" 󰋋", background="#363a4f", foreground="#1e2030"),
            widget.Volume(background="#363a4f", foreground="#cad3f5"),
            widget.TextBox("", fontsize="250",
                           foreground="#1e2030", background="#363a4f", width=19),
            widget.Clock(format="󰥔 %I:%M ", background="#1e2030",
                         width=80, foreground="#cad3f5"),
        ], 27, background="#181926")
    ),
    Screen(
        top=bar.Bar([

            widget.Wallpaper(background='#363a4f', directory='~/Pictures/Wallpapers/',
                             label=' 󰣇 ', random_selection='True', fontsize='24', foreground='#cad3f5'),
            widget.GroupBox(background="#363a4f", highlight_method="block", active="#FFF", this_current_screen_border="#ed8796",
                            foreground="#ed8796", inactive="#b7bdf8", other_current_screen_border="#eed49f", this_screen_border="#8bd5ca"),
            widget.TextBox("", fontsize="50",
                           foreground="#363a4f", ),
            window_name,
            widget.TextBox("", fontsize="250",
                           foreground="#8aadf4", width=19),
            widget.CPU(background="#8aadf4", foreground="#181926",
                       format=' {freq_current}GHz {load_percent}%'),
            widget.TextBox("", fontsize="250",
                           foreground="#b7bdf8", background="#8aadf4", width=19),
            widget.OpenWeather(app_key="b8d241d5e318d53d05e4311bee5b5cb3", location="Harrisburg", metric=False,
                               format='󰖐 {main_temp}F, {weather_details}', background="#b7bdf8", foreground="#181926"),             widget.TextBox("", fontsize="250",
                                                                                                                                                    background="#b7bdf8", foreground="#939ab7", width=19),
            widget.CurrentLayoutIcon(scale=0.7, background="#939ab7"),
            widget.TextBox("", fontsize="250",
                           foreground="#6e738d", background="#939ab7", width=19),
            widget.Net(format=' {up}  {down}',
                       background="#6e738d", foreground="#cad3f5"),
            widget.TextBox("", fontsize="250",
                           foreground="#363a4f", background="#6e738d", width=19),
            widget.TextBox(" 󰋋", background="#363a4f", foreground="#1e2030"),
            widget.Volume(background="#363a4f", foreground="#cad3f5"),
            widget.TextBox("", fontsize="250",
                           foreground="#1e2030", background="#363a4f", width=19),
            widget.Clock(format="󰥔 %I:%M ", background="#1e2030",
                         width=80, foreground="#cad3f5"),
        ], 27),    ),
]
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = False
focus_on_window_activation = 'smart'
# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.


@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/autostart.sh'])


wmname = "qtile"
