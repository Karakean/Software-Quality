import unittest
import codecs
from requests.utils import guess_json_utf

class TestGuessJsonUtf(unittest.TestCase):
    def test_valid_utf8(self):
        data = '{"key": "value"}'
        result = guess_json_utf(data.encode('utf-8'))
        self.assertEqual(result, 'utf-8')

    def test_utf8_sig_bom(self):
        # Test "utf-8-sig" encoding with BOM
        data = codecs.BOM_UTF8 + '{"name": "John", "age": 30}'.encode('utf-8')
        self.assertEqual(guess_json_utf(data), "utf-8-sig")

    def test_utf32_bom(self):
        # Test "utf-32" encoding with BOM
        data_le = codecs.BOM_UTF32_LE + '{"name": "John", "age": 30}'.encode('utf-32-le')
        data_be = codecs.BOM_UTF32_BE + '{"name": "John", "age": 30}'.encode('utf-32-be')
        self.assertEqual(guess_json_utf(data_le), "utf-32")
        self.assertEqual(guess_json_utf(data_be), "utf-32")

    def test_utf16_bom(self):
        # Test "utf-16" encoding with BOM
        data_le = codecs.BOM_UTF16_LE + '{"name": "John", "age": 30}'.encode('utf-16-le')
        data_be = codecs.BOM_UTF16_BE + '{"name": "John", "age": 30}'.encode('utf-16-be')
        self.assertEqual(guess_json_utf(data_le), "utf-16")
        self.assertEqual(guess_json_utf(data_be), "utf-16")

    def test_utf16_le(self):
        data = '{"key": "value"}'
        result = guess_json_utf(data.encode('utf-16-le'))
        self.assertEqual(result, 'utf-16-le')

    def test_utf16_be(self):
        data = '{"key": "value"}'
        result = guess_json_utf(data.encode('utf-16-be'))
        self.assertEqual(result, 'utf-16-be')

    def test_utf32_le(self):
        data = '{"key": "value"}'
        result = guess_json_utf(data.encode('utf-32-le'))
        self.assertEqual(result, 'utf-32-le')

    def test_utf32_be(self):
        data = '{"key": "value"}'
        result = guess_json_utf(data.encode('utf-32-be'))
        self.assertEqual(result, 'utf-32-be')

    def test_invalid_utf8(self):
        # create invalid utf-8 encoding by placing a null byte in the middle
        invalid_utf8 = "he\x00llo".encode("utf-8")
        self.assertEqual(guess_json_utf(invalid_utf8), None)
 