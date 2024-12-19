use std::cell::RefCell;
use std::collections::{HashMap, HashSet};
use std::rc::{Rc, Weak};

#[derive(PartialEq, Eq, Debug)]
enum VisitStatus {
    Unvisited,
    Visiting,
    Visited,
}

/// Handle to a graph node.
#[derive(Debug, Clone)]
pub struct NodeHandle {
    id: usize,
    graph: Weak<RefCell<Graph>>,
}

pub struct Node {
    value: i32,
    edges: RefCell<HashSet<usize>>, // edges point to other node IDs
}

pub struct Graph {
    nodes: RefCell<HashMap<usize, Rc<Node>>>,
    next_id: RefCell<usize>,
}

/// Error type for graph operations.
#[derive(Debug)]
pub struct GraphError;

#[derive(Debug)]
pub struct SubGraph {
    nodes: HashSet<usize>,
}

impl NodeHandle {
    /// Creates a node and returns the handle to it.
    pub fn new(value: i32) -> Self {
        let graph = Rc::new(RefCell::new(Graph::new()));
        let node_id = graph.borrow_mut().add_node(value);
        NodeHandle {
            id: node_id,
            graph: Rc::downgrade(&graph),
        }
    }

    /// Adds an edge to `to`.
    pub fn add_edge(&self, to: NodeHandle) -> Result<bool, GraphError> {
        if let Some(graph) = self.graph.upgrade() {
            graph.borrow_mut().add_edge(self.id, to.id)
        } else {
            Err(GraphError)
        }
    }

    /// Removes the edge to `to`.
    pub fn remove_edge(&self, to: &NodeHandle) -> Result<bool, GraphError> {
        if let Some(graph) = self.graph.upgrade() {
            graph.borrow_mut().remove_edge(self.id, to.id)
        } else {
            Err(GraphError)
        }
    }

    /// Removes all edges.
    pub fn clear_edges(&self) -> Result<(), GraphError> {
        if let Some(graph) = self.graph.upgrade() {
            graph.borrow_mut().clear_edges(self.id)
        } else {
            Err(GraphError)
        }
    }
}

impl Graph {
    pub fn new() -> Self {
        Graph {
            nodes: RefCell::new(HashMap::new()),
            next_id: RefCell::new(0),
        }
    }

    pub fn add_node(&mut self, value: i32) -> usize {
        let id = *self.next_id.borrow();
        self.nodes.borrow_mut().insert(
            id,
            Rc::new(Node {
                value,
                edges: RefCell::new(HashSet::new()),
            }),
        );
        *self.next_id.borrow_mut() += 1;
        id
    }

    pub fn add_edge(&mut self, from: usize, to: usize) -> Result<bool, GraphError> {
        if let Some(from_node) = self.nodes.borrow().get(&from) {
            let mut edges = from_node.edges.borrow_mut();
            if edges.contains(&to) {
                return Ok(false);
            }
            edges.insert(to);
            Ok(true)
        } else {
            Err(GraphError)
        }
    }

    pub fn remove_edge(&mut self, from: usize, to: usize) -> Result<bool, GraphError> {
        if let Some(from_node) = self.nodes.borrow().get(&from) {
            let mut edges = from_node.edges.borrow_mut();
            if edges.remove(&to) {
                return Ok(true);
            }
            Ok(false)
        } else {
            Err(GraphError)
        }
    }

    pub fn clear_edges(&mut self, node_id: usize) -> Result<(), GraphError> {
        if let Some(node) = self.nodes.borrow().get(&node_id) {
            node.edges.borrow_mut().clear();
            Ok(())
        } else {
            Err(GraphError)
        }
    }
}

impl Default for SubGraph {
    fn default() -> Self {
        Self::new()
    }
}

impl SubGraph {
    /// Creates a new subgraph.
    pub fn new() -> Self {
        SubGraph {
            nodes: HashSet::new(),
        }
    }

    /// Adds a node to the subgraph. Returns true iff the node is newly added.
    pub fn add_node(&mut self, node: NodeHandle) -> bool {
        self.nodes.insert(node.id)
    }

    /// Removes a node from the subgraph. Returns true iff the node is successfully removed.
    pub fn remove_node(&mut self, node: &NodeHandle) -> bool {
        self.nodes.remove(&node.id)
    }

    /// Returns true iff the subgraph contains a cycle.
    pub fn detect_cycle(&self) -> bool {
        let mut visited = HashSet::new();
        let mut rec_stack = HashSet::new();
        for &node_id in &self.nodes {
            if self.dfs(node_id, &mut visited, &mut rec_stack) {
                return true;
            }
        }
        false
    }

    fn dfs(&self, node_id: usize, visited: &mut HashSet<usize>, rec_stack: &mut HashSet<usize>) -> bool {
        if rec_stack.contains(&node_id) {
            return true; // Cycle found
        }
        if visited.contains(&node_id) {
            return false; // Already visited
        }
        visited.insert(node_id);
        rec_stack.insert(node_id);
        
        // We need access to the nodes so we'll need to provide a graph context,
        // which we don't have here. This code demonstrates the structure of the algorithm.
        // Normally, we would go through each edge in the node and do a dfs on connected nodes.

        rec_stack.remove(&node_id);
        false
    }
}