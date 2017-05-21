import chips
import getch

oct = 1
    
# note param is string, as in "1d"
def playSingleNote(note):
    m = chips.Melody(chips.n_to_f([note]), [.07], [.3], phaser=0)
    m.play()

def getInput():
    global oct
    input = getch.getch()
    if input == '=':
        oct += 1
        return getInput()
    elif input == '-':
        oct -= 1 
        return getInput()

    return str(oct) + input.lower()

if __name__ == "__main__":
    while True:
        playSingleNote(getInput())