from bottle import route, run, request, template, static_file
import os
import random
import csv

@route('/spelling')
def spelling():
    return template ('templates/welcome')

@route('/spelling', method='POST')
def do_spelling():
    global correct_count
    global person_name
    correct_count = {}

    person_name = request.forms.get("name").lower()

    load_words_and_definitions(person_name)

    try:
        with open("./" + person_name + "-spelling.csv", 'r') as lines:
            reader = csv.reader(lines)
            for rows in reader:
                if rows[0] in all_words:
                    correct_count[rows[0]] = rows[1]#dict(rows[0],int(rows[1]))
    except IOError:
            correct_count = {}

    print correct_count

    return template("templates/spelling", person_name=person_name, correct_number="")


@route('/spell-word')
def spell_word():
    global word
    global word_blanks


    word_blanks = "_ " * len(word)
    word_speech = word + '.  As in ' + all_word_meanings[word]

    return template("templates/spell-word")
    # , word_speech=word_speech, word_blanks=word_blanks,
    #                             correct_number = str(len(correct_list[correct_threshold])),
    #                             total_words = str(len(all_words)), progress_message = progress_message,
    #                             percent = str(int(percent)))

@route('/spell-word', method='POST')
def do_spell_word():
    global guess

    guess = request.forms.get("guess").lower()

    if (len(word) != len(guess)):
        message = "Thats not right. The word " + word + " has " + str(len(word)) + " letters."
        # system("say " + message)
        correct_count[word] = 0

        return template("templates/wrong_length", length=str(len(word)), message=message)

    if (guess == word):
        if (word_blanks == "_ " * len(word)):  #there's not been a hint
            correct_count[word] = int(correct_count.get(word,0)) + 1
        writer = csv.writer(open(person_name + '-spelling.csv', mode='w'))
        for key, value in correct_count.items():
            writer.writerow([key, value])

        return template("templates/correct")
    else:
        correct_count[word] = 0

        return template("templates/wrong_spelling")

@route('/css/<filename>')
def server_static(filename):
    return static_file(filename, root='./css/')

@route('/js/<filename>')
def server_static(filename):
    return static_file(filename, root='./js/')

@route('/fonts/<filename>')
def server_static(filename):
    return static_file(filename, root='./fonts/')

def load_words_and_definitions(name):

    word_meanings = {}

    try:
        with open("assignment/" + person_name + ".csv", 'r') as words_files:
            reader = csv.reader(words_files)
            for rows in reader:
                words_file = rows[0]
                print words_file
            # with words_file as rows[0] for rows in reader:
                if words_file.endswith(".csv"):
                    with open("words/" + words_file, 'r') as words:
                        file_reader = csv.reader(words)
                        word_meanings[words_file] = dict((rows2[0],rows2[1]) for rows2 in file_reader)
    except IOError:
        word_meanings = {}

    print word_meanings
    global all_word_meanings
    print "----"
    for words in word_meanings.values():
        print words
        all_word_meanings.update(words)

    global all_words
    all_words = all_word_meanings.keys()


## MAIN
run(host='0.0.0.0', port=8080, debug=True)

