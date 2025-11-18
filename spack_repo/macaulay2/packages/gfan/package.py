# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack_repo.builtin.build_systems.makefile import MakefilePackage

from spack.package import *


class Gfan(MakefilePackage):
    """Gfan computes Gröbner fans and tropical varieties of polynomial
    ideals, with tools for universal Gröbner bases, tropical curves,
    hypersurfaces, and related structures in tropical geometry."""

    homepage = "https://users-math.au.dk/jensen/software/gfan/gfan.html"
    url = "https://users-math.au.dk/jensen/software/gfan/gfan0.7.tar.gz"

    maintainers("d-torrance")

    license("GPL-2.0-or-later", checked_by="d-torrance")

    version("0.7", sha256="ab833757e1e4d4a98662f4aa691394013ea9a226f6416b8f8565356d6fcc989e")

    depends_on("cxx", type="build")

    depends_on("cddlib+gmp")
    depends_on("gmp")

    def flag_handler(self, name: str, flags: List[str]):
        if name == "cppflags":
            flags.extend(
                [
		    "-DNOCDDPREFIX",
                    f"-I{self.spec['cddlib'].prefix.include}/cddlib",
                ]
            )
        return (flags, None, None)

    @property
    def install_targets(self):
        return [
            "install",
            f"PREFIX={self.spec.prefix}"
        ]
