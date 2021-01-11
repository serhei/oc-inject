% oc-inject(1) version VERSION |

# NAME

**oc-inject** - Copy and run an executable into an OpenShift container

# SYNOPSIS

| **oc-inject** _pod-ID_ \[**-c** _container-ID_\] _executable_
| **oc-inject** _pod-ID_ \[**-c** _container-ID_\] \-\- _executable_ _args_...

# DESCRIPTION

Copy an executable into an OpenShift container and run the executable.

**oc-inject** is a tool for last-resort troubleshooting of a running container, when a required debugging tool is not present in the container image.

