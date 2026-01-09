Macaulay2 spack repo
====================

## Installing Macaulay2

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

## Running Macaulay2

After installing the package, the quickest way to run Macaulay2 is to load it into your environment and start the interpreter:

    spack load macaulay2
    M2

This makes the M2 executable available on your `PATH` for the duration of your shell session.

If you prefer not to modify your shell environment, you can also run Macaulay2 directly via spack:

    spack exec macaulay2 M2

### Spack environments and modules

Spack provides more advanced ways to manage software, including *environments* and *environment modules*. These are especially useful if you work with multiple versions of Macaulay2 or integrate it into a larger software stack.

Rather than duplicating that documentation here, we recommend consulting the Spack documentation:

* Spack environments: https://spack.readthedocs.io/en/latest/environments.html

* Environment modules: https://spack.readthedocs.io/en/latest/module_file_support.html
