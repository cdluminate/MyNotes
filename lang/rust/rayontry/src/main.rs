use rayon::prelude::*;
use std::ops::Mul;

fn factorial(n: u64) -> u64 {
    (1..n + 1).into_iter()
        .map(u64::from)
        .fold(1 as u64, Mul::mul)
}

fn factorial_parallel(n: u64) -> u64 {
    (1..n + 1).into_par_iter()
        .map(u64::from)
        .reduce_with(Mul::mul).unwrap()
}

fn main() {
    println!("{}", factorial(5));
    println!("{}", factorial_parallel(5));
}
