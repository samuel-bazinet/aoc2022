use std::{
    cell::RefCell,
    fs::File,
    io::{
        self, 
        BufRead,
    },
    path::Path,
};

static mut MAX: usize = 0;

struct Node {
    path: Vec<(usize, usize)>,
    childs: Vec<RefCell<Node>>,
    value: usize,
}

impl Node {
    fn new(path: Vec<(usize, usize)>, childs: Vec<RefCell<Node>>, value: usize) -> Self {
        Node {path, childs, value}
    }

    fn new_child(self: &mut Self, new_node: (usize, usize)) {
        if !self.path.contains(&new_node) {
            let mut new_path = self.path.clone();
            new_path.push(new_node);
            self.childs.push(RefCell::new(Node::new(new_path, Vec::new(), self.value.clone() + 1)));
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
                self.new_child(new_node);
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
                self.new_child(new_node);
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
                self.new_child(new_node);
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
                self.new_child(new_node);
                if new_node == end {
                    unsafe {
                        MAX = self.value;
                    }
                    return self.value;
                }
            }
        }

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
    let (grid, start, end, max) = get_grid_setup("./input.txt");
    println!("{:?}", grid);
    println!("Start: {:?}\nEnd: {:?}\nMax: {}", start, end, max);
    unsafe {
        MAX = max;
    }
    let mut parent_node = Node::new(vec![(0, 0)], vec![], 1);
    let solution = parent_node.traverse_grid(&grid, end, max);
    println!("Solution: {}", solution);
}
