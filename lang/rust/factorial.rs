
fn factorial (n: i64) -> i64
{
    match n {
        0 | 1 => 1,
        _ => n * factorial(n-1),
    }
}

fn main ()
{
    println!("factorial calculation");
    println!("{}", factorial(4));
}
