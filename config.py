from libqtile.config import Key, Screen, Group, Match, Drag, Click
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
from libqtile.log_utils import logger
import asyncio


try:
    import uvloop
except ImportError:
    uvloop = None


def main(qtile):
    if uvloop:
        logger.warn('set uvloop')
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


@hook.subscribe.client_new
def func(c):
    if c.name in ("amandine", "olivia"):
        c.togroup("i")
    elif c.name == "mutt":
        c.togroup("m")

mod = "mod4"


keys = [
    Key([mod, "control"], "r", lazy.restart()),
    Key([mod, "control"], "q", lazy.shutdown()),
    Key([mod], "r", lazy.spawncmd()),

    Key([mod], 't', lazy.spawn('/home/gawel/bin/notify-status')),
    Key([mod], "c", lazy.spawn("gnome-terminal")),
    Key([mod], "f", lazy.spawn("firejail firefox")),
    Key([mod], 'i', lazy.spawn('/home/gawel/bin/tmux-amandine')),
    Key([mod], 'm', lazy.spawn('/home/gawel/bin/mails show')),
    Key([mod], 'p', lazy.spawn('/home/gawel/bin/zic -s')),
    Key([mod], 'n', lazy.spawn('/home/gawel/bin/zic -n')),
    Key([mod], "q", lazy.window.kill()),

    Key([mod, "control"], "Left", lazy.layout.shuffle_left()),
    Key([mod, "control"], "Right", lazy.layout.shuffle_right()),
    Key([mod], "Left", lazy.screen.prev_group()),
    Key([mod], "Right", lazy.screen.next_group()),
    Key([mod], "Up", lazy.next_layout()),
    Key([mod], "Down", lazy.window.toggle_fullscreen()),
    Key([mod], "Tab", lazy.layout.next()),
    Key([mod], "l", lazy.layout.replace_vim()),
]

groups = [
    Group("i"),
    Group("w",
          layout="columns",
          spawn=["gnome-terminal"],
          ),
    Group("f",
          matches=[Match(wm_class=["Firefox"])],
          spawn=["firejail firefox"]
          ),
    Group("m",
          spawn=['/home/gawel/bin/mails show']
          ),
]


class Columns(layout.Columns):

    def add_column(self, prepend=True):
        return super().add_column(prepend=len(self.columns) == 1)

    def add(self, client):
        super().add(client)
        if 'gvim' in client.window.get_wm_class():
            self.cmd_replace_vim()

    def cmd_replace_vim(self):
        if len(self.columns) == 2:
            vim = None
            for c in self.columns:
                for client in c:
                    if 'gvim' in client.window.get_wm_class():
                        vim = client
                        c.remove(vim)
            if vim is not None:
                for client in self.columns[0]:
                    self.columns[0].remove(client)
                    self.columns[1].add(client)
                self.columns[0].add(vim)
                self.group.layoutAll()


layouts = [
    layout.Max(),
    Columns(border_width=1),
]

widget_defaults = dict(
    font='Arial',
    fontsize=12,
    padding=2,
)


class Bar(bar.Bar):

    def _configure(self, *args):
        super()._configure(*args)
        self.show(False)
        logger.warn('is_show: %r', self.is_show())

    def cmd_show(self):
        self.show(not self.is_show())
        self.qtile.currentGroup.layoutAll()

bottom = Bar(
            [
                widget.GroupBox(),
                widget.Prompt(),
                widget.TaskList(),
                widget.Clock(format='%H:%M'),
                widget.BatteryIcon(battery_name='BAT1'),
                widget.BatteryIcon(battery_name='BAT0'),
                widget.Systray(),
            ],
            30,
        )

screens = [Screen(bottom=bottom)]


keys.extend([
    Key([mod], 'b', lazy.bar['bottom'].show()),
])


# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating()
auto_fullscreen = True
focus_on_window_activation = "smart"
wmname = "LG3D"
