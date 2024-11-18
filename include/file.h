// file.h
#ifndef FILE_H
#define FILE_H

#include "defs.h"

Pager* pager_open(const char*);
Table* db_open(const char*);
void db_close(Table*);


#endif  // FILE_H