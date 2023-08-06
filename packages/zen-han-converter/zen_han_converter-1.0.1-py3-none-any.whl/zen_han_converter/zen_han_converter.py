from .han_to_zen_table import LATIN_ALPHABET as HAN2ZEN_LATIN_ALPHABET, \
                             ARABIC_NUMERALS as HAN2ZEN_ARABIC_NUMERALS, \
                             ASCII_SYMBOL as HAN2ZEN_ASCII_SYMBOL
from .zen_to_han_table import LATIN_ALPHABET as ZEN2HAN_LATIN_ALPHABET, \
                             ARABIC_NUMERALS as ZEN2HAN_ARABIC_NUMERALS, \
                             ASCII_SYMBOL as ZEN2HAN_ASCII_SYMBOL


class BaseConverter:
    """
    コンバーターの基底クラス
    """
    def __init__(self, table):
        self.table = str.maketrans(table)

    def convert(self, text):
        """
        変換する
        """
        return text.translate(self.table)


class ZenToHan(BaseConverter):
    """
    全角を半角に変換するクラス
    """
    def __init__(self, alphabet_table=True, number_table=True, ascii_symbol_table=True):
        _table = {}
        if alphabet_table:
            _table.update(ZEN2HAN_LATIN_ALPHABET)
        if number_table:
            _table.update(ZEN2HAN_ARABIC_NUMERALS)
        if ascii_symbol_table:
            _table.update(ZEN2HAN_ASCII_SYMBOL)
        super().__init__(_table)


class HanToZen(BaseConverter):
    """
    半角を全角に変換するクラス
    """
    def __init__(self, alphabet_table=True, number_table=True, ascii_symbol_table=True):
        _table = {}
        if alphabet_table:
            _table.update(HAN2ZEN_LATIN_ALPHABET)
        if number_table:
            _table.update(HAN2ZEN_ARABIC_NUMERALS)
        if ascii_symbol_table:
            _table.update(HAN2ZEN_ASCII_SYMBOL)
        super().__init__(_table)
