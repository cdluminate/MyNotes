// one-line comment
/*
 * block of commnet
 */

struct Structure(i32);

impl std::fmt::Display for Structure {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        write!(f, "{}", self.0)
    }
}

#[derive(Debug)]
struct Point2D {
    x: f64, y:f64,
}

/// generate docs for the following item
// //! generate docs for the enclosing item
fn main() {
    println!("Hello world!");

    let x = 5 + /* 90 + */ 5;
    println!("x is {}", x);

    eprintln!("this prints to stderr");
    print!("you have to add the new line character by your self\n");

    // formatted print
    println!("{} days", 31);
    println!("{a}, {b}", a="a", b="b");
    println!("{:?}", "a"); // :? marker is used for debugging
    println!("{:#?}", "a"); // :#? marker is used for pretty print

    // print structure
    println!("{}", Structure(100));
    println!("{:#?}", Point2D{x: 1., y: 2.});
}
