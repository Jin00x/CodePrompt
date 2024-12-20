use std::cell::RefCell;
use std::collections::{HashSet, HashMap};
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

#[derive(Debug)]
pub struct Graph {
    nodes: HashMap<usize, Rc<RefCell<Node>>>,
    id_counter: usize,
}

#[derive(Debug)]
pub struct Node {
    value: i32,
    edges: HashSet<usize>,
}

#[derive(Debug)]
pub struct GraphError;

#[derive(Debug)]
pub struct SubGraph {
    nodes: HashSet<usize>,
    graph: Weak<RefCell<Graph>>,
}

impl NodeHandle {
    pub fn new(value: i32) -> Self {
        let graph = Rc::new(RefCell::new(Graph::new()));
        let node_id = {
            let mut g = graph.borrow_mut();
            g.add_node(value)
        };
        NodeHandle {
            id: node_id,
            graph: Rc::downgrade(&graph),
        }
    }

    pub fn add_edge(&self, to: NodeHandle) -> Result<bool, GraphError> {
        if let Some(graph) = self.graph.upgrade() {
            let mut g = graph.borrow_mut();
            if g.nodes.contains_key(&self.id) && g.nodes.contains_key(&to.id) {
                return g.nodes[&self.id].borrow_mut().add_edge(to.id);
            }
        }
        Err(GraphError)
    }

    pub fn remove_edge(&self, to: &NodeHandle) -> Result<bool, GraphError> {
        if let Some(graph) = self.graph.upgrade() {
            let mut g = graph.borrow_mut();
            if g.nodes.contains_key(&self.id) && g.nodes.contains_key(&to.id) {
                return g.nodes[&self.id].borrow_mut().remove_edge(to.id);
            }
        }
        Err(GraphError)
    }

    pub fn clear_edges(&self) -> Result<(), GraphError> {
        if let Some(graph) = self.graph.upgrade() {
            let mut g = graph.borrow_mut();
            if g.nodes.contains_key(&self.id) {
                g.nodes[&self.id].borrow_mut().clear_edges();
                return Ok(());
            }
        }
        Err(GraphError)
    }
}

impl Default for SubGraph {
    fn default() -> Self {
        Self::new()
    }
}

impl SubGraph {
    pub fn new() -> Self {
        SubGraph {
            nodes: HashSet::new(),
            graph: Weak::new(),
        }
    }

    pub fn add_node(&mut self, node: NodeHandle) -> bool {
        if self.nodes.insert(node.id) {
            self.graph = node.graph.clone();
            true
        } else {
            false
        }
    }

    pub fn remove_node(&mut self, node: &NodeHandle) -> bool {
        self.nodes.remove(&node.id)
    }

    pub fn detect_cycle(&self) -> bool {
        let mut visited = HashSet::new();
        let mut recursion_stack = HashSet::new();

        for &node_id in &self.nodes {
            if !visited.contains(&node_id) {
                if self.dfs(node_id, &mut visited, &mut recursion_stack) {
                    return true;
                }
            }
        }
        false
    }

    fn dfs(&self, node_id: usize, visited: &mut HashSet<usize>, recursion_stack: &mut HashSet<usize>) -> bool {
        visited.insert(node_id);
        recursion_stack.insert(node_id);

        if let Some(graph) = self.graph.upgrade() {
            let g = graph.borrow();
            if let Some(node) = g.nodes.get(&node_id) {
                for &neighbor_id in &node.borrow().edges {
                    if !visited.contains(&neighbor_id) {
                        if self.dfs(neighbor_id, visited, recursion_stack) {
                            return true;
                        }
                    } else if recursion_stack.contains(&neighbor_id) {
                        return true;
                    }
                }
            }
        }

        recursion_stack.remove(&node_id);
        false
    }
}

impl Graph {
    fn new() -> Self {
        Graph {
            nodes: HashMap::new(),
            id_counter: 0,
        }
    }

    fn add_node(&mut self, value: i32) -> usize {
        let id = self.id_counter;
        self.nodes.insert(id, Rc::new(RefCell::new(Node::new(value))));
        self.id_counter += 1;
        id
    }
}

impl Node {
    fn new(value: i32) -> Self {
        Node {
            value,
            edges: HashSet::new(),
        }
    }

    fn add_edge(&mut self, to_id: usize) -> Result<bool, GraphError> {
        if self.edges.insert(to_id) {
            Ok(true)
        } else {
            Ok(false)
        }
    }

    fn remove_edge(&mut self, to_id: usize) -> Result<bool, GraphError> {
        if self.edges.remove(&to_id) {
            Ok(true)
        } else {
            Ok(false)
        }
    }

    fn clear_edges(&mut self) {
        self.edges.clear();
    }
}