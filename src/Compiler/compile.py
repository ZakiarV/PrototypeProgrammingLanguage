import subprocess
from src.Translator.c_code.get_c_code_directory import get_c_code_directory


class Compiler:
    def compile(self):
        try:
            subprocess.run(["clang", rf"{get_c_code_directory()}\main.cpp", rf"{get_c_code_directory()}\std_lib.cpp", "-o", rf"{get_c_code_directory()}\main"])
        except Exception as e:
            print(f"Compilation failed: {e}")
            return
        print("Compilation successful.\n\n")
        subprocess.run([rf"{get_c_code_directory()}\main"])
        print("\n\nExecution successful.")
