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
   head: Option<Box<Node<T>>>,
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
       let mut new_node = Box::new(Node::new(value));
       new_node.next = self.head.take();
       self.head = Some(new_node);
   }


   /// Adds the given node to the back of the list.
   pub fn push_back(&mut self, value: T) {
       let new_node = Box::new(Node::new(value));
       if let Some(ref mut head) = self.head {
           let mut current = head.as_mut();
           while let Some(ref mut next) = current.next {
               current = next.as_mut();
           }
           current.next = Some(new_node);
       } else {
           self.head = Some(new_node);
       }
   }


   /// Removes and returns the node at the front of the list.
   pub fn pop_front(&mut self) -> Option<T> {
       self.head.take().map(|node| {
           self.head = node.next;
           node.value
       })
   }


   /// Removes and returns the node at the back of the list.
   pub fn pop_back(&mut self) -> Option<T> {
       let mut current = self.head.take()?;
       let mut prev = None;


       while let Some(next) = current.next.take() {
           prev = Some(current);
           current = next;
       }


       let value = current.value;
       if let Some(mut prev_node) = prev {
           prev_node.next = None;
           self.head = Some(prev_node);
       } else {
           self.head = None;
       }
       Some(value)
   }


   /// Create a new list from the given vector `vec`.
   pub fn from_vec(vec: Vec<T>) -> Self {
       let mut list = Self::new();
       for value in vec {
           list.push_back(value);
       }
       list
   }


   /// Convert the current list into a vector.
   pub fn into_vec(self) -> Vec<T> {
       let mut vec = Vec::new();
       let mut current = self.head;


       while let Some(node) = current {
           vec.push(node.value);
           current = node.next;
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
   pub fn map<F: Fn(T) -> T>(self, f: F) -> Self {
       let mut new_list = Self::new();
       let mut current = self.head;


       while let Some(node) = current {
           new_list.push_back(f(node.value));
           current = node.next;
       }
       new_list
   }


   /// Apply given function `f` for each adjacent pair of elements in the list.
   pub fn pair_map<F: Fn(T, T) -> T>(self, f: F) -> Self
   where
       T: Clone,
   {
       let mut new_list = Self::new();
       let mut current = self.head;


       while let Some(node) = current {
           if let Some(next_node) = node.next.as_ref() {
               new_list.push_back(f(node.value.clone(), next_node.value.clone()));
           }
           current = node.next;
       }
       new_list
   }
}


// A list of lists.
impl<T: Debug> SinglyLinkedList<SinglyLinkedList<T>> {
   /// Flatten the list of lists into a single list.
   pub fn flatten(self) -> SinglyLinkedList<T> {
       let mut flat_list = SinglyLinkedList::new();
       let mut current = self.head;


       while let Some(node) = current {
           let mut inner_current = node.value.head;
           while let Some(inner_node) = inner_current {
               flat_list.push_back(inner_node.value);
               inner_current = inner_node.next;
           }
           current = node.next;
       }
       flat_list
   }
}
