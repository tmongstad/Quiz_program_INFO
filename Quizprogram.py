import json


def run_quiz(questions_dict):
    while True:
        wrong_answers, questions_dict = get_answers(questions_dict)
        # Returns a list of question answered wrong and the updated dict with the wrong answer
        print(f"You got {len(questions_dict)-len(wrong_answers)} out of {len(questions_dict)} correct\n")
        print('Du svarte feil på følgende spørsmål:')
        for questions in wrong_answers:
            print(questions[0]['prompt'])
            print(f'    Du svarte: {questions[1]}', '\n')
        if (len(wrong_answers) > 0) and get_yes_or_no('Vil du øve mer på disse ?'):
            run_quiz([x[0] for x in wrong_answers])
            break
        elif get_yes_or_no('Vil du prøve quizen en gang til?'):
            continue
        else:
            break


def get_yes_or_no(prompt): # Alternatives as list of strings:
    user_input = input(f'{prompt} (j/n)')
    while user_input.lower() != 'j' and user_input.lower() != 'n':
        user_input = input('Tastet du feil? prøv igjen (j/n)')
    if user_input.lower() == 'j':
        return True
    elif user_input.lower() == 'n':
        return False


def get_answers(questions_dict):
    wrong_answers = []
    for question in questions_dict:
        print_question(question)
        answer = int_validator('venligst velg et svaralternativ:', 4)
        print('\n')
        answer_index = int(answer-1)
        if question["choices"][answer_index] != question["answer"]:
            wrong_answers.append((question, question['choices'][answer_index]))
        elif answer == 0:
            break
    return wrong_answers, questions_dict


def print_question(question):
    print(question["prompt"])
    for i, choice in enumerate(question["choices"]):
        print(f"{i + 1}: {choice}")


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


emner = {'INFO100': 'Innføring i informasjonsvitenskap',
         'INFO125': 'Datahåndtering',
         'INFO132': 'Innføring i programmering',
         'INFO162': 'HCI',
         'INFO180': 'Innføring i kunstig intelligens',
         'Trivielle': 'Ikke-faglige spørsmål',
         'Test': 'For å teste programmet'
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

