use std::collections::HashMap;

#[allow(non_snake_case)]
fn twoSum(nums: Vec<i64>, target: i64) -> Vec<i64> {
    let mut x2i: HashMap<_, _> = HashMap::new();
    for (i, x) in nums.iter().enumerate() {
        if x2i.contains_key(&(target-x)) {
            return vec!(x2i[&(target-x)], i as i64);
        }
        x2i.insert(x, i as i64);
    }
    vec!(0,0)
}

fn main() {
    let x: Vec<i64> = vec!(2, 7, 11, 15);
    println!("input {:?}", x);
    println!("result {:?}", twoSum(x, 9));
}
