import mido
from time import sleep

out = mido.open_output("Arduino Leonardo")
i = 0
j = 0

while True:
    print(i,j)
    out.send(mido.Message('note_on',note=i,velocity=j))
    if i == 63:
        i=0
    else:
        i=i+1
    if j == 127:
        j=0
    else:
        j=j+1
    sleep(0.05)
