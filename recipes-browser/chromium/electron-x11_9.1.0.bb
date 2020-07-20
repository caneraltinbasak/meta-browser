require electron-gn.inc
require electron-source.inc

inherit features_check

REQUIRED_DISTRO_FEATURES = "x11"

DEPENDS += "\
        libnotify \
        libx11 \
        libxcomposite \
        libxcursor \
        libxdamage \
        libxext \
        libxfixes \
        libxi \
        libxrandr \
        libxrender \
        libxscrnsaver \
        libxtst \
"
GN_ARGS_append='import("//electron/build/args/release.gn")'
