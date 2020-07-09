import os
import bb
from   bb    import data
from   bb.fetch2 import FetchMethod
from   bb.fetch2 import runfetchcmd
from   bb.fetch2 import logger

class Gclient(FetchMethod):
    """Class for sync code from depot-based repositories"""
    def init(self, d):
        pass

    def supports(self, ud, d):
        """
        Check to see if a given url starts with "depot" or "gclient".
        """
        return ud.type in ["depot", "gclient"]

    def urldata_init(self, ud, d):
        """
        supported options:
            name: package name
            jobs: number of parallel jobs
            hash: Hash to checkout
            tag: Tag to checkout
            branch: Branch to checkout
            custom_deps: gclient custom_deps parameter
        """
        ud.name = ud.parm.get('name', '')
        ud.njobs = ud.parm.get('jobs', '1')
        ud.tag = ud.parm.get('tag','')
        ud.packname = "gclient_%s%s_%s%s" % (ud.host, ud.path.replace("/", "."), ud.name, ud.tag)
        ud.localfile = data.expand("%s.tar.gz" % ud.packname, d)
        ud.hash = ud.parm.get('hash','')
        ud.branch = ud.parm.get('branch', 'origin/master')
        ud.download_path = ud.parm.get('download_path','')
        local_custom_var = d.getVar('GCLIENT_CUSTOM_VARS', '')
        ud.custom_vars = []
        if (local_custom_var) :
            ud.custom_vars = local_custom_var.split()

    def download(self, ud, d):
        """
        do fetch
        """

        if os.access(os.path.join(d.getVar("DL_DIR"), ud.localfile), os.R_OK):
            logger.debug(1, "%s already exists (or was stashed). Skipping gclient sync.", ud.localpath)
            return

        depot_dir = d.getVar("DEPOTDIR") or os.path.join(d.getVar("DL_DIR"), "depot")
        sync_dir = os.path.join(depot_dir, ud.packname)

        bb.utils.mkdirhier(sync_dir)
        os.chdir(sync_dir)

        if not os.path.exists(os.path.join(sync_dir, ".gclient")):
            logger.info('This is the first time to sync this depot, config it as http://%s%s'
                    % (ud.host, ud.path))
            fetchcmd = 'gclient.py config --unmanaged http://%s%s' % (ud.host, ud.path)
            if (ud.download_path) :
                fetchcmd = fetchcmd + ' --name ' + ud.download_path
            for custom_var in ud.custom_vars:
                fetchcmd = fetchcmd + ' --custom-var ' + custom_var
            fetchcmd = fetchcmd + ' http://' + ud.host + ud.path
            logger.info(fetchcmd)
            runfetchcmd(fetchcmd, d)
        runfetchcmd('gclient.py sync' , d)
        logger.info('goto src dir')
        logger.info(os.path.join(sync_dir,ud.download_path))
        if (ud.download_path):
            os.chdir(os.path.join(sync_dir,ud.download_path))
        logger.info('Checkout specific tag')
        runfetchcmd('git fetch --all --tags', d)
        runfetchcmd('git checkout tags/%s' % ud.tag, d)

        logger.info('Sync subprojects')
        runfetchcmd('gclient.py sync --with_branch_heads --with_tags --jobs %s' % ud.njobs, d)
        os.chdir(sync_dir)

        logger.info('Creating tarball %s.' % ud.localfile)
        runfetchcmd('tar --exclude .svn --exclude .git -czf %s ./' %
                os.path.join(d.getVar("DL_DIR"), ud.localfile), d)

    def _build_revision(self, url, ud, d):
        return None

