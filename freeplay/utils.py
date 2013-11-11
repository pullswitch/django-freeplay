import re


def encode_utf8_to_iso88591(utf8_text):
    """
    By James Murty
    http://jamesmurty.com/2011/12/30/python-code-utf8-to-latin1/

    Encode and return the given UTF-8 text as ISO-8859-1 (latin1) with
    unsupported characters replaced by '?', except for common special
    characters like smart quotes and symbols that we handle as well as we
    can.
    For example, the copyright symbol => '(c)' etc.

    If the given value is not a string it is returned unchanged.

    References:

    en.wikipedia.org/wiki/Quotation_mark_glyphs#Quotation_marks_in_Unicode
    en.wikipedia.org/wiki/Copyright_symbol
    en.wikipedia.org/wiki/Registered_trademark_symbol
    en.wikipedia.org/wiki/Sound_recording_copyright_symbol
    en.wikipedia.org/wiki/Service_mark_symbol
    en.wikipedia.org/wiki/Trademark_symbol
    """
    if not isinstance(utf8_text, basestring):
        return utf8_text
    # Replace "smart" and other single-quote like things
    utf8_text = re.sub(
        u'[\u02bc\u2018\u2019\u201a\u201b\u2039\u203a\u300c\u300d]',
        "'", utf8_text)
    # Replace "smart" and other double-quote like things
    utf8_text = re.sub(
        u'[\u00ab\u00bb\u201c\u201d\u201e\u201f\u300e\u300f]',
        '"', utf8_text)
    # Replace copyright symbol
    utf8_text = re.sub(u'[\u00a9\u24b8\u24d2]', '(c)', utf8_text)
    # Replace registered trademark symbol
    utf8_text = re.sub(u'[\u00ae\u24c7]', '(r)', utf8_text)
    # Replace sound recording copyright symbol
    utf8_text = re.sub(u'[\u2117\u24c5\u24df]', '(p)', utf8_text)
    # Replace service mark symbol
    utf8_text = re.sub(u'[\u2120]', '(sm)', utf8_text)
    # Replace trademark symbol
    utf8_text = re.sub(u'[\u2122]', '(tm)', utf8_text)
    # Replace/clobber any remaining UTF-8 characters that aren't in ISO-8859-1
    return utf8_text.encode('ISO-8859-1', 'replace')
