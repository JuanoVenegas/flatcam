import pkgutil
import inspect
import sys

# allowed command modules
import tclCommands.TclCommandExteriors
import tclCommands.TclCommandInteriors


__all__=[]

for loader, name, is_pkg in pkgutil.walk_packages(__path__):
    module = loader.find_module(name).load_module(name)
    __all__.append(name)


def register_all_commands(app, commands):
    """
    Static method which register all known commands.

    Command should  be for now in directory tclCommands and module should start with TCLCommand
    Class  have to follow same  name as module.

    we need import all  modules  in top section:
    import tclCommands.TclCommandExteriors
    at this stage we can include only wanted  commands  with this, autoloading may be implemented in future
    I have no enought knowledge about python's anatomy. Would be nice to include all classes which are descendant etc.

    :param app: FlatCAMApp
    :param commands: array of commands  which should be modified
    :return: None
    """

    tcl_modules = {k: v for k, v in sys.modules.items() if k.startswith('tclCommands.TclCommand')}

    for key, module in tcl_modules.items():
        if key != 'tclCommands.TclCommand':
            classname = key.split('.')[1]
            class_ = getattr(module, classname)
            commandInstance=class_(app)

            for alias in commandInstance.aliases:
                commands[alias]={
                    'fcn': commandInstance.execute_wrapper,
                    'help': commandInstance.get_decorated_help()
                }