use std::{
    cell::RefCell,
    fs::File,
    io::{
        self, 
        BufRead,
    },
    path::Path,
    cmp::Ordering::*, borrow::Borrow,
};

static mut MAX: usize = 0;

struct Node {
    path: Vec<(usize, usize)>,
    childs: Vec<RefCell<Node>>,
    value: usize,
    dist: usize,
}

impl Eq for Node {

}

impl Ord for Node {
    fn cmp(&self, other: &Self) -> std::cmp::Ordering {
        if &self.dist > &other.dist {
            Greater
        } else if &self.dist < &other.dist {
            Less
        } else {
            Equal
        }
    }
}

impl PartialEq for Node {
    fn eq(&self, other: &Self) -> bool {
        self.path == other.path
    }
}

impl PartialOrd for Node {
    fn partial_cmp(&self, other: &Self) -> Option<std::cmp::Ordering> {
        self.dist.partial_cmp(&other.dist)
    }

    fn lt(&self, other: &Self) -> bool {
        matches!(self.partial_cmp(other), Some(Less))
    }

    fn le(&self, other: &Self) -> bool {
        // Pattern `Some(Less | Eq)` optimizes worse than negating `None | Some(Greater)`.
        // FIXME: The root cause was fixed upstream in LLVM with:
        // https://github.com/llvm/llvm-project/commit/9bad7de9a3fb844f1ca2965f35d0c2a3d1e11775
        // Revert this workaround once support for LLVM 12 gets dropped.
        !matches!(self.partial_cmp(other), None | Some(Greater))
    }

    fn gt(&self, other: &Self) -> bool {
        matches!(self.partial_cmp(other), Some(Greater))
    }

    fn ge(&self, other: &Self) -> bool {
        matches!(self.partial_cmp(other), Some(Greater | Equal))
    }
}

impl Node {
    fn new(path: Vec<(usize, usize)>, childs: Vec<RefCell<Node>>, value: usize, dist: usize) -> Self {
        Node {path, childs, value, dist}
    }

    fn new_child(self: &mut Self, new_node: (usize, usize), dist: usize) {
        if !self.path.contains(&new_node) {
            let mut new_path = self.path.clone();
            new_path.push(new_node);
            self.childs.push(RefCell::new(Node::new(new_path, Vec::new(), self.value.clone() + 1, dist)));
        }
    }

    fn traverse_grid(self: &mut Self, grid: &Vec<Vec<u32>>, end: (usize, usize), max: usize) -> usize {
        unsafe {
            if self.value > MAX {
                return max;
            }
        }
        let mut current_max = max;
        let current = self.path.last().unwrap().clone();
        if current.0 != 0 {
            let new_node = (current.0 - 1, current.1);
            if can_move_to(grid[current.0][current.1], grid[new_node.0][new_node.1]) {
                self.new_child(new_node, dist_to(new_node, end));
                if new_node == end {
                    unsafe {
                        MAX = self.value;
                    }
                    return self.value;
                }
            }
        }
        if current.0 != grid.len() - 1 {
            let new_node = (current.0 + 1, current.1);
            if can_move_to(grid[current.0][current.1], grid[new_node.0][new_node.1]) {
                self.new_child(new_node, dist_to(new_node, end));
                if new_node == end {
                    unsafe {
                        MAX = self.value;
                    }
                    return self.value;
                }
            }
        }
        if current.1 != 0 {
            let new_node = (current.0, current.1 - 1);
            if can_move_to(grid[current.0][current.1], grid[new_node.0][new_node.1]) {
                self.new_child(new_node, dist_to(new_node, end));
                if new_node == end {
                    unsafe {
                        MAX = self.value;
                    }
                    return self.value;
                }
            }
        }
        if current.1 != grid[0].len() - 1 {
            let new_node = (current.0, current.1 + 1);
            if can_move_to(grid[current.0][current.1], grid[new_node.0][new_node.1]) {
                self.new_child(new_node, dist_to(new_node, end));
                if new_node == end {
                    unsafe {
                        MAX = self.value;
                    }
                    return self.value;
                }
            }
        }

        self.childs.sort();

        for child in self.childs.iter() {
            let val = child.borrow_mut().traverse_grid(grid, end, max);
            if val < current_max {
                current_max = val;
            }
        }
        return current_max;
    }
}

fn can_move_to(start: u32, end: u32) -> bool {
    end as i32-start as i32 <= 1
}

fn dist_to(start: (usize, usize), end: (usize, usize)) -> usize {
    ((end.0 as i64 - start.0 as i64).abs() + (end.1 as i64 - start.1 as i64).abs()) as usize
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

fn main() {
    let (grid, start, end, max) = get_grid_setup("./input2.txt");
    println!("{:?}", grid);
    println!("Start: {:?}\nEnd: {:?}\nMax: {}", start, end, max);
    unsafe {
        MAX = max;
    }
    println!("{}", dist_to(start, end));
    let mut parent_node = Node::new(vec![start], vec![], 1, dist_to(start, end));
    let solution = parent_node.traverse_grid(&grid, end, max);
    println!("Solution: {}", solution);
}
