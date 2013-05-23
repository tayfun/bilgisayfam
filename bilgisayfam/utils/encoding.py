# -*- coding: utf-8 -*-
"""
Provides a translation method that strips Turkish characters and replaces
them with ASCII equivalents.
"""


translate_table = {
    ord(u"ğ"): u"g",
    ord(u"ü"): u"u",
    ord(u"ş"): u"s",
    ord(u"ı"): u"i",
    ord(u"ö"): u"o",
    ord(u"ç"): u"c",
    ord(u"Ğ"): u"G",
    ord(u"Ü"): u"U",
    ord(u"Ş"): u"S",
    ord(u"İ"): u"I",
    ord(u"Ö"): u"O",
    ord(u"Ç"): u"C",
}


def normalize(s):
    return s.translate(translate_table)
