// process.h
#ifndef PROCESS_H
#define PROCESS_H

#include "defs.h"

InputBuffer* new_input_buffer();
void print_prompt();
void read_input(InputBuffer*);
void close_input_buffer(InputBuffer*);
void pager_flush(Pager*, uint32_t);
MetaCommandResult do_meta_command(InputBuffer*, Table *);
PrepareResult prepare_insert(InputBuffer*, Statement*);
PrepareResult prepare_statement(InputBuffer*, Statement*);
ExecuteResult execute_insert(Statement*, Table*);
ExecuteResult execute_select(Statement*, Table*);
ExecuteResult execute_statement(Statement*, Table *);

#endif  // PROCESS_H