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

The `macaulay2` package landed in the builtin repository in August 2026, which
is after `spack-packages`' most recent tagged release (`v2026.06.0`, June
2026); several of Macaulay2's dependencies have picked up build fixes since
then as well.  So until the next release, point the builtin repo at its
`develop` branch by adding the following to `~/.spack/repos.yaml`:

```yaml
repos:
  builtin:
    branch: develop
```

and running `spack repo update`.  Then install
[Macaulay2](https://macaulay2.com) using [spack](https://spack.io/) with:

```
spack install --verbose macaulay2
```

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
demand), [the workflow](.github/workflows/build.yml) installs Macaulay2 from
scratch on AlmaLinux 8, 9 and 10, Ubuntu 22.04, 24.04 and 26.04, and Fedora 45
— spanning gcc 8 through 16 — plus Fedora 45 with clang, Ubuntu 24.04 on
`aarch64`, and macOS on Apple silicon.
It then runs [`smoke-test.m2`](smoke-test.m2) to check that the resulting
Macaulay2 can actually find and run the external programs spack installed with
it.  The development build also generates the documentation, which runs every
example in every package.  A failure here means there's a bug to fix in spack
or in Macaulay2, not in this repo.

Macaulay2's dependencies are built once per platform and shared with the
release and development builds through a build cache on `ghcr.io`, so a run
only rebuilds what actually changed.  The Linux jobs run in each
distribution's stock container image, not spack's, and install spack into it
the way most users do: by cloning it.  macOS has a dependency tier of its own,
since it can't run in those containers.  Every job, on both platforms, runs the
latest spack release — what users run — with `spack-packages` pinned to one
`develop` commit.

That build cache is CI scaffolding, not a place to get binaries.  It is
unsigned, it holds only Macaulay2's dependencies and not Macaulay2 itself, and
every entry is keyed to one pinned `spack-packages` commit, one distribution's
compiler, and one microarchitecture — so anything else gets no cache hits at
all.  For prebuilt binaries, use [spack's own signed build
cache](https://spack.readthedocs.io/en/latest/binary_caches.html) instead.

Every job builds both the latest release and Macaulay2's `development`
branch.  The package recipes left here, in [`spack_repo/macaulay2_ci`](spack_repo/macaulay2_ci), are small overlays
that subclass the builtin ones and add what CI needs ahead of upstream: a
`develop` version of `macaulay2`, which builtin has no reason to carry, plus
fixes still under review upstream: a `gfan` that builds on macOS
([spack-packages#6090]), an `lrslib` that builds with gcc 15 and later
([spack-packages#7758]), and a `macaulay2` that carries several macOS fixes
not yet upstream.  Each is meant to be deleted the moment upstream can do
without it; once they're all gone this repo will contain nothing but CI.

[spack-packages#6090]: https://github.com/spack/spack-packages/pull/6090
[spack-packages#7758]: https://github.com/spack/spack-packages/pull/7758
