use std::sync::{Arc, Mutex};
use std::thread;

const N: usize = 10;

fn main() {
    let safe_data = Arc::new(Mutex::new(0));
    println!("Data: {:?}", safe_data);

    let handles = (0..N).into_iter().map(|_| {
        let data = Arc::clone(&safe_data);
        thread::spawn(move || {
            let mut data = data.lock().unwrap();
            *data += 1;
        })
    })
    .collect::<Vec<thread::JoinHandle<_>>>();

    for thread in handles {
        thread.join().unwrap();
    }

    println!("Data: {:?}", safe_data);
}
