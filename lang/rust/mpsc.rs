use std::sync::mpsc::channel;
use std::thread;

enum Transaction {
    Withdrawl(f64),
    Deposit(f64),
}

fn main() {
    let n_customers = 10;
    let (customers, banker) = channel();
    let handles = (0..n_customers).into_iter().map(|i| {
        let customer = customers.clone();
        let handle = thread::spawn(move || {
            let trans_type = match i % 2 {
                0 => Transaction::Deposit(i as f64 * 10.0),
                _ => Transaction::Withdrawl(i as f64 * 5.0),
            };
            customer.send(trans_type).unwrap();
        });
        handle
    }).collect::<Vec<thread::JoinHandle<_>>>();

    for handle in handles {
        handle.join().unwrap()
    }

    let bank = thread::spawn(move || {
        let mut bank: f64 = 10000.0;
        banker.into_iter().for_each(|i| {
            match i {
                Transaction::Withdrawl(amount) => {
                    bank = bank - amount;
                },
                Transaction::Deposit(amount) => {
                    bank = bank + amount;
                },
            }
            println!("Bank value: {}", bank);
        });
    });
    bank.join().unwrap();
}
