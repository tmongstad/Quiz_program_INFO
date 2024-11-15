import json


def run_quiz(questions):
    while True:
        score = 0
        wrong_answers = []
        for question in questions:
            print(question["prompt"])
            for i, choice in enumerate(question["choices"]):
                print(f"{i+1}: {choice}")
            answer = int_validator('venligst velg et svaralternativ:', 4)
            print('\n')
            if question["choices"][int(answer) - 1] == question["answer"]:
                score += 1
            elif question["choices"][int(answer) - 1] != question["answer"]:
                wrong_answers.append(question['prompt'])
            elif answer == 0:
                break
        print(f"You got {score} out of {len(questions)} correct\n")
        print('Du svarte feil på følgende spørsmål:')
        for answers in wrong_answers:
            print(answers, '\n')
        user_input = input('Vil du prøve igjen? (j/n)')
        while user_input.lower() != 'j' and user_input.lower() != 'n':
            user_input = input('Tastet du feil? prøv igjen (j/n)')
        if user_input.lower() == 'j':
            continue
        elif user_input.lower() == 'n':
            break


def int_validator(prompt, number_of_alternatives):
    while True:
        try:
            user_input = int(input(prompt))
            if user_input in range(0, number_of_alternatives+1):
                return user_input
            else:
                continue
        except ValueError:
            print('vennligst tast inn et gyldig tall')
            continue


class Emner:
    emneliste = []

    def __init__(self, index, emnekode, emnenavn):
        self.emnekode = emnekode
        self.emnenavn = emnenavn
        self.index = index
        self.highscores = []
        self.emneliste.append(self)

    def load_quizzes(self):
        with open(f'Quiz_{self.emnekode}.json') as file:
            quiz = dict(json.load(file))
            return quiz

    def print_quiz_menu(self):
        quiz = self.load_quizzes()
        print("'-.,_,.-" * 10)
        for topics in quiz:
            print(topics)
        print("'-.,_,.-" * 10)


class Quizzers:
    participants_list = []
    def __init__ (self, name):
        self.name = name


emner = {'INFO100': 'Innføring i informasjonsvitenskap',
         'INFO125': 'Datahåndtering',
         'INFO132': 'Innføring i programmering',
         'INFO162': 'HCI',
         'Trivielle': 'Ikke-faglige spørsmål'
         }


def make_objects():
    for i, e in enumerate(emner.items()):
        Emner(int(i)+1, e[0], e[1])


def get_quiz(quiz_list, choice):
    for i, quizname in enumerate(quiz_list):
        if i+1 == choice:
            return quiz_list[quizname]


def menu():
    while True:
        emneliste = []
        print("'-.,_,.-" * 10)
        for emne in Emner.emneliste:
            emneliste.append(emne)
            print(f'| {emne.index}) {emne.emnekode}: {emne.emnenavn}')
        print("_,.-'-.," * 10)
        user_input = int_validator('Hvilket emne vil du øve på', len(emneliste))
        for emne in emneliste:
            if user_input == emne.index:
                sub_menu(emne)
        break


def sub_menu(emne):
    while True:
        emne.print_quiz_menu()
        user_input = int_validator('venligst velg fra menyen:', 14)
        if user_input == 0:
            quit()
        quiz_list = emne.load_quizzes()
        quiz = get_quiz(quiz_list, user_input)
        run_quiz(quiz)


make_objects()
menu()