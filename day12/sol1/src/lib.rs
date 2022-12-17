pub mod pos;

use crate::pos::Pos;
use std::{
    cmp::Reverse,
    collections::{BinaryHeap, HashMap},
    fs::File,
    io::{self, BufRead},
    path::Path,
};

fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where
    P: AsRef<Path>,
{
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}

pub fn get_grid_setup(filename: &str) -> (Vec<Vec<u32>>, (usize, usize), (usize, usize)) {
    let mut grid = vec![];
    let mut start = (0, 0);
    let mut end = (0, 0);
    if let Ok(lines) = read_lines(filename) {
        for (i, line_attempt) in lines.enumerate() {
            let mut grid_line = vec![];
            if let Ok(line) = line_attempt {
                for (j, char) in line.chars().enumerate() {
                    if char == 'S' {
                        grid_line.push('a' as u32);
                        start = (i, j);
                    } else if char == 'E' {
                        grid_line.push('z' as u32);
                        end = (i, j)
                    } else {
                        grid_line.push(char as u32);
                    }
                }
            }
            grid.push(grid_line);
        }
    }
    (grid, start, end)
}

fn prepend(vec: Vec<Pos>, s: &[Pos]) -> Vec<Pos> {
    let mut temp = s.to_owned();
    temp.extend(vec);
    temp
}

fn reconstruct_path(came_from: HashMap<Pos, Pos>, mut current: Pos) -> Vec<Pos> {
    let mut total_path = vec![current.clone()];
    while came_from.contains_key(&current) {
        current = came_from.get(&current).unwrap().clone();
        total_path = prepend(total_path, &[current.clone()]);
    }
    return total_path;
}

pub fn a_star(grid: &Vec<Vec<u32>>, start: Pos, end: Pos) -> Vec<Pos> {
    let mut open_set = BinaryHeap::new();
    open_set.push(Reverse(start.clone()));

    let mut came_from = HashMap::new();

    let mut gscore = HashMap::new();
    gscore.insert(start.clone(), 0 as usize);

    let mut fscore = HashMap::new();
    fscore.insert(start.clone(), start.dist_to(&end));

    while !open_set.is_empty() {
        let current = open_set.pop().unwrap().0;
        if current == end {
            return reconstruct_path(came_from, current);
        }

        for neighbor in current.neighbors(grid) {
            let open_sec_vec = open_set.clone().into_vec();
            let tent_gscore = gscore.get(&current).unwrap() + 1;
            if gscore.contains_key(&neighbor) {
                if tent_gscore < *gscore.get(&neighbor).unwrap() {
                    println!("{}", tent_gscore);
                    came_from.insert(neighbor.clone(), current.clone());
                    *gscore.entry(neighbor.clone()).or_insert(tent_gscore) = tent_gscore;
                    *fscore
                        .entry(neighbor.clone())
                        .or_insert(tent_gscore + neighbor.dist_to(&end)) = tent_gscore + neighbor.dist_to(&end);
                    if !open_sec_vec.contains(&Reverse(neighbor.clone())) {
                        open_set.push(Reverse(neighbor.clone()));
                    }
                }
            } else {
                println!("{}", tent_gscore);
                gscore.insert(neighbor.clone(), tent_gscore);
                came_from.insert(neighbor.clone(), current.clone());
                *fscore
                    .entry(neighbor.clone())
                    .or_insert(tent_gscore + neighbor.dist_to(&end)) = tent_gscore + neighbor.dist_to(&end);
                open_set.push(Reverse(neighbor.clone()));
            }
        }
    }
    return vec![];
}
