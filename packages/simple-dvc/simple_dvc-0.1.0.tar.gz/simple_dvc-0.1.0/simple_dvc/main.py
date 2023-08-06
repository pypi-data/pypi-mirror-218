####
# SimpleDVC CLI Stuff (should move to a new file)
import scriptconfig as scfg  # NOQA
from simple_dvc.api import SimpleDVC

from simple_dvc.registery import DVC_RegisteryCLI


class SimpleDVC_CLI(scfg.ModalCLI):
    """
    A DVC CLI That uses our simplified (and more permissive) interface.

    The main advantage is that you can run these commands outside a DVC repo as
    long as you point to a valid in-repo path.
    """

    class Add(scfg.DataConfig):
        """
        Add data to the DVC repo.
        """
        __command__ = 'add'

        paths = scfg.Value([], nargs='+', position=1, help='Input files / directories to add')

        @classmethod
        def main(cls, cmdline=1, **kwargs):
            config = cls.cli(cmdline=cmdline, data=kwargs, strict=True)
            dvc = SimpleDVC()
            dvc.add(config.paths)

    class Request(scfg.DataConfig):
        """
        Pull data if the requested file doesn't exist.
        """
        __command__ = 'request'

        paths = scfg.Value([], nargs='+', position=1, help='Data to attempt to pull')
        remote = scfg.Value(None, short_alias=['r'], help='remote to pull from if needed')

        @classmethod
        def main(cls, cmdline=1, **kwargs):
            config = cls.cli(cmdline=cmdline, data=kwargs, strict=True)
            dvc = SimpleDVC()
            dvc.request(config.paths)

    class CacheDir(scfg.DataConfig):
        """
        Print the cache directory
        """
        __command__ = 'cache_dir'

        dvc_root = scfg.Value('.', position=1, help='get the cache path for this DVC repo')

        @classmethod
        def main(cls, cmdline=1, **kwargs):
            config = cls.cli(cmdline=cmdline, data=kwargs, strict=True)
            dvc = SimpleDVC(dvc_root=config.dvc_root)
            print(dvc.cache_dir)

    registery = DVC_RegisteryCLI


main = SimpleDVC_CLI.main


if __name__ == '__main__':
    """
    CommandLine:
        python ~/code/simple_dvc/simple_dvc/main.py
    """
    main()
