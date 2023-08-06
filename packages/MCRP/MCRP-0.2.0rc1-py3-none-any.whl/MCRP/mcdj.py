"""
    MCDJ
    ====
    Module contains implementation of 'debug journal' for Minecraft Protocol.
"""

from cubelib.types import  VarInt

class DebugJournal:
    """
        DebugJournal
        ============
    """

    def __init__(self, file_path: str):
        """
            Open debug journal in selected path
        """
        self.file = open(file_path, "wb")
    
    def append_clientbound(self, packet: bytes):
        """
            Add binary data as clientbound
        """
        self.add_record(type=0x01, data=packet)
    
    def append_serverbound(self, packet: bytes):
        """
            Add binary data as serverbound
        """
        self.add_record(type=0x02, data=packet)
    
    def set_enckey(self, key: bytes):
        """
            Set encryption key
            Record of this type should be presented after 'EncryptionResponse'
        """
        self.add_record(type=0x03, data=key)

    def add_record(self, type: int, data: bytes):
        """
            Add record

            Args:
                Type: int - record type
                Data: bytes - binary record data
        """
        self.file.write(VarInt.build(type))
        self.file.write(VarInt.build(len(data)))
        self.file.write(data)
    
    def close(self):
        """
            Close debug journal
        """
        self.file.close()
