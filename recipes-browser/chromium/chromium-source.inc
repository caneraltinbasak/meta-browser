DESCRIPTION = "Chromium is an open-source browser project that aims to build a safer, faster, and more stable way for all users to experience the web."
HOMEPAGE = "https://www.chromium.org/Home"

CVE_PRODUCT = "chromium:chromium google:chrome"

SRC_URI += "https://commondatastorage.googleapis.com/chromium-browser-official/chromium-${PV}.tar.xz"
SRC_URI[md5sum] = "aa180a004af1cc542d5a50c36bfcabd6"
SRC_URI[sha256sum] = "bb0c7e8dfee9f3a5e30eca7f34fc9f21caefa82a86c058c552f52b1ae2da2ac3"

S = "${WORKDIR}/chromium-${PV}"

# electron doesn't checkout native_client, it only exists in chromium source.
LIC_FILES_CHKSUM += "\
    file://${S}/native_client/LICENSE;md5=cbbd27594afd089daa160d3a16dd515a \
"
