import pathlib
from typing import ClassVar

import fabric
import np_config

from np_services.proxies import NoCamstim

class ThemeSetter(NoCamstim):
    """Base class for setting the background wallpaper on a remote machine,
    then hiding all desktop icons, hiding the taskbar, minimizing all windows"""
    local_file: ClassVar[str | pathlib.Path] 
    remote_file: ClassVar[str | pathlib.Path] 
    
    extra_args: ClassVar[list[str]] = []
    ssh: ClassVar[fabric.Connection]
    user: ClassVar[str] = 'svc_neuropix'
    password: ClassVar[str] = np_config.fetch('logins')['svc_neuropix']['password']
    
    @classmethod
    def initialize(cls):
        with cls.get_ssh() as ssh:
            ssh.put(cls.local_file, cls.remote_file)
        super().initialize()
        
class BlackThemeSetter(ThemeSetter):
    local_file = pathlib.Path(__file__).parent / 'resources' / 'black_wallpaper.ps1'
    remote_file: ClassVar[str | pathlib.Path] = 'c:/users/svc_neuropix/desktop/black_wallpaper.ps1'
    
class GreyThemeSetter(ThemeSetter):
    local_file = pathlib.Path(__file__).parent / 'resources' / 'grey_wallpaper.ps1'
    remote_file: ClassVar[str | pathlib.Path] = 'c:/users/svc_neuropix/desktop/grey_wallpaper.ps1'