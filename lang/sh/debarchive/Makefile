LOGIN ?= packages@qa.debian.org
target ?= jessie
section ?= main
target_sources := debian/dists/$(target)/$(section)/source/Sources.gz
SourcesGZ := $(target_sources)

.PHONY: jessie jessie-backports
jessie:
	debmirror --config-file ./jessie.conf ./jessie/
jessie-backports:
	debmirror --config-file ./jessie-backports.conf ./jessie-backports/
.PHONY: sid exp
sid:
	@echo "USE debmirror/sid, dak change (Mar.2016) breaks debmirror/jessie."
	debmirror --config-file ./sid.conf ./sid/
exp:
	@echo "USE debmirror/sid, dak change (Mar.2016) breaks debmirror/jessie."
	debmirror --config-file ./experimental.conf ./experimental/

default:
	./sync.sh
bg:
	nohup ./sync.sh &
	sleep 5
	tailf debian.log
dumpmail:
	@python3 dumpmail.py $(SourcesGZ)
stat:
	@python3 stat.py $(SourcesGZ)
who_is_the_most_energetic_dd:
	make dumpmail | sort | uniq -c | sort -n | tac | nl | tac
	# [Rank] [Package count] [Mail]
	# if you want to query your rank, just append "| grep myself"
rank:
	make dumpmail | sort | uniq -c | sort -n | tac | nl | grep $(LOGIN)
	# [Rank] [Package count] [Mail]
dangerous:
	-rm -rf debian/
	-rm debian.log
	-rm nohup.out
