# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage

from spack.package import *


class Mathic(AutotoolsPackage):
    """Mathic is a C++ library providing optimized data structures for
    Gröbner basis computation. It includes support for ordering
    S-pairs, divisor queries, and polynomial term ordering during
    reduction. The library is template-based and can be used with
    arbitrary monomial and coefficient representations, though it
    currently works best with dense term representations."""

    homepage = "https://github.com/Macaulay2/mathic"
    git = "https://github.com/Macaulay2/mathic"

    maintainers("d-torrance")

    license("LGPL-2.0-or-later", checked_by="d-torrance")

    version("master", branch="master")

    depends_on("cxx", type="build")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")

    depends_on("memtailor")
