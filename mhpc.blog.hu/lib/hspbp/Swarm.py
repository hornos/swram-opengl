# TAB: 2SPACE
import sys
from random import gauss, random
from math import sqrt


class Vector():
  def __str__(self):
    vp = lambda x: x / self.viewport
    return '%12.9f %12.9f %12.9f' % ( vp( self.x ), vp( self.y ), vp( self.z ) )
  # end def

  def __init__( self, x = 0, y = 0, z = 0, vp = 100 ):
    self.viewport = vp
    self.x = x
    self.y = y
    self.z = z
  # end def

  def dist( self, other = None ):
    p2 = lambda x: x * x
    if not other:
      other = Vector()
    # end if
    return sqrt( p2( self.x - other.x ) +
                 p2( self.y - other.y ) +
                 p2( self.z - other.z ) )
  # end def

  def norm( self, d = 0, c = 0 ):
    cpd = lambda x: x * c / d
    # TODO: epsilon ?
    if not d == 0:
      self.x = cpd( self.x )
      self.y = cpd( self.y )
      self.z = cpd( self.z )
    # end def
    return self
  # end def

  def grav( self, other = None, d = 0, c = 0 ):
    g = lambda x: x * c / ( d * d * d * d )
    return Vector( g( self.x - other.x ),
                   g( self.y - other.y ),
                   g( self.z - other.z ) )
  # end def

  def add( self, other = None ):
    self.x += other.x
    self.y += other.y
    self.z += other.z
  # def
# end class


class Agent:
  def __str__( self ):
    return "%s %s" % ( str( self.pos ), self.species )
  # end def

  def __init__( self, parent = None, m = 1.0, s = 0.05 ):
    self.gms = gauss( self.mu, self.si )
    ga = lambda x: x * self.gms

    # set species defaults
    self.default()
    if parent:
      # handle mutations
      self.speed      = ga( parent.speed )
      self.matingZone = ga( parent.matingZone )
      self.eatingZone = ga( parent.eatingZone )
      self.hunger     = ga( parent.hunger * self.speed )
      self.nutrition  = dict( [ ( key, ga( value ) ) 
                                for ( key, value ) 
                                in parent.nutrition.items() ] )
    # end if
  # end def

  def move( self, swarm = None, world = None, m = 0.3 ):
    self.mortality = m
    p2 = lambda x: x * x
    if self.vitality <= 0.0:
      return
    # end if

    v = Vector()
    p = self.pos
    vital = lambda x: x / self.vitality
    for agent in swarm:
      d = self.pos.dist( agent.pos )
      # calculate vector of next move
      for zone in self.zones[agent.species]:
        if vital( zone['min'] ) < d <= vital( zone['max'] ):
          v.add( p.grav( agent.pos, d, zone['c'] ) )
        # end if
      # end for

      # handle health
      if agent.species == self.prey and d < self.eatingZone \
                                    and agent.vitality > 0.0:
        # do damage/nutrition
        # how much we bite?
        c = ( 1.0 - ( d / self.eatingZone ) )
        self.vitality  += c * self.nutrition[agent.species]
        agent.vitality += c * agent.nutrition[self.species]
      elif agent.species == self.species and self.vitality >= 1 \
                                         and d < self.matingZone:
        # try to breed
        # how much we the chance we breed?
        c = ( 1.0 - ( d / self.matingZone ) )
        if( random() < c * p2( self.vitality ) ):
          world.swarm[self.species].append( self.breed() )
          self.vitality = 1.0 - self.mortality
        # end if
      # end if

      if self.vitality > 2.0:
        # glutony results in emptying everything
        self.vitality = 0.5
      else:
        self.vitality += self.hunger
      # end if
    # end for

    max_move = v.norm( v.dist(), ( 0.5 + self.vitality / 2 ) * self.speed )
    if v.dist() > max_move.dist():
      self.pos.add( max_move )
    else:
      self.pos.add( v )
    # end if
  # end class


class World():
  def __str__( self ):
    return '\n' . join( map( str, self.living() ) ) + '\n'
  # end def

  def __init__( self, swarm = None ):
    self.swarm = [ [ specie() for i in range( pop ) ] for specie, pop in swarm ]
  # end def

  def living( self ):
    return ( agent for species in self.swarm for agent in species if agent.vitality > 0 )
  # end def

  def nextFrame(self):
    for a in self.living():
      a.move( self.living(), self )
    # end def
  # en def

  def run( self ):
    i = 0
    while True:
      print self
      if i % 50 == 0:
        counts = [ len( [ 1 for agent in species if agent.vitality > 0 ] ) 
                   for species in self.swarm ]
        sys.stderr.write( "i = %d counts = %s\n" % ( i, counts ) )
        if 1 in counts:
          sys.exit( 0 )
        # end if
      # end if
      i += 1
      self.nextFrame()
    # end while
  # end def
# end class


class Fish( Agent ):
  def __init__( self ):
    self.species    = 0
    self.speed      = 3
    self.vitality   = 0.7
    self.pos        = Vector( ( random() - 0.5 ) * 2000,
                              ( random() - 0.5 ) * 2000,
                              ( random() - 0.5 ) * 2000 )
    self.zones      = [ [ { 'min': 0,  'max': 20,   'c': 100 },
                          { 'min': 50, 'max': 200,  'c': -1000 } ],
                        [ { 'min': 0,  'max': 700,  'c': 5000 } ],
                        [ { 'min': 0,  'max': 1000, 'c': -15000 } ] ]
    self.matingZone = 30
    self.eatingZone = 40
    self.prey       = 2
    self.nutrition  = { 1: -0.1, 2: 0.033 }
    self.hunger     = -0.000001
  # end def

  def breed( self ):
    return Fish()
  # end def
# end class


class Shark( Agent ):
  def __init__( self ):
    self.species    = 1
    self.speed      = 6
    self.vitality   = 0.8
    self.pos        = Vector( ( random() - 0.5 ) * 2000,
                              ( random() - 0.5 ) * 2000,
                              ( random() - 0.5 ) * 2000 )
    self.zones      = [ [ { 'min': 0,   'max': 600, 'c': -1200 } ],
                        [ { 'min': 0,   'max': 100, 'c': 10 },
                          { 'min': 200, 'max': 800, 'c': -1000 } ],
                        [ { 'min': 0,   'max': 140, 'c': 800 } ] ]
    self.matingZone = 40
    self.eatingZone = 20
    self.prey       = 0
    self.nutrition  = { 0: 0.005, 2: -0.0045 }
    self.hunger     = -0.0000001
  # end def

  def breed( self ):
    return Shark()
  # end def
# end class


class Plankton( Agent ):
  def __init__( self ):
    self.species    = 2
    self.speed      = 0.1
    self.vitality   = 0.5
    self.pos        = Vector( ( random() - 0.5 ) * 2000,
                              ( random() - 0.5 ) * 2000,
                              ( random() - 0.5 ) * 2000 )
    self.zones      = [ [ { 'min': 0, 'max': 5,    'c': 1000 } ],
                        [ { 'min': 0, 'max': 1000, 'c': -10000 } ],
                        [ { 'min': 0, 'max': 380,  'c': 50000 } ] ]
    self.matingZone = 400
    self.eatingZone = 100
    self.prey       = 1
    self.nutrition  = { 0: -0.12, 1: 0.33 }
    self.hunger     = -0.000001
  # end def

  def breed( self ):
    return Plankton()
  # end def
# end class
