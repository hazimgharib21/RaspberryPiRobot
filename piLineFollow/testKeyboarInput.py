import keyboardInput

userInput = keyboardInput.keyboardInput()

try:
    while True:
        keyp = userInput.readkey()
        print(keyp)
        if keyp == 'q':
            break

except KeyboardInterrupt:
    pass

finally:
    pass
