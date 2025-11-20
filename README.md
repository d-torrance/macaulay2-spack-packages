Macaulay2 spack repo
====================

To install Macaulay2 using [spack](https://spack.io/), run the following:

```
# set up Macaulay2 repo
spack repo add https://github.com/d-torrance/macaulay2-spack-packages

# check out recent changes to builtin repo (for various M2 dependencies)
cd $(spack location --repo builtin)
git fetch origin develop
git checkout origin/develop

# install Macaulay2
spack install --verbose macaulay2
```
