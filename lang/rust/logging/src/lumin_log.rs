/// GLOG-Like screen logging utility
/// 
/// Copyright (C) 2016 Zhou Mo <cdluminate@gmail.com>
/// License: MIT License
/// 
extern crate libc; // dependency: libc="0.2.0"
use self::libc::{pid_t};
use self::libc::{time_t, tm};

// import the part of libc to be used
#[link(name = "c")]
extern {
  // pid_t getpid(void); // <unistd.h>
  fn getpid () -> pid_t;
  // time_t time(time_t *t);
  fn time (t: &mut time_t) -> time_t;
  // struct tm *gmtime(const time_t *timep); // <time.h>
  fn gmtime (timep: &time_t) -> &tm;
}

/// backend: PID
pub fn _lumin_log_getpid () -> String {
  unsafe { getpid() }.to_string()
}

/// backend: mmddhhmmss
pub fn _lumin_log_mmddhhmmss () -> String {
  let t;
  unsafe {
    let mut timep: time_t = 0 as time_t;
    time(&mut timep);
    let ptm: &tm = gmtime(&timep);
    t = (ptm.tm_mon, ptm.tm_mday, ptm.tm_hour, ptm.tm_min, ptm.tm_sec);
  }
  format!("{:02}{:02} {:02}:{:02}:{:02}", t.0, t.1, t.2, t.3, t.4)
}

/// backend: general summary
pub fn _lumin_log_summary (file: &'static str, line: u32) -> String {
  format!("{} {} {}:{}]", _lumin_log_mmddhhmmss(), _lumin_log_getpid(), file, line)
}

/// backend: debug message
pub fn _debug (msg: String, file: &'static str, line: u32) {
  println!("\x1b[36;1mD{} {}\x1b[m", _lumin_log_summary(file, line), msg);
}
/// interface: debug
// borrowed from rust:src/libcollections/macros.rs
#[macro_export]
macro_rules! debug {
  ($($arg:tt)*) => {{
    lumin_log::_debug( (std::fmt::format(format_args!($($arg)*))), file!(), line!());
  }};
}

/// backend: info message
pub fn _info (msg: String, file: &'static str, line: u32) {
  println!("\x1b[32;1mI{} {}\x1b[m", _lumin_log_summary(file, line), msg);
}
/// interface: info
// borrowed from rust:src/libcollections/macros.rs
#[macro_export]
macro_rules! info {
  ($($arg:tt)*) => {{
    lumin_log::_info( (std::fmt::format(format_args!($($arg)*))), file!(), line!());
  }};
}

/// backend: warn message
pub fn _warn (msg: String, file: &'static str, line: u32) {
  println!("\x1b[33;1mW{} {}\x1b[m", _lumin_log_summary(file, line), msg);
}
/// interface: warn
// borrowed from rust:src/libcollections/macros.rs
#[macro_export]
macro_rules! warn {
  ($($arg:tt)*) => {{
    lumin_log::_warn( (std::fmt::format(format_args!($($arg)*))), file!(), line!());
  }};
}

/// backend: error message
pub fn _error (msg: String, file: &'static str, line: u32) {
  println!("\x1b[31;1mE{} {}\x1b[m", _lumin_log_summary(file, line), msg);
}
/// interface: error
// borrowed from rust:src/libcollections/macros.rs
#[macro_export]
macro_rules! error {
  ($($arg:tt)*) => {{
    lumin_log::_error( (std::fmt::format(format_args!($($arg)*))), file!(), line!());
  }};
}

/// backend: fatal message
pub fn _fatal (msg: String, file: &'static str, line: u32) {
  println!("\x1b[35;1mF{} {}\x1b[m", _lumin_log_summary(file, line), msg);
}
/// interface: fatal
// borrowed from rust:src/libcollections/macros.rs
#[macro_export]
macro_rules! fatal {
  ($($arg:tt)*) => {{
    lumin_log::_fatal( (std::fmt::format(format_args!($($arg)*))), file!(), line!());
  }};
}

#[macro_export]
macro_rules! die {
  ($($arg:tt)*) => {{
    lumin_log::_fatal( (std::fmt::format(format_args!($($arg)*))), file!(), line!());
    panic!("panic! due to calling die!() at {}:{}", file!(), line!());
  }};
}

#[cfg(test)]
mod tests {
  #[test]
  fn test_lumin_log_getpid () {
    assert!(super::_lumin_log_getpid() != "".to_string());
  }
  #[test]
  fn test_lumin_log_mmddhhmmss () {
    assert!(super::_lumin_log_mmddhhmmss() != "".to_string());
  }
  #[test]
  fn test_lumin_log_summary () {
    assert!(super::_lumin_log_summary(file!(), line!()) != "".to_string());
  }
  #[test]
  fn test_debug () {
    super::_debug("test_debug".to_string(), file!(), line!());
  }
}
