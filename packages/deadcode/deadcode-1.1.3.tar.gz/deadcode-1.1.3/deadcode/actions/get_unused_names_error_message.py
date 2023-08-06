from typing import Dict, Optional

from deadcode.data_types import Filename, VariableName
from deadcode.data_types import Args


def get_unused_names_error_message(unused_names: Dict[VariableName, Filename], args: Args) -> Optional[str]:
    if not unused_names:
        return None

    if args.quiet:
        return ""

    if args.count:
        return f"{len(unused_names)}"

    if args.no_color:
        return "\n".join([f"{filename} DC100 Global {name} is never used" for name, filename in unused_names.items()])

    return "\n".join(
        [
            f"{filename} \033[91mDC100\033[0m Global \033[1m{name}\033[0m is never used"
            for name, filename in unused_names.items()
        ]
    )
