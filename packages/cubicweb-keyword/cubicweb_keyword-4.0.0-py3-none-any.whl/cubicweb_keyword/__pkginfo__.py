# pylint: disable-msg=W0622
"""cubicweb-classification-schemes packaging information"""

modname = "keyword"
distname = "cubicweb-keyword"

numversion = (4, 0, 0)
version = ".".join(str(num) for num in numversion)

license = "LGPL"
copyright = """Copyright (c) 2003-2010 LOGILAB S.A. (Paris, FRANCE).
http://www.logilab.fr/ -- mailto:contact@logilab.fr"""

author = "Logilab"
author_email = "contact@logilab.fr"
web = f"https://forge.extranet.logilab.fr/cubicweb/cubes/{distname}"

description = "classification schemes system for the Cubicweb framework"

classifiers = [
    "Environment :: Web Environment",
    "Framework :: CubicWeb",
    "Programming Language :: Python",
    "Programming Language :: JavaScript",
]

__depends_cubes__ = {}
__depends__ = {
    "cubicweb": ">= 4.0.0, < 5.0.0",
    "cubicweb-web": ">= 1.0.0, < 2.0.0",
}
