from zen_han_converter.zen_han_converter import ZenToHan, HanToZen


def test_ZenToHan():
    zen_to_han = ZenToHan(alphabet_table=True, number_table=True, ascii_symbol_table=True)
    assert zen_to_han.convert('ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ') == 'abcdefghijklmnopqrstuvwxyz'
    assert zen_to_han.convert('abcdefghijklmnopqrstuvwxyz') == 'abcdefghijklmnopqrstuvwxyz'
    assert zen_to_han.convert('０１２３４５６７８９') == '0123456789'
    assert zen_to_han.convert('0123456789') == '0123456789'
    assert zen_to_han.convert("！＂＃＄％＆＇（）＊＋，－．／：；＜＝＞？＠［＼］＾＿｀｛｜｝～") == "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
    assert zen_to_han.convert("!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~") == "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"


def test_HanToZen():
    han_to_zen = HanToZen(alphabet_table=True, number_table=True, ascii_symbol_table=True)
    assert han_to_zen.convert("abcdefghijklmnopqrstuvwxyz") == "ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ"
    assert han_to_zen.convert("ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ") == "ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ"
    assert han_to_zen.convert("0123456789") == "０１２３４５６７８９"
    assert han_to_zen.convert("０１２３４５６７８９") == "０１２３４５６７８９"
    assert han_to_zen.convert("!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~") == "！＂＃＄％＆＇（）＊＋，－．／：；＜＝＞？＠［＼］＾＿｀｛｜｝～"
    assert han_to_zen.convert("！＂＃＄％＆＇（）＊＋，－．／：；＜＝＞？＠［＼］＾＿｀｛｜｝～") == "！＂＃＄％＆＇（）＊＋，－．／：；＜＝＞？＠［＼］＾＿｀｛｜｝～"
