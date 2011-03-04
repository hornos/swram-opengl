include arch.make

# pyopengl
PGL_URL=http://sourceforge.net/projects/pyopengl/files/PyOpenGL/3.0.1/PyOpenGL-3.0.1.tar.gz/download
PGL_TGZ=pyopengl.tgz

# PIL
PIL_URL=http://effbot.org/downloads/Imaging-1.1.7.tar.gz
PIL_TGZ=pil.tgz

.PHONY: all gl pil

all: gl pil

gl:
	if ! test -d ./OpenGL; then \
	  if ! test -f $(PGL_TGZ); then \
	    $(DL) -O $(PGL_TGZ) $(PGL_URL); \
	  fi; \
	  $(TAR) xvzf $(PGL_TGZ); \
	  mv ./PyOpenGL-* ./PyOpenGL.src; \
	  cd ./PyOpenGL.src; MACOSX_DEPLOYMENT_TARGET=$(TARGET) ARCHFLAGS=$(ARCH) python setup.py build; \
	  cd ..; ln -s ./PyOpenGL.src/OpenGL ./OpenGL; \
	fi;

pil:
	if ! test -d ./PIL; then \
	  if ! test -f $(PIL_TGZ); then \
	    $(DL) -O $(PIL_TGZ) $(PIL_URL); \
	  fi; \
	  $(TAR) xvzf $(PIL_TGZ); \
	  mv ./Imaging-* ./pil.src; \
	  cd ./pil.src; MACOSX_DEPLOYMENT_TARGET=$(TARGET) ARCHFLAGS=$(ARCH) python setup.py build; \
	  cd ..; ln -s ./pil.src/PIL ./PIL; \
	fi;

clean:
	rm -fR ./PyOpenGL.src
	rm -fR ./pil.src
	rm -fR ./pc.src
	rm *.tar.gz *.tgz PIL OpenGL
