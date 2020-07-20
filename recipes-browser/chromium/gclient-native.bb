SUMMARY = "Google Client"
SRC_URI = "git://chromium.googlesource.com/chromium/tools/depot_tools.git;protocol=https"
SRCREV = "9af33fa208fbb6e2212c7f62d55bf644e1f731ae"
PV = "1.0+git${SRCPV}"
S = "${WORKDIR}/git"
LICENSE = "GPLv3"
LIC_FILES_CHKSUM = "file://LICENSE;md5=c2c05f9bdd5fc0b458037c2d1fb8d95e"

inherit native

do_install() {
        mkdir -p ${D}${bindir}
        cp -r ${S} ${D}${bindir}/${PN}
        rm ${D}${bindir}/${PN}/gn
        rm ${D}${bindir}/${PN}/gn.py
}

FILES_${PN}="${bindir}/*"
