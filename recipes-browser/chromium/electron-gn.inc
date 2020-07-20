require chromium.inc
require chromium-unbundle.inc
require gn-utils.inc
require chromium-common-gn.inc

do_compile() {
    ninja -v ${PARALLEL_MAKE} electron chromedriver
}

do_install() {
    install -d ${D}${bindir}
    install -d ${D}${libdir}/electron
    install -d ${D}${libdir}/electron/locales
    install -d ${D}${libdir}/electron/resources

    install -m 0755 electron ${D}${libdir}/electron/electron
    install -m 0644 resources/default_app.asar ${D}${libdir}/electron/resources/default_app.asar
    install -m 0644 *.bin ${D}${libdir}/electron/
    install -m 0644 icudtl.dat ${D}${libdir}/electron/icudtl.dat
    # Chromium *.pak files
    install -m 0644 chrome_*.pak ${D}${libdir}/electron/
    install -m 0644 resources.pak ${D}${libdir}/electron/resources.pak

    # Locales.
    install -m 0644 locales/*.pak ${D}${libdir}/electron/locales/

    install -m 0755 libffmpeg.so ${D}${libdir}/electron/

    if [ -n "${@bb.utils.contains('PACKAGECONFIG', 'component-build', 'component-build', '', d)}" ]; then
        install -m 0755 *.so ${D}${libdir}/electron/
    fi

    # When building chromium with use_system_minigbm=false,
    # libminigbm.so does not seem to get linked in statically.
    # So we simply check whether it exists in all cases and ship it.
    if [ -e libminigbm.so ]; then
        install -m 0755 libminigbm.so ${D}${libdir}/electron/
    fi

    # Swiftshader is only built for x86 and x86-64.
    if [ -d "swiftshader" ]; then
        install -d ${D}${libdir}/electron/swiftshader
        install -m 0644 swiftshader/libEGL.so ${D}${libdir}/electron/swiftshader/
        install -m 0644 swiftshader/libGLESv2.so ${D}${libdir}/electron/swiftshader/
    fi

    install -m 0755 chromedriver ${D}${bindir}/chromedriver
}

PACKAGES =+ "${PN}-chromedriver"

FILES_${PN}-chromedriver = "${bindir}/chromedriver"

FILES_${PN} = " \
    ${bindir}/electron \
    ${libdir}/electron/* \
"

PACKAGE_DEBUG_SPLIT_STYLE = "debug-without-src"

# There is no need to ship empty -dev packages.
ALLOW_EMPTY_${PN}-dev = "0"
