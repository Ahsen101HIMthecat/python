# AHSEN KHAN
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
import time, sys, os, pygame
pygame.init()
# Audio
pygame.mixer.init()
# BGM
BGM = pygame.mixer.music.load('BGM.mp3')
# Play
pygame.mixer.music.play()

# COLORS
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE  = (20,20,255)
GREEN = (20,255,20)
WHITE_BG = (255, 255, 255) 

FPS = 60

# SPACESHIP SPEED
VLS = 8.4

# LAZER SPEED
VLR = 4.2

# SHIP DIMENSION
SHIPWIDTH , SHIPHEIGHT = 100, 90

# COLLISIONS
RHIT = pygame.USEREVENT + 2
LHIT = pygame.USEREVENT + 1


# Resolution + Header
WIDTH, HEIGHT = 1280, 780 # 1600 x 900 OR 1980 x 1080 too
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spacemen: The Endgame")
 
# DIVIDING BORDER
CENTREB = pygame.Rect(0, HEIGHT//2 - 5, WIDTH, 5.5)
# Border Color
CENTREBCOLOR = (0,0,0)

# icon and caption
iconimg = pygame.image.load("PygameIcon.png")
pygame.display.set_icon(iconimg)

# Background
BG = pygame.transform.scale(pygame.image.load("BG.png"),(WIDTH, HEIGHT)) 
# Assets -------------------------------------------------------------------------------------- Ships #

# Load Image + Resize
TSHIP = pygame.image.load("Z TOP.png")
TSHIPT = pygame.transform.scale(TSHIP, (SHIPWIDTH, SHIPHEIGHT))
TSHIPT = pygame.transform.rotate(TSHIPT,180)

# Load Image + Resize
BSHIP = pygame.image.load("Z BOT.png")
BSHIPB = pygame.transform.scale(BSHIP, (SHIPWIDTH, SHIPHEIGHT))
# No Need To Rotate :)

# Max Lazer
MAXLAZERS = 220
SHOOT = pygame.mixer.Sound("BOOM.wav")
SHOOT2 = pygame.mixer.Sound("BOOM2.wav")

# HEART DIMENSIONS (Not using anymore)
HEARTWIDTH, HEARTHEIGHT = 100,200

############################################
# HEARTS 
# BOTTOM SPACESHIP HEALTH [RIGHT/R1/BOTTOM]
BOT_100HP = pygame.image.load("100HP.png")
BOT_80HP = pygame.image.load("80HP.png")
BOT_60HP = pygame.image.load("60HP.png")
BOT_40HP = pygame.image.load("40HP.png")
BOT_20HP = pygame.image.load("20HP.png")
BOT_0HP = pygame.image.load("0HP.png")

# TOP SPACESHIP HEALTH [LEFT/L1/TOP]
TOP_100HP = pygame.image.load("100HP.png")
TOP_80HP = pygame.image.load("80HP.png")
TOP_60HP = pygame.image.load("60HP.png")
TOP_40HP = pygame.image.load("40HP.png")
TOP_20HP = pygame.image.load("20HP.png")
TOP_0HP = pygame.image.load("0HP.png")



# WIN IMAGES
BlueWin = pygame.image.load("TOPWINS.png")
PinkWin = pygame.image.load("BOTTOMWINS.png")

############################################################

# Drawing Window (Everything that's on the window)       
def window(R1, L1, RLazer, LLazer, TOP_HP, BOT_HP):
    
    # Default
    WIN.fill(WHITE_BG)
    
    # BG
    WIN.blit(BG, (0,0))
    
    # Border
    pygame.draw.rect(WIN, CENTREBCOLOR, CENTREB)
    
    # Top Ship
    WIN.blit(TSHIPT, (L1.x, L1.y))
    
    # Bottom Ship
    WIN.blit(BSHIPB, (R1.x, R1.y))
    
    # Hearts
   
    # TOP
    if TOP_HP >= 80:
        WIN.blit(TOP_100HP, (0, 0))
    elif TOP_HP >= 60:
        WIN.blit(TOP_80HP, (0, 0))
    elif TOP_HP >= 40:
        WIN.blit(TOP_60HP, (0, 0))
    elif TOP_HP >= 20:
        WIN.blit(TOP_40HP, (0, 0))
    elif TOP_HP > 0:
        WIN.blit(TOP_20HP, (0, 0))
    else:
        WIN.blit(TOP_0HP, (0, 0))
        
    # BOTTOM 
    if BOT_HP >= 80:
        WIN.blit(BOT_100HP, (0, HEIGHT - BOT_100HP.get_height()))
    elif BOT_HP >= 60:
        WIN.blit(BOT_80HP, (0, HEIGHT - BOT_80HP.get_height()))
    elif BOT_HP >= 40:
        WIN.blit(BOT_60HP, (0, HEIGHT - BOT_60HP.get_height()))
    elif BOT_HP >= 20:
        WIN.blit(BOT_40HP, (0, HEIGHT - BOT_40HP.get_height()))
    elif BOT_HP > 0:
        WIN.blit(BOT_20HP, (0, HEIGHT - BOT_20HP.get_height()))
    else:
        WIN.blit(BOT_0HP, (0, HEIGHT - BOT_0HP.get_height()))
        


    
    # Drawing Lazers
    for Lazer in RLazer:
        pygame.draw.rect(WIN, GREEN, Lazer)
        
    for Lazer in LLazer:
        pygame.draw.rect(WIN, BLUE, Lazer)


    pygame.display.update()
    
def winner(win): 
            win = pygame.transform.scale(win,(600,600)) 
            WIN.blit(win, (WIDTH//2 - win.get_width()//2, HEIGHT//2 - win.get_height()//2))   
            pygame.display.update()
            pygame.time.delay(5000)
            launcher()

# TOP SHIP
def topmoveL1(pressedkey, L1):
    # BLUE (TOP SPACESHIP)
    if pressedkey[pygame.K_a] and L1.x - VLS > 0: # Left 
        L1.x -= VLS
    if pressedkey[pygame.K_d] and L1.x + VLS + L1.width < WIDTH: # Right
        L1.x += VLS

    if pressedkey[pygame.K_w] and L1.y - VLS > 0: # Forward
        L1.y -= VLS
    if pressedkey[pygame.K_s] and L1.y + VLS + L1.height < CENTREB.y: # Back
        L1.y += VLS
        
# BOTTOM SHIP           
def bottommoveR1(pressedkey, R1):
        # (BOTTOM SPACESHIP)
        if pressedkey[pygame.K_LEFT] and R1.x - VLS > 0: # Left  
            R1.x -= VLS
        if pressedkey[pygame.K_RIGHT] and R1.x + VLS + R1.width < WIDTH: # Right
            R1.x += VLS
        if pressedkey[pygame.K_DOWN] and R1.y + VLS + SHIPHEIGHT < HEIGHT: # Back 
            R1.y += VLS
        if pressedkey[pygame.K_UP] and R1.y - VLS + 8.2 > CENTREB.y:# Forward
            R1.y -= VLS
            
def ManageLazers(lLazer, rLazer, LShip, RShip):
    # Manage Lazers (Lazers moving)
    for Lazer in lLazer:
        Lazer.y += VLR
        if Lazer.colliderect(RShip):
            pygame.event.post(pygame.event.Event(RHIT))
            lLazer.remove(Lazer)
        elif Lazer.y < 0:
            lLazer.remove(Lazer)

    for Lazer in rLazer:
        Lazer.y -= VLR
        if Lazer.colliderect(LShip):
            pygame.event.post(pygame.event.Event(LHIT))
            rLazer.remove(Lazer)
        elif Lazer.y > HEIGHT:
            rLazer.remove(Lazer)


# Main Game Launcher (Contains FPS/Lazers/Health/)
def launcher():
    R1 = pygame.Rect(550, 600, SHIPWIDTH, SHIPHEIGHT)
    L1 = pygame.Rect(850, 100, SHIPWIDTH, SHIPHEIGHT)
    
    TOP_HP = 100
    BOT_HP = 100
    RLazer = []
    LLazer = []
    
    clock = pygame.time.Clock()
    
    run = True
    while run:
        
 
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and len(LLazer) < MAXLAZERS: 
                    Lazer = pygame.Rect(L1.x + L1.width//2 - 5, L1.y + L1.height, 13, 9.1) # LAZER DIMENSIONS
                    pygame.mixer.Sound.play(SHOOT)
                    LLazer.append(Lazer)              
                if event.key == pygame.K_PAGEDOWN and len(RLazer) < MAXLAZERS:
                    Lazer = pygame.Rect(R1.x + R1.width//2 - 5, R1.y - R1.height, 13, 9.1)
                    RLazer.append(Lazer)
                    pygame.mixer.Sound.play(SHOOT2)
                    
                    
            # TOP SPACESHIP HIT [HEALTH SYSTEM]       
            if event.type == LHIT: # TOP 
                TOP_HP -= 20  # Decrease health by 20
                if TOP_HP < 0:
                    TOP_HP = 0  # Ensure health doesn't go below 0
                    break 
                    
            if event.type == RHIT: # BOTTOM
                BOT_HP -= 20  # Decrease health by 20
                if BOT_HP < 0:
                    BOT_HP = 0  # Ensure health doesn't go below 0

                    break
                print("LOW HIT!")
    
        pressedkey = pygame.key.get_pressed()
        topmoveL1(pressedkey, L1)
        bottommoveR1(pressedkey, R1)
        
        # Move lasers
        for Lazer in RLazer:
            Lazer.y -= VLR
            if Lazer.bottom > HEIGHT:
                RLazer.remove(Lazer)
                
        for Lazer in LLazer:
            Lazer.y += VLR
            if Lazer.top < 0:
                LLazer.remove(Lazer)
        ManageLazers(LLazer, RLazer, L1, R1)
        window(R1,L1, LLazer, RLazer, TOP_HP, BOT_HP)    
        if BOT_HP <= 0:
            winner(BlueWin)
        
        if TOP_HP <= 0:
            winner(PinkWin)
    
    pygame.quit()
    
# Final                      
if __name__ == "__main__":

    launcher()   
    print("\033c")
    print("Thanks For Playing!")
    
# Credits to Himanish for helping 