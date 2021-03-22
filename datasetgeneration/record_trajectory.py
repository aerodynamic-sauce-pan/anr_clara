import sys
from unrealcv import client
from pynput import keyboard

client.connect()
if not client.isconnected():
    print('UnrealCV server is not running. Run the game downloaded from http://unrealcv.github.io first.')
    sys.exit(-1)
f = open('trajectory.txt', 'a')
n = 0
    
def _onkeypress(key):
    try: k = key.char # single-char keys
    except: k = key.name # other keys
    #check for quit condition
    if key == keyboard.Key.esc:
        print("LOG INFO: Time to quit")
        f.close()
        return False
    try:
        if k == 'p': #On pressing 'p', capture position.
            print("Capturing position!")
            pose = client.request('vget /camera/0/pose')
            n += 1
            print("Position {} : {} captured!".format(n, pose))
            f.write(str(pose)+'\n')
    except:
        pass

def main():
    keyboard_listener = keyboard.Listener(on_press=_onkeypress)
    keyboard_listener.start()   
    keyboard_listener.join()
    print("LOG INFO: Quit command completed")

if __name__ == "__main__":
    sys.exit(main())