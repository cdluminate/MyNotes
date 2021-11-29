// Reference: http://rustbyexample.com/index.html (* this)
// Reference: https://doc.rust-lang.org/book/
// Reference: https://wayslog.gitbooks.io/rustprimer/content/

fn main () {
  helloworld();
  comments();
  formatted_print();

  primitives();
  literals_and_operators();
  tuples();
  arrays_and_slices();

  structures();
  enums();
  constants();

  variable_binding();

  debug("Debug Message");
}

// 0. Customization: screen logging util
fn debug (msg:&'static str) {
  use std::time::SystemTime;
  let now = SystemTime::now();
  println!("\x1b[1;36mD {:?} {file}:{line}] {msg}\x1b[m",
    now,
    file=file!(),
    line=line!(),
    msg=msg);
}

// 1. Hello world

// This is comment
// compile this rust source with command
//   $ rustc hello.rs
fn helloworld () {
  println! ("Hello world!"); // println! is a macro
}

// 1.1 Comments

fn comments () {
  //  // single-line comment
  //  /* block comments */
  //  /// (Doc comment) generate lib doc for the following item
  //  //! (Doc comment) generate lib doc for the enclosing item
  let x = 5 + /* 90 + */ 5;
  println! ("var 'x' ? x = {}", x);
}

// 1.2 Formatted print

fn formatted_print () {
  // format! : write formatted text to String
  // print!  : write formatted text to console
  // println!: write formatted text to console, and append a newline

  println! ("{} days", 31); // general case
  println! ("{0}, this is {1}. {1}, this is {0}", "Alice", "Bob"); // positional arguments
  println! ("{subject} {verb} {object}.", subject="I", verb="eat", object="apple"); // named arguments
  println! ("dec {} and binary {:b}", 2, 2); // binary
  println! ("right-align {number:>width$}", number=1, width=7); // right align
  println! ("right-align + padding {number:>0width$}", number=1, width=7); // padding
  println! ("My name is {1} {0}.", "Bond", "James"); // argcheck when "James" is missing
  // struct Structure(i32); // name a structure "Structure"
    // but as an argument to print functions this structure won't work.
  println! ("{:?}", "debugging purpose");

  // 1.2.1 Debug
  // struct UnPrintable(i32); // won't be printable via fmt::Display or fmt::Debug
  // #[derive(Debug)]
  // struct DebugPrintable(i32); // printable via fmt::Debug
  #[derive(Debug)]
  struct Structure(i32);
  #[derive(Debug)]
  struct Deep(Structure);

  println!("{:?} months in a year.", 12);
  println!("{1:?} {0:?} is the {actor:?} name.", "Slater", "Christian", actor="actor's");
  println!("Now {:?} will print!", Structure(3));
  println!("Now {:?} will print!", Deep(Structure(7))); // manually implementing fmt::Display can make output elegant

  // 1.2.2 Display
  use std::fmt;
  impl fmt::Display for Structure {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
      write!(f, "({})", self.0)
    }
  }
  println! ("{} is now printed elegantly", Structure(123));

  #[derive(Debug)]
  struct MinMax(i64, i64);
  impl fmt::Display for MinMax {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
      // Use `self.number` to refer to each positional data point.
      write!(f, "({}, {})", self.0, self.1)
    }
  }
  println! ("display MinMax {}", MinMax(123,321));
  println! ("debug MinMax {:?}", MinMax(123,321));

  #[derive(Debug)]
  struct Point2 { x: f64, y: f64, }
  impl fmt::Display for Point2 {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
      // Customize so only `x` and `y` are denoted.
      write!(f, "x: {}, y: {}", self.x, self.y)
    }
  }
  println! ("display Point2 {}", Point2{x: 1.1, y: 2.2});
  println! ("debug Point2 {:?}", Point2{x: 1.1, y: 2.2});

  // 1.2.2.1 Testcase: list
  struct List(Vec<i32>);
  impl fmt::Display for List {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
      let List(ref vec) = *self;
      try!(write!(f, "["));
      for (count, v) in vec.iter().enumerate() {
        if count != 0 { try!(write!(f, ", ")); }
        try!(write!(f, "{}:{}", count, v));
      }
      write!(f, "]")
    }
  }
  let v = List(vec![1, 2, 3]);
  println!("{}", v);

  // 1.2.3 Formatting
  struct City { name: &'static str, lat: f32, lon: f32, }
  impl fmt::Display for City {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
      let lat_c = if self.lat >= 0.0 { 'N' } else { 'S' };
      let lon_c = if self.lon >= 0.0 { 'E' } else { 'W' };
      write!(f, "{}: {:.3}°{} {:.3}°{}",
        self.name, self.lat.abs(), lat_c, self.lon.abs(), lon_c)
    }
  }
  for city in [
      City { name: "Dublin", lat: 53.347778, lon: -6.259722 },
      City { name: "Oslo", lat: 59.95, lon: 10.75 },
      City { name: "Vancouver", lat: 49.25, lon: -123.1 },
  ].iter() {
      println!("{}", *city);
  }

  #[derive(Debug)]
  struct Color { red: u8, green: u8, blue: u8, }
  impl fmt::Display for Color {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
      write!(f, "RGB({}, {}, {}) 0x{:02X}{:02X}{:02X}",
        self.red, self.green, self.blue, self.red, self.green, self.blue)
    }
  }
  for color in [
      Color { red: 128, green: 255, blue: 90 },
      Color { red: 0, green: 3, blue: 254 },
      Color { red: 0, green: 0, blue: 0 },
  ].iter() {
      println!("{:?}", *color);
      println!("{}", *color);
  }
}

