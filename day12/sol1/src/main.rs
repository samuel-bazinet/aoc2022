mod pos;
use std::char::from_u32;
use pathfinding::prelude::astar;
use sol1::{
    a_star, get_grid_setup,
    pos::{Pos, END},
};

fn main() {
    let (grid, start, end) = get_grid_setup("./input.txt");
    unsafe {
        END = Pos { x: end.0, y: end.1 };
    }
    println!("{:?}", grid);
    println!("Start: {:?}\nEnd: {:?}", start, end);
    let path = a_star(
        &grid,
        Pos {
            x: start.0,
            y: start.1,
        },
        Pos { x: end.0, y: end.1 },
    );
    let mut path_grid = Vec::new();
    for i in 0..grid.len() {
        path_grid.push(vec![]);
        for _ in 0..grid[0].len() {
            path_grid[i].push('.');
        }
    }
    for pos in path.iter() {
        path_grid[pos.x][pos.y] = '!';
    }
    let mut path_str = "".to_owned();
    for i in 0..grid.len() {
        for j in 0..grid[0].len() {
            path_str += path_grid[i][j].to_string().as_str();
        }
        path_str += "\n";
    }
    println!("{}", path_str);
    println!("Length of path = {}", path.len() - 1);
    // Don't tell anyone I cheated
    let start = Pos {x: start.0, y: start.1};
    let result = astar(&start, |p| p.neighbors(&grid).into_iter().map(|p| (p, 1)), unsafe {|p| p.dist_to(&END)}, unsafe{ |p| p == &END});
    println!("{}", result.unwrap().1);

    for i in 0..grid.len() {
        let start = Pos {x: i, y: 0};
        let result = astar(&start, |p| p.neighbors(&grid).into_iter().map(|p| (p, 1)), unsafe {|p| p.dist_to(&END)}, unsafe{ |p| p == &END});
        println!("{}", result.unwrap().1);
    }
}
