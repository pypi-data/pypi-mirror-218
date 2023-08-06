import unittest
from translator_duck import TranslatorDuck



class TestStringMethods(unittest.TestCase):
    def test_english_to_azerbaijani(self):
        translator = TranslatorDuck()

        translated = translator.translate('Say hello to my little friend', dest='az')
        text = translated.text
        self.assertEqual(text.lower(), 'balaca dostuma salam de')

    def test_upper(self):
        translator = TranslatorDuck()

        translated = translator.translate('Hello World', dest='de')
        text = translated.text
        self.assertEqual(text.lower(), 'hallo welt')

    def test_unicode(self):
        translator = TranslatorDuck()

        translated = translator.translate('안녕하세요', src='ko', dest='ja')
        self.assertEqual(translated.text, 'じゃない')

    def test_language_name(self):
        translator = TranslatorDuck()

        translated = translator.translate('Hello World', src='ENGLISH', dest='HUNGaRiAn')
        self.assertEqual(translated.text.lower(), 'helló világ')

    def test_language_name_with_space(self):
        translator = TranslatorDuck()

        translated = translator.translate('Hello', src='en', dest='chinese simplified')
        self.assertEqual(translated.dest, 'zh-Hans')

    def test_change_vqt(self):
        translator = TranslatorDuck()

        old_vqd = translator.vqd
        translator._change_vqd()
        self.assertNotEqual(old_vqd, translator.vqd)

    def test_change_useragent(self):
        translator = TranslatorDuck()

        old_useragent= translator.headers['User-Agent']
        translator._change_useragent()
        self.assertNotEqual(old_useragent, translator.headers['User-Agent'])

if __name__ == '__main__':
    unittest.main()
