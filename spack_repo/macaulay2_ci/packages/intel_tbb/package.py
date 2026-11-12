# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.packages.intel_tbb.package import IntelTbb as BuiltinIntelTbb

from spack.package import *


class IntelTbb(BuiltinIntelTbb):
    """
    CI-only overlay of the builtin intel-tbb package, vendoring
    spack-packages#7645 so that macOS isn't blocked until it merges.  Delete
    this whole directory once it does.

    spack-packages#7402 added a tcm variant, on by default, that builds
    oneTBB's Thread Composability Manager.  TCM doesn't support macOS -- it
    has no export list or compiler settings for it, and Apple's ld rejects
    the Linux --version-script it gets instead:

        ld: unknown options: --version-script=.../src/def/lin.def

    The conflict makes the concretizer pick ~tcm on macOS by itself.
    """

    # https://github.com/uxlfoundation/oneTBB/issues/2241
    conflicts("+tcm", when="platform=darwin", msg="TCM does not support macOS")
