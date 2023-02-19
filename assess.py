import random
import time

def run_test(real_words, made_up_words):
    words = real_words + made_up_words
    random.shuffle(words)
    correct = 0
    start_time = time.time()
    for word in words:
        is_real = word in real_words
        print(word)
        answer = input("Is this a real word? (y/n) ").lower()
        if answer == 'y' and is_real or answer == 'n' and not is_real:
            print("Correct!")
            correct += 1
        else:
            print("Incorrect!")
    end_time = time.time()
    total_time = end_time - start_time
    accuracy = correct / len(words) * 100
    return total_time, accuracy
