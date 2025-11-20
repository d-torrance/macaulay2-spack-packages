Macaulay2 spack repo
====================

To install [Macaulay2](https://macaulay2.com) using
[spack](https://spack.io/), run the following:

First, set up the Macaulay2 repo:

```
spack repo add https://github.com/d-torrance/macaulay2-spack-packages
```

Some of Macaulay2's dependencies are available in the builtin repository, but at the moment (November 2025), they are in the `develop` branch of the repository and not the most recent stable release.  Check out this branch for access to these dependencies:

```
cd $(spack location --repo builtin)
git fetch origin develop
git checkout origin/develop
```

Finally, install Macaulay2:

```
spack install --verbose macaulay2
```
