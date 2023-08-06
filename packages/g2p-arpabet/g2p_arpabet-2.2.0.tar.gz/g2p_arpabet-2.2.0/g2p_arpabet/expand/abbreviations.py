import re

# List of (regular expression, replacement) pairs for abbreviations in english:
abbreviations_en = [
    (re.compile('\\b%s\\b' % x[0], re.IGNORECASE), x[1])
    for x in [
        ('mrs', 'misess'),
        ('mr', 'mister'),
        ('dr', 'doctor'),
        ('st', 'saint'),
        ('co', 'company'),
        ('jr', 'junior'),
        ('maj', 'major'),
        ('gen', 'general'),
        ('drs', 'doctors'),
        ('rev', 'reverend'),
        ('lt', 'lieutenant'),
        ('hon', 'honorable'),
        ('sgt', 'sergeant'),
        ('capt', 'captain'),
        ('esq', 'esquire'),
        ('ltd', 'limited'),
        ('col', 'colonel'),
        ('ft', 'fort'),
        ('dept', 'department'),
        ('gov', 'governor'),
        ('mgr', 'manager'),
        ('prof', 'professor'),
        ('asst', 'assistant'),
        ('assoc', 'associate'),
    ]
]

def expand_abbreviations(text):
    for regex, replacement in abbreviations_en:
        text = re.sub(regex, replacement, text)
    return text
