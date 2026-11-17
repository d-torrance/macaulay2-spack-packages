# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.packages.lrslib.package import Lrslib as BuiltinLrslib

from spack.package import *


class Lrslib(BuiltinLrslib):
    """
    CI-only overlay of the builtin lrslib package, vendoring
    spack-packages#7758 so that gcc 15 and later aren't blocked until it
    merges.  Delete this whole directory once it does.

    lrslib 7.3 declares its signal handlers as `void checkpoint()`, which C23
    -- gcc 15's default -- reads as taking no arguments, so passing one to
    signal() is an error:

        lrslib.h:40:24: error: passing argument 2 of 'signal' from
        incompatible pointer type [-Wincompatible-pointer-types]

    7.3a, a patch release, gives the handlers their `int` argument.
    """

    version("7.3a", sha256="7fb16ad5c2b7380ef8deaecbfaf53599eef074fd225012aa431b76ee0bded6a6")
