import subprocess
import unittest
import os

class TestDatabase(unittest.TestCase):
    DATABASE_PATH = "./main.o"  # Path to your compiled database binary
    TEST_DB_PATH = "test.db"  # Path to your test database file


    @classmethod
    def setUpClass(cls):
        # Compile the C program before running tests
        compile_process = subprocess.run(["make"], capture_output=True, text=True)
        if compile_process.returncode != 0:
            raise RuntimeError(f"Compilation failed:\n{compile_process.stderr}")
    
    def setUp(self):
        # Remove the database file before each test to ensure a clean slate
        if os.path.exists("test.db"):
            os.remove("test.db")

    def run_script(self, commands):
        # Run the compiled C program and feed it commands
        process = subprocess.Popen(["./main.o", "test.db"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate("\n".join(commands) + "\n")
        out = stdout.splitlines()
        # print(out)
        return out
    
    """ def run_script(self, commands):
        try:
            # Run the compiled C program and feed it commands
            process = subprocess.Popen(["./main.o", "test.db"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate("\n".join(commands) + "\n")
            if stderr:
                print(f"Error from program: {stderr.strip()}")
            out = stdout.splitlines()
            print("Captured Output:", out)
            return out
        except Exception as e:
            self.fail(f"Error running script: {e}") """

    def assertMatchArray(self, result, expected_output):
        # Sort both lists for order-agnostic comparison
        self.assertEqual(sorted(result), sorted(expected_output), f"\nExpected: {expected_output}\nGot: {result}")
    
    def test_insert_and_retrieve_row(self):
        result = self.run_script([
            "insert 1 user1 person1@example.com",
            "select",
            ".exit",
        ])
        expected_output = [
            "db > Executed.",
            "db > (1, user1, person1@example.com)",
            "Executed.",
            "db > "
        ]
        self.assertMatchArray(result, expected_output)
    
    def test_data_persistence_after_exit(self):
        # Run first script to insert a row and exit
        result1 = self.run_script([
            "insert 1 user1 person1@example.com",
            ".exit",
        ])
        expected_output1 = [
            "db > Executed.",
            "db > ",
        ]
        self.assertMatchArray(result1, expected_output1)

        # Run a second script to verify the row is still there after reopening
        result2 = self.run_script([
            "select",
            ".exit",
        ])
        expected_output2 = [
            "db > (1, user1, person1@example.com)",
            "Executed.",
            "db > ",
        ]
        self.assertMatchArray(result2, expected_output2)

    def test_table_full_error(self):
        script = [f"insert {i} user{i} person{i}@example.com" for i in range(1, 1402)]
        script.append(".exit")
        result = self.run_script(script)
        
        expected_output = [
            "db > Executed.",
            "db > Need to implement updating parent after split",
        ]
        self.assertGreater(len(result), 1, "Output is too short; possible crash.")
        self.assertMatchArray(result[-2:], expected_output)
    
    def test_insert_max_length_strings(self):
        long_username = "a" * 32
        long_email = "a" * 255
        script = [
            f"insert 1 {long_username} {long_email}",
            "select",
            ".exit",
        ]
        result = self.run_script(script)
        expected_output = [
            "db > Executed.",
            f"db > (1, {long_username}, {long_email})",
            "Executed.",
            "db > "
        ]
        self.assertMatchArray(result, expected_output)
    
    def test_error_on_long_strings(self):
        long_username = "a" * 33
        long_email = "a" * 256
        script = [
            f"insert 1 {long_username} {long_email}",
            "select",
            ".exit",
        ]
        result = self.run_script(script)
        expected_output = [
            "db > String is too long.",
            "db > Executed.",
            "db > "
        ]
        self.assertMatchArray(result, expected_output)
    
    def test_error_on_negative_id(self):
        script = [
            "insert -1 cstack foo@bar.com",
            "select",
            ".exit",
        ]
        result = self.run_script(script)
        expected_output = [
            "db > ID must be positive.",
            "db > Executed.",
            "db > "
        ]
        self.assertMatchArray(result, expected_output)
    
    def test_print_btree_structure(self):
        script = [
            "insert 3 user3 person3@example.com",
            "insert 1 user1 person1@example.com",
            "insert 2 user2 person2@example.com",
            ".btree",
            ".exit"
        ]
        result = self.run_script(script)
        expected_output = [
            "db > Executed.",
            "db > Executed.",
            "db > Executed.",
            "db > Tree:",
            "- leaf (size 3)",
            "  - 1",
            "  - 2",
            "  - 3",
            "db > "
        ]
        self.assertMatchArray(result, expected_output)

    def test_print_constants(self):
        script = [
            ".constants",
            ".exit",
        ]
        result = self.run_script(script)
        expected_output = [
            "db > Constants:",
            "ROW_SIZE: 293",
            "COMMON_NODE_HEADER_SIZE: 6",
            "LEAF_NODE_HEADER_SIZE: 10",
            "LEAF_NODE_CELL_SIZE: 297",
            "LEAF_NODE_SPACE_FOR_CELLS: 4086",
            "LEAF_NODE_MAX_CELLS: 13",
            "db > ",
        ]
        self.assertMatchArray(result, expected_output)
    
    def test_duplicate_id_error(self):
        script = [
            "insert 1 user1 person1@example.com",
            "insert 1 user1 person1@example.com",
            "select",
            ".exit",
        ]
        result = self.run_script(script)
        expected_output = [
            "db > Executed.",
            "db > Error: Duplicate key.",
            "db > (1, user1, person1@example.com)",
            "Executed.",
            "db > ",
        ]
        self.assertMatchArray(result, expected_output)

    def test_3_leaf_node_btree_structure(self):
        script = [f"insert {i} user{i} person{i}@example.com" for i in range(1, 15)]
        script.append(".btree")
        script.append("insert 15 user15 person15@example.com")
        script.append(".exit")
        print(script)
        result = self.run_script(script)
        print(result)
        expected_output = [
            "db > Tree:",
            "- internal (size 1)",
            "  - leaf (size 7)",
            "    - 1",
            "    - 2",
            "    - 3",
            "    - 4",
            "    - 5",
            "    - 6",
            "    - 7",
            "  - key 7",
            "  - leaf (size 7)",
            "    - 8",
            "    - 9",
            "    - 10",
            "    - 11",
            "    - 12",
            "    - 13",
            "    - 14",
            "db > Executed.",
            "db > ",
        ]
        # Only compare the specific part of the result with the tree structure and error message
        self.assertMatchArray(result[14:], expected_output)
    
    def test_multi_level_tree_select(self):
        # Insert multiple rows to create a multi-level tree and select all rows
        script = []
        for i in range(1, 16):
            script.append(f"insert {i} user{i} person{i}@example.com")
        script.append("select")
        script.append(".exit")

        result = self.run_script(script)

        expected_output = [
            "db > (1, user1, person1@example.com)",
            "(2, user2, person2@example.com)",
            "(3, user3, person3@example.com)",
            "(4, user4, person4@example.com)",
            "(5, user5, person5@example.com)",
            "(6, user6, person6@example.com)",
            "(7, user7, person7@example.com)",
            "(8, user8, person8@example.com)",
            "(9, user9, person9@example.com)",
            "(10, user10, person10@example.com)",
            "(11, user11, person11@example.com)",
            "(12, user12, person12@example.com)",
            "(13, user13, person13@example.com)",
            "(14, user14, person14@example.com)",
            "(15, user15, person15@example.com)",
            "Executed.", 
            "db > "
        ]

        # Assert that the relevant portion of the output matches the expected output
        self.assertEqual(result[15:], expected_output)


if __name__ == "__main__":
    unittest.main()