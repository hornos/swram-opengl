#
# Types package
#

import sys
import copy
import string
import numpy
from numpy import linalg

class Enum( object ):
  def __init__( self, elist ):
    for num, name in enumerate( elist.split() ) :
      setattr( self, name, num )
    # end for
  # end def
# end class


PT  = Enum( 'Direct Cart' )
PTD = { PT.Direct : 'Direct', PT.Cart : 'Cart' }
IOT = Enum( 'Input Output' )


def TF( logical ):
  if logical:
    return 'T'
  return 'F'
# end def


class Debug:
  def __init__( self, sysopts = { "verbose" : False, "debug" : False } ):
    self.verbose = sysopts["verbose"]
    self.debug   = sysopts["debug"]
  # end def
# end class


class Buffer:
  def __init__( self ):
    self.lc    = -1
    self.line  = ""
    self.lines = {} 
  # end def

  def clean( self ):
    self.lc = -1
    self.lines = {}
  # end def

  def rewind( self ):
    self.lc = -1
  # end def

  def read( self, lines = None ):
    self.clean()
    for line in lines:
      self.lc += 1
      self.lines[self.lc] = line.strip()
    # end for
    self.rewind()
  # end def

  def getline( self ):
    self.lc += 1
    self.line = self.lines[self.lc]
    return self.line
  # end def

  def putline( self, line = None ):
    self.lc += 1
    self.line = line
    self.lines[self.lc] = self.line
  # end def
# end class


class VecPos:
  def __init__( self, vec = numpy.zeros( 3 ), moveable = None ):
    self.position  = numpy.array( vec )
    self.force     = numpy.zeros( 3 )
    self.velocity  = numpy.zeros( 3 )
    self.moveable  = []
    if( moveable == None ):
      for i in range(0,3):
        self.moveable.append( True )
      # end for
    else:
      for m in moveable:
        if string.upper( m ) == 'T':
          self.moveable.append( True )
        else:
          self.moveable.append( False )
        # end if
      # end for
    # end if
  # end def
# end class


class AtomPos(VecPos):
  def __init__( self,  symbol = "", no = 0, cl_shift = 0.000, 
                vec = numpy.zeros( 3 ), moveable = None ):
    VecPos.__init__( self, vec, moveable )
    self.symbol = symbol
    # not the atomic number !
    self.no  = no
    self.rno = no
    self.cl_shift = cl_shift
  # end def

  def info( self ):
    print " %4d" % self.no, "%2s" % self.symbol, self.position, self.moveable
  # end def

  def move( self, S = numpy.zeros( 3 ) ):
    for i in range( 0, 3 ):
      self.position[i] += S[i]
    # end for
  # end def
# end class


class Vector:
  def __init__(self, tail = numpy.zeros(3), head = numpy.array([1,1,1])):
    self.tail = tail
    self.head = head
  # end def

  def vert(self):
    return [self.tail, self.head]
  # end def
  
  def nv(self):
    r = numpy.subtract( self.head, self.tail )
    n = numpy.linalg.norm(r)
    return numpy.dot( r, 1.0 / n )
  
  def rm(self, ax = numpy.array([1,0,0])):
    # A = ( U X^T ) inv( X X^T )
    XXT = numpy.linalg.inv( numpy.kron( ax, ax ).reshape(3,3))
    UXT = numpy.kron(self.nv(),ax).reshape(3,3)
    print XXT,UXT
  # end def
# end class