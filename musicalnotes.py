import mido
from time import sleep
import enum

class chord_type(enum.Enum):
    Major=1
    Minor=2
    Augmented=3
    Diminished=4

class strum_pattern(enum.Enum):
    DDUUDU=1
    DDUUDD=2
    DDU=3
    DDUDUDUDUDU=4
    DDDD=5

#region : Enumerating Notes
A = 57
A_sharp=58
B=59
C=60
C_sharp=61
D=62
D_sharp=63
E=64
F=65
F_sharp=66
G=67
G_sharp=68
#endregion

outport = mido.open_output()            #Play all the messages written in mido

def note(note, velocity=64, time=2):
    '''
    Sends a message to mido to play a note
    :param note: Number that specifies a certain note
    :param velocity: Volume
    :param time: duration
    :return: message to the mido
    '''
    return mido.Message('note_on', note=note, velocity=velocity, time=time)

def note_off(note, velocity=64, time=2):
   '''

   :param note: Number that specifies a certain note
   :param velocity: Volume
   :param time: duration
   :return: message to the mido
   '''
   return mido.Message('note_off', note=note, velocity=velocity, time=time)

def pause():
    '''

    :return:#Pausing for random time to make it sound more natural
    '''
    sleep(.01)

def Chord(root,duration,is_natural_sounding,is_down,chord_type):
    '''
    Plays chord
    a and b are local variables that define a chord_type
    :param root:Main note of chord
    :param duration: sustain time
    :param is_natural_sounding: True when u want a natural sound , and false when u want digital
    :param is_down: True if u want similar like strumming down in guitar, False if you strum up
    :param chord_type: these are given in class Enum: chord_name
    :return: Sends message to play chord
    '''

    if chord_type==chord_type.Major:
        a =4
        b= 7
    elif chord_type==chord_type.Minor:
        a=3
        b=7
    elif chord_type==chord_type.Augmented:
        a=4
        b=8
    elif chord_type==chord_type.Diminished:
        a=3
        b=6

    if is_down==True:

        outport.send(note(root -12+a))
        if is_natural_sounding == True: pause()
        outport.send(note(root -12+b))
        if is_natural_sounding==True: pause()
        outport.send(note(root))
        if is_natural_sounding == True: pause()
        outport.send(note(root+a))
        if is_natural_sounding == True: pause()
        outport.send(note(root+b))

        sleep(duration)

        outport.send(note_off(root-12+a))
        outport.send(note_off(root-12+b))
        outport.send(note_off(root))
        outport.send(note_off(root+a))
        outport.send(note_off(root+b))
        outport.send(note_off(root + b))

    else:
        outport.send(note(root,54))
        if is_natural_sounding == True: pause()
        outport.send(note(root+a,54))
        if is_natural_sounding == True: pause()
        outport.send(note(root+b,54))
        if is_natural_sounding == True: pause()
        outport.send(note(root -12+b,54))
        if is_natural_sounding == True: pause()
        outport.send(note(root - 12 + a,54))


        sleep(duration)

        outport.send(note_off(root ))
        outport.send(note_off(root +a))
        outport.send(note_off(root + b))
        outport.send(note_off(root-12+b))
        outport.send(note_off(root - 12 + a))

