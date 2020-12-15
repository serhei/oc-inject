# oc-inject

    $ ./oc-inject <pod_ID> [-c <container_ID>] <executable>
    $ ./oc-inject <pod_ID> [-c <container_ID>] -- <executable> <args...>

Copy an executable to an [OpenShift](https://www.openshift.com/) container and run the executable.

`oc-inject` is a prototype tool for last-resort troubleshooting of a
running container, when a required debugging tool is not present in
the container image.

## Requirements

`oc-inject` requires Python 3, `ldd`, `ldconfig`, and the OpenShift
command line tool `oc`. I may rewrite the tool in Go once it is
ready to move beyond a proof-of-concept.

## Examples

**1)** `strace` is a convenient tool for printing syscalls
made by a process. The following command installs `strace` into the
first container in `myapp-zrblm` and invokes it to trace all syscalls
made by the process with PID `414`:

    $ oc-inject -it myapp-zrblm -- strace -p 414

**2)** `gdbserver` is included in RHEL-based container images on enterprise
OpenShift, but is not available in CentOS-based images (this is a
[known
issue](https://github.com/CentOS/sig-cloud-instance-build/issues/140)).
Suppose we want to use GDB to debug a running OpenShift pod
`myapp-zrblm`, which is based on a CentOS image and does not have
`gdbserver` preinstalled. The following commands will copy the
`gdbserver` executable from the local machine to the first container
in `myapp-zrblm` and request a backtrace of all threads in the process
with PID `23`:

    $ gdb
    (gdb) target extended-remote | ./oc-inject -i myapp-zrblm -- gdbserver --multi -
    (gdb) attach 23
    (gdb) thread apply all bt

**3)** Suppose we are curious to use [`iperf3`](https://iperf.fr/) to check
the network bitrate to/from a Minishift container. After installing the `iperf3`
package, we launch an `iperf3` test between the container and a host of our choice:

    myhost.mydomain$ iperf3 -s -1
    -----------------------------------------------------------
    Server listening on 5201
    -----------------------------------------------------------
    
    myhost.mydomain$ ./oc-inject -i myapp-zrblm -- iperf3 -c myhost.mydomain -p 5201
    Connecting to host myhost.mydomain, port 5201
    [  5] local 172.8.8.8 port 50740 connected to 192.168.8.8 port 5201
    [ ID] Interval           Transfer     Bitrate         Retr  Cwnd
    [  5]   0.00-1.00   sec   137 MBytes  1.15 Gbits/sec  1137   71.3 KBytes       
    [  5]   1.00-2.00   sec   163 MBytes  1.37 Gbits/sec    0   71.3 KBytes       
    [  5]   2.00-3.00   sec   166 MBytes  1.40 Gbits/sec    0   71.3 KBytes       
    [  5]   3.00-4.00   sec   161 MBytes  1.34 Gbits/sec    0   71.3 KBytes       
    [  5]   4.00-5.00   sec   165 MBytes  1.38 Gbits/sec    0   71.3 KBytes       
    [  5]   5.00-6.00   sec   179 MBytes  1.50 Gbits/sec    0   71.3 KBytes       
    [  5]   6.00-7.00   sec   166 MBytes  1.40 Gbits/sec    0   71.3 KBytes       
    [  5]   7.00-8.01   sec   168 MBytes  1.40 Gbits/sec    0   71.3 KBytes       
    [  5]   8.01-9.00   sec   149 MBytes  1.27 Gbits/sec    0   71.3 KBytes       
    [  5]   9.00-10.00  sec   165 MBytes  1.39 Gbits/sec    0   71.3 KBytes       
    - - - - - - - - - - - - - - - - - - - - - - - - -
    [ ID] Interval           Transfer     Bitrate         Retr
    [  5]   0.00-10.00  sec  1.58 GBytes  1.36 Gbits/sec  1137             sender
    [  5]   0.00-10.00  sec  1.58 GBytes  1.36 Gbits/sec                  receiver
    
    iperf Done.

(Note that in order to run an `iperf3` test like this, the container must be able
to route to `myhost.mydomain`. This happens to be true by default on the
Minishift setup I was testing with.)

Or, in the other direction using `oc port-forward`:

    $ oc port-forward myapp-zrblm 9021:5201
    $ ./oc-inject -i myapp-zrblm -- iperf3 -s -1
    -----------------------------------------------------------
    Server listening on 5201
    -----------------------------------------------------------
    
    $ iperf3 -c 127.0.0.1 -p 9021

... *More demos coming soon.* ...

## Troubleshooting

`oc-inject` is an experimental tool and many edge cases still need to
be tested. The following recipes may help troubleshoot why it's not
working for you.

Needless to say, the system you are copying the executable from and the
target container must be running on compatible processor architectures.

Dry-run mode, shows full list of commands that would be executed:

    ./oc-inject -it -n myapp-zrblm -- ls

Show the list of loaded objects:

    ./oc-inject -it -v myapp-zrblm -D LD_TRACE_LOADED_OBJECTS=yes -- ls

For example, you might see problems if it is trying to use the
version of `ld.so` already within the container:

    ...
    oc exec -it nodejs-ex-1-gsc9q -- env LD_LIBRARY_PATH=/tmp/oc-inject-0b54a840 LD_TRACE_LOADED_OBJECTS=yes /tmp/oc-inject-0b54a840/ls
        linux-vdso.so.1 =>  (0x00007fff647fb000)
	    libselinux.so.1 => /tmp/oc-inject-0b54a840/libselinux.so.1 (0x00007f128d52b000)
	    libcap.so.2 => /tmp/oc-inject-0b54a840/libcap.so.2 (0x00007f128d326000)
	    libc.so.6 => /tmp/oc-inject-0b54a840/libc.so.6 (0x00007f128cf70000)
	    libpcre2-8.so.0 => /tmp/oc-inject-0b54a840/libpcre2-8.so.0 (0x00007f128ccea000)
	    libdl.so.2 => /tmp/oc-inject-0b54a840/libdl.so.2 (0x00007f128cae6000)
	    /lib64/ld-linux-x86-64.so.2 (0x00007f128d754000)
	    libpthread.so.0 => /tmp/oc-inject-0b54a840/libpthread.so.0 (0x00007f128c8c8000)

Then you would specify a `--custom-loader` option:

    $ ./oc-inject -it -n myapp-zrblm --custom-loader ld-linux-x86-64.so.2 -- ls

(The current version of the script already defaults to using
`ld-linux-x86-64.so.2` as the custom loader, but you may need a
different loader on your system.)

Show detailed debugging output for `ld.so`:

    $ ./oc-inject -it -v myapp-zrblm -D LD_DEBUG=symbols,bindings -- ls

To reproduce issues cleanly, make sure leftover processes were killed
and older `oc-inject` directories in a container are removed:

    $ oc exec myapp-zrblm ps
    PID TTY          TIME CMD
    ... ...           ... ...
    593 ?        00:00:10 ld-linux-x86-64
    605 ?        00:00:00 ps
    $ oc exec myapp-zrblm -- kill -9 ps
    $ oc rsh myapp-zrblm
    sh-4.2$ rm -rf /tmp/oc-inject-*

## Limitations, known and suspected

*The following limitations will be removed with further work:*

- `oc-inject` does not clean up after the injected
  executable. Executables such as `gdbserver` may continue running
  after `oc-inject` has exited, and the executable along with its
  dependencies will remain within the target container's `/tmp`
  folder.

- `oc-inject` only copies executables that are installed on the local
  system. A best-practice approach would be to copy executables from a
  local container image, and to provide a container image of debugging
  tools that have been tested with `oc-inject`.

- `oc-inject` does not check if suitable shared libraries are already
  present in the container (e.g. from invocations of `oc-inject` with
  other commands), instead always copying the entire set of
  dependencies. (However, the fact that `oc-inject` uses `rsync` and a
  consistent naming scheme for its temporary files does mean that
  repeated invocations of the same executable will cache and reuse the
  particular set of shared objects used by that executable.)

- Executables have a number of potential ways to hardcode library
  search paths, e.g. `DT_RPATH` on some systems. If this becomes a
  practical issue, a `chrpath` step can be added to the staging process.

*The following limitations must be investigated further:*

- If the injected executable starts another process (e.g. `strace
  ls`), the child process will inherit the `LD_LIBRARY_PATH` settings
  used to run the injected executable and will most likely fail to
  load.

*The following limitations may be resolved depending on subsequent
discussions with the OpenShift development teams:*

- `oc rsync`/`oc cp` and `oc exec`, respectively, are used to copy and
  run the executable. Therefore, the user must have permissions to
  perform these actions on the target container. In addition, the
  requirements for `oc cp` must be satisfied. That is, a `tar` binary
  must be present in the target container, and an `rsync` binary is
  nice-to-have.

- The injected executable is stored in the `/tmp` folder. Therefore,
  the target container's `/tmp` folder must be writable and its
  filesystem must have sufficient free space to store the executable.

- `oc-inject` does not increase the container's memory limit. The
  running executable must fit within the target container's existing
  memory limits.

*The following limitations are more philosophical:*

- `oc-inject` does not copy any other dependencies for the executable
  aside from shared libraries. If the executable requires
  configuration files, you will have to set them up manually. If the
  executable requires a complex installation procedure, you may not
  want to be installing it for a transient debugging session. If using
  the executable requires debug information, you need an additional
  solution to provide the debug information.
