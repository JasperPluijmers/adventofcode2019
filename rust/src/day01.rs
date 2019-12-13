use std::fs::File;
use std::io::{BufReader, BufRead};

pub fn calculatetotalmass(){
    let filename = "src/input1.txt";
    let file = File::open(filename).unwrap();
    let reader = BufReader::new(file);
    let mut sum: i32 = 0;
    for (index, line) in reader.lines().enumerate() {
        let line = line.unwrap();
        println!("{}. {}, {}", index + 1, line, calculate_mass(&line));
        sum += calculate_mass(&line);
    }
    println!("{}", sum)
}

fn calculate_mass(mass: &str) -> i32 {
    let massnumber: i32 = mass.parse().unwrap();
    return massnumber/3 -2
}