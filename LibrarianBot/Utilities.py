# static variables
true = True
false = False


# Function to determine is a given token is "noisy"
# Concept from: https://www.analyticsvidhya.com/blog/2017/04/natural-language-processing-made-easy-using-spacy-%E2%80%8Bin-python/
def isNoisy(token, pos_exclusions=[], min_char_length=3, force_include=["aid", "mcg", "bi", "pi", "mi"]):
    exclude = false
    # default exclusion
    if token.is_stop:
        exclude = true
    if token.pos_ in pos_exclusions:
        exclude = true
    if len(token.string) <= min_char_length:
        exclude = true
    if token.string in force_include:
        exclude = false
    return exclude
