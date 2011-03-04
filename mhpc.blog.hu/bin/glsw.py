#!/usr/bin/env python
#f3--&7-9-V13------21-------------------42--------------------64------72
### HEADER
import os
import sys
sys.path.append( os.path.dirname( sys.argv[0] ) + "/../lib" )

### IMPORTS
import PIL.Image as Image
import itertools
from threading import Thread, Lock, Event
from time import sleep
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


Colors=[(1,1,1),(1,0,0),(0,1,0)]
counter=itertools.count()
dumpFrames=False

class Camera:
	zoom = 1.0
	pos = [20, 20, 20]
	up = [0, 1, 0 ]
	center = [0, 0, 0]
	rotation = [0, 0, 0]

class SwarmEntity:
	def __init__(self, line):
		parts = line.split()
		self.x = float(parts[0])
		self.y = float(parts[1])
		self.z = float(parts[2])
		self.race = int(parts[3])

class Reader(Thread):
	lock = Lock()
	changed = Event()
	swarm_entities = []
	paused=False
	def run(self):
		print 'Waithing for data on stdin'
		while True:
			while Reader.paused:
				sleep(0.1)
			try:
				self.read_entities()
			except:
				break

	def read_entities(self):
		entities = []
		line = sys.stdin.readline()
		if not line:
			raise Exception()
		while line:
			if line.startswith('done'):
				sleep(0.1)
				break
			if line.startswith('exit'):
				sys.exit(0)
			try:
				entities.append(SwarmEntity(line.strip()))
			except:
				print 'Invalid line: %s' % line.strip()
			line = sys.stdin.readline()
		self.done(entities)

	def done(self, entities):
		print 'Updating view'
		Reader.lock.acquire()
		Reader.swarm_entities = entities
		Reader.lock.release()
		Reader.changed.set()

def idle():
	if Reader.changed.isSet():
		Reader.changed.clear()
		glutPostRedisplay()

def display():
	glLoadIdentity()
	dist = 20.0 / Camera.zoom
	gluLookAt(Camera.pos[0], Camera.pos[1], Camera.pos[2],
				 Camera.center[0], Camera.center[1], Camera.center[2],
				 Camera.up[0], Camera.up[1], Camera.up[2])
	glRotatef(Camera.rotation[0], 1, 0, 0);
	glRotatef(Camera.rotation[1], 0, 1, 0);
	glRotatef(Camera.rotation[2], 0, 0, 1);
	axis()
	mySphere = gluNewQuadric()
	gluQuadricDrawStyle(mySphere, GLU_LINE)

	Reader.lock.acquire()
	for entity in Reader.swarm_entities:
		glPushMatrix()
		r,g,b=Colors[entity.race]
		glColor3f(r,g,b)
		glTranslatef(entity.x, entity.y, entity.z)
		gluSphere(mySphere, 0.015, 12, 12)
		glPopMatrix()
	Reader.lock.release()

	if dumpFrames:
		frame = glReadPixels( 0,0, 1280, 700, GL_RGBA, GL_UNSIGNED_BYTE)
		im = Image.frombuffer("RGBA", (1280,700), frame, "raw", "RGBA", 0, 0)
		im.save("frames/frame%08d.png" % counter.next())

	glFlush()

def axis():
	glClear(GL_COLOR_BUFFER_BIT)

	glBegin(GL_LINES)
	glColor3f(0.3, 0.3, 0.3)
	glVertex3f(-10.0, 0.0, 0.0)
	glVertex3f(10.0, 0.0, 0.0)
	glVertex3f(0.0, -10.0, 0.0)
	glVertex3f(0.0, 10.0, 0.0)
	glVertex3f(0.0, 0.0, -10.0)
	glVertex3f(0.0, 0.0, 10.0)
	glEnd()

	biggest = 10
	x = 88
	y = 89
	z = 90
	r = range (0, (biggest + 1))
	for i in r:
		ascii = 48+i

		# x axis positive
		glRasterPos3f(i, 0.0, 0.0)
		glColor3f(0.3, 0.3, 0.3)
		if i == biggest:
			glutBitmapCharacter(GLUT_BITMAP_8_BY_13, x)
		else:
			glutBitmapCharacter(GLUT_BITMAP_8_BY_13, ascii)
		# x axis negative
		glRasterPos3f(-i, 0.0, 0.0)
		glColor3f(0.5, 0.0, 0.0)
		if i == biggest:
			glutBitmapCharacter(GLUT_BITMAP_8_BY_13, x)
		else:
			glutBitmapCharacter(GLUT_BITMAP_8_BY_13, ascii)

		# y axis positive
		glRasterPos3f(0.0, i, 0.0)
		glColor3f(0.3, 0.3, 0.3)
		if i == biggest:
			glutBitmapCharacter(GLUT_BITMAP_8_BY_13, y)
		else:
			glutBitmapCharacter(GLUT_BITMAP_8_BY_13, ascii)
		# x axis negative
		glRasterPos3f(0.0, -i, 0.0)
		glColor3f(0.5, 0.0, 0.0)
		if i == biggest:
			glutBitmapCharacter(GLUT_BITMAP_8_BY_13, y)
		else:
			glutBitmapCharacter(GLUT_BITMAP_8_BY_13, ascii)

		# z axis positive
		glRasterPos3f(0.0, 0.0, i)
		glColor3f(0.3, 0.3, 0.3)
		if i == biggest:
			glutBitmapCharacter(GLUT_BITMAP_8_BY_13, z)
		else:
			glutBitmapCharacter(GLUT_BITMAP_8_BY_13, ascii)
		# z axis negative
		glRasterPos3f(0.0, 0.0, -i)
		glColor3f(0.5, 0.0, 0.0)
		if i == biggest:
			glutBitmapCharacter(GLUT_BITMAP_8_BY_13, z)
		else:
			glutBitmapCharacter(GLUT_BITMAP_8_BY_13, ascii)

	glFlush()

def init():
	glClearColor(0.0, 0.0, 0.0, 0.0)
	glColor3f(0.0, 0.0, 0.0)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(30, 1.0, 0.0, 1.0)
	glMatrixMode(GL_MODELVIEW)

def mykeyb(key, x, y):
	if key == '+':
		Camera.zoom *= 1.2
	elif key == '-':
		Camera.zoom /= 1.2
	elif key== 'q':
		sys.exit(0);
	elif key=='w':
		Camera.pos[0] -= 0.5
		Camera.pos[1] -= 0.5
		Camera.pos[2] -= 0.5
	elif key=='s':
		Camera.pos[0] += 0.5
		Camera.pos[1] += 0.5
		Camera.pos[2] += 0.5
	elif key=='a':
		Camera.rotation[1] -= 1
	elif key=='d':
		Camera.rotation[1] += 1
	elif key=='z':
		Camera.rotation[2] -= 1
	elif key=='x':
		Camera.rotation[2] += 1
	elif key==' ':
		Reader.paused=not Reader.paused
	else:
		return
	glutPostRedisplay()

def mymouse(but, stat, x, y):
	if stat == GLUT_DOWN:
		if but == GLUT_LEFT_BUTTON:
			print x, y, "Press right button to exit"
		else:
			sys.exit()

glutInit(sys.argv)
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
glutInitWindowSize(500, 500)
glutInitWindowPosition(0, 0)
glutCreateWindow('Swarm visualization')
glutDisplayFunc(display)
glutKeyboardFunc(mykeyb)
glutMouseFunc(mymouse)
glutIdleFunc(idle)

init()

if '--dumpFrames' in sys.argv:
	dumpFrames=True

rdr = Reader()
rdr.start()
glutMainLoop()
