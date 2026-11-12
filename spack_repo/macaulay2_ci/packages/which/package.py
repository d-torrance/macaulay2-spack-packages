# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.packages.which.package import Which as BuiltinWhich

from spack.package import *


class Which(BuiltinWhich):
    """
    CI-only overlay of the builtin which package, vendoring
    spack-packages#7646 so that macOS isn't blocked until it merges.  Delete
    this whole directory once it does.  (4ti2 needs which at run time.)

    which 2.25's configure asks for C23, and its bundled getopt.h declares
    `extern int getopt();` whenever the C library isn't glibc.  C23 reads that
    as taking no arguments, which contradicts macOS's unistd.h:

        ./getopt.h:105:12: error: conflicting types for 'getopt'
    """

    # https://lists.gnu.org/archive/html/which-bugs/2025-03/msg00000.html
    patch("c23-getopt.patch", when="@2.23:2.25")
