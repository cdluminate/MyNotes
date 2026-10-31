say [+] (1..^1000).grep(* %% (3|5));

sub sum-multiples(Int $k, Int $limit = 999) {
    my $n = $limit div $k;
    $k * $n * ($n + 1) div 2
}
say sum-multiples(3) + sum-multiples(5) - sum-multiples(15);
