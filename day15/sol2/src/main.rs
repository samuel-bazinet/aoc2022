use std::{
    path::Path, 
    io::{
        self,
        BufRead,
    }, 
    fs::File,
    thread, 
    sync::Arc,
};

fn dist(x_a: i32, y_a: i32, x_b: i32, y_b: i32) -> u32 {
    x_a.abs_diff(x_b) + y_a.abs_diff(y_b)
}

fn dist_tuple(tuple_a: &(i32, i32), tuple_b: &(i32, i32)) -> u32 {
    dist(tuple_a.0, tuple_a.1, tuple_b.0, tuple_b.1)
}

fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where
    P: AsRef<Path>,
{
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}

fn str_num(string: &mut String) -> i32 {
    string.pop();
    string.remove(0);
    string.remove(0);
    string.parse::<i32>().unwrap()
}

fn str_num_no_pop(string: &mut String) -> i32 {
    string.remove(0);
    string.remove(0);
    string.parse::<i32>().unwrap()
}

fn get_sensors(filename: &str) -> Vec<(((i32, i32), (i32, i32)), u32)> {
    let mut output = vec![];
    if let Ok(lines) = read_lines(filename) {
        for line_attempt in lines {
            if let Ok(line) = line_attempt {
                let mut line: Vec<String> = line.split(' ').map(|x| x.to_owned()).collect();
                let sensor = (str_num(&mut line[2]), str_num(&mut line[3]));
                let beacon = (str_num(&mut line[8]), str_num_no_pop(&mut line[9]));
                output.push(((sensor, beacon), dist_tuple(&sensor, &beacon)));
            }
        }
    }
    return output;
}

fn part_2_old(max_x: i32, max_y: i32, pairs: Vec<(((i32, i32), (i32, i32)), u32)>) {
    for x in 0..=max_x {
        for y in 0..=max_y {
            let mut good = true;
            for s in pairs.iter() {
                let new_dist = dist_tuple(&(x, y), &s.0.0);
                let d = s.1;
                if new_dist <= d{
                    good = false;
                    break; 
                }
            }
            if good {
                println!("Answer = {}, x: {}, y: {}", x*4000000+y, x, y);
            }
        }
    }
}

fn possible(x: i32, y: i32, pairs: &Vec<(((i32, i32), (i32, i32)), u32)>) -> bool {
    for i in pairs.iter() {
        let sx = ((i.0).0).0;
        let sy = ((i.0).0).1;
        let d = i.1;
        if x.abs_diff(sx) + y.abs_diff(sy) <= d {
            return false
        }
    }
    return true;
}

fn part_2(max_x: i32, max_y: i32, pairs: &Vec<(((i32, i32), (i32, i32)), u32)>) {
    let pos_comb: Vec<(i32, i32)> = vec![(-1, 1), (1, -1), (-1, -1), (1, 1)];
    for i in pairs.iter() {
        let sx = ((i.0).0).0;
        let sy = ((i.0).0).1;
        let d = i.1;
        for dx in 0..d+2 {
            let dy = d+1-dx;
            for (mx, my) in pos_comb.iter() {
                let (x, y) = (sx + (dx as i32* mx), sy + (dy as i32 * my));
                if (x < 0 || x > max_x) || ( y < 0 || y > max_y) {
                    continue;
                }
                if possible(x, y, &pairs) {
                    println!("Answer: {}, x: {}, y: {}", x as u64 * 4000000 + y as u64, x, y);
                    return;
                }
            }
        }
    }
}

fn main() {
    let pairs = get_sensors("./input.txt");
    /*
    for i in pairs.iter() {
        println!("{:?}", i);
    }
    */
    let max_x = 4000000;
    let max_y = 4000000;
    part_2(max_x, max_y, &pairs);
}
