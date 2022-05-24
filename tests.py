import pytest
import os


class TestClass:
    @pytest.mark.asyncio
    async def test_sigverify_fail(self):
        from main import sigverify
        from fastapi import HTTPException
        from cryptography.exceptions import InvalidSignature

        with pytest.raises(InvalidSignature):
            await sigverify(
                "".join("ba" for _ in range(32)), "badbad", "badbad", b"badbad"
            )

    @pytest.mark.asyncio
    async def test_sigverify_pass(self):
        """
        Example data:
        public_key: b47713cfcd33190be17d8b8402517c6d3db3a9f53d27091e472765636a0d7cc6
        signature: ae149d1e2c9e2e07e91f292a14abc91faf46cd283cd04f877239a7a3849c971989a424601a509895cf0e571b1e66c222a8d9d205cb1bf9f31f98963a1386db04
        timestamp: 1618076862
        data: b'Test data'
        """
        from main import sigverify
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
        from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
        import time

        data = b"Test data"
        timestamp = str(int(time.time()))
        private_key = Ed25519PrivateKey.generate()
        signature = private_key.sign(timestamp.encode() + data).hex()
        public_key = (
            private_key.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw).hex()
        )

        print(public_key, signature, timestamp, data)

        assert await sigverify(public_key, signature, timestamp, data) == None
