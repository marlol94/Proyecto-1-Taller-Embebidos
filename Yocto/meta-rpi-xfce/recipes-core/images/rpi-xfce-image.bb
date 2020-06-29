LICENSE = "MIT"

# Base this image on rpi-basic-image
require recipes-core/images/core-image-base.bb

IMAGE_LINGUAS = "en-us"

COMPATIBLE_MACHINE = "^rpi$"

IMAGE_INSTALL_append += " \
  wpa-supplicant \
  hostapd \
  dnsmasq \
  iptables \
  ntp \
  nano \
  crda \
  iw \
"

IMAGE_INSTALL = "packagegroup-core-boot \
    packagegroup-core-x11 \
    packagegroup-xfce-base \
    kernel-modules \
    linux-firmware-rpidistro-bcm43455 \
    linux-firmware-bcm43455 \
"
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
  python-modules \
  python3-modules \
  git \
  wget \
  apt \
"

inherit distro_features_check
REQUIRED_DISTRO_FEATURES = "x11"


