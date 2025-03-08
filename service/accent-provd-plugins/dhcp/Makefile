SHELL := /bin/sh
SRCDIR := dhcp
SRCFILES := $(shell find $(SRCDIR) -type f)
TARFILE := dhcpd.tar.bz2


$(TARFILE) : $(SRCFILES)
	cd $(SRCDIR) && tar caf "$$OLDPWD/$(TARFILE)" --exclude '.*' *


.PHONY : upload
upload : $(TARFILE)
	scp $(TARFILE) root@webserver.accentvoice.io:/var/www/provd/accent/dhcpd-update/13.17


.PHONY : clean
clean :
	rm -f $(TARFILE)
