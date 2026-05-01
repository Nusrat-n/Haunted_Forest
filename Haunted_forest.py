from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math

eyeX, eyeY, eyeZ = 0, 2, 12
angle = 0.0
clash = False 


ghostX, ghostZ = 0.0, -5.0

def init():
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
    
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glLightfv(GL_LIGHT0, GL_POSITION, [5, 10, 5, 1])
    
    glEnable(GL_FOG)
    glFogfv(GL_FOG_COLOR, [0.1, 0.1, 0.1, 1.0])
    glFogf(GL_FOG_DENSITY, 0.15)
    glFogi(GL_FOG_MODE, GL_EXP2)

def checkCollision():
    global eyeX, eyeZ, ghostX, ghostZ, clash
    distance = math.sqrt((eyeX - ghostX)**2 + (eyeZ - ghostZ)**2)
    if distance < 2.5: 
        clash = True
    else:
        clash = False

def draw_tree(x, z):
    
    glPushMatrix()
    glTranslatef(x, 0, z)
    
    
    if clash:
        glColor3f(0.5, 0.0, 0.0) 
    else:
        glColor3f(0.2, 0.1, 0.0) 
        
    glRotatef(-90, 1, 0, 0)
    glutSolidCone(0.5, 4, 10, 10)
    
   
    glTranslatef(0, 0, 2)
    if clash:
        glColor4f(0.4, 0.0, 0.0, 0.8) 
    else:
        
        glColor4f(0.0, 0.4, 0.1, 0.7) 
        
    glutSolidSphere(1.5, 10, 10)
    glPopMatrix()

def draw_environment():
    
    if clash: glColor3f(0.2, 0.0, 0.0)
    else: glColor3f(0.05, 0.1, 0.05)
    
    glBegin(GL_QUADS)
    glVertex3f(-50, 0, -50); glVertex3f(50, 0, -50)
    glVertex3f(50, 0, 50); glVertex3f(-50, 0, 50)
    glEnd()

    
    for i in range(-25, 25, 6):
        for j in range(-30, 10, 7):
           
            if abs(i - ghostX) > 2 or abs(j - ghostZ) > 2:
                draw_tree(i, j)

def display():
    global eyeX, eyeY, eyeZ, angle, clash
    checkCollision()
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    if clash: glClearColor(0.2, 0, 0, 1)
    else: glClearColor(0.05, 0.05, 0.05, 1)
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, 1.0, 0.1, 100)
    
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    lookX = eyeX + math.sin(angle)
    lookZ = eyeZ - math.cos(angle)
    gluLookAt(eyeX, eyeY, eyeZ, lookX, eyeY, lookZ, 0, 1, 0)

    draw_environment()
    
   
    t = glutGet(GLUT_ELAPSED_TIME) / 1000.0
    glPushMatrix()
    glTranslatef(ghostX, 2 + math.sin(t*2), ghostZ)
    if clash: glColor4f(1, 0, 0, 0.9)
    else: glColor4f(1, 1, 1, 0.5)
    glutSolidSphere(0.8, 20, 20)
    glPopMatrix()

    glutSwapBuffers()

def move_camera(key, x, y):
    global eyeX, eyeZ, angle
    fraction = 0.5
    if key == b'w' or key == GLUT_KEY_UP:
        eyeX += math.sin(angle) * fraction
        eyeZ -= math.cos(angle) * fraction
    elif key == b's' or key == GLUT_KEY_DOWN:
        eyeX -= math.sin(angle) * fraction
        eyeZ += math.cos(angle) * fraction
    elif key == b'a' or key == GLUT_KEY_LEFT:
        angle -= 0.1
    elif key == b'd' or key == GLUT_KEY_RIGHT:
        angle += 0.1
    glutPostRedisplay()


glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize(900, 700)
glutCreateWindow(b"Haunted Forest")
init()
glutDisplayFunc(display)
glutIdleFunc(display)
glutKeyboardFunc(move_camera)
glutSpecialFunc(move_camera)
glutMainLoop()