GlowScript 2.8 VPython
#
# game_starter.py
#
# Een interactie met 3D graphics bouwen met Python
#   Documentatie: https://www.glowscript.org/docs/VPythonDocs/index.html
#   Voorbeelden:  https://www.glowscript.org/#/user/GlowScriptDemos/folder/Examples/
#

scene.bind('keydown', keydown_fun)        # Functie voor toetsaanslagen
scene.bind('click', click_fun)            # Functie voor muiskliks
scene.background = 0.8 * vector(1, 1, 1)  # Lichtgrijs (0.8 van 1.0)
scene.width = 640                         # Maak het 3D-scherm groter
scene.height = 480


# +++ Begin van het AANMAKEN van OBJECTEN
# Deze functies maken "container"-objecten, ofwel "compounds"

class PoolGame:
    #PoolGame class waar alle objecten van de game in worden bewaard
    def __init__(self, state):
        #The constructor for objects of type PoolGame
        self.state = state
       
    def getGameState(self):
        #returns the gamestate as an Integer
        return self.state
        
    def setGameState(state):
        #this method sets the GameState of the PoolGame object to the input state (valid states: 0,1,2)
        if(state < 0 or state > 2):
            print("Cannot set GameState to " + state + " invalid GameState!")
        else:
            self.state = state
            
class Player:
    #Player class where all player values are stored
    def __init__(self, username):
        #The constructor for objects of type Player
        self.username = username
        self.score = 0
        self.selected = 0
        
    def getPlayerScore(self):
        #returns the Player score as an Integer
        return self.score
        
    def setPlayerScore(amount):
        #This method sets the Player score to the input amount
        self.score = amount
        
    def getSelectedBall(self):
        #returns the ball that the player has selected
        return self.selected
        
    def toggleSelectedBall(self):
        #This method sets the selected ball
        if(self.selected >= 1):
            self.selected = 0
        else:
            self.selected = 1
        
class Guard:
    #Gaurd class where all  
    def __init__(self, id, startX, startZ):
        #The constructor for objects of type Player
        self.id = id
        self.startX = startX
        self.startZ = startZ

def make_alien(starting_position, starting_vel=vector(0, 0, 0)):
    """The lines below make a new "frame", which is a container with a
       local coordinate system.
       The arguments to make_alien allow for any initial starting position
       and initial starting velocity, with a default starting velocity
       of vector(0, 0, 0).

       Compounds can have any number of components.  Here are the
       alien's components:
    """
    alien_body = sphere(size=1.0 * vector(1, 1, 1), pos=vector(0, 0, 0), color=color.green)
    alien_eye1 = sphere(size=0.3 * vector(1, 1, 1), pos=.42 * vector(.7, .5, .2), color=color.white)
    alien_eye2 = sphere(size=0.3 * vector(1, 1, 1), pos=.42 * vector(.2, .5, .7), color=color.white)
    alien_hat = cylinder(pos=0.42 * vector(0, .9, -.2), axis=vector(.02, .2, -.02), size=vector(0.2, 0.7, 0.7), color=color.magenta)
    alien_objects = [alien_body, alien_eye1, alien_eye2, alien_hat]  # maak een lijst die we "aan elkaar plakken" met een compound
    # we gaan nu een compound maken -- we noemen hem com_alien:
    com_alien = compound(alien_objects, pos=starting_position)
    com_alien.vel = starting_vel   # stel de beginsnelheid in
    return com_alien

# We maken een GamePool en Player object
PoolGame = PoolGame(0)
player = Player("Player1")

# We maken de grond door middel van een box (VPython's rechthoekige vorm)
# https://www.glowscript.org/docs/VPythonDocs/box.html
ground = box(size=vector(20, 1, 20), pos=vector(0, -1, 0), color=.4*vector(1, 1, 1))

