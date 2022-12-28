use Terminal::ANSIColor;  # zef install Terminal::ANSIColor
for ^5 {
	$_ %% 2 ?? print color('red'), $_, color('reset') !! print $_;
}
print "\n";
