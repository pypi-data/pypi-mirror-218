"""
    MineCraft Rewrite Proxy
    =======================
"""

import traceback
import logging
from importlib import import_module
from unittest.mock import MagicMock
from time import time, sleep

import datetime

import cubelib
import MCRP

from ku import ku

from typing import Optional, List, Callable, Union
from types import ModuleType

from copy import copy
import json

Relative = MagicMock()

from .mcenc import ProtocolDecryptor
from .mcsession import MinecraftSession

class MCRewriteProxy(ku):
    """    
        Ku-proxy with mcsession, join() ja cross-session handlers.
    """
    
    handlers: dict
    relative_handlers: dict
    PSM = 0 # broken timings on compression establishment issue[cubelib #3] (don't stop! don't stop!)

    def __init__(self, listen: tuple, upstream: tuple,
        loglevel = logging.INFO, session: MinecraftSession = MinecraftSession,
        decryptor: Optional[ProtocolDecryptor] = None,
        leave_debug_journals: bool = False, maxcon: int = -1,
        upstream_6: bool = False, ku_loglevel = logging.ERROR):

        self.version_string = f"MCRP/{MCRP.version} (cubelib version {cubelib.version})"
        
        self.logger = logging.getLogger("MCRP")
        self.logger.setLevel(loglevel)
        self.logger.info(f"Running {self.version_string}")
        self.logger.info(f"Proxying config is: \u001b[97m{listen[0]}:{listen[1]} \u001b[92m-> \u001b[97m{':'.join([str(a) for a in upstream])}")
        self.logger.info(f"Using protocol decryptor: {decryptor.name}/{decryptor.version}") if decryptor else None
        self.logger.info(f"Debug journaling enabled!") if leave_debug_journals else None

        if decryptor:
            crlogger = logging.getLogger("MCRP/CRYPTO")
            crlogger.setLevel(loglevel)
            self.decryptor = decryptor(crlogger)              

        self.listen = listen
        self.upstream = upstream

        self.session = session
        self.maxcon = maxcon
        self.upstream_6 = upstream_6
        self.leave_debug_journals = leave_debug_journals
        self.loglevel = loglevel
        self.ku_loglevel = ku_loglevel

        self.handlers: dict = {}
        self.relative_handlers: dict = {}

    def join(self):
        
        self.logger.info(f'Registred direct handlers list[{len(self.handlers)}]:')
        for name, handlers in self.handlers.items():
            self.logger.info(f"[{len(handlers[1])}]    {name}")

        self.logger.info(f'Registred relative handlers list[{len(self.relative_handlers)}]:')
        for name, handlers in self.relative_handlers.items():
            self.logger.info(f"[{len(handlers)}]    {'.'.join(name._extract_mock_name().split('.')[1:])}")

        args = (self.logger, self.handlers, self.relative_handlers, self.leave_debug_journals)
        super().__init__(self.listen, self.upstream, self.session, args, self.maxcon, self.upstream_6, self.ku_loglevel)

        self.logger.debug("Entering mainloop")
        while self.alive:
            try:
                sleep(0.017)
            except KeyboardInterrupt:
                self.logger.debug("Shutting down...")
                self.shutdown()
                break

        self.logger.debug("Exiting...")

    def on(self, type_):
        def no(fun):
            if isinstance(type_, MagicMock):
                if type_ in self.relative_handlers:
                    self.relative_handlers[type_].append(fun)
                else:
                    self.relative_handlers[type_] = [fun]
            else:
                if type_ in self.handlers:
                    self.handlers[type_][1].append(fun)
                else:
                    self.handlers[type_] = [False, [fun]]
            return fun
        return no
    
    def purge_rel_handlers(self):
        """Remove active relative handlers"""

        for handler in dict(self.handlers):
            if self.handlers[handler][0] == True: # if relative
                del self.handlers[handler]

        self.relative_handlers.clear() # remove relative handlers from all sessions
