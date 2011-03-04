#!/usr/bin/env python
#f3--&7-9-V13------21-------------------42--------------------64------72
### HEADER
import os
import sys
sys.path.append( os.path.dirname( sys.argv[0] ) + "/../lib" )

### IMPORTS
from pypak.Script import *
from hsbp.Swarm import *

### Program
class Program( Script ):
  def __init__( self ):
    Script.__init__( self )
    self.ini()
  # end def __init__

  def main( self ):
    (options, args) = self.par()

    Swarm = [ ( Fish,     self.cfgi( "Fish" ) ),
              ( Shark,    self.cfgi( "Shark" ) ),
              ( Plankton, self.cfgi( "Plankton" ) ) ]

    w = World( Swarm )
    w.run()
  # end def
# end class


if __name__ == '__main__':
  p = Program()
  p.main()
# end if