# We maken twee muren, ook met een box
wall_a = box(pos=vector(0, 0, -10), axis=vector(1, 0, 0), size=vector(20, 1, .2), color=vector(1.0, 0.7, 0.3))  # geel
wall_b = box(pos=vector(-10, 0, 0), axis=vector(0, 0, 1), size=vector(20, 1, .2), color=color.blue)   # blauw
wall_c = box(pos=vector(10, 0, 0), axis=vector(0, 0, 1), size=vector(20, 1, .2), color=color.red)   # red
wall_d = box(pos=vector(0, 0, 10), axis=vector(1, 0, 0), size=vector(20, 1, .2), color=color.green) # green

# Boost aanmaken, klein doosje met grote power
boost_a = box(pos=vector(8, 0, 8), axis=vector(1, 0, 0), size=vector(1, 1, 1), color=vector(1,0.7,0.2))

# Een bal die we kunnen besturen
ball = sphere(size=1.0*vector(1, 1, 1), color=vector(0.8, 0.5, 0.0))   # ball is een object van de klasse sphere
ball.vel = vector(0, 0, 0)     # dit is de beginsnelheid

# Een bal die we kunnen besturen
ball2 = sphere(size=1.0*vector(1, 1, 1), color=vector(0.4, 0.8, 0.0))   # ball is een object van de klasse sphere
ball2.vel = vector(0, 0, 0)     # dit is de beginsnelheid

# We maken twee aliens met twee aanroepen naar de functie make_alien (hierboven)
alien = make_alien(starting_position=vector(6, 0, -6), starting_vel=vector(0, 0, -1))
alien2 = make_alien(starting_position=vector(-10, 5, -10))  # geen startsnelheid


# +++ Eind van het AANMAKEN van OBJECTEN


# +++ Begin van de ANIMATIE

# Andere constanten
RATE = 30                # Het aantal keer dat de while-lus per seconde wordt uitgevoerd
dt = 1.0/RATE            # De tijdstap per keer dat de while-lus wordt uitgevoerd
scene.autoscale = False  # Voorkomen dat het beeld automatisch wordt aangepast
scene.forward = vector(0, -3, -2)  # De scene vanuit de lucht wordt bekeken...

# Dit is de "event loop" ("gebeurtenissenlus") of "animatielus"
# Elke keer dat deze lus uitgevoerd wordt beweegt alles één tijdstap van dt seconden
#
while True:

    rate(RATE)   # Maximaal aantal keer per seconden dat de while-lus uitgevoerd wordt

    # +++ Begin van het UITVOEREN van de PHYSICS -- werk alle posities elke tijdstap bij

    alien.pos = alien.pos + alien.vel*dt   # Werk de positie van de alien bij
    ball.pos = ball.pos + ball.vel*dt      # Werk de positie van de bal bij
    ball2.pos = ball2.pos + ball2.vel*dt   # Werk de positie van bal 2 bij

    # +++ Eind van het UITVOEREN van de PHYSICS -- zorg dat alle objecten goed zijn bijgewerkt!


    # +++ Begin van BOTSINGEN -- zorg voor botsingen & doe het "goede"

    arena_collide(ball)
    arena_collide(ball2)
    arena_collide(alien)

    # Geef de alien verticale snelheid als de bal de alien raakt
    if mag(ball.pos - alien.pos) < 1.0:
        print("Op naar de sterren, en daar voorbij!")
        alien.color = color.gray(.8)
        alien.vel = vector(0, 1, 0)

    # Als de alien te ver loopt, stel deze dan willekeurige opnieuw in -- maar alleen
    # als deze niet verticaal beweegt.
    """
    if mag(alien.pos) > 10 and alien.vel.y < 1:
        alien.pos.x = choice([-6, 6])
        alien.pos.z = choice([-6, 6])
        alien.vel = 2*vector.random()  # Willekeurige vector uit de module
        alien.vel.y = 0.0              # Geen verticale snelheid
    """

    # +++ Einde van BOTSINGEN


# +++ Begin van het AFHANDELEN van EVENTS -- aparte functies voor
#                                          toetsaanslagen and muiskliks...


def keydown_fun(event):
    """This function is called each time a key is pressed."""
    ball.color = randcolor()
    key = event.key
    ri = randint(0, 10)
    #print("toets:", key, ri)  # Drukt de ingedrukte toets af

    amt = 0.42              # Hoeveel de snelheid per toetsaanslag wordt aangepast
    if key == 'up' or key in 'wWiI':
        if(player.getSelectedBall() == 0):
            ball.vel = ball.vel + vector(0, 0, -amt) 
        else:
            ball2.vel = ball2.vel + vector(0, 0, -amt) 
        #ball.vel = ball.vel + vector(0, 0, -amt)
    elif key == 'left' or key in 'aAjJ':
        if(player.getSelectedBall() == 0):
            ball.vel = ball.vel + vector(-amt, 0, 0) 
        else:
            ball2.vel = ball2.vel + vector(-amt, 0, 0) 
        #ball.vel = ball.vel + vector(-amt, 0, 0)
    elif key == 'down' or key in 'sSkK':
        if(player.getSelectedBall() == 0):
            ball.vel = ball.vel + vector(0, 0, amt) 
        else:
            ball2.vel = ball2.vel + vector(0, 0, amt) 
        #ball.vel = ball.vel + vector(0, 0, amt)
    elif key == 'right' or key in "dDlL":
        if(player.getSelectedBall() == 0):
            ball.vel = ball.vel + vector(amt, 0, 0) 
        else:
            ball2.vel = ball2.vel + vector(amt, 0, 0) 
        #ball.vel = ball.vel + vector(amt, 0, 0)
    elif key in 'rR':
        ball.vel = vector(0, 0, 0)  # Opnieuw beginne! via de spatiebalk, " "
        ball.pos = vector(0, 0, 0)
    elif key in ' ':
        #toggle tussen de twee ballen
        player.toggleSelectedBall(player.getSelectedBall() + 1)
        print("selected:", player.getSelectedBall())
        


def click_fun(event):
    """This function is called each time the mouse is clicked."""
    print("event is", event.event, event.which)


# +++ Einde van het AFHANDELEN van EVENTS



# +++ Andere functies kan je hier neerzetten...

def arena_collide(ball):
    """Arena collisions!
       Ball must have a .vel field and a .pos field.
    """
    if ball.pos.z < wall_a.pos.z:  # Geraakt -- vergelijk de z-positie
        ball.pos.z = wall_a.pos.z  # Zorg dat de bal binnen de grenzen blijft
        ball.vel.z *= -0.9        # Draai de z-snelheid om

    # Als de ball wall_b raakt
    if ball.pos.x < wall_b.pos.x:  # Geraakt -- vergelijk de x-positie
        ball.pos.x = wall_b.pos.x  # Zorg dat de bal binnen de grenzen blijft
        ball.vel.x *= -0.9         # Draai de x-snelheid om
        
    # Als de ball wall_c raakt    
    if ball.pos.x > wall_c.pos.x:
        ball.pos.x = wall_c.pos.x
        ball.vel.x *= -0.9
        
    if ball.pos.z > wall_d.pos.z:
        ball.pos.z = wall_d.pos.z
        ball.vel.z *= -0.9
        
    if mag(ball.pos - boost_a.pos) < 1.0:
        print("WOOSH!")
        ball.vel = vector(-14.5, 0, -14.5)

def choice(L):
    """Implements Python's choice using the random() function."""
    length = len(L)              # Haal de lengte op
    random_index = int(length * random())  # Kies een willekeurige index
    return L[random_index]       # Geef dat element terug


def randint(low, hi):
    """Implements Python's randint using the random() function.
       returns an int from low to hi _inclusive_ (so, it's not 100% Pythonic)
    """
    if hi < low:
        low, hi = hi, low                   # Draai ze om als ze verkeerd om staan!
    length = int(hi) - int(low) + 1.        # Bereken het verschil en voeg 1 toe
    rand_value = length * random() + int(low)  # Kies een willekeurige waarde
    return int(rand_value)                  # Geef het integergedeelte terug


def randcolor():
    """Returns a vector of (r, g, b) random from 0.0 to 1.0."""
    r = random(0.0, 1.0)
    g = random(0.0, 1.0)
    b = random(0.0, 1.0)
    return vector(r, g, b)  # Een kleur is een tuple met drie elementen