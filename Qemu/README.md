Aqui irán archivos del qemu configuracion entre otros

En el Local Config; 

MACHINE ?= "qemuarm64"

Revisar los directorios de: 
  Downloads (DL_DIR)
  sstate (SSTATE_DIR)
  Tmp (TMPDIR)
  
Incluir todos los paquetes Linux: 
  PACKAGE_CLASSES ?= "package_rpm package_deb package_ipk"
  
Agregar: 

  LICENSE_FLAGS_WHITELIST = "commercial"

#OpenCV
IMAGE_INSTALL_append += " \
  opencv \
  ffmpeg \
"
#----------------------------------------------------------------------------------------------------------------
#ssh
IMAGE_INSTALL_append += " \
  openssh \
"
#-----------------------------------------------------------------------------------------------------------------
#toolbox
IMAGE_INSTALL_append += " \
  nano \
  python-modules \
  python3-modules \
  git \
  wget \
  apt \
