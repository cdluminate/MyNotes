export CXXFLAGS += -Wall -Wpedantic -std=c++11 -O2 -fPIE -pie -fstack-protector-strong -Wformat -Werror=format-security
export CPPFLAGS += -Wdate-time -D_FORTIFY_SOURCE=2
export LDFLAGS  += -Wl,-z,relro -Wl,-z,now
# Query system flags with e.g. dpkg-buildflags --get CFLAGS

main:
	@parallel 'printf " CXX %s\n" {} ; $(CXX) $(CPPFLAGS) $(CXXFLAGS) $(LDFLAGS) {} -o {.}.elf' ::: *.cc
	# TODO: compile those cc sources without a main function into object files
	# with an common header.

compile:
	sh compile.sh # FIXME

test:
	@for TESTBIN in $(shell ls *.elf); do \
		echo --------------- TEST $$TESTBIN --------------------; \
		./$$TESTBIN < /dev/null; \
	   	done
	# TODO: collect return value

clean:
	$(RM) *.elf

pdf:
	python3 z.genbook.py
	evince *.pdf

.PHONY: main test clean pdf

#SRC=$(ls *.cc)
#CXX=g++
#main: compile_all_parallel
#compile_all_serial:
#	@for X in $(shell ls *.cc); do \
#		printf " CC %s\n" $$X; \
#	   	$(CXX) -g -Wall -std=c++11 "$$X" -o "$$X.elf"; \
#   	done
#compile_all_parallel:
#	# Compiling sources in parallel using GNU parallel
#	@parallel 'printf " CC %s\n" {} ; $(CXX) -g -Wall -std=c++11 {} -o {.}.elf' ::: *.cc
#	# Done
#clean:
#	-$(RM) *.elf
#%.elf:
#	$(CXX) -g -Wall -std=c++11 $(patsubst %.elf,%.cc,$@) -o $@
