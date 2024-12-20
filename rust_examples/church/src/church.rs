use std::cell::RefCell;
use std::rc::Rc;

pub type Church<T> = Rc<dyn Fn(Rc<dyn Fn(T) -> T>) -> Rc<dyn Fn(T) -> T>>;

pub fn one<T: 'static>() -> Church<T> {
    Rc::new(move |f| Rc::new(move |x| f(x)))
}

pub fn two<T: 'static>() -> Church<T> {
    Rc::new(move |f| Rc::new(move |x| f(f(x))))
}

pub fn zero<T: 'static>() -> Church<T> {
    Rc::new(|_| Rc::new(|x| x))
}

pub fn succ<T: 'static>(n: Church<T>) -> Church<T> {
    Rc::new(move |f| {
        Rc::new(move |x| {
            let n_func = n.clone();
            f(n_func(f)(x))
        })
    })
}

pub fn add<T: 'static>(n: Church<T>, m: Church<T>) -> Church<T> {
    Rc::new(move |f| {
        Rc::new(move |x| {
            let n_func = n.clone();
            let m_func = m.clone();
            m_func(f)(n_func(f)(x))
        })
    })
}

pub fn mult<T: 'static>(n: Church<T>, m: Church<T>) -> Church<T> {
    Rc::new(move |f| {
        Rc::new(move |x| {
            let n_func = n.clone();
            m(f)(n_func(f)(x))
        })
    })
}

pub fn exp<T: 'static>(n: usize, m: usize) -> Church<T> {
    let n_church = from_usize(n);
    let m_church = from_usize(m);
    
    m_church(n_church)
}

pub fn to_usize<T: 'static + Default>(n: Church<T>) -> usize {
    let mut count = 0;
    let mut f = |_: T| { count += 1; T::default() };
    n(Rc::new(f))(T::default());
    count
}

pub fn from_usize<T: 'static>(n: usize) -> Church<T> {
    let mut result = zero::<T>();
    for _ in 0..n {
        result = succ(result);
    }
    result
}