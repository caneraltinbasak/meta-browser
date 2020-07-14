require electron-gn.inc
require electron-source.inc

DEPENDS += "\
        libnotify \
        at-spi2-atk \
        libxkbcommon \
        virtual/egl \
        ${@bb.utils.contains('DISTRO_FEATURES', 'wayland', 'wayland wayland-native gtk+3', '', d)} \
        ${@bb.utils.contains('DISTRO_FEATURES', 'x11', 'libx11 libxcomposite libxcursor libxdamage libxext libxfixes libxi libxrandr libxrender libxscrnsaver libxtst gtk+3', '', d)} \
"

RRECOMMENDS_${PN} += " \
        ttf-bitstream-vera \
"

WAYLAND_GN_ARGS = " \
        ozone_platform_wayland=true \
        system_wayland_scanner_path="${STAGING_BINDIR_NATIVE}/wayland-scanner" \
        use_system_libwayland=true \
"

X11_GN_ARGS = " \
        ozone_platform_x11=true \
"

GN_ARGS += "\
        ${PACKAGECONFIG_CONFARGS} \
        use_ozone=true \
        ozone_auto_platforms=false \
        ozone_platform_headless=true \
        use_xkbcommon=true \
        use_system_minigbm=true \
        use_system_libdrm=true \
        ${@bb.utils.contains('DISTRO_FEATURES', 'wayland', '${WAYLAND_GN_ARGS}', '', d)} \
        ${@bb.utils.contains('DISTRO_FEATURES', 'x11', '${X11_GN_ARGS}', '', d)} \
        import("//electron/build/args/release.gn") \
        use_gtk=false \
"

SRC_URI += " file://0001-electron-Remove-x11-and-gtk-dependencies-for-ozone-b.patch;patchdir=${S}/electron \
"
