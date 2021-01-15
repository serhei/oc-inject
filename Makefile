# oc-inject
.POSIX:

include config.mk

SRC = oc-inject

all: options oc-inject oc-inject.1

# XXX no build options
options:

oc-inject.1: oc-inject.1.md
	pandoc --standalone --to man oc-inject.1.md -o oc-inject.1

clean:

dist: clean
	mkdir -p oc-inject-$(VERSION)
	cp -R LICENSE README.md TODO.md oc-inject.1.md oc-inject.1\
		Makefile oc-inject.spec config.mk $(SRC)\
		oc-inject-$(VERSION)
	tar -cf - oc-inject-$(VERSION) | gzip >oc-inject-$(VERSION).tar.gz
	rm -rf oc-inject-$(VERSION)

install: oc-inject oc-inject.1
	mkdir -p $(DESTDIR)$(PREFIX)/bin
	cp -f oc-inject $(DESTDIR)$(PREFIX)/bin
	chmod 755 $(DESTDIR)$(PREFIX)/bin/oc-inject
	mkdir -p $(DESTDIR)$(MANPREFIX)/man1
	sed "s/VERSION/$(VERSION)/g" <oc-inject.1 >$(DESTDIR)$(MANPREFIX)/man1/oc-inject.1
	chmod 644 $(DESTDIR)$(MANPREFIX)/man1/oc-inject.1

uninstall:
	rm -f $(DESTDIR)$(PREFIX)/bin/oc-inject
	rm -f $(DESTDIR)$(MANPREFIX)/man1/oc-inject.1

.PHONY: all options clean dist install uninstall
