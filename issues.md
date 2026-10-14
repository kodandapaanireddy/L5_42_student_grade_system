# Issues Found and Fixed

Tools: Pylint (5.51/10 before), Bandit (6 findings: 2 High, 1 Medium, 3 Low), Flake8 (8 findings).
All issues below were fixed. After the fixes: Pylint 10.00/10, Bandit 0 issues, Flake8 0 issues.

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| Shell command injection via `os.system` (Bandit B605, High) | Security | 60 | `os.system("echo ... " + filename)` passes a user-controlled filename to a shell, so a name like `x; rm -rf ~` would run commands. | Removed the shell call; the export is now reported with `logging.info`. |
| Weak MD5 hash (Bandit B324, High) | Security | 49 | MD5 is broken and unsuitable for hashing identifiers. | Replaced with `hashlib.sha256`. |
| Use of `eval()` on a parameter (Bandit B307 Medium, Pylint W0123) | Security | 44 | `eval(gpa_expr)` runs arbitrary code from the caller. | Removed `eval`. `compute_weighted_gpa(student_id, scale)` now computes `average / scale` directly. |
| Hardcoded secret and printed in output (Bandit B105, Low) | Security | 64, 72 | Admin token written in source and printed to the console. | Read from env var `GRADE_PORTAL_TOKEN`; only prints whether it is configured. |
| Insecure random for PIN (Bandit B311, Low) | Security | 53 | `random.randint` is predictable. | Used `secrets.randbelow(9000) + 1000`. |
| Mutable default argument (Pylint W0102) | Bug | 15 | `grade_list=[]` is shared between calls, so log entries leak across calls. | Default is `None`; a new list is created inside the function. |
| Bare `except: pass` (Pylint W0702, Flake8 E722, Bandit B110) | Bug | 26-27 | Hides every error, including unknown student IDs and bad types, and reports success regardless. | Catch only `KeyError`, log a warning, return `False`; the function returns `True` on success. |
| Missing input validation | Bug | 16, 25 | Marks accepted any type and values above 100; attendance accepted negatives and non-numbers. | Check type and range (0-100) in `add_grade`; check type and non-negative in `record_attendance`. |
| GPA outside 4.0 scale (found by running the program) | Bug | 68 | The output was `4.35`, which is above the 4.0 maximum, because the average was divided by 20. | Default scale is now `100 / 4.0 = 25`, and the result is capped at 4.0. S01 now gives 3.48. |
| Division by zero on empty marks | Bug | 34, 43 | `sum / len` crashes when a student has no marks. | Return `False` / raise a clear `ValueError` when there are no marks. |
| Unused variables `grace_marks`, `avg_score` (Pylint W0612, Flake8 F841) | Code quality | 31, 43 | Variables assigned but never used. | Removed `grace_marks`; `avg_score` is now used in the return. |
| Unused import `json` (Pylint W0611, Flake8 F401) | Code quality | 6 | Imported but never used. | Now used for exporting the gradebook with `json.dump`; unused `random` import replaced by `secrets`. |
| File opened without `with` or encoding (Pylint R1732, W1514) | Code quality | 57-59 | The file is not closed if `write` fails, and the encoding is system-dependent. | `with open(filename, "w", encoding="utf-8")`. |
| Comparison to `None` with `==` (Pylint C0121, Flake8 E711) | Style | 32 | Should use identity. | `student is None`. |
| Redundant if/else returning bool (Pylint R1703, R1705) | Style | 35-38 | Needless branching. | `return avg >= pass_threshold`. |
| Function name `addGrade` (Pylint C0103) | Style | 15 | Not snake_case. | Renamed to `add_grade`; call in `main` updated. |
| `%` string formatting (Pylint C0209) | Style | 19 | Old-style formatting. | f-string. |
| Missing docstrings (Pylint C0116) | Style | 15-63 | Functions undocumented. | Added a docstring to every function. |
| Long lines (Flake8 E501) | Style | 19, 34 | Over 79 characters. | Wrapped or shortened. |
| Missing final newline (Pylint C0304, Flake8 W292) | Style | 75 | File does not end with a newline. | Added. |
| `main()` runs on import and no logging setup | Code quality | 75 | Importing the module runs the program. | Added `if __name__ == "__main__":` with `logging.basicConfig(...)`. |
