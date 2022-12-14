use std::{
    fs::File,
    io::{
        self, 
        BufRead,
    },
    path::Path, 
    collections::{
        HashMap,
        BinaryHeap,
    }, cmp::Reverse,
};

#[derive(Hash)]
struct Pos {
    x: usize,
    y: usize,
}

static mut END : Pos = Pos {x: 0, y: 0};

impl Clone for Pos {
    fn clone(&self) -> Self {
        Self { x: self.x.clone(), y: self.y.clone() }
    }
}

impl Eq for Pos {

}

impl Ord for Pos {
    fn cmp(&self, other: &Self) -> std::cmp::Ordering {
        let dis_a;
        let dis_b;
        unsafe {
            dis_a = dist_to(self, &END);
            dis_b = dist_to(other, &END);
        }
        if dis_a > dis_b {
            std::cmp::Ordering::Greater
        } else if dis_a < dis_b {
            std::cmp::Ordering::Less
        } else {
            std::cmp::Ordering::Equal
        }
    }

    fn max(self, other: Self) -> Self
    where
        Self: Sized,
        //Self: ~const std::marker::Destruct,
    {
        // HACK(fee1-dead): go back to using `self.max_by(other, Ord::cmp)`
        // when trait methods are allowed to be used when a const closure is
        // expected.
        match self.cmp(&other) {
            std::cmp::Ordering::Less | std::cmp::Ordering::Equal => other,
            std::cmp::Ordering::Greater => self,
        }
    }

    fn min(self, other: Self) -> Self
    where
        Self: Sized,
        //Self: ~const std::marker::Destruct,
    {
        // HACK(fee1-dead): go back to using `self.min_by(other, Ord::cmp)`
        // when trait methods are allowed to be used when a const closure is
        // expected.
        match self.cmp(&other) {
            std::cmp::Ordering::Less | std::cmp::Ordering::Equal => self,
            std::cmp::Ordering::Greater => other,
        }
    }

    fn clamp(self, min: Self, max: Self) -> Self
    where
        Self: Sized,
        //Self: ~const std::marker::Destruct,
        //Self: ~const PartialOrd,
    {
        assert!(min <= max);
        if self < min {
            min
        } else if self > max {
            max
        } else {
            self
        }
    }
}

impl PartialEq for Pos {
    fn eq(&self, other: &Self) -> bool {
        self.x == other.x && self.y == other.y
    }

    fn ne(&self, other: &Self) -> bool {
        !self.eq(other)
    }
}

impl PartialOrd for Pos {
    fn partial_cmp(&self, other: &Self) -> Option<std::cmp::Ordering> {
        match self.x.partial_cmp(&other.x) {
            Some(core::cmp::Ordering::Equal) => {}
            ord => return ord,
        }
        self.y.partial_cmp(&other.y)
    }

    fn lt(&self, other: &Self) -> bool {
        matches!(self.partial_cmp(other), Some(Less))
    }

    fn le(&self, other: &Self) -> bool {
        // Pattern `Some(Less | Eq)` optimizes worse than negating `None | Some(Greater)`.
        // FIXME: The root cause was fixed upstream in LLVM with:
        // https://github.com/llvm/llvm-project/commit/9bad7de9a3fb844f1ca2965f35d0c2a3d1e11775
        // Revert this workaround once support for LLVM 12 gets dropped.
        !matches!(self.partial_cmp(other), None | Some(std::cmp::Ordering::Greater))
    }

    fn gt(&self, other: &Self) -> bool {
        matches!(self.partial_cmp(other), Some(Greater))
    }

    fn ge(&self, other: &Self) -> bool {
        matches!(self.partial_cmp(other), Some(std::cmp::Ordering::Greater | std::cmp::Ordering::Equal))
    }
}

fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where P: AsRef<Path>, {
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}

fn get_grid_setup(filename: &str) -> (Vec<Vec<u32>>, (usize, usize), (usize, usize), usize) {
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
    let max = grid.len() * grid[0].len();
    (grid, start, end, max)
}

fn dist_to(start: &Pos, end: &Pos) -> usize {
    ((end.x as i64 - start.x as i64).abs() + (end.y as i64 - start.y as i64).abs()) as usize
}

fn prepend(vec: Vec<Pos>, s: &[Pos]) -> Vec<Pos> {
    let mut temp = s.to_owned();
    temp.extend(vec);
    temp
}

