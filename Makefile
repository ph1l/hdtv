install:
	install -m 755 hdtv $(DESTDIR)/usr/bin/hdtv
	install -m 644 completion.bash $(DESTDIR)/etc/bash_completion.d/hdtv
