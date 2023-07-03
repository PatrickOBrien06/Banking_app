def random_string():
    
    import random
    import string

    # printing lowercase
    letters = string.ascii_lowercase
    new_word = ''.join(random.choice(letters) for i in range(10)) 

    # printing uppercase
    letters = string.ascii_uppercase
    new_word += ''.join(random.choice(letters) for i in range(10)) 

    # printing letters
    letters = string.ascii_letters
    new_word += ''.join(random.choice(letters) for i in range(10)) 

    # printing digits
    letters = string.digits
    new_word += ''.join(random.choice(letters) for i in range(10)) 

    # printing punctuation
    letters = string.punctuation
    new_word += ''.join(random.choice(letters) for i in range(10)) 

    return new_word
