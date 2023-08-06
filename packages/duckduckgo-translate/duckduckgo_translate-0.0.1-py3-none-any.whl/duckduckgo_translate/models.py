from requests import Response

class Base:
    def __init__(self, response: Response = None):
        self._response = response


class Translated(Base):
    """Translate result object

    :param src: source language (default: auto)
    :param dest: destination language (default: en)
    :param origin: original text
    :param text: translated text
    """

    def __init__(self, src, dest, text, origin,  detected=None,**kwargs):
        super().__init__(**kwargs)
        self.src = src
        self.dest = dest
        self.text = text
        self.origin = origin
        self.detected = detected

    def __str__(self):
        return (f'Translated(src={self.src}, dest={self.dest}, text={self.text}, detected={self.detected}, ...)')

