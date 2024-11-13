import subprocess
import unittest

class TestDatabase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Compile the C program before running tests
        compile_process = subprocess.run(["gcc", "main.c", "-o", "main.o"], capture_output=True, text=True)
        if compile_process.returncode != 0:
            raise RuntimeError(f"Compilation failed:\n{compile_process.stderr}")

    def run_script(self, commands):
        # Run the compiled C program and feed it commands
        process = subprocess.Popen("./main.o", stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate("\n".join(commands))
        return stdout.splitlines()
    
    def assertMatchArray(self, result, expected_output):
        # Sort both lists for order-agnostic comparison
        self.assertEqual(sorted(result), sorted(expected_output), f"\nExpected: {expected_output}\nGot: {result}")
    
    def test_insert_and_retrieve_row(self):
        result = self.run_script([
            "insert 1 user1 person1@example.com",
            "select",
            ".exit ",
        ])
        expected_output = [
            "db > Executed.",
            "db > (1, user1, person1@example.com)",
            "Executed.",
            "db > "
        ]
        self.assertMatchArray(result, expected_output)

    def test_table_full_error(self):
        script = [f"insert {i} user{i} person{i}@example.com" for i in range(1, 1402)]
        script.append(".exit ")
        result = self.run_script(script)
        # Check the second-to-last line for the "table full" error
        self.assertEqual(result[-2], "db > Error: Table full.")
    
    def test_insert_max_length_strings(self):
        long_username = "a" * 32
        long_email = "a" * 255
        script = [
            f"insert 1 {long_username} {long_email}",
            "select",
            ".exit ",
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
            ".exit ",
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
            ".exit ",
        ]
        result = self.run_script(script)
        expected_output = [
            "db > ID must be positive.",
            "db > Executed.",
            "db > "
        ]
        self.assertMatchArray(result, expected_output)

if __name__ == "__main__":
    unittest.main()