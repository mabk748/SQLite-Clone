// dataStructs.h
#ifndef DATA_STRUCTS_H
#define DATA_STRUCTS_H

#include "defs.h"

#include <string.h>

uint32_t* leaf_node_num_cells(void*);
void* leaf_node_cell(void*, uint32_t);
uint32_t* leaf_node_key(void*, uint32_t);
void* leaf_node_value(void*, uint32_t);
NodeType get_node_type(void*);
void set_node_type(void*, NodeType);
void serialize_row(Row*, void*);
void deserialize_row(void *, Row*);
uint32_t* internal_node_num_keys(void*);
uint32_t* internal_node_right_child(void*);
uint32_t* internal_node_cell(void*, uint32_t);
bool is_node_root(void*);
void set_node_root(void*, bool);
void initialize_leaf_node(void*);
void initialize_internal_node(void*);
uint32_t* internal_node_child(void*, uint32_t);
uint32_t* internal_node_key(void*, uint32_t);
uint32_t get_node_max_key(void*);
uint32_t get_unused_page_num(Pager*);
void* get_page(Pager*, uint32_t);
Cursor* table_start(Table*);
Cursor* leaf_node_find(Table*, uint32_t, uint32_t);
void create_new_root(Table*, uint32_t);
Cursor* internal_node_find(Table*, uint32_t, uint32_t);
void leaf_node_split_and_insert(Cursor*, uint32_t, Row*);
Cursor* table_find(Table*, uint32_t);
void* cursor_value(Cursor*);
void cursor_advance(Cursor*);
void leaf_node_insert(Cursor*, uint32_t, Row*);
void print_row(Row*);
void print_constants();
void indent(uint32_t);
void print_tree(Pager* pager, uint32_t page_num, uint32_t);

#endif  // DATA_STRUCTS_H