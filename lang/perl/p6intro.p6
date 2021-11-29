#!/usr/bin/perl6
use v6;
=begin comment
multiline document looks like this
perl6 looks quite different from perl5.
perl6 supports mutli-dimensional array.
perl6 supports explicit type declaration.
=end comment
# https://perl6intro.com
say 'hello' if True;
my $kebab-case-var = 1;

my @animals = 'camel', 'llama', 'owl';
@animals.push('cat');
say 'there are ' ~ @animals.elems ~ " animals";
for @animals.sort -> $i {
	print "$i\n";
}
loop (my $j = 0; $j < 4; $j++) {
	say "$j, @animals[$j]";
}

my %info = (Name => "John", Age => 42);
%info.push: (Address => "London");
say %info.keys, %info.values, %info.kv;

my Str $var = "Text";
my Int $foo := 123; # immutable

my $age = 42;
if $age > 18 {
	say "Hi!";
} elsif $age > 32 {
	say "Hii!";
} else {
	say "Hello!";
}
given $age {
	when 0..10 { say "[0,10]" }
	when Int { say "Int" }
	when 42 { say 42 }
	default { say "???" }
}

#my $name = prompt "hi> ";
run 'echo', 'hello!'; # without involving a shell
shell 'ls'; # pass everything to shell

my $data = slurp "p6intro.p6";
spurt "out.txt", "HELLO\n";
say "out.txt".IO.e, "out.txt".IO.f;

sub say-hello (Str $name?, $title="Dr.") {
	say "Hello " ~ $title ~ $name ~ "!!!";
}
say-hello;
say-hello "Paul";

multi greet($name) {
	say "good morning $name";
}
multi greet($name, $title) {
	say "good morning $title $name";
}

sub squared($x) returns Int {
	$x ** 2;
}
say squared(4);
my @ns = <1 2 3 4 5>;
say map(&squared, @ns);
say map(-> $x {$x ** 2}, @ns);

my @array = <0 1 2 3 4 5 6 7 8 9 10>;
sub is-even($var) { $var %% 2 };
say @array>>.is-prime;
say @array>>.&is-even;

my $var = 2;
if $var == 1|2|3 {
  say "The variable is 1 or 2 or 3"
}

my $lazylist = (1 ... 10);
say $lazylist;

sub greeting-generator($period) {
  return sub ($name) {
    return "Good $period $name"
  }
}
my $morning = greeting-generator("Morning");
my $evening = greeting-generator("Evening");
say $morning("John");
say $evening("Jane");

if 'name@company.com' ~~ m/ "@" / {
    say "This is a valid email address because it contains an @ character";
}

my $α = 1;

say @array.race.map({ is-prime $_ });
say @array.hyper.map({ is-prime $_ });
.say for @array;

constant $LIBPATH="$*CWD";
say $LIBPATH;

#die "Error!";
