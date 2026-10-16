# Reflection — Lab 5: Static Code Analysis

## 1. What is static code analysis, and why is it useful?

Static code analysis checks source code without executing it. It helps identify potential bugs, security vulnerabilities, and coding-style problems early, making the program easier to maintain and safer to use.

## 2. What is the difference between Pylint, Bandit, and Flake8?

Pylint checks overall code quality, naming, documentation, and possible programming mistakes. Bandit identifies potentially insecure coding patterns. Flake8 checks Python formatting and PEP 8 style rules. Using all three provides a more complete review of the code.

## 3. Which issues did you find, and how did you fix them?

I found weak SHA-1 hashing, a hardcoded gateway secret, unsafe temporary-file creation, and the use of a non-cryptographic random generator for OTP generation. I also corrected a mutable default argument, naming and documentation problems, and formatting violations. These changes improved security and maintainability.

## 4. How did static analysis improve the program, and what are its limitations?

After fixing the reported issues, Pylint improved from 5.69/10 to 10/10, Bandit reported no findings, and Flake8 reported no violations. This showed me how static analysis can identify problems before deployment. However, clean reports do not guarantee that a program is completely secure or functionally correct, so testing and code review are still necessary.
