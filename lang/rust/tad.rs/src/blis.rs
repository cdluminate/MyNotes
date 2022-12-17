extern crate libc;
use libc::*;

#[allow(dead_code)]
#[link(name="blis")]
extern "C" {
    /* https://github.com/flame/blis/blob/master/docs/BLISTypedAPI.md
     */
    // level-1v functions
    pub fn bli_saddv(conjx: u8, n: c_int,
                     x: *const c_float, incx: c_int,
                     y: *mut c_float, incy: c_int);
    
    pub fn bli_samaxv(n: c_int, x: *const c_float, incx: c_int,
                      index: *mut c_int);
   
    // utility operations
    pub fn bli_sasumv(n: c_int, x: *const c_float, incx: c_int,
                      asum: *mut c_float);
}
