import os
import asyncio
import colorama
import settings
from collections.abc import Sequence
from CommonClient import get_base_parser, handle_url_arg

def launch_ap_turok2_client(*args: Sequence[str]) -> None:  
    from .turok2_client import main
    
    """
    Set up the Turok 2 options - we need the executable name
    """
    full_path = settings.get_settings()["turok2_options"]["turok2_path"]
    exe_name = os.path.basename(full_path)

    parser = get_base_parser()
    parser.add_argument("--name", default=None, help="Slot Name to connect as.")
    parser.add_argument("url", nargs="?", help="Archipelago connection url")

    launch_args = handle_url_arg(parser.parse_args(args))

    colorama.just_fix_windows_console()

    asyncio.run(main(launch_args, exe_name))

    colorama.deinit()
