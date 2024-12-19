pub mod linked_list {
    // mod linked_list_src;  // private to the module
    pub mod linked_list;  // public interface
    #[cfg(test)]
    mod test_linked_list;
}

pub mod graph {
    // mod graph_src;
    pub mod graph;
    #[cfg(test)]
    mod test_graph;
}