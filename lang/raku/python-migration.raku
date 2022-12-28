put "hello, world!";

my Str $planet = 'earth';
say "hello, $planet, {1+2}";  # double-quotes allow interpolation

my @l = 1,2,3;  # holds an array
say @l[0], "\t", @l[2]; # 0-indexed

my %d = a => 12, b => 13;  # holds an hash
say %d<a>, "\t", %d{'a'};

my \pi = 3.14;  # sigilless is immutable
say pi;

my \x = 10;
for 1, 2, 3 -> \x {
	say x;  # another scope
}
say x;  # still 10

my $lambda = -> $i { $i + 12 }
say $lambda(1);
my $lambda2 = * + 12;  # in this lambda expression, * is positional placeholder
say $lambda2(1);

for ^5 -> $i {
	next if $i == 2;  # continue
	last if $i == 3;  # break
	say $i;
}

my @elems = <neutronium hydrogen helium lithium>;
for @elems.kv -> $i, $e {
	say "elem no. $i is $e";
}
my @symbols = <n H He Li>;
my %elem-for-symbol;
%elem-for-symbol{@symbols} = @elems;
for %elem-for-symbol.kv -> $symbol, $element {  # iteration order differs from python
	say "symbol $symbol stands for $element";
}

sub add($a, $b) {
	$a + $b
}
say add(1, 2);

multi sub speak($word, $times) {  # positional parameters
	say $word for ^$times;
}
multi sub speak(:$word, :$times) {  # named parameters, multiple dispatch
	speak($word, $times);
}
speak(word => "hi", times => 2);
speak(:word<hi>, :times<2>);

say ($_ * 2 for ^5);  # list comprehension
my @ll = ($_ ** 2 if $_ % 2 == 0 for ^5);
say @ll;

say ({$_[0] + $_[1]} for (1,2) X (3,4)); # X means cross-product
say (-> (\i, \j) {i+j} for (1,2) X (3,4));

class Animal {
	method jump {
		say "$.name is jumping";
	}
}
class Dog is Animal {
	my $kind = 'canine';
	method kind {$kind};
	has $.name is rw;
}

my $d = Dog.new(name => 'Fido');
say $d.name;
$d.jump;

sub world {
	say "world";
}
&world.wrap(sub () {
	say "hello";
	callsame;
}); # this is python's decorator
world;

multi sub trait_mod:<is>(Routine $r, :$greeter) {
	$r.wrap(sub {
		print 'hello, '.gist;
		callsame;
	})
}
sub world2 is greeter {
	say 'world';
}
world2;
