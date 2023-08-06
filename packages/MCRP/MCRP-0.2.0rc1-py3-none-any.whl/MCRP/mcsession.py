"""
    # Minecraft Protocol Session
    Module that contains implementation of Minecraft protocol sessions on top of ku.tcpsession
"""

from types import ModuleType
from ku import tcpsession, Reject, Pass
from typing import Optional, List, Callable, Union

from .mcenc import AESComplex, ProtocolDecryptor
from socket import socket
from logging import Logger

import datetime
from .mcdj import DebugJournal
import cubelib
from traceback import format_exc
from importlib import import_module
from copy import copy
from json import dumps

class MinecraftSession(tcpsession):
    
    ServerBoundBuff: List[bytes]
    ClientBoundBuff: List[bytes]

    protocol: ModuleType = cubelib.proto
    proto_state: cubelib.state = cubelib.state.Handshaking
    compression: int = -1

    pass_through: bool = False
    decryptor: Optional[ProtocolDecryptor] = None
    cipher: Optional[AESComplex] = None

    handlers: dict # {cubelib.proto.v47.ServerBound.ChatMessage: [False, <function handler at 0x00000...>]}
    relative_handlders: dict

    ServerBoundHandler: Optional[Callable] = None
    ClientBoundHandler: Optional[Callable] = None
    IntersessionHandler: Optional[Callable] = None
    RewriteHandler: Optional[Callable] = None

    def __init__(self, client: socket, server: socket, proxy, logger: Logger, handlers: dict = None,
        relative_handlers: dict = None, debug_journal: bool = False) -> None:

        self.id = id(self)

        self.ServerBoundBuff = [b""] # it's a little trick to make immutable type (bytes)
        self.ClientBoundBuff = [b""] # mutable to pass reference to it

        self.handlers = {} if not handlers else handlers
        self.relative_handlers = {} if not relative_handlers else relative_handlers

        self.logger = logger

        if debug_journal:
            dt = datetime.datetime.now()
            m = dt.strftime("%B")[:3]
            ts = dt.strftime(f"%d {m} %Y %H-%M-%S")
            self.logger.info(f"{self.id} Starting debug journaling in file [{ts}.mcdj]")
            self.journal = DebugJournal(f"{ts}.mcdj")            
        else:
            self.journal = None
        
        self.IntersessionHandler() if self.IntersessionHandler else None
        self.logger.info(f"#{self.id} ready for trasmission")

    def clientbound(self, data: bytes) -> Union[bytes, Reject, Pass]:
        return self._handle_bytes(data, self.ClientBoundBuff, cubelib.bound.Client)

    def serverbound(self, data: bytes) -> Union[bytes, Reject, Pass]:
        return self._handle_bytes(data, self.ServerBoundBuff, cubelib.bound.Server)

    def connection_lost(self, side: Union[socket, None], err: Union[Exception, None]) -> None:
        side = 'client' if side is self.client else 'server' if side is not None else 'proxy'
        self.logger.info(F"#{self.id} connection_lost by {side} due to {err}")
    
    def shutdown(self) -> None:
        if self.proto_state != cubelib.state.Play:
            return

        if hasattr(self.protocol.ClientBound.Play, "Disconnect") and not self.pass_through:
            outro = f"{self.proxy.version_string}\nserved here for you =]"            
            chat_component = dumps({"text": "", "extra": [{"text":"proxy closed\n", "bold": True, "color": "aqua"}, {"text": outro, "color": "light_purple"}]})
            dconn_packet = self.protocol.ClientBound.Play.Disconnect(chat_component)
            self.sendClient(dconn_packet)

    def _handle_bytes(self, data: bytes, buff: List[bytes], bound: cubelib.bound) -> Union[bytes, Reject, Pass]:
        if self.journal:
            (self.journal.append_clientbound if bound is cubelib.bound.Client else self.journal.append_serverbound)(data)

        if data[:3] == b"\xFE\x01\xFA" and self.proto_state == cubelib.state.Handshaking:
            self.logger.warn("Client sent legacy MC|PingHost! Unsupported! Enabling pass-trough!")
            self.pass_through = True     

        if self.pass_through:
            if buff[0]:
                output = buff[0]
                buff[0] = b""
                return output + data
            else:
                return Pass

        was_encrypted = False
        if self.cipher:
            if bound is cubelib.bound.Server:
                data = self.cipher.ServerCipher.Decryptor.decrypt(data)
            elif bound is cubelib.bound.Client:
                data = self.cipher.ClientCipher.Decryptor.decrypt(data)
            was_encrypted = True
        
        packets = []
        buff[0] += data
        try:
            buff[0] = cubelib.readPacketsStream(buff[0], self.compression, bound, packets, 1 if self.proto_state is cubelib.state.Login else -1)
        except Exception as e:
            self.logger.error(f"Stream violation! Error during parsing packets stream: {e}")
            self.logger.error("\n" + format_exc())
            self.terminate()
            return Reject

        output = b""

        for packet in packets:
            if self.pass_through:
                output += packet.build(self.compression if packet.compressed else -1)
                continue # if the Handshake is sent in one buffer with LoginStart
                            # but proto is unsupported, we need to skip it right there
            try:
                handler_response = self._handle_packet(packet)
                if isinstance(handler_response, bytes):
                    output += handler_response

                elif isinstance(handler_response, cubelib.p.Night):
                    output += handler_response.build(self.compression if packet.compressed else -1)

                elif handler_response is False:
                    pass

                else:
                    output += packet.build(self.compression if packet.compressed else -1)

                    if handler_response is not None:
                        self.logger.warn(f'обработчик вернул неизвестный тип ({handler_response})')                    

            except Exception as e:
                self.logger.warn(f"Exception in {bound.name}Bound Handler: {e}")
                self.logger.warn("\n" + format_exc())

                output += packet.build(self.compression if packet.compressed else -1)
        
        if self.cipher and was_encrypted:
            return self.cipher.ServerCipher.Encryptor.encrypt(output) if bound is cubelib.bound.Server else self.cipher.ClientCipher.Encryptor.encrypt(output)
        return output

    def _handle_packet(self, packet: cubelib.p.Packet) -> Union[bytes, cubelib.p.Night, bool, None]:
        p = packet.resolve(self.proto_state, self.protocol)
        t = p.__class__

        # Global bound handlers
        if packet.bound == cubelib.bound.Client:
            self.ClientBoundHandler(p) if self.ClientBoundHandler else None
        else:
            self.ServerBoundHandler(p) if self.ServerBoundHandler else None                

        # Handle handshake
        if t is cubelib.proto.ServerBound.Handshaking.Handshake:
            self._handle_handshake(p)
            # Call a handler if exists, prematurely to prevent state check if proto hasn't been loaded
            return self.call_handlers(p)

        if self.proto_state is cubelib.state.Login:
            
            # Handle SetCompression
            if t is self.protocol.ClientBound.Login.SetCompression:
                self.logger.info(f"Point of switching-on compression with threshold {p.Threshold}")
                self.compression = p.Threshold

            # Handle LoginSuccess
            if t is self.protocol.ClientBound.Login.LoginSuccess:
                self.proto_state = cubelib.state.Play
                self.logger.info(f"State changed to {self.proto_state}")
            
            # Handle EncryptionRequest
            if t is self.protocol.ClientBound.Login.EncryptionRequest:
                if self.decryptor:
                    hr = self.decryptor.EncryptionRequest(p.ServerID, p.PublicKey, p.VerifyToken)
                    return self.protocol.ClientBound.Login.EncryptionRequest(*hr)
                return

            # Handle EncryptionResponse
            if t is self.protocol.ServerBound.Login.EncryptionResponse:
                if self.decryptor:
                    hr = self.decryptor.EncryptionResponse(p.SharedSecret, p.VerifyToken)
                    self.cipher = AESComplex(hr[0])
                    self.logger.info(f"Protocol encryption is set, but you provided a shared secret")
                    self.logger.info(f"Shared secret: {hr[0].hex()}")
                    if self.leave_debug_journals:
                        self.journal.set_enckey(hr[0])
                    return self.protocol.ServerBound.Login.EncryptionResponse(*hr[1:])
                self.logger.warn(f"Minecraft client sent EncryptionResponse! That mean full symmetric encryption enabling, so we can't proceed with protocol analyzing. Just proxying!")
                self.pass_through = True
                return
            
            elif self.proto_state is cubelib.state.Play:
                pass
        
        return self.call_handlers(p)

    def _handle_handshake(self, p: cubelib.proto.ServerBound.Handshaking.Handshake):

        if p.NextState == cubelib.NextState.Status:
            self.proto_state = cubelib.state.Status
            return
        
        self.proto_state = cubelib.state.Login
        self.logger.info(f"State changed to {self.proto_state}, trying to load protocol v{p.ProtoVer}")
        if p.ProtoVer in cubelib.supported_versions:        
            self.protocol = import_module(f"cubelib.proto.v{p.ProtoVer}")
        else:
            self.logger.warn(f"Failed to load protocol v{p.ProtoVer}, looks like it's unsupported! Enabling enabling pass-through")
            self.pass_through = True
            return

        self.logger.info(f"Successfuly loaded protovol v{p.ProtoVer}" + (f", compiling {len(self.relative_handlers)} handlers..." if self.relative_handlers else ""))
        self.resolve_handlers()

    def resolve_handlers(self) -> None:
        """Resolve relative handlers into version specific"""

        for handler in self.relative_handlers:
            attrs = handler._extract_mock_name().split('.')[1:]
            obj = self.protocol
            for attr in attrs:
                obj = getattr(obj, attr, None)
                if not obj:
                    self.logger.warn(f'Failed to resolve handler {self.protocol.__name__}.{".".join(attrs)}')
                    break
            if obj:
                self.logger.debug(f"Successfully resolved {handler} into {obj}")
                self.handlers[obj] = [True, self.relative_handlers[handler]]
    
    def call_handlers(self, packet: cubelib.p.Night) -> Union[bytes, cubelib.p.Night, bool, None]:
        """Call all handlers assigned to the packet's type"""

        src = copy(packet)
        t = packet.__class__
        if t in self.handlers:
            handlers_list = self.handlers[t][1]
            output = None
            for handler in handlers_list:
                hr = handler(self, packet)
                if hr is not None:
                    output = hr
            if output is not None and output != src:
                self.RewriteHandler(src, output) if self.RewriteHandler else None            
            return output
   
    def _send(self, fd: socket, data: bytes) -> None:
        """Send data in any direction"""
        self.proxy.send(fd, data)

    def sendClient(self, packet: cubelib.p.Night) -> None:
        """Send packet to the client"""
        raw_packet = packet.build(self.compression)

        if self.cipher:
            raw_packet = self.cipher.ClientCipher.Encryptor.encrypt(raw_packet)

        self._send(self.client, raw_packet)

    def sendServer(self, packet: cubelib.p.Night) -> None:
        """Send packet to the client"""
        raw_packet = packet.build(self.compression)
        
        if self.cipher:
            raw_packet = self.cipher.ServerCipher.Encryptor.encrypt(raw_packet)

        self._send(self.server, raw_packet)

    def chatClient(self, content: Union[str, dict]) -> None:
        """Send chat message to the client"""
        if isinstance(content, str):
            content = {"text": content}
        elif not isinstance(content, dict):            
            raise RuntimeError("chatClient requires str or dict")

        abs_packet = self.protocol.ClientBound.Play.ChatMessage
        position = abs_packet.Position.System
        packet = abs_packet(content, position)

        self.sendClient(packet)
