CC = gcc
CFLAGS = -Wall -g
OBJ_DIR = obj
SRC_DIR = src
INCLUDE_DIR = include
OUTPUT = main.o

# Create object directory
$(shell mkdir -p $(OBJ_DIR))

# List all source files
SRC = $(SRC_DIR)/main.c $(SRC_DIR)/dataStructs.c $(SRC_DIR)/file.c $(SRC_DIR)/process.c

# Generate a list of object files in the object directory
OBJ = $(patsubst $(SRC_DIR)/%.c, $(OBJ_DIR)/%.o, $(SRC))

# Default target
all: $(OUTPUT)

# Link object files to create the final executable
$(OUTPUT): $(OBJ)
	$(CC) $(CFLAGS) $(OBJ) -o $(OUTPUT)

# Compile C files into object files in the object directory
$(OBJ_DIR)/%.o: $(SRC_DIR)/%.c
	$(CC) $(CFLAGS) -I$(INCLUDE_DIR) -c $< -o $@

# Clean up
clean:
	rm -rf $(OBJ_DIR) $(OUTPUT)

# Run the program
run: all
	./$(OUTPUT) test.db
