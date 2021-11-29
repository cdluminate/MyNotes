#[macro_use]
mod lumin_log;

fn main () {
  debug!("This is a {} message.", "Debug");
  info!("This is a {} message.", "Info");
  warn!("This is a {} message.", "Warn");
  error!("This is a {} message.", "Error");
  fatal!("This is a {} message.", "Fatal");
  die!("this program should panic and dump backtrace");
}
