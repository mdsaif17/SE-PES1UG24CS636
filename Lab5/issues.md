# Static Analysis Findings — Lab 5

## Summary

The `digital_wallet.py` program was analyzed using Pylint, Bandit, and Flake8. The initial reports identified code-quality, security, and formatting issues. After making corrections, all three tools were run again.

# Issues Identified and Fixed

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| Weak SHA-1 Hash | Security | 14 | SHA-1 is a weak hashing algorithm for security purposes. | Replaced SHA-1 with SHA-256 for the lab demonstration. |
| Unsafe Temporary File | Security | 60 | `tempfile.mktemp()` can create a security risk due to a race condition. | Replaced it with `tempfile.NamedTemporaryFile()`. |
| Hardcoded Gateway Secret | Security | 6 | The gateway secret was directly stored in the source code. | Read the secret from the `WALLET_GATEWAY_SECRET` environment variable. |
| Insecure OTP Generation | Security | 64 | `random.randint()` is not suitable for security-sensitive OTP generation. | Replaced it with `secrets.randbelow()`. |
| Mutable Default Argument | Bug | 17 | `log=[]` is shared across function calls and can retain data unexpectedly. | Changed the default to `None` and initialized the list inside the function. |
| Missing Docstrings | Code Quality | Multiple | Functions and the module did not have sufficient documentation. | Added module and function docstrings. |
| Inconsistent Naming | Code Quality | Multiple | Function and variable names did not follow Python naming conventions. | Renamed functions and variables using `snake_case`. |
| Flake8 Formatting Violations | Style | 76, 78–80 | Missing spaces around operators and commas, incorrect inline-comment spacing, and missing blank lines. | Corrected spacing and blank-line formatting. |

## Verification Results

- **Pylint:** Improved from 5.69/10 to 10.00/10.
- **Bandit:** Four initial findings; no issues identified after fixes.
- **Flake8:** Four initial formatting violations; no violations after fixes.


## Conclusion

Static analysis helped identify security weaknesses, maintainability problems, and formatting mistakes. After fixing the findings, the program ran successfully and the final checks reported a Pylint score of 10/10, no Bandit findings, and no Flake8 violations.

**Note:** SHA-256 is an improvement over SHA-1 for this demonstration, but production PIN storage should use a salted, deliberately slow password-hashing method and include appropriate attempt limits.
