# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.packages.macaulay2.package import Macaulay2 as BuiltinMacaulay2

from spack.package import *


def _emacs_submodule(package):
    # --with-system-libs makes the library submodules (bdwgc, flint, givaro,
    # googletest, ...) unnecessary.  autogen.sh only needs M2.el, and cloning
    # the rest would add several hundred megabytes to every CI run.
    return ["M2/Macaulay2/editors/emacs"]


class Macaulay2(BuiltinMacaulay2):
    """
    CI-only overlay of the builtin macaulay2 package, adding Macaulay2's
    development branch.  Everything else is inherited from builtin; nothing is
    duplicated here.  This whole repo goes away once the develop version is
    upstreamed.
    """

    git = "https://github.com/Macaulay2/M2.git"

    # M2's development branch.  Note the repository's *default* branch is
    # "stable", not "development", and there is no "master".
    version("develop", branch="development", submodules=_emacs_submodule)

    variant("doc", default=True, when="@develop",
            description="build the documentation (adds hours to the build)")

    with when("@develop"):
        # a git checkout has no generated M2/configure
        depends_on("autoconf", type="build")
        depends_on("automake", type="build")
        depends_on("libtool", type="build")

        # M2's development branch requires gfan 0.8, which spack doesn't have
        # yet (spack-packages#6090 adds 0.8beta).  Until then, drop the minimum
        # version as builtin does for @1.26.06 -- but builtin's patch edits the
        # generated M2/configure, which doesn't exist in a git checkout, so
        # patch M2/configure.ac instead.  This goes away by itself once gfan
        # 0.8beta is available.
        patch("allow-older-gfan-configure-ac.patch", when="^gfan@:0.7")

    def autoreconf(self, spec, prefix):
        if spec.satisfies("@develop"):
            with working_dir(join_path(self.stage.source_path, "M2")):
                Executable("./autogen.sh")()

    def configure_args(self):
        args = super().configure_args()

        # builtin sets FLIBS/FCLIBS = "-lgfortran -lm -lquadmath" to work
        # around Macaulay2/M2#4074.  All that value has to do is (1) be
        # nonempty, so autoconf takes its "let the user override the test"
        # path and skips the AC_FC_LIBRARY_LDFLAGS probe that spack's compiler
        # wrapper breaks, and (2) name the Fortran runtime, for the static
        # librefblas.a/liblapack.a that BUILD_lapack=yes produces.  -lquadmath
        # was only along for the ride: it is what gfortran's link spec emits
        # on x86, so it showed up in the probe output that value was copied
        # from.  There is no libquadmath on aarch64 -- long double is already
        # IEEE binary128 there, so gcc doesn't build one -- and the
        # AC_F77_DUMMY_MAIN probe dies with "linking to Fortran libraries from
        # C fails".  Nothing in refblas/lapack uses REAL(16), and M2 finds
        # libquadmath for boost-math by itself with
        # AC_SEARCH_LIBS([ldexpq], [quadmath]), so dropping it is safe
        # everywhere.  Upstream fix pending; this override goes away with it.
        args = [
            arg.replace(" -lquadmath", "")
            if arg.startswith(("FLIBS=", "FCLIBS="))
            else arg
            for arg in args
        ]

        if self.spec.satisfies("@develop"):
            # builtin passes --enable-documentation=download, which fetches
            # Macaulay2-docs-$(PACKAGE_VERSION).tar.gz.  That tarball is only
            # built after the corresponding release, so it is missing for a
            # development snapshot whenever M2/VERSION is ahead of the last
            # release.  Drop the option and let M2 build the documentation
            # itself, as it does by default.
            args = [
                arg for arg in args if not arg.startswith("--enable-documentation=")
            ]
            if self.spec.satisfies("~doc"):
                args.append("--enable-documentation=no")
        return args
