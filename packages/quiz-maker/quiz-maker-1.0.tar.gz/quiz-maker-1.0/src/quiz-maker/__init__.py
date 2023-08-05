from PySimpleGUI import *

argv = sys.argv

if len(argv) < 0:
    fileOpen = argv[0]
else:
    raise Exception("Expected one argument, found zero.")

file = open(fileOpen, "r")

contents = file.read().split("\n")

state = "q"

layout = []

currentQuestion = ""

questionList = []

for line in contents:
    if state == "q":
        layout.append([Text(text=line, key=line)])
        currentQuestion = line
        state = "a"
    elif state == "a":
        answers = line.split("; ")
        answerGUI = []
        for answer in answers:
            answerGUI.append(Button(button_text=answer, key=f"{currentQuestion}{answer}"))
        layout.append(answerGUI)
        state = "c"
    elif state == "c":
        questionList.append([currentQuestion, line])
        state = "q"

window = Window("Quiz Maker", layout)

ansChoice = False

while True:
    event, values = window.read()
    if event == WIN_CLOSED:
        break
    for q in questionList:
        if event == f"{q[0]}{q[1]}":
            popup("Correct!")
            ansChoice = True

    if not ansChoice:
        popup("Wrong!")

    ansChoice = False

window.close()

file.close()
