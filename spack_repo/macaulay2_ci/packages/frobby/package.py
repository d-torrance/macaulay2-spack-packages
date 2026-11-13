# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.packages.frobby.package import Frobby as BuiltinFrobby

from spack.package import *


class Frobby(BuiltinFrobby):
    """
    CI-only overlay of the builtin frobby package, so that macOS isn't blocked
    until frobby's next release, which moves to automake.  Delete this whole
    directory once builtin has that release.

    frobby's Makefile gives its shared library a Linux-style soname on macOS
    too: `-install_name libfrobby.so.1`, with no path.  Everything linked
    against it records that bare name, which dyld can't find:

        dyld: Library not loaded: libfrobby.so.1
    """

    # Name it @rpath/libfrobby.so.1 instead.  Darwin only, so the Linux
    # builds keep their hashes.
    patch("darwin-install-name.patch", when="@0.9.9 platform=darwin")
