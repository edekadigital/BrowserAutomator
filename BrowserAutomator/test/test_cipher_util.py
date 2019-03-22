from unittest import TestCase, main
from unittest.mock import patch
from BrowserAutomator.cipher_util import *
from BrowserAutomator.test.mocks import KeyMock, OAEPMock


class CipherUtilTest(TestCase):
    priv_key, pub_key, filename = "priv_key_path", "pub_key_path", "file_path"

    @patch("BrowserAutomator.cipher_util.interact_with_file")
    @patch("BrowserAutomator.cipher_util.generate", side_effect=lambda x: KeyMock())
    def test_key_generator(self, generate_mock, file_util_mock):
        key_generator(self.priv_key, self.pub_key, 1023)
        generate_mock.assert_called_with(1023)
        file_util_mock.assert_called_with(self.pub_key, "wb", "key")

    @patch("BrowserAutomator.cipher_util.PKCS1_OAEP.new", side_effect=OAEPMock().new)
    @patch("BrowserAutomator.cipher_util.importKey", side_effect=lambda key: KeyMock())
    @patch("BrowserAutomator.cipher_util.interact_with_file", side_effect=lambda file, mode, content=None: "test")
    def test_encrypt_no_output(self, file_util_mock, import_key_mock, oaep_mock):
        out = encrypt("decrypted", self.priv_key)
        self.assertEqual(b"encrypteddecrypted", out)
        file_util_mock.assert_called_with(self.priv_key, "rb")
        import_key_mock.assert_called_with("test")
        oaep_mock.assert_called_with(KeyMock())

    @patch("BrowserAutomator.cipher_util.PKCS1_OAEP.new", side_effect=OAEPMock().new)
    @patch("BrowserAutomator.cipher_util.importKey", side_effect=lambda key: KeyMock())
    @patch("BrowserAutomator.cipher_util.interact_with_file", side_effect=lambda file, mode, content=None: "test")
    def test_encrypt_no_output(self, file_util_mock, import_key_mock, oaep_mock):
        out = encrypt("decrypted", self.priv_key, self.filename)
        self.assertEqual(b"encrypteddecrypted", out)
        file_util_mock.assert_called_with(self.filename, "wb", b"encrypteddecrypted")
        import_key_mock.assert_called_with("test")
        oaep_mock.assert_called_with(KeyMock())

    @patch("BrowserAutomator.cipher_util.PKCS1_OAEP.new", side_effect=OAEPMock().new)
    @patch("BrowserAutomator.cipher_util.importKey", side_effect=lambda key: KeyMock())
    @patch("BrowserAutomator.cipher_util.interact_with_file", side_effect=lambda file, mode, content=None: "test")
    def test_decrypt(self, file_util_mock, import_key_mock, oaep_mock):
        out = decrypt("encrypted", self.priv_key)
        self.assertEqual(out, "decryptedencrypted")
        file_util_mock.assert_called_with(self.priv_key, "rb")
        import_key_mock.assert_called_with("test")
        oaep_mock.assert_called_with(KeyMock())

    @patch("BrowserAutomator.cipher_util.decrypt", side_effect=lambda x, y: "decrypted")
    @patch("BrowserAutomator.cipher_util.interact_with_file", side_effect=lambda file, mode, content=None: "text")
    def test_decrypt_file(self, file_util_mock, decrypt_mock):
        out = decrypt_file(self.priv_key, self.filename)
        self.assertEqual(out, "decrypted")
        file_util_mock.assert_called_with(self.filename, "rb")
        decrypt_mock.assert_called_with("text", self.priv_key)

    @patch("BrowserAutomator.cipher_util.decrypt_file", side_effect=lambda priv, enc: "decrypted")
    def test_decrypt_content(self, decrypt_file_mock):
        decrypt_content({"private_key_path": self.priv_key, "encrypted_file_path": self.filename})
        decrypt_file_mock.assert_called_with(self.priv_key, self.filename)

    @patch("BrowserAutomator.cipher_util.open")
    def test_interact_with_file(self, open_mock):
        interact_with_file(self.filename, "wb")
        open_mock.assert_called_with(self.filename, "wb")
        interact_with_file(self.filename, "wb", content="abc")
        open_mock.assert_called_with(self.filename, "wb")


if __name__ == '__main__':
    main()
