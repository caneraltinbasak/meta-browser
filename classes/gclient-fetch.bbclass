#
# gclient-fetch class
#
# Registers GCLIENT method for Bitbake fetch2.
#
# Adds support for following format in recipe SRC_URI:
# gclient://<packagename>;version=<version>
#
#
DEPENDS_prepend = "gclient-native xz-native nodejs-native"
do_fetch[depends] += "gclient-native:do_populate_sysroot xz-native:do_populate_sysroot nodejs-native:do_populate_sysroot"
EXTRANATIVEPATH += "gclient-native"
DEPOTDIR ?= "${DL_DIR}/depot"
DEPOTDIR[doc] = "Download path for gclient"

GCLIENT ?= "gclient"

python () {
        import gclient
        bb.fetch2.methods.append( gclient.Gclient() )
}