def strum(root,chord_type,bpm,is_natural_sounding,strum):
    '''
    Strums like a guitar
    :param root: Key note in Number
    :param chord_type: as given in the Enum list chord_type
    :param bpm: speed of playing
    :param is_natural_sounding: True if u want to sound natural Or False if u want to sound digital
    :param strum: as given in strum_pattern Enum
    :return:
    '''

    if strum==strum_pattern.DDUUDD:
        '''
        for this pattern,
         in 60bpm, 16 parts are played in 4 seconds
         in 60bpm, 1 part is played in 4/16 seconds
         in 1 bpm, 1 part is played in 4/16*60 seconds
         in bpm , 1 part is played in 4/16*60/bpm seconds
        '''
        duration=4/16*60/bpm

        Chord(root, duration*4,is_natural_sounding,True,chord_type)
        Chord(root, duration*3, is_natural_sounding,True,chord_type)
        Chord(root, duration*2, is_natural_sounding,False,chord_type)
        Chord(root, duration, is_natural_sounding,False,chord_type)
        Chord(root, duration*2, is_natural_sounding,True,chord_type)
        Chord(root, duration*2, is_natural_sounding,True,chord_type)
        Chord(root, duration , is_natural_sounding, True,chord_type)
        Chord(root, duration, is_natural_sounding, False,chord_type)

    elif strum==strum_pattern.DDUUDU:
        '''
               for this pattern,
                in 60bpm, 8 parts are played in 2 seconds
                in 60bpm, 1 part is played in 2/8 seconds
                in 1 bpm, 1 part is played in 2/8*60 seconds
                in bpm , 1 part is played in 2/8*60/bpm seconds
        '''
        duration=2/12*60/bpm
        Chord(root, duration * 3, is_natural_sounding, True,chord_type)
        Chord(root, duration*2, is_natural_sounding, True,chord_type)
        Chord(root, duration*3, is_natural_sounding, False,chord_type)
        Chord(root, duration, is_natural_sounding, False,chord_type)
        Chord(root, duration*2, is_natural_sounding, True,chord_type)
        Chord(root, duration, is_natural_sounding, True,chord_type)

    elif strum == strum_pattern.DDU:
        '''
        for this pattern,
                        in 60bpm, 6 parts are played in 1 seconds
                        in 60bpm, 1 part is played in 1/6 seconds
                        in 1 bpm, 1 part is played in 1/6*60 seconds
                        in bpm , 1 part is played in 1/6*60/bpm seconds
        '''
        duration = 1 / 6 * 60 / bpm
        Chord(root, duration * 3, is_natural_sounding, True,chord_type)
        Chord(root, duration*2, is_natural_sounding, True,chord_type)
        Chord(root, duration, is_natural_sounding, False,chord_type)
    elif strum == strum_pattern.DDUDUDUDUDU:
        '''for this pattern,
                    in 60bpm, 17.5 parts are played in 4 seconds
                    in 60bpm, 1 part is played in 4/17.5 seconds
                    in 1 bpm, 1 part is played in 4/17.5*60 seconds
                    in bpm , 1 part is played in 4/17.5*60/bpm seconds
        '''
        duration = 4 / 17.5 * 60 / bpm
        Chord(root, duration *3.5, is_natural_sounding, True,chord_type)
        Chord(root, duration, is_natural_sounding, True,chord_type)
        Chord(root, duration, is_natural_sounding, False,chord_type)
        Chord(root, duration, is_natural_sounding, True,chord_type)
        Chord(root, duration*3.5, is_natural_sounding, False,chord_type)
        Chord(root, duration, is_natural_sounding, True,chord_type)
        Chord(root, duration, is_natural_sounding, False,chord_type)
        Chord(root, duration, is_natural_sounding, True,chord_type)
        Chord(root, duration*2.5 , is_natural_sounding, False,chord_type)
        Chord(root, duration, is_natural_sounding, True,chord_type)
        Chord(root, duration, is_natural_sounding, True, chord_type)
    elif strum==strum_pattern.DDDD:
        '''
        for this pattern,
        in 60bpm, 2 parts are played in 1 seconds
        in 60bpm, 1 part is played in 1/2 seconds
        in 1 bpm, 1 part is played in 1/2*60 seconds
        in bpm  , 1 part is played in 1/2*60/bpm seconds
        '''
        duration = 1 / 2 * 60 / bpm
        Chord(root, duration , is_natural_sounding, True, chord_type)
        Chord(root, duration, is_natural_sounding, True, chord_type)

while True:
    duration = 2
    Chord(G, duration, False, True, chord_type.Major)
    Chord(E, duration, False, True, chord_type.Minor)
    Chord(C, duration, False, True, chord_type.Major)
    Chord(D, duration, False, True, chord_type.Major)
    bpm=60
    strum(G, chord_type.Major, bpm, False, strum_pattern.DDU)
    strum(C, chord_type.Major, bpm, False, strum_pattern.DDU)
    strum(D, chord_type.Major, bpm, False, strum_pattern.DDU)
    strum(G, chord_type.Major, bpm, False, strum_pattern.DDU)

    strum(G, chord_type.Major, bpm, True, strum_pattern.DDU)
    strum(C, chord_type.Major, bpm, True, strum_pattern.DDU)
    strum(D, chord_type.Major, bpm, True, strum_pattern.DDU)
    strum(G, chord_type.Major, bpm, True, strum_pattern.DDU)

    strum(G, chord_type.Major, bpm, True, strum_pattern.DDUUDU)
    strum(E, chord_type.Minor, bpm, True, strum_pattern.DDUUDU)
    strum(C, chord_type.Major, bpm, True, strum_pattern.DDUUDU)
    strum(D, chord_type.Major, bpm, True, strum_pattern.DDUUDU)

    Chord(G, duration, False, True, chord_type.Major)
