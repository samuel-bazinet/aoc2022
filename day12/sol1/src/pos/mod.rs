use std::{
    cmp::Ordering::{Equal, Greater, Less},
    fmt::Display,
};

#[derive(Hash, Debug)]
pub struct Pos {
    pub x: usize,
    pub y: usize,
}

impl Pos {
    pub fn dist_to(&self, other: &Pos) -> usize {
        self.x.abs_diff(other.x) + self.y.abs_diff(other.y)
    }

    pub fn neighbors(&self, grid: &Vec<Vec<u32>>) -> Vec<Pos> {
        let mut neigbors = vec![];

        if self.x > 0 {
            if grid[self.x - 1][self.y] as i32 - grid[self.x][self.y] as i32 <= 1 {
                neigbors.push(Pos {
                    x: self.x - 1,
                    y: self.y,
                });
            }
        }
        if self.x < grid.len() - 1 {
            if grid[self.x + 1][self.y] as i32 - grid[self.x][self.y] as i32 <= 1 {
                neigbors.push(Pos {
                    x: self.x + 1,
                    y: self.y,
                });
            }
        }
        if self.y > 0 {
            if grid[self.x][self.y - 1] as i32 - grid[self.x][self.y] as i32 <= 1 {
                neigbors.push(Pos {
                    x: self.x,
                    y: self.y - 1,
                });
            }
        }
        if self.y < grid[0].len() - 1 {
            if grid[self.x][self.y + 1] as i32 - grid[self.x][self.y] as i32 <= 1 {
                neigbors.push(Pos {
                    x: self.x,
                    y: self.y + 1,
                });
            }
        }

        neigbors
    }
}

pub static mut END: Pos = Pos { x: 0, y: 0 };

impl Clone for Pos {
    fn clone(&self) -> Self {
        Self {
            x: self.x.clone(),
            y: self.y.clone(),
        }
    }
}

impl Eq for Pos {}

impl Ord for Pos {
    fn cmp(&self, other: &Self) -> std::cmp::Ordering {
        let dis_a;
        let dis_b;
        unsafe {
            dis_a = self.dist_to(&END);
            dis_b = other.dist_to(&END);
        }
        if dis_a > dis_b {
            Greater
        } else if dis_a < dis_b {
            Less
        } else {
            Equal
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
            Less | Equal => other,
            Greater => self,
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
            Less | Equal => self,
            Greater => other,
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
        !matches!(
            self.partial_cmp(other),
            None | Some(std::cmp::Ordering::Greater)
        )
    }

    fn gt(&self, other: &Self) -> bool {
        matches!(self.partial_cmp(other), Some(Greater))
    }

    fn ge(&self, other: &Self) -> bool {
        matches!(
            self.partial_cmp(other),
            Some(std::cmp::Ordering::Greater | std::cmp::Ordering::Equal)
        )
    }
}

impl Display for Pos {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "({}, {})", self.x, self.y)
    }
}
