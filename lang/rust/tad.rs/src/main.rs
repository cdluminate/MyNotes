mod blis;
use crate::blis::*;

fn main() {
    println!("Hello, world!");

    let xs: [f32; 4] = [1., 2., 3., 4.];
    let mut ys: [f32; 4] = [0.; 4];

    let mut s: f32 = 0.;

    unsafe {
        bli_sasumv(4, &xs[0], 1, &mut s);
    }

    for i in xs.iter() {
        println!("{}", i);
    }

    println!("{}", s);

    unsafe {
        bli_saddv(b'N', 4, &xs[0], 1, &mut ys[0], 1);
        bli_saddv(b'N', 4, &xs[0], 1, &mut ys[0], 1);
    }
    for i in ys.iter() {
        println!("{}", i);
    }
}
