struct Vector {
    x: f32,
    y: f32,
}

trait Norms {
    fn nrm1(&self) -> f32;
    fn nrm2(&self) -> f32;
    fn nrminf(&self) -> f32;
}

impl Norms for Vector {
    fn nrm1(&self) -> f32 {
        self.x.abs() + self.y.abs()
    }
    fn nrm2(&self) -> f32 {
        (self.x.powi(2) + self.y.powi(2)).sqrt()
    }
    fn nrminf(&self) -> f32 {
        self.x.max(self.y)
    }
}

fn main() {
    let v = Vector{ x: 1., y: -2. };
    println!("nrm1 {}", v.nrm1());
    println!("nrm2 {}", v.nrm2());
    println!("nrminf {}", v.nrminf());
}
