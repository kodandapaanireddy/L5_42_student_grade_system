# Reflection



**1. Which issues were the easiest and hardest to fix?**
The easiest were the style issues (naming, docstrings, final newline, `is None`, unused import), since the tools tell you exactly what to change. The hardest was `eval()` in `compute_weighted_gpa`: removing it meant changing the function's interface, because the caller passed an expression string. I replaced it with a `scale` parameter. Replacing the bare `except: pass` was also harder than it looks, because I had to decide what the function should return and log.

**2. Did the tools report any false positives?**
Mostly no. Bandit B105 (hardcoded password) on `portal_token` was low confidence, but here it really was a hardcoded secret. B311 (`random`) would be a false positive if the PIN were only a non-secret label, but for a registration PIN `secrets` is the right choice. MD5 for a non-security checksum would also be a false positive, but here it was used to hash a student identifier.

**3. How would you integrate static analysis into your development workflow?**
Run Flake8 and Pylint in a pre-commit hook so style problems are caught before a commit, and run all three tools in CI (for example GitHub Actions) on every pull request, failing the build on Bandit High/Medium findings or a Pylint score below a set threshold. Keep a config file (`.pylintrc`, `setup.cfg`) so the team shares the same rules.

**4. What tangible improvements did you see in code quality, readability and security?**
The Pylint score went from 5.51/10 to 10.00/10, Bandit went from 6 findings (2 High) to none, and Flake8 went from 8 findings to none. The shell-injection, `eval` and weak-hash risks are gone, the secret no longer lives in source, and errors are logged instead of silently swallowed. The code is easier to read and maintain, and the module can be imported without running. One thing the tools could not find was the GPA of 4.35 above the 4.0 maximum, which I found only by running the program, so static analysis complements but does not replace testing.
