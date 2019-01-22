- README: discuss why gdbserver on CentOS is wanted even with gdb in some containers
  - reason 1: we want to use debuginfo provided outside the container
  - reason 2: we want to use a custom tool that speaks gdbserver protocol, e.g. gdb-strace
- README: add ordinary strace example (after checking how well it works)
- README: add gdb-strace example when ready
- solve solvable limitations described in README
- double-check Fedora packaging guidelines (e.g. man-page)
- longer term: decide on a one-liner invocation syntax for stapdyn

Potential upstream issue:
- when `oc rsync` uses tar fallback, result is inconsistent with docs:

      $ oc rsync ./local/dir/ target-pod:/remote/dir/ # does not work
      $ oc rsync ./local/dir target-pod:/remote/ # work
