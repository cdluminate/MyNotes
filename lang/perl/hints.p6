#!/usr/bin/perl6
multi infix:<in>(Str $sub, Str $str) { $str.contains: $sub };
say "1" in "123";
