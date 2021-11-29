impl Solution {
    pub fn remove_duplicates(nums: &mut Vec<i32>) -> i32 {
        let mut idx: usize = 0;
        for j in &mut nums {
            if j != nums[idx] {
                idx += 1;
                nums[idx] = j;
            }
        }
        return (idx + 1) as i32;
    }
}
