#![crate_type = "dylib"]
use std::mem;

#[no_mangle]
pub extern fn square(x: i32) -> i32 {
    x * x
}

#[repr(C)]
pub struct Point {
    x: f64,
    y: f64,
}

#[no_mangle]
pub extern fn move_point(p: Point, x_diff: f64, y_diff: f64) -> Point {
    Point { x: p.x + x_diff, y: p.y + y_diff }
}

#[no_mangle]
pub extern fn move_point_inplace(p: &mut Point, x_diff: f64, y_diff: f64) -> () {
    p.x += x_diff;
    p.y += y_diff;
}

#[repr(C)]
pub struct Slice {
    ptr: *mut i32,
    len: usize,
}

fn vec_return() -> Vec<i32> {
    vec![11, 13, 17, 19, 23, 29]
}

#[no_mangle]
pub extern fn wrapper() -> Slice {
    let mut v = vec_return();
    let p = v.as_mut_ptr();
    let len = v.len();
    mem::forget(v);
    Slice { ptr: p, len: len }
}
