"""
    iautil
    ======
    Internet addresses transforming utilities
"""

import re
from typing import Tuple

def addr_parser(addr: str, default_port: int) -> Tuple[str, int]:
    """        
        Parse internet address into Tuple[host: str, port: int]
        with default port support...
    """

    IPv6_PORT = r"^(\[[\d\D]{1,}\]):([0-9]{1,5})$" # [::1]:65535 -> Tuple["[::1]", 65535]
    IPv6 = r"^(\[[\d\D]{1,}\])$" # [::1] -> Tuple["[::1]", default_port]

    IPv4_PORT = r"^([0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}):([0-9]{1,5})$" # 1.1.1.1:80 -> Tuple["1.1.1.1", 80]
    IPv4 = r"^[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}$" # 1.1.1.1 -> Tuple["1.1.1.1", default_port]

    TLD_PORT = r"^(.*):([0-9]{1,5})$" # yt.be:80 -> Tuple["yt.be", 80]
    TLD = r"^(.*)$" # yt.be -> Tuple["yt.be", default_port]

    PATTERNS = [
        IPv6_PORT,
        IPv6,
        IPv4_PORT,
        IPv4,
        TLD_PORT,
        TLD
    ]

    for pattern in PATTERNS:
        i = re.findall(pattern, addr)
        if i:
            if isinstance(i[0], str):
                return i[0], default_port

            return i[0][0], int(i[0][1])
