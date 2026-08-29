# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.packages.gfan.package import Gfan as BuiltinGfan

from spack.package import *


class Gfan(BuiltinGfan):
    """
    CI-only overlay of the builtin gfan package, vendoring
    spack-packages#6090 so that macOS isn't blocked until it merges.  Delete
    this whole directory once it does.

    Builtin's gfan 0.6.2 doesn't build on macOS: gfan's Makefile hardcodes its
    own compiler, so the build never goes through spack's compiler wrapper.
    On Linux that's invisible -- the wrapper directory has a `g++` in it,
    because the compiler is gcc -- but with apple-clang the wrapper is named
    `clang++`, `g++` falls through to Apple's, and nothing spack knows about
    the dependencies reaches the compile line:

        src/field_rationals.h:6:10: fatal error: 'gmp.h' file not found
    """

    version("0.8beta", sha256="fa7884e5f317c50f8fb4f37bcf5d419f0fd5f7b90d6037349d1957ea73cebbee")

    depends_on("tbb", when="@0.8beta:")

    # 0.8beta builds only on a narrow set of toolchains as shipped: it wants
    # std::execution (absent from libc++), a few library features newer than
    # the compilers on older distributions, and it pins macOS to Homebrew's
    # gcc-15.  This is the patch under review upstream.
    patch("compile-on-more-systems-0.8beta.patch", when="@0.8beta")

    def flag_handler(self, name: str, flags: List[str]):
        # Builtin puts -DNOCDDPREFIX and cddlib's include directory here, which
        # reaches the compiler through SPACK_CPPFLAGS -- and so only through
        # the wrapper.  build_targets below passes both on the make command
        # line instead, where they arrive whatever the Makefile does.
        return (flags, None, None)

    @property
    def build_targets(self):
        # Name the compiler explicitly so the Makefile's own choice doesn't
        # win, and override the include and link options gfan hardcodes for
        # Homebrew.  GMP_INCLUDEOPTIONS is emptied rather than set: with the
        # wrapper back in the picture, spack supplies gmp's include directory
        # by itself.
        targets = [
            f"CXX={spack_cxx}",
            "CDDDEFINE_PREFIX=-DNOCDDPREFIX",
            f"CDD_INCLUDEOPTIONS=-I{self.spec['cddlib'].prefix.include}/cddlib",
            "CDD_LINKOPTIONS=-lcddgmp",
            "GMP_INCLUDEOPTIONS=",
            "GMP_LINKOPTIONS=-lgmp",
        ]
        if self.spec.satisfies("@0.8beta:"):
            targets.append("TBB_INCLUDEOPTIONS=")
            if self.spec.satisfies("platform=darwin"):
                # -rdynamic is Linux-only.
                targets.append("PLATFORM_LINKOPTIONS=-ltbb")
            else:
                targets.append("PLATFORM_LINKOPTIONS=-rdynamic -ltbb")
        return targets
