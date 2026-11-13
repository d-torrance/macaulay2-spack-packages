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
    development branch and vendoring the pending upstream fixes noted below.
    Everything else is inherited from builtin; nothing is duplicated here.
    This whole repo goes away once the develop version is upstreamed.
    """

    git = "https://github.com/Macaulay2/M2.git"

    # M2's development branch.  Note the repository's *default* branch is
    # "stable", not "development", and there is no "master".
    version("develop", branch="development", submodules=_emacs_submodule)

    variant("doc", default=True, when="@develop",
            description="build the documentation (adds hours to the build)")

    # Both the release and the development branch want gfan 0.8, which the
    # overlay in ../gfan supplies until spack-packages#6090 merges.  This
    # constraint is what selects it: 0.8beta is a prerelease, so a bare `gfan`
    # concretizes to builtin's 0.6.2 instead, and 0.6.2 doesn't build on macOS
    # at all.  ("@1.26.06:" covers develop too -- spack sorts branch versions
    # above numeric ones.)  It also keeps the two tiers in step: the deps job
    # adds this repo unconditionally, so if a build job didn't, the two would
    # concretize gfan differently and miss the build cache.
    depends_on("gfan@0.8beta:", type=("build", "run"), when="@1.26.06:")

    # Vendored from spack-packages#7643; delete once it merges.  M2 always
    # builds with TBB, and its e/m2tbb.hpp includes mathicgb's mtbb.hpp with
    # TBB on, so a mathicgb built without it defines the same mtbb classes
    # differently on the other side of the link.
    depends_on("mathicgb+tbb")

    # Not yet upstream.  M2's configure rejects GNU make 3.81 and requires GNU
    # tar.  macOS ships make 3.81 and bsdtar, and `spack external find`
    # registers that make as gmake, so without a version spack uses it.
    # (spack's tar is GNU tar and only detects GNU tar as an external.)
    depends_on("gmake@4:", type="build")
    depends_on("tar", type="build")

    # Not yet upstream.  M2's configure requires OpenMP, which apple-clang
    # only provides through `-Xpreprocessor -fopenmp -lomp` with libomp on the
    # include and link paths -- and the compiler wrapper only adds those for
    # direct dependencies.
    depends_on("llvm-openmp", when="%apple-clang")

    # Not yet upstream.  Run M2's Fortran library probes before anything is
    # added to LIBS.  The probe links with -v, which spack's compiler wrapper
    # passes through without its search paths, so with LIBS already full the
    # link fails and autoconf scrapes the linker's errors into FLIBS (M2 issue
    # #4074).  Builtin works around that by hard-coding FLIBS and FCLIBS to
    # "-lgfortran -lm" instead, which only links where the C compiler is the
    # gcc that provides gfortran: apple-clang can't find libgfortran.
    patch("fortran-probe-1.26.06.patch", when="@1.26.06")
    patch("fortran-probe-develop.patch", when="@develop")

    # Both a git checkout, which has no generated M2/configure, and the patch
    # above need configure regenerated.  For 1.26.06 that also drops builtin's
    # allow-older-gfan.patch from configure, which only matters for gfan
    # older than the 0.8beta required above.
    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")

    def autoreconf(self, spec, prefix):
        with working_dir(join_path(self.stage.source_path, "M2")):
            Executable("./autogen.sh")()

    def configure_args(self):
        # Let the patched probes find the Fortran libraries themselves.
        args = [
            arg
            for arg in super().configure_args()
            if not arg.startswith(("FLIBS=", "FCLIBS="))
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
