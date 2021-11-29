fn fib(i: i32) -> i32 {
    match i {
        0 | 1 => 1,
        _ => fib(i-1) + fib(i-2),
    }
}

fn main() {
    println!("{}", fib(1));
    println!("{}", fib(8));
}

