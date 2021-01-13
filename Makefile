# oc-inject
.POSIX:

# TODO: Specify from rpmspec; defaults for standalone install should be:
# VERSION = 0.0.8
# DESTDIR =
# PREFIX = /usr/local
# MANPREFIX = $(PREFIX)/share/man

all: oc-inject.1

oc-inject.1: oc-inject.1.md
	pandoc --standalone --to man oc-inject.1.md -o oc-inject.1

install: oc-inject oc-inject.1
	mkdir -p $(DESTDIR)$(PREFIX)/bin
	cp -f oc-inject $(DESTDIR)$(PREFIX)/bin
	chmod 755 $(DESTDIR)$(PREFIX)/bin/oc-inject
	mkdir -p $(DESTDIR)$(MANPREFIX)/man1
	sed "s/VERSION/$(VERSION)/g" <oc-inject.1 >$(DESTDIR)$(MANPREFIX).1
	chmod 644 $(DESTDIR)$(MANPREFIX)/man1/oc-inject.1

.PHONY: all install uninstall