// 2. Primitives

fn primitives () {
  let logical: bool = true;
  let a_float: f64 = 1.0;  // Regular annotation
  let an_integer   = 5i32; // Suffix annotation
  let default_float   = 3.0; // `f64`
  let default_integer = 7;   // `i32`
  let mut mutable = 12; // Mutable `i32`.
  // Error! The type of a variable can't be changed
  // mutable = true;
  // char is unicode scalar
}

// 2.1
fn literals_and_operators () {
  println!("1 + 2 = {}", 1u32 + 2);
  println!("1 - 2 = {}", 1i32 - 2);
  println!("true AND false is {}", true && false);
  println!("true OR false is {}", true || false);
  println!("NOT true is {}", !true);
  println!("0011 AND 0101 is {:04b}", 0b0011u32 & 0b0101);
  println!("0011 OR 0101 is {:04b}", 0b0011u32 | 0b0101);
  println!("0011 XOR 0101 is {:04b}", 0b0011u32 ^ 0b0101);
  println!("1 << 5 is {}", 1u32 << 5);
  println!("0x80 >> 2 is 0x{:x}", 0x80u32 >> 2);
  println!("One million is written as {}", 1_000_000u32);
}

// 2.2
fn tuples () {
  fn reverse(pair: (i32, bool)) -> (bool, i32) {
    let (integer, boolean) = pair;
    (boolean, integer)
  }
  #[derive(Debug)]
  struct Matrix(f32, f32, f32, f32);
  let long_tuple = (1u8, 2u16, 3u32, 4u64, -1i8, -2i16, -3i32, -4i64,
                      0.1f32, 0.2f64, 'a', true);
  println!("long tuple first value: {}", long_tuple.0);
  println!("long tuple second value: {}", long_tuple.1);
  let tuple_of_tuples = ((1u8, 2u16, 2u32), (4u64, -1i8), -2i16);
  println!("tuple of tuples: {:?}", tuple_of_tuples);
  let pair = (1, true);
  println!("pair is {:?}", pair);
  println!("the reversed pair is {:?}", reverse(pair));
  println!("one element tuple: {:?}", (5u32,));
  println!("just an integer: {:?}", (5u32));
  let tuple = (1, "hello", 4.5, true);
  let (a, b, c, d) = tuple; // create bindings
  println!("{:?}, {:?}, {:?}, {:?}", a, b, c, d);

  let matrix = Matrix(1.1, 1.2, 2.1, 2.2);
  println!("{:?}", matrix)
}

// 2.3
fn arrays_and_slices () {
  use std::mem;

  fn analyze_slice(slice: &[i32]) {
    println!("first element of the slice: {}", slice[0]);
    println!("the slice has {} elements", slice.len());
  }
  let xs: [i32; 5] = [1, 2, 3, 4, 5];
  let ys: [i32; 500] = [0; 500]; // initialize all elements as 0
  println!("first element of the array: {}", xs[0]); // index starts from 0
  println!("second element of the array: {}", xs[1]);
  println!("array size: {}", xs.len());
  println!("array occupies {} bytes", mem::size_of_val(&xs)); // arrays allocated on stack
  println!("borrow the whole array as a slice");
  analyze_slice(&xs);
  println!("borrow a section of the array as a slice");
  analyze_slice(&ys[1 .. 4]);
  // Out of bound indexing yields a panic
  // println!("{}", xs[5]);
}

