from words2numsrus.extractor import NumberExtractor

text_number = 'один миллион шестьсот пятьдесят одна тысяча шестьсот семнадцать'
extractor = NumberExtractor()
print(extractor.replace_groups(text_number))