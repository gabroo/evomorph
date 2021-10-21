# evomorph

## Setup

Install [Bazel](https://docs.bazel.build/versions/main/install.html) or
(preferrably) [Bazelisk](https://github.com/bazelbuild/bazelisk#installation).

## Build

```
bazel[isk] build <component>:main
```

Where `<component>` is one of `{controller, engine}`.

## Run

[tbd]

## Help

Protobuf references can be built using Bazel.

```
bazel[isk] build docs:all
```

Output files will be available in `build/bin/docs` in HTML and Markdown format.
