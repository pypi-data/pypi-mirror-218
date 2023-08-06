# pylint: disable=W0622
"""cubicweb-varnish application packaging information"""

modname = "cubicweb_varnish"
distname = "cubicweb-varnish"

numversion = (1, 0, 0)
version = ".".join(str(num) for num in numversion)

license = "LGPL-2.1"
author = "LOGILAB S.A. (Paris, FRANCE)"
author_email = "contact@logilab.fr"
description = "cubicweb varnish helper"
web = f"https://forge.extranet.logilab.fr/cubicweb/cubes/{distname}"

__depends__ = {
    "cubicweb": ">= 3.31.0, < 5.0.0",
}
__recommends__ = {}

classifiers = [
    "Environment :: Web Environment",
    "Framework :: CubicWeb",
    "Programming Language :: Python :: 3",
    "Programming Language :: JavaScript",
]
