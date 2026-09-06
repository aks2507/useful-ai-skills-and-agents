# Language Profiles

Honor the user's requested language. Otherwise select the first available profile in this order: Java, Python, TypeScript, C++. Apply the same ownership and packaging principles when another language is requested.

Use a problem-specific root package such as `vendingmachine`; do not literally use `problem` in final code. Add `policy` only when the article demonstrates a behavior that varies.

## Java

- Target the installed JDK; avoid preview features and external libraries.
- Use the standard source tree even for a dependency-free solution:

```text
solution/
└── src/
    ├── main/java/<root-package>/
    │   ├── model/       # entities, records, enums, domain errors
    │   ├── service/     # public orchestrator and workflows
    │   ├── policy/      # only for earned interchangeable behavior
    │   └── demo/        # deterministic Main entry point
    └── test/java/<root-package>/
        └── SolutionTest.java
```

- Omit unused directories. A small junior solution often needs only `model`, `service`, and `demo`.
- Use records only when supported and useful for immutable domain records.
- Prefer `enum` for closed lifecycle states and `java.time.Clock` for testable time.
- Keep tests dependency-free with assertions or a small self-checking runner unless a build tool is already justified.

Dependency-free commands from `solution/`:

```bash
mkdir -p out
javac -d out $(find src/main/java src/test/java -name '*.java' | sort)
java -ea -cp out <root-package>.SolutionTest
java -cp out <root-package>.demo.Main
```

If tests live in a `.test` package, reflect that package in the test command.

## Python 3

- Use type hints and small modules; do not emulate Java with an interface for every class.
- Prefer `dataclasses`, `Enum`, and explicit domain exceptions.
- Use `unittest` unless the existing project already uses pytest.
- Inject a callable clock or identifier supplier when needed.

```text
solution/
├── src/<root_package>/
│   ├── __init__.py
│   ├── model.py          # split into model/ only when it is genuinely clearer
│   ├── service.py
│   ├── policy.py         # optional
│   └── demo.py
└── tests/
    └── test_<root_package>.py
```

Commands from `solution/`:

```bash
PYTHONPATH=src python3 -m compileall -q src tests
PYTHONPATH=src python3 -m unittest discover -s tests -p 'test_*.py'
PYTHONPATH=src python3 -m <root_package>.demo
```

## TypeScript

- Use an installed TypeScript/Node configuration when present. Do not create a dependency-heavy toolchain for one article.
- Prefer discriminated unions for closed state variants and interfaces for demonstrated behavioral boundaries.
- Keep compiler strictness enabled.
- Use the built-in `node:test` runner when supported.

```text
solution/
├── src/
│   ├── model/
│   ├── service/
│   ├── policy/           # optional
│   └── demo.ts
├── tests/
└── tsconfig.json
```

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

```text
solution/
├── src/
│   ├── model/
│   ├── service/
│   ├── policy/           # optional
│   └── main.cpp
└── tests/
    └── solution_test.cpp
```

Dependency-free commands should name every source directory explicitly or use a small justified build file. Do not rely on `src/*.cpp` after introducing subdirectories.

## Package design rules

- Package by responsibility, not one directory per type.
- Keep dependencies pointed inward: `model` knows no `service`; `service` coordinates `model` and optional `policy`; `demo` and tests call the public service API.
- Keep domain exceptions beside the state they protect or in a small shared model file. Avoid a generic `exceptions` package with one class.
- Avoid `common`, `misc`, `helpers`, and `utils` unless several cohesive operations genuinely belong there.
- Explain the chosen tree in the article so the reader learns both object design and code organization.

## Cross-language release rules

- Include exact tool versions when behavior depends on them.
- Keep the solution buildable from a fresh directory with documented commands.
- Prefer one obvious public entry point, one demo command, and one test command.
- Never mix pseudocode markers into runnable source.
- Link article class and method names to their source-file locations when useful.
- Include all production, test, and required build files in the PDF appendix.
