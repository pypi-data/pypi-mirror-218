import unittest
from duckduckgo_translate import Translator



class TestStringMethods(unittest.TestCase):
    def test_english_to_azerbaijani(self):
        translator = Translator()

        translated = translator.translate('Say hello to my little friend', dest='az')
        text = translated.text
        self.assertEqual(text.lower(), 'balaca dostuma salam de')

    def test_upper(self):
        translator = Translator()

        translated = translator.translate('Hello World', dest='de')
        text = translated.text
        self.assertEqual(text.lower(), 'hallo welt')

    def test_unicode(self):
        translator = Translator()

        translated = translator.translate('안녕하세요', src='ko', dest='ja')
        self.assertEqual(translated.text, 'じゃない')

    def test_language_name(self):
        translator = Translator()

        translated = translator.translate('Hello World', src='ENGLISH', dest='HUNGaRiAn')
        self.assertEqual(translated.text.lower(), 'helló világ')

    def test_language_name_with_space(self):
        translator = Translator()

        translated = translator.translate('Hello', src='en', dest='chinese simplified')
        self.assertEqual(translated.dest, 'zh-Hans')
    
    def test_translate_without_src(self):
        translator = Translator()

        translated = translator.translate('Hello World', dest='danish')
        self.assertEqual(translated.text, 'Hej verden')

    def test_detected_src(self):
        translator = Translator()

        translated = translator.translate('Hola Mundo', dest='en')
        self.assertEqual(translated.detected, 'es')

    def test_change_vqt(self):
        translator = Translator()

        old_vqd = translator.vqd
        translator._change_vqd()
        self.assertNotEqual(old_vqd, translator.vqd)

    def test_change_useragent(self):
        translator = Translator()

        old_useragent= translator.headers['User-Agent']
        translator._change_useragent()
        self.assertNotEqual(old_useragent, translator.headers['User-Agent'])

if __name__ == '__main__':
    unittest.main()
