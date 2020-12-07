# import necessary libraries
import pygame
import numpy as np
import time

# init pygame and set title
pygame.init()
pygame.display.set_caption('Sudoku')


# set screen size
screen=pygame.display.set_mode((470,470))

# get clock and font control
clock=pygame.time.Clock()
font = pygame.font.SysFont('Arial', 25)

# boolean variables
running=True
solving=False

# initialise size of cell and margin
size=50
margin=2


# create an array of zeros
puzzle=np.zeros((9,9))
puzzle=puzzle.astype('int32')


# function that returns valid number to specified cell
def check(value,row,column):
    global puzzle
    if(value>9):
        return False,value
    elif((value in puzzle[row,:] or value in puzzle[:,column] or value in puzzle[int(row/3)*3:int(row/3)*3+3,int(column/3)*3:int(column/3)*3+3]) and value<=9):
        return check(value+1,row,column)
    else:
        return True,value


# initaialise stack and selected variables
selected=()
stack=[]

try:
    # inifinte loop
    while(running):
        # filling gray color on screen
        screen.fill((150,150,150))
        
        # listening to events
        for event in pygame.event.get():

            # if close button is pressed
            if(event.type==pygame.QUIT):
                running=False

            # if mouse is clicked on a cell
            elif(event.type == pygame.MOUSEBUTTONDOWN and not solving):
                pos = pygame.mouse.get_pos()
                selected=(pos[0]-2*pos[0]//50)//50,(pos[1]-pos[1]//50*2)//50

            # if keyboard keys are clicked
            elif(event.type == pygame.KEYDOWN and not solving):

                # if RETURN
                if(event.key == pygame.K_RETURN):
                    print("solve")
                    selected=()
                    solving=True

                # if numbers
                elif(pygame.key.name(event.key)[1] in ['1','2','3','4','5','6','7','8','9'] and len(selected)!=0):
                    puzzle[selected[1]][selected[0]]=int(pygame.key.name(event.key)[1])
                
                # if backspace
                elif(event.key == pygame.K_BACKSPACE):
                    puzzle[selected[1]][selected[0]]=0

                # if arrow up
                elif(event.key == pygame.K_UP):
                    if(len(selected) and selected[1]!=0):
                        selected=(selected[0],selected[1]-1)
                
                # if arrow down
                elif(event.key == pygame.K_DOWN):
                    if(len(selected) and selected[1]!=8):
                        selected=(selected[0],selected[1]+1)

                # if arrow left
                elif(event.key == pygame.K_LEFT):
                    if(len(selected) and selected[0]!=0):
                        selected=(selected[0]-1,selected[1])

                # if arrow right
                elif(event.key == pygame.K_RIGHT):
                    if(len(selected) and selected[0]!=8):
                        selected=(selected[0]+1,selected[1])

        # if not solving listen for entering values
        if(not solving):
            for i in range(9):
                for j in range(9):
                    color=(255,255,255)
                    if((j,i)==selected):
                        # color=(250,250,143)
                        color=(255,178,102)
                    rect=pygame.Rect(j*(size+margin)+margin,i*(size+margin)+margin,size,size)
                    pygame.draw.rect(screen,color,rect)
                    screen.blit(font.render(str(puzzle[i,j]) if puzzle[i,j]!=0 else '', True, (0,0,0)), (j*(size+margin)+20,i*(size+margin)+10))

                    if((i)%3==0 and i!=0):
                        pygame.draw.line(screen, (0,0,0), (i*(size+margin), 0), (i*(size+margin), 470),2)
                    if((j)%3==0 and j!=0):
                        pygame.draw.line(screen, (0,0,0), (0,j*(size+margin)), (470,j*(size+margin)),2)

        # else solve
        else:
            i=0
            while(i<9):
                j=0
                while(j<9):
                    selected=(i,j)
                    try:
                        value=value if(value!=1) else 1
                    except:
                        value=1

                    if(puzzle[i,j]==0):
                        result=check(value=value,row=i,column=j)
                        if(result[0]):
                            puzzle[i,j]=result[1]
                            stack.append([i,j])
                            value=1
                        else:
                            item=stack.pop()
                            puzzle[i,j]=0
                            i=item[0]
                            j=item[1]
                            value=puzzle[i,j]+1
                            puzzle[i,j]=0
                            continue
                    for k in range(9):
                        for l in range(9):
                            color=(255,255,255)
                            if((k,l)==selected):
                                # color=(250,250,143)
                                color=(255,178,102)
                            rect=pygame.Rect(l*(size+margin)+margin,k*(size+margin)+margin,size,size)
                            pygame.draw.rect(screen,color,rect)
                            screen.blit(font.render(str(puzzle[k,l]) if puzzle[k,l]!=0 else '', True, (0,0,0)), (l*(size+margin)+20,k*(size+margin)+10))
                            if((k)%3==0 and k!=0):
                                pygame.draw.line(screen, (0,0,0), (k*(size+margin), 0), (k*(size+margin), 470),2)
                            if((l)%3==0 and l!=0):
                                pygame.draw.line(screen, (0,0,0), (0,l*(size+margin)), (470,l*(size+margin)),2)

                    # print(puzzle)
                    pygame.display.flip()

                    # delay of 100ms
                    time.sleep(0.1)

                    j+=1
                i+=1
            solving=False
        pygame.display.flip()

        # limit fps to 24
        clock.tick(24)
        

except Exception as e:
    print(e)


# quit pygame
pygame.quit()