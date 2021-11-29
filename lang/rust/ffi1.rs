
extern {
  // write(2): ssize_t write(int fd, const void *buf, size_t count);
  fn write(fd: i32, data: *const u8, len: usize) -> usize;
}

fn main() {
  let data = b"Hello, world!\n";
  unsafe {
    write(1, &data[0], data.len());
  }
}
