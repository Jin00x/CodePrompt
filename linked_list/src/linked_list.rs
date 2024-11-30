//! Singly linked list.
//!
//! Consult <https://doc.rust-lang.org/book/ch15-01-box.html>.

use std::fmt::Debug;

/// Node of the list.
#[derive(Debug)]
pub struct Node<T: Debug> {
    /// Value of current node.
    pub value: T,

    /// Pointer to the next node. If it is `None`, there is no next node.
    pub next: Option<Box<Node<T>>>,
}

impl<T: Debug> Node<T> {
    /// Creates a new node.
    pub fn new(value: T) -> Self {
        Self { value, next: None }
    }
}

/// A singly-linked list.
#[derive(Debug)]
pub struct SinglyLinkedList<T: Debug> {
    /// Head node of the list. If it is `None`, the list is empty.
    head: Option<Node<T>>,
}

impl<T: Debug> Default for SinglyLinkedList<T> {
    fn default() -> Self {
        Self::new()
    }
}

impl<T: Debug> SinglyLinkedList<T> {
    /// Creates a new list.
    pub fn new() -> Self {
        Self { head: None }
    }

    /// Adds the given node to the front of the list.
    pub fn push_front(&mut self, value: T) {
        let new_node = Node {
            value,
            next: self.head.take().map(Box::new),
        };
        self.head = Some(new_node);
    }

    /// Adds the given node to the back of the list.
    pub fn push_back(&mut self, value: T) {
        let new_node = Node { value, next: None };
        match &mut self.head {
            Some(mut current) => {
                while let Some(next) = &mut current.next {
                    current = next;
                }
                current.next = Some(Box::new(new_node));
            }
            None => self.head = Some(new_node),
        }
    }

    /// Removes and returns the node at the front of the list.
    pub fn pop_front(&mut self) -> Option<T> {
        self.head.take().map(|head| {
            self.head = head.next.map(|boxed| *boxed);
            head.value
        })
    }

    /// Removes and returns the node at the back of the list.
    pub fn pop_back(&mut self) -> Option<T> {
        match &mut self.head {
            Some(mut current) => {
                if current.next.is_none() {
                    return self.head.take().map(|node| node.value);
                }
                while current.next.as_ref().unwrap().next.is_some() {
                    current = current.next.as_mut().unwrap();
                }
                current.next.take().map(|boxed| boxed.value)
            }
            None => None,
        }
    }

    /// Create a new list from the given vector `vec`.
    pub fn from_vec(vec: Vec<T>) -> Self {
        let mut list = Self::new();
        for value in vec.into_iter().rev() {
            list.push_front(value);
        }
        list
    }

    /// Convert the current list into a vector.
    pub fn into_vec(self) -> Vec<T> {
        let mut vec = Vec::new();
        let mut current = self.head;
        while let Some(node) = current {
            vec.push(node.value);
            current = node.next.map(|boxed| *boxed);
        }
        vec
    }

    /// Return the length (i.e., number of nodes) of the list.
    pub fn length(&self) -> usize {
        let mut count = 0;
        let mut current = &self.head;
        while let Some(node) = current {
            count += 1;
            current = &node.next;
        }
        count
    }

    /// Apply function `f` on every element of the list.
    ///
    /// # Examples
    ///
    /// `self`: `[1, 2]`, `f`: `|x| x + 1` ==> `[2, 3]`
    pub fn map<F: Fn(T) -> T>(self, f: F) -> Self {
        let mut new_list = Self::new();
        let mut current = self.head;
        while let Some(node) = current {
            new_list.push_back(f(node.value));
            current = node.next.map(|boxed| *boxed);
        }
        new_list
    }

    /// Apply given function `f` for each adjacent pair of elements in the list.
    /// If `self.length() < 2`, do nothing.
    ///
    /// # Examples
    ///
    /// `self`: `[1, 2, 3, 4]`, `f`: `|x, y| x + y`
    /// // each adjacent pair of elements: `(1, 2)`, `(2, 3)`, `(3, 4)`
    /// // apply `f` to each pair: `f(1, 2) == 3`, `f(2, 3) == 5`, `f(3, 4) == 7`
    /// ==> `[3, 5, 7]`
    pub fn pair_map<F: Fn(T, T) -> T>(self, f: F) -> Self
    where
        T: Clone,
    {
        let mut new_list = Self::new();
        let mut current = self.head;
        while let Some(node1) = current {
            if let Some(node2) = node1.next.map(|boxed| *boxed) {
                new_list.push_back(f(node1.value.clone(), node2.value.clone()));
                current = node1.next.map(|boxed| *boxed);
            } else {
                break;
            }
        }
        new_list
    }
}

// A list of lists.
impl<T: Debug> SinglyLinkedList<SinglyLinkedList<T>> {
    /// Flatten the list of lists into a single list.
    ///
    /// # Examples
    /// `self`: `[[1, 2, 3], [4, 5, 6], [7, 8]]`
    /// ==> `[1, 2, 3, 4, 5, 6, 7, 8]`
    pub fn flatten(self) -> SinglyLinkedList<T> {
        let mut new_list = SinglyLinkedList::new();
        let mut current = self.head;
        while let Some(list) = current {
            let inner_list = list.value;
            for value in inner_list.into_vec() {
                new_list.push_back(value);
            }
            current = list.next.map(|boxed| *boxed);
        }
        new_list
    }
}
