Macaulay2 spack builds
======================

[![Build spack package](https://github.com/d-torrance/macaulay2-spack-packages/actions/workflows/build.yml/badge.svg)](https://github.com/d-torrance/macaulay2-spack-packages/actions/workflows/build.yml)

> [!IMPORTANT]
> **This repo is no longer needed to install Macaulay2.**  As of August 2026,
> [Macaulay2](https://macaulay2.com) is part of spack's builtin package
> repository, so there is no reason to add this repo to your spack
> installation.  If you added it following the old instructions, remove it
> with:
>
> ```
> spack repo remove macaulay2
> ```

## Installing Macaulay2

Install [Macaulay2](https://macaulay2.com) using [spack](https://spack.io/)
with:

```
spack install --verbose macaulay2
```

Some of Macaulay2's dependencies are available in the builtin repository, but
at the moment (August 2026), they are in the `develop` branch of the repository
and not the most recent stable release.  Until then, add the following to
`~/.spack/repos.yaml`:

```yaml
repos:
  builtin:
    branch: develop
```

and run `spack repo update`.

## Running Macaulay2

After installing the package, the quickest way to run Macaulay2 is to load it into your environment and start the interpreter:

    spack load macaulay2
    M2

This makes the M2 executable available on your `PATH` for the duration of your shell session.

### Spack environments and modules

Spack provides more advanced ways to manage software, including *environments* and *environment modules*. These are especially useful if you work with multiple versions of Macaulay2 or integrate it into a larger software stack.

Rather than duplicating that documentation here, we recommend consulting the Spack documentation:

* Spack environments: https://spack.readthedocs.io/en/latest/environments.html

* Environment modules: https://spack.readthedocs.io/en/latest/module_file_support.html

## What this repo is for now

It exists to make sure the spack *builds* keep working.  Every Tuesday (and on
demand), [the workflow](.github/workflows/build.yml) installs the builtin
`macaulay2` package from scratch on AlmaLinux 8 and 9, Ubuntu Jammy and Noble,
and Fedora 40 — spanning gcc 8 through 14 — plus Ubuntu Noble on `aarch64` and,
experimentally, macOS.  It then runs [`smoke-test.m2`](smoke-test.m2) to
check that the resulting Macaulay2 can actually find and run the external
programs spack installed with it.  The development build also generates the
documentation, which runs every example in every package.  A failure here means
there's a bug to fix in spack or in Macaulay2, not in this repo.

Macaulay2's dependencies are built once per distribution and shared with the
release and development builds through a build cache on `ghcr.io`, so a run only
rebuilds what actually changed.

That build cache is CI scaffolding, not a place to get binaries.  It is
unsigned, it holds only Macaulay2's dependencies and not Macaulay2 itself, and
every entry is keyed to one pinned `spack-packages` commit, one distribution's
compiler, and one microarchitecture — so anything else gets no cache hits at
all.  For prebuilt binaries, use [spack's own signed build
cache](https://spack.readthedocs.io/en/latest/binary_caches.html) instead.

Both the latest release and Macaulay2's `development` branch are built.  The
builtin package has no `develop` version, so the one package recipe left here,
[`spack_repo/macaulay2_ci`](spack_repo/macaulay2_ci), is a small overlay that
subclasses the builtin one and adds it.  Once that lands upstream, this repo
will contain nothing but CI.