// 3 Custome types
// struct, enum, const, static

// 3.1 Structures
fn structures () {
  struct Nil;
  struct Pair(i32, f64); // tuple struct
  struct Point { // structure with 2 fields
    x: f64,
    y: f64,
  }
  #[allow(dead_code)]
  struct Rectangle { // reuse Point
    p1: Point,
    p2: Point,
  }
  let point: Point = Point { x: 0.3, y: 0.4 }; // point instance
  println!("point coordinates: ({}, {})", point.x, point.y);
  let Point { x: my_x, y: my_y } = point; // Destructure the point using a `let` binding
  let _rectangle = Rectangle {
    p1: Point { x: my_y, y: my_x },
    p2: point,
  };
  let _nil = Nil;
  let pair = Pair(1, 0.1);
  let Pair(integer, decimal) = pair;
  println!("pair contains {:?} and {:?}", integer, decimal);
}

// 3.2 Enums
fn enums () {
  enum Person {
    Engineer,
    Scientist,
    Height(i32),
    Weight(i32),
    Info { name: String, height: i32 }
  }

  fn inspect(p: Person) {
    // Usage of an `enum` must cover all cases (irrefutable)
    // so a `match` is used to branch over it.
    match p {
        Person::Engineer  => println!("Is an engineer!"),
        Person::Scientist => println!("Is a scientist!"),
        // Destructure `i` from inside the `enum`.
        Person::Height(i) => println!("Has a height of {}.", i),
        Person::Weight(i) => println!("Has a weight of {}.", i),
        // Destructure `Info` into `name` and `height`.
        Person::Info { name, height } => { println!("{} is {} tall!", name, height); },
    }
  }
  let person   = Person::Height(18);
  let amira    = Person::Weight(10);
  // `to_owned()` creates an owned `String` from a string slice.
  let dave     = Person::Info { name: "Dave".to_owned(), height: 72 };
  let rebecca  = Person::Scientist;
  let rohan    = Person::Engineer;
  inspect(person);
  inspect(amira);
  inspect(dave);
  inspect(rebecca);
  inspect(rohan);
  println! ("{}", 32 as i32);

  // 3.2.3 Testcase: linked-list
  enum List {
    Cons(u32, Box<List>),
    Nil,
  }
  // methods can be attached to enum
  impl List {
    fn new() -> List {
        List::Nil // `Nil` has type `List`
    }
    fn prepend(self, elem: u32) -> List {
        List::Cons(elem, Box::new(self))
    }
    fn len(&self) -> u32 {
        match *self {
            List::Cons(_, ref tail) => 1 + tail.len(),
            List::Nil => 0
        }
    }
    fn stringify(&self) -> String {
        match *self {
            List::Cons(head, ref tail) => { format!("{}, {}", head, tail.stringify()) },
            List::Nil => { format!("Nil") },
        }
    }
  } // impl List
  let mut list = List::new();
  list = list.prepend(1);
  list = list.prepend(2);
  list = list.prepend(3);
  println!("linked list has length: {}", list.len());
  println!("{}", list.stringify());
}

// 3.3 Constants
static LANGUAGE: &'static str = "Rust";
const  THRESHOLD: i32 = 10;
fn constants () {
  fn is_big(n: i32) -> bool {
      // Access constant in some function
      n > THRESHOLD
  }
  let n = 16;
  println!("This is {}", LANGUAGE);
  println!("The threshold is {}", THRESHOLD);
  println!("{} is {}", n, if is_big(n) { "big" } else { "small" });
}

// 4. Variable binding
fn variable_binding () {

  // 4.1 mutable
  let _immutable_binding = 1; // fails when .. += 1
  let mut mutable_binding = 1; // ok when .. += 1
  println!("Before mutation: {}", mutable_binding);
  mutable_binding += 1;
  println!("After mutation: {}", mutable_binding);

  // 4.2 scope and shadowing
  let long_lived_binding = 1;
  {
    let short_lived_binding = 2;
    println!("inner short: {}", short_lived_binding);
    let long_lived_binding = 5_f32; // shadows the outer one
    println!("inner long: {}", long_lived_binding);
  }
  //  println!("outer short: {}", short_lived_binding); // not exists
  println!("outer long: {}", long_lived_binding);
  let long_lived_binding = 'a'; // shadows the previous binding
  println!("outer long: {}", long_lived_binding);

  // 4.3 Declare first
  // The compiler forbids use of uninitialized variable 
}
