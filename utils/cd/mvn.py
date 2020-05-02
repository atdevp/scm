import os
import xml.dom.minidom
import cfg
from utils.exceptions import MvnParametersNotFind, MvnProjectNotFind, MvnModPathNotFind
from utils.exceptions import MvnPomFileNotFind, MvnFinalNameFieldNotFind, MvnPackagingFieldNotFind


class Mvn(object):
    """

    """
    def __init__(self, name=None, ptype=None):

        if name is None or ptype is None:
            raise MvnParametersNotFind("name or ptype invalid")

        self.name = name
        self.ptype = ptype
        self.ws_path = cfg.CICD_CFG['SRC_CODE_PATH']

        if os.getcwd() != self.ws_path:
            os.chdir(self.ws_path)

    def get_mods(self):
        mods = []

        p = os.path.join(self.ws_path, self.name)
        if not os.path.isdir(p):
            raise MvnProjectNotFind("{} path not find".format(p))

        os.chdir(p)
        if not os.path.exists("pom.xml"):
            raise MvnPomFileNotFind("pom.xml file not find")

        domTree = xml.dom.minidom.parse('pom.xml')
        tagMods = domTree.documentElement.getElementsByTagName('module')
        if not tagMods:
            return mods

        return [m.childNodes[0].data for m in tagMods]

    def get_pkg_name(self, mod_name=None):

        if self.ptype == "zip" and mod_name is not None:
            return self.name + "_" + mod_name + ".zip"

        if self.ptype == "zip" and mod_name is None:
            return self.name + "_" + "no-module.zip"

        if self.ptype == "jar" or self.ptype == "war":
            path = self.name if mod_name is None else os.path.join(
                self.name, mod_name)

            ok = os.path.isdir(os.path.join(self.ws_path, path))
            if not ok:
                raise MvnModPathNotFind("{} path not find".format(
                    os.path.join(self.ws_path, path)))
            os.chdir(os.path.join(self.ws_path, path))

            if not os.path.exists("pom.xml"):
                raise MvnPomFileNotFind("pom.xml file not find")

            DomTree = xml.dom.minidom.parse('pom.xml')

            pre = DomTree.documentElement.getElementsByTagName('finalName')
            if not pre:
                raise MvnFinalNameFieldNotFind(
                    "finalName field not exist in pom.xml")

            suf = DomTree.documentElement.getElementsByTagName('packaging')
            if not suf:
                raise MvnPackagingFieldNotFind(
                    "packaging field not exist in pom.xml")

            pre_name = pre[0].childNodes[0].data
            suf_name = suf[0].childNodes[0].data

            return pre_name + "." + suf_name
