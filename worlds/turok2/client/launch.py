import asyncio
import colorama
import settings
from collections.abc import Sequence
from CommonClient import get_base_parser

def launch_ap_turok2_client(*args: Sequence[str]) -> None:  
    from .turok2_client import main
    
    """
    Set up the Turok 2 options - we need the executable name
    """
    exe_path = settings.get_settings()["turok2_options"]["turok2_path"]

    parser = get_base_parser()
    parser.add_argument(
        "patch_file",
        default="",
        type=str,
        nargs="?",
        help="Path to a rando.kpf Turok 2 patch file")
    args = parser.parse_args(args)
    
    colorama.just_fix_windows_console()
    asyncio.run(main(args, exe_path))
    colorama.deinit()