fn reconstruct_path(came_from : HashMap<Pos, Pos>, current: Pos) -> Vec<Pos> {
    let mut total_path = vec![current.clone()];
    while came_from.contains_key(&current) {
        let current = &*came_from.get(&current).unwrap();
        total_path = prepend(total_path, &[current.clone()]);
    }
    return total_path;
}

fn a_Star(grid: Vec<Vec<usize>>, start:Pos, end: Pos) -> Vec<Pos>{
    let mut open_set = BinaryHeap::new();
    open_set.push(Reverse(start.clone()));

    let mut came_from = HashMap::new();

    let mut gscore = HashMap::new();
    gscore.insert(start.clone(), 0 as usize);

    let mut fscore = HashMap::new();
    fscore.insert(start.clone(), dist_to(&start, &end));

    while !open_set.is_empty() {
        let current = open_set.pop().unwrap().0;
        if current == end {
            return reconstruct_path(came_from, current);
        }

        if current.x > 0 {
            let neighbor = Pos {x: current.x.clone() - 1, y: current.y.clone()};
            if grid[neighbor.x][neighbor.y] as i32 - grid[current.x][current.y] as i32 <= 1 {
                let tent_gscore = gscore.get(&current).unwrap() + dist_to(&start, &neighbor);
                if gscore.contains_key(&neighbor) {
                    if tent_gscore < *gscore.get(&neighbor).unwrap() {
                        came_from.insert(neighbor.clone(), current.clone());
                        gscore.entry(neighbor.clone()).or_insert(tent_gscore);
                        fscore.entry(neighbor.clone()).or_insert(tent_gscore + dist_to(&neighbor, &end));
                    }
                }
            }
        }
        if current.x > 0 {
            let neighbor = Pos {x: current.x.clone() - 1, y: current.y.clone()};
            if grid[neighbor.x][neighbor.y] as i32 - grid[current.x][current.y] as i32 <= 1 {
                let tent_gscore = gscore.get(&current).unwrap() + dist_to(&start, &neighbor);
                if gscore.contains_key(&neighbor) {
                    if tent_gscore < *gscore.get(&neighbor).unwrap() {
                        came_from.insert(neighbor.clone(), current.clone());
                        gscore.entry(neighbor.clone()).or_insert(tent_gscore);
                        fscore.entry(neighbor.clone()).or_insert(tent_gscore + dist_to(&neighbor, &end));
                    }
                }
            }
        }
        if current.y > 0 {
            let neighbor = Pos {x: current.x.clone(), y: current.y.clone() - 1};
            if grid[neighbor.x][neighbor.y] as i32 - grid[current.x][current.y] as i32 <= 1 {
                let tent_gscore = gscore.get(&current).unwrap() + dist_to(&start, &neighbor);
                if gscore.contains_key(&neighbor) {
                    if tent_gscore < *gscore.get(&neighbor).unwrap() {
                        came_from.insert(neighbor.clone(), current.clone());
                        gscore.entry(neighbor.clone()).or_insert(tent_gscore);
                        fscore.entry(neighbor.clone()).or_insert(tent_gscore + dist_to(&neighbor, &end));
                    }
                }
            }
        }
        if current.y > 0 {
            let neighbor = Pos {x: current.x.clone() - 1, y: current.y.clone()};
            if grid[neighbor.x][neighbor.y] as i32 - grid[current.x][current.y] as i32 <= 1 {
                let tent_gscore = gscore.get(&current).unwrap() + dist_to(&start, &neighbor);
                if gscore.contains_key(&neighbor) {
                    if tent_gscore < *gscore.get(&neighbor).unwrap() {
                        came_from.insert(neighbor.clone(), current.clone());
                        gscore.entry(neighbor.clone()).or_insert(tent_gscore);
                        fscore.entry(neighbor.clone()).or_insert(tent_gscore + dist_to(&neighbor, &end));
                    }
                }
            }
        }
    }
    return vec![];
}

fn main() {
    
    let (grid, start, end, max) = get_grid_setup("./input2.txt");
    unsafe {
        END = Pos {x: end.0, y: end.1};
    }
    println!("{:?}", grid);
    println!("Start: {:?}\nEnd: {:?}", start, end);
}