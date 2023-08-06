# pylint: disable=W0622
"""cubicweb-postgis application packaging information"""

modname = "postgis"
distname = f"cubicweb-{modname}"

numversion = (1, 0, 0)
version = ".".join(str(num) for num in numversion)

license = "LGPL"
author = "LOGILAB S.A. (Paris, FRANCE)"
author_email = "contact@logilab.fr"
description = "Test for postgis"
web = f"https://forge.extranet.logilab.fr/cubicweb/cubes/{distname}"

__depends__ = {
    "cubicweb": ">= 4.0.0, < 5.0.0",
    "cubicweb-web": ">= 1.0.0, < 2.0.0",
}

__recommends__ = {}

classifiers = [
    "Environment :: Web Environment",
    "Framework :: CubicWeb",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 3",
    "Programming Language :: JavaScript",
    "Topic :: Scientific/Engineering :: GIS",
    "Topic :: Database",
]
