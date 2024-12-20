use std::fmt;
use std::iter::zip;
use std::ops::*;

#[derive(Debug, Clone)]
pub struct BigInt {
    pub carrier: Vec<u32>,
}

impl BigInt {
    pub fn new(n: u32) -> Self {
        Self { carrier: vec![n] }
    }

    pub fn new_large(carrier: Vec<u32>) -> Self {
        assert!(!carrier.is_empty());
        let mut bigint = Self { carrier };
        bigint.truncate();
        bigint
    }
}

const SIGN_MASK: u32 = 1 << 31;

impl BigInt {
    fn sign_extension(&self, len: usize) -> Self {
        let mut extended = self.carrier.clone();
        let sign_bit = (self.carrier.last().unwrap() & SIGN_MASK) != 0;
        while extended.len() < len {
            extended.push(if sign_bit { u32::MAX } else { 0 });
        }
        Self { carrier: extended }
    }

    fn two_complement(&self) -> Self {
        let mut result = self.carrier.iter().map(|x| !x).collect::<Vec<u32>>();
        let mut carry = 1;
        for x in result.iter_mut() {
            let (sum, overflow) = x.overflowing_add(carry);
            *x = sum;
            carry = if overflow { 1 } else { 0 };
        }
        Self { carrier: result }
    }

    fn truncate(&self) -> Self {
        let mut truncated = self.carrier.clone();
        while truncated.len() > 1
            && ((truncated[truncated.len() - 1] == 0 && truncated[truncated.len() - 2] & SIGN_MASK == 0)
                || (truncated[truncated.len() - 1] == u32::MAX
                    && truncated[truncated.len() - 2] & SIGN_MASK != 0))
        {
            truncated.pop();
        }
        Self { carrier: truncated }
    }
}

impl Add for BigInt {
    type Output = Self;

    fn add(self, rhs: Self) -> Self::Output {
        let max_len = self.carrier.len().max(rhs.carrier.len()) + 1;
        let lhs_ext = self.sign_extension(max_len).carrier;
        let rhs_ext = rhs.sign_extension(max_len).carrier;

        let mut result = Vec::with_capacity(max_len);
        let mut carry = 0;

        for (a, b) in zip(lhs_ext, rhs_ext) {
            let (sum1, overflow1) = a.overflowing_add(b);
            let (sum2, overflow2) = sum1.overflowing_add(carry);
            result.push(sum2);
            carry = (overflow1 as u32) + (overflow2 as u32);
        }

        Self { carrier: result }.truncate()
    }
}

impl Sub for BigInt {
    type Output = Self;

    fn sub(self, rhs: Self) -> Self::Output {
        self.add(rhs.two_complement())
    }
}

impl fmt::Display for BigInt {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        for i in self.carrier.iter().rev() {
            write!(f, "{:08x}", i)?;
        }
        Ok(())
    }
}
