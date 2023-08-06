def convert_to_coptic_font(text):
    conversion_map = {
        'а': 'ⲁ',
        'б': 'ⳝ',
        'в': 'ⲃ',
        'г': 'ⲅ',
        'д': 'ⲇ',
        'е': 'ⲉ',
        'ё': 'ё',
        'ж': 'ⲯ',
        'з': 'ⳅ',
        'и': 'υ',
        'й': 'ύ',
        'к': 'ⲕ',
        'л': 'ⲗ',
        'м': 'ⲙ',
        'н': 'ⲏ',
        'о': 'ⲟ',
        'п': 'п',
        'р': 'ⲣ',
        'с': 'ⲥ',
        'т': 'ⲧ',
        'у': 'ⲩ',
        'ф': 'ⲫ',
        'х': 'ⲭ',
        'ц': 'ⲭ',
        'ч': 'ⳡ',
        'ш': 'ⳃ',
        'щ': 'ⲱ.',
        'ъ': 'ъ',
        'ы': 'ы',
        'ь': 'ь',
        'э': 'ⲉ',
        'ю': 'ⲩ',
        'я': 'я',
    }
    
    converted_text = ''
    for char in text:
        if char.lower() in conversion_map:
            converted_text += conversion_map[char.lower()]
        else:
            converted_text += char
    
    return converted_text
    