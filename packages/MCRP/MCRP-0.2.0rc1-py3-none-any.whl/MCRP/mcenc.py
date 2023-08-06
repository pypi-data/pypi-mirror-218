"""
    MCENC
    =====
    Module contains implementation of Minecraft protocol encryption primitives
"""

from Crypto.Cipher import AES
from typing import Tuple

class ProtocolDecryptor:
    """
        Protocol Decryptor Prototype
    """

    name: str
    version: str

    def __init__(self, logger):
        pass

    def EncryptionRequest(self, server_id: str, public_key: bytes, verify_token: str) -> Tuple[bytes, str, str]:
        """
        External Encryption Request handler for decryption setup purposes

        Args:
            server_id (str): EncryptionRequest.ServerID
            public_key (bytes): EncryptionRequest.PublicKey
            verify_token (bytes): EncryptionRequest.VerifyToken
        
        Returns:
            server_id (str): New server id
            public_key (bytes): New public key
            verify_token (bytes): New verify token
        """        
        pass
    
    def EncryptionResponse(self, shared_secret: bytes, verify_token: bytes) -> Tuple[bytes, bytes, bytes]:
        """
        External Encryption Response handler for decryption setup purposes

        Args:
            shared_secret (bytes): EncryptionResponse.SharedSecret
            verify_token (bytes): EncryptionResponse.VerifyToken
        
        Returns:
            shared_secret (bytes): Plain shared secret
            shared_secret (bytes): Encrypted shared secret
            verify_token (bytes): Encrypted verify token
        """          
        pass

class AESCipher:
    
    Encryptor: AES
    Decryptor: AES

    def __init__(self, secret: bytes):
        self.Encryptor = AES.new(secret, AES.MODE_CFB, iv=secret)
        self.Decryptor = AES.new(secret, AES.MODE_CFB, iv=secret)

class AESComplex:

    ClientCipher: AESCipher
    ServerCipher: AESCipher

    def __init__(self, secret):
        self.ClientCipher = AESCipher(secret)
        self.ServerCipher = AESCipher(secret)
