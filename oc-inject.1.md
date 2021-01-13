% oc-inject(1) version VERSION |

# NAME

**oc-inject** - Copy and run an executable into an OpenShift container

# SYNOPSIS

| **oc-inject** _pod-ID_ \[**-c** _container-ID_\] _executable_
| **oc-inject** _pod-ID_ \[**-c** _container-ID_\] \-\- _executable_ _args_...

# DESCRIPTION

Copy an executable into an OpenShift container and run the executable.

**oc-inject** is a tool for last-resort troubleshooting of a running container, when a required debugging tool is not present in the container image.

**oc-inject** collects an executable from the local system together with
the minimal dependencies (shared libraries and **ld.so** loader binary)
required to run it, then copies the executable and dependencies
into an OpenShift container by invoking **oc cp**.
**oc-inject** then runs the executable by invoking **oc exec**.
This can be used to install and run basic debugging tools such as
**gdbserver** and **strace** into running containers that would
otherwise lack debugging facilities.

# EXAMPLES

The following command installs **strace** from the local machine into the
first container in pod _myapp-zrblm_ and invokes it to trace all syscalls
made by the process with PID _414_:

    $ oc-inject -it myapp-zrblm -- strace -p 414

The following commands install the **gdbserver** executable
from the local machine into the first container in pod _myapp-zrblm_
and request a backtrace of all threads in the process with PID _23_:

    $ gdb
    (gdb) target extended-remote | ./oc-inject -i myapp-zrblm -- gdbserver --multi -
    (gdb) attach 23
    (gdb) thread apply all bt

# OPTIONS

-c _container-ID_, \-\-container _container-ID_

:   Name of target container in the pod.
    If omitted, the first container in the pod will be chosen.

\-\-custom-loader _custom-loader_

:   Use a custom loader binary instead of **ld.so**.

-h, \-\-help

:   Show a help message and exit.

-i, \-\-stdin

:   For interactive programs: pass stdin to the container.

\-\-java

:   Treat executable as a JDK tool: copy and load additional Java libraries.

-n, \-\-dry-run

:   Output the **oc** commands that would be used to copy
    and run the executable, but do not execute them.

\-\-oc-command _oc_

:   Use a custom command instead of **oc** to access the container.
    For example, use **\-\-oc-command=kubectl** to access a Kubernetes container.

-s, \-\-static

:   Treat executable as a static binary: do not copy any dependencies.

-t, \-\-tty

:   For interactive programs: treat stdin passed to the container as a TTY.

-T _custom-tmpdir_, \-\-custom-tmpdir _custom-tmpdir_

:   Use a custom temporary directory for collecting the executable
    and dependencies.

-v, \-\-verbose

:   Output the **oc** commands used to copy and run the executable.

# BUGS

See GitHub Issues: <https://github.com/serhei/oc-inject/issues>

# AUTHORS

Serhei Makarov <smakarov@redhat.com>

# WWW

https://github.com/serhei/oc-inject

# SEE ALSO

**oc(1)**, **oc-exec(1)**, **kubectl(1)**, **ldd(1)**, **ld.so(8)**
