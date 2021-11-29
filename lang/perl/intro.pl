#!/usr/bin/perl
use strict;
use warnings;

# basic syntax
print "Perl quick Introduction\n";
print "Reference: http://perldoc.perl.org/perlintro.html\n"; print 'in this case \n is not excaped';
print "\n";
print 42, "\n";
print ("hello perl, you can omit parentheses.\n");

# variables
print " -- [scalar variable] --\n";
my $animal = "camel";
my $answer = 42;
print $animal;
print "The animal is $animal\n";
print "The square of $answer is ", $answer * $answer, "\n";

print " -- [array] --\n";
my @animals = ("camel", "llama", "owl");
my @numbers = (23, 42, 69);
my @mixed   = ("camel", 42, 1.23);
print $animals[0];              # prints "camel"
print $animals[1];              # prints "llama"
print $mixed[$#mixed];       # last element, prints 1.23
print "\n";
if (@animals < 5) {
  print "array @animals < 5\n";
}
print @animals[0,1], "\n";
print @animals[0..2], "\n";
print @animals[1..$#animals], "\n"; # slicing operation

my @sorted = sort @animals;
my @backwards = reverse @numbers;
print @sorted, "\n";
print @backwards, "\n";

my %fruit_color_simple = ("apple", "red", "banana", "yellow"); # hashes
my %fruit_color = (
  apple => "red",
  banana => "yellow",
);
print %fruit_color, "\n";
print $fruit_color{"apple"}, "\n";
my @fruits = keys %fruit_color; # get keys of the hash table
my @colors = values %fruit_color; # get values from the hash table

# variable scoping
## my $var = "value"; # create a local variable
## $var = "value";    # create a global variable

# conditional and loop constructs

##if ( condition ) {
##  ...
##} elsif ( condition2 ) {
##  ...
##} else {
##  ...
##}

##unless ( condition ) {
##  ... 
##}
##equivalant to 
##if (! condition ) { ... }

## if ($zippy) {
##     print "Yow!"; // traditional way
## }
## print "Yow!" if $zippy; // perlish
## print "We have no bananas" unless $bananas; // perlish

## while (condition) { ... }
## until (condition) { ... }
## print "hello" while 1;

print "For-loop\n";
my $i;
for ($i = 0; $i < 10; $i++) {
  print "$i\n";
}

foreach (@animals) {
  print "This is $_\n";
}

foreach my $key (keys %fruit_color) {
  print "The value of $key is $fruit_color{$key}\n";
}

# built in operators and functions
# eq, ne, lt, gt, le, ge are for string comparison
# . is for string concatenation
# x is for string multiplication
# .. is range operator

# files and I/O
open(my $in, "<", "input.txt")   or die "missing input.txt: $!";
open(my $out, ">", "output.txt") or die "cannot open output.txt: $!";
open(my $log, ">>", "my.log")    or die "cannot open my.log: $!";

my $line = <$in>; # this reads a line
my @lines = <$in>; # this reads lines into a list

seek($in, 0, 0);
while (<$in>) { # assign each line to $_
  print "read: $_";
}

print STDERR "print to stderr\n";
print $out "print to out\n";
print $log "print to log\n";

close $in or die "in: $!";
close $out or die "out: $!";
close $log or die "log: $!";

# regular expressions
print "--[ regular expressions ]--\n";
my $msg = "hello world";
if ($msg =~ /hello/) { # simple match
  print "variable \$msg contains hello\n";
}
$msg =~ s/world/perl/; # replace one instance
print "$msg\n";
$msg =~ s/l/x/g; # global replace
print "$msg\n";
# more complex regular expressions
#     .                   a single character
#     \s                  a whitespace character (space, tab, newline, ...)
#     \S                  non-whitespace character
#     \d                  a digit (0-9)
#     \D                  a non-digit
#     \w                  a word character (a-z, A-Z, 0-9, _)
#     \W                  a non-word character
#     [aeiou]             matches a single character in the given set
#     [^aeiou]            matches a single character outside the given set
#     (foo|bar|baz)       matches any of the alternatives specified
#     ^                   start of string
#     $                   end of string
#
#     *                   zero or more of the previous thing
#     +                   one or more of the previous thing
#     ?                   zero or one of the previous thing
#     {3}                 matches exactly 3 of the previous thing
#     {3,6}               matches between 3 and 6 of the previous thing
#     {3,}                matches 3 or more of the previous thing
#
#     /^\d+/              string starts with one or more digits
#     /^$/                nothing in the string (start and end are
#                         adjacent)
#     /(\d\s){3}/         three digits, each followed by a whitespace
#                                              character (eg "3 4 5 ")
#      /(a.)+/             matches a string in which every odd-numbered
#                                              letter is a (eg "abacadaf")
#      # This loop reads from STDIN, and prints non-blank lines:
#      while (<>) {
#              next if /^$/;
#         print;
#     }

my $email = "user\@example.org";
if ($email =~ /([^@]+)@(.+)/) {
  print "username $1\n";
  print "hostname $2\n";
}

# subroutines
sub logger {
  my $logmessage = shift;
  open my $logfile, ">>", "my.log" or die "Could not open my.log: $!";
  print $logfile $logmessage;
}

logger("We have a logger subroutine!");

sub square {
    my $num = shift;
    my $result = $num * $num;
    return $result;
}

my $sq = square(8);
