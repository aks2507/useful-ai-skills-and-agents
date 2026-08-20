# Language Profiles

Honor the user's requested language. Otherwise select the first available profile in this order: Java, Python, TypeScript, C++. Use another language when requested, applying the same principles.

## Java

- Target the installed JDK; avoid preview features.
- Prefer a small package rooted under `src/main/java` and tests under `src/test/java` only when Maven or Gradle is already justified.
- For a dependency-free solution, keep package-free `.java` files under `solution/src` and use a self-checking `SolutionTest` main class.
- Use records only when supported by the installed JDK and they simplify immutable domain records.
- Prefer `enum` for closed lifecycle states and `java.time.Clock` for testable time.

Dependency-free commands:

```bash
javac -d out src/*.java
java -ea -cp out SolutionTest
java -cp out Main
```

## Python 3

- Use type hints and small modules; do not emulate Java with excessive interfaces.
- Prefer `dataclasses`, `Enum`, and explicit domain exceptions.
- Use `unittest` from the standard library unless an existing project already uses pytest.
- Inject a callable clock or identifier supplier when needed.

Commands:

```bash
python3 -m compileall -q solution
python3 -m unittest discover -s solution -p 'test_*.py'
python3 solution/main.py
```

## TypeScript

- Use the installed TypeScript/Node configuration when present. Do not create a dependency-heavy toolchain for one article.
- Prefer discriminated unions for closed state variants and interfaces for behavioral boundaries, not every data record.
- Keep compiler strictness enabled.
- Use the built-in `node:test` runner when the available Node version supports it.

Typical commands:

```bash
npx tsc --noEmit
npm test
npm run demo
```

Do not claim these commands ran unless the project contains the corresponding scripts and dependencies.

## C++

- Target the installed compiler and use at least C++17 when available.
- Express ownership with values and smart pointers; avoid raw owning pointers.
- Use `enum class` for lifecycle state and RAII locks for concurrency.
- Keep tests dependency-free unless the repository already has a test framework.

Dependency-free commands:

```bash
c++ -std=c++17 -Wall -Wextra -pedantic src/*.cpp -o solution_test
./solution_test
```

## Cross-language release rules

- Include exact tool versions when behavior depends on them.
- Keep the solution buildable from a fresh directory with documented commands.
- Prefer one obvious entry point and one obvious test command.
- Never mix pseudocode markers into runnable source.
- Link article class and method names to their source-file locations when useful.
