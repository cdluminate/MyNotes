#!/usr/bin/perl
# http://blob.perl.org/books/impatient-perl/iperl.htm
use strict;
use warnings;

print "Hello world\n";

# perl has 3 basic storage types: scalar, array, and hash
# scalar can store strings, numbers, references and file handles

my $name = 'John';
print "name is $name\n";

my ($first,$last) = qw(John Doe);
my $mystr = "first=$first, last=$last\n";
print $mystr;
chomp $mystr; # remove newline
print $mystr . "\n"; # concat
print "." x 32 . "\n"; # repeat
print length($mystr);

my ($a, $b, $c) = split(/ /, "aa bb cc");
print $a, $c;

print join('.', 'a', 'b', 'c');

my $longstring = << "EOF";
verbatim mode
EOF

warn $longstring;

print "\n", abs(-3.4), int(9.9);
my $mystr = sprintf("%.1f", 1.111);
print "$mystr\n";
print 2**10, sqrt(1024), "\n";

print rand, rand(10);

my $a = 999.1 + ''; # to-string
my $b = '888.1' + 0; # to-number
print "$a $b \n";

if (rand gt 0.5 && 1) {
	print "Foobar!\n";
} elsif (rand > 0.5) {
	print "Second try succeed!\n";
} else {
	print "Oops!\n";
}
my $result = rand > 0.9 ? 1 : 0;
my $result_reference = \$result;
print $$result_reference; # dereference

sub mysub {
	my ($left,$right) = @_;
	$left ||= 1.0;
	$right = $right || 2.0;
}

open(my $fp, ">out.txt");
print $fp "hello!\n";
close($fp);

# array is one-dimensional only. index starts at 0.
#
my @Ns = qw( 0 1 2 3 4 );
print $Ns[1], $Ns[-1], scalar(@Ns);
push(@Ns, 5); push(@Ns, qw(6 7 8));
pop(@Ns); shift(@Ns); unshift(@Ns, -1);

foreach my $i (@Ns) {
	print $i, "\n";
}
my @sorted = sort(@Ns);
print @sorted;
my @numerically_sorted = sort{$a <=> $b}(@Ns);
print reverse(@Ns);

# hashes are preceded with a percent sign sigil.
# perl hashes are one-dimensional only.
my %info = qw(name John age 42);
$info{address} = 'earth';
delete($info{address});
print keys(%info), values(%info);
print $info{name}, exists($info{invalidkey})?1:0;

while (my($k, $v)=each(%info)) {
	print "k=$k,v=$v\n";
}
print reverse(%info);

# list context
my @cart1 = qw(milk bread);
my @cart2 = qw(eggs bacon);
my @checkout_counter = (@cart1, @cart2);
print join(' ', @checkout_counter);

#
sub foobar {
print caller(0);
}
foobar;

#
foreach my $v (@INC) {
	print "$v\n";
}

#
print glob("~/withlinux/*"), <~/withlinux/*>;
my @files = glob("./*");

# cmd args
print join("\t", @ARGV);

# io
open(my $fp, "impatient.pl") or die "cannot open file";
while (<$fp>) {
	if (/foobar/) {
		print $_;
	}
}
if (-x "impatient.pl") {
	print "executable!\n";
}

# find
use File::Find;

# os commands
my $retval = system("ls"); # catches return value
print $retval, `ls`; # catches stdout

# perl regular expressions
# match m{}; substitute s{}{}; transliterate tr{}{};
# =~ match; !~ unmatch
# /patt/  is equivalant to  $_ =~ m/patt/

# done
