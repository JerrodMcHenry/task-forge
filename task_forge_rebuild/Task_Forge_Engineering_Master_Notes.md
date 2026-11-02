# Task Forge — Engineering Master Notes

**Version:** 3.0 — October 31, 2026  
**Scope:** Task Manager CLI completed: Python fundamentals, CRUD, JSON persistence, modular architecture, debugging, pytest unit tests and filesystem integration tests.  
**Purpose:** A section-specific reference containing only material covered in the Task Manager project. This is a review guide, **not proof of mastery**.

## How to use this reference

- **After a lesson (5 minutes):** Review only the new concepts and explain them without reading.
- **Once a week (20–30 minutes):** Answer the retrieval questions, write a small example from memory, and revisit anything you missed.
- **Before interviews:** Prioritize the “Interview checks” and implement the exercises without AI.
- **Progress labels:** **Covered** = encountered in working code; **Practice** = requires more independent repetition; **Independently verified** = demonstrated without supplied implementation.
- **Note-taking rule:** Do not transcribe lessons. Add only a new principle, a surprising failure, or a reusable pattern that you did not already know.

---

# Part I — Python fundamentals

## 1. Variables, objects, and mutability — Covered; practice explaining

A variable is a name bound to an object. Some objects are mutable (e.g., `dict`, `list`); others are immutable (e.g., `int`, `str`, `tuple` containing only immutable values). Mutating an object is different from rebinding a variable.

```python
items = {1: "pending"}
alias = items
alias[1] = "completed"  # items[1] is also "completed"
alias = {}               # items still refers to the original dictionary
```

**Remember:** Functions receive references to objects through parameters. Mutating a passed-in dictionary is visible to the caller; assigning a new dictionary to the parameter does not rebind the caller's variable.

**Common mistake:** Assuming `x = ...` and `x[key] = ...` have the same effect.

**Interview check:** Explain mutation versus reassignment with a dictionary passed into a function.

## 2. Functions, parameters, arguments, and return values — Covered; priority practice

A **parameter** is a name in a function definition. An **argument** is the value supplied when calling it. `return` gives the caller a value; `print` only displays output.

```python
def task_label(task):       # task is a parameter
    return task["title"]   # value goes back to caller

label = task_label({"title": "Study"})  # dictionary is an argument
print(label)
```

Without an explicit `return`, a Python function returns `None`. A function can mutate a passed-in object and also return a value; these are separate behaviors.

**Common mistake:** Printing a result when other code needs to use it; relying on globals instead of clear parameters.

**Interview check:** Explain `return` vs `print`, local scope, and what happens to a mutable argument.

## 3. Dictionaries and lists — Covered; high priority

A list is an ordered sequence accessed by position; a dictionary maps **hashable keys** to values. Your Task Manager uses a dictionary keyed by task ID for direct access.

```python
tasks = {}
tasks[1] = {"id": 1, "title": "Study", "status": "pending"}  # create
task = tasks[1]                                            # read
tasks[1]["status"] = "completed"                          # update
del tasks[1]                                               # delete
```

Useful dictionary methods:

```python
for key, value in tasks.items():
    print(key, value)
for task in tasks.values():
    print(task)
if 42 in tasks:
    print("Found")
```

**Complexity:** Dictionary lookup, insertion, and deletion are **O(1) average-case**, with possible worst-case degradation. Looking for a value by scanning a list is generally **O(n)**. List access by index is **O(1)**; inserting or removing near the front usually requires shifting elements, **O(n)**.

**Common mistake:** Treating a dictionary key as a list index; forgetting that accessing a missing key with `tasks[id]` raises `KeyError`.

**Interview check:** Why choose a dictionary keyed by task ID instead of a list of task dictionaries?

## 4. Control flow and iteration — Covered

- `if` / `elif` / `else` select branches.
- `for` iterates over a sequence or iterable.
- `while` repeats while a condition is true.
- `break` exits the nearest loop; `continue` skips to the next iteration.
- A `while True` menu needs an explicit exit path, such as `break`.

**Common mistake:** Confusing `continue` with `break`, or putting an update in a branch that never runs.

**Interview check:** Trace a loop through valid, invalid, and exit inputs.

## 5. Input validation and exceptions — Covered

Validate data at the boundary before trusting it. For a CLI, user input arrives as strings.

```python
title = input("Title: ").strip()
if not title:
    print("Title required")

try:
    task_id = int(input("Task ID: "))
except ValueError:
    print("Enter a whole number")
```

`int("abc")` raises `ValueError`; opening a missing file for reading raises `FileNotFoundError`; looking up a missing dictionary key raises `KeyError`.

**Remember:** Catch exceptions you can handle meaningfully. Avoid a broad `except Exception` that hides bugs. Check whether a task exists before changing or deleting it.

**Interview check:** What is the difference between validation and exception handling? When would you use each?

---

# Part II — Data, storage, and application structure

## 6. CRUD and data modeling — Covered

**CRUD** means Create, Read, Update, Delete. The Task Manager models each task as a record:

```python
{"id": 7, "title": "Write tests", "status": "pending"}
```

Think about fields, types, allowed states, unique identifiers, and invalid transitions. A simple model is fine when it meets requirements.

**Interview check:** How would you prevent two tasks from receiving the same ID?

## 7. In-memory state versus persistence — Covered

An in-memory dictionary is lost when the process ends. Persistence writes information somewhere that survives the process, such as a file or database.

```python
import json

with open("tasks.json", "w") as file:
    json.dump(tasks, file, indent=4)
```

`with open(...)` uses a context manager to close the file when the block exits, including on most exceptions.

**Important:** Writing JSON this way replaces the file contents. It does not provide database-style transactions, concurrent write protection, or robust crash recovery.

**Interview check:** Why use PostgreSQL rather than a JSON file for a multi-user backend? Discuss queries, concurrent access, transactions, constraints, and reliability.

## 8. JSON serialization and deserialization — Covered

**Serialization** converts application data into a representation that can be stored or transmitted. **Deserialization** reconstructs data from that representation.

```python
json.dump(tasks, file)   # Python object -> JSON file
loaded = json.load(file) # JSON file -> Python object
```

JSON object keys are strings. A Python dictionary keyed by integers becomes a JSON object with string keys. The Task Manager restores integer keys on load:

```python
restored = {int(key): value for key, value in loaded.items()}
```

**Common mistake:** Assuming JSON preserves integer dictionary keys. Also distinguish `dump` / `load` (file objects) from `dumps` / `loads` (strings).

**Interview check:** Why might `tasks[1]` work before saving but fail after loading if you skip key conversion?

## 9. Separation of concerns — Introduced; practice pending

Different responsibilities should be clear even when code is in one file:

- **Interface:** Gather input and show output.
- **Business logic:** Create, complete, list, and delete task records.
- **Storage:** Read and write saved data.

Separating these responsibilities can improve testing and maintainability. **It does not automatically require one file per responsibility.** Choose structure appropriate to the project's size.

**Interview check:** Why is a function that calls `input()`, changes data, and writes a file harder to unit-test than one that accepts arguments and returns a result?

## 10. Refactoring versus feature development — Introduced

**Refactoring** changes internal code structure while preserving intended external behavior. **Feature development** changes or adds behavior. A refactor should have a concrete reason and be protected by tests where possible.

**Remember:** Do not intentionally build throwaway architecture when the known requirements already justify a straightforward structure. Also avoid speculative overengineering.

**Interview check:** How would you safely extract a function from a working CLI? Describe preserving behavior and running tests.

---

# Part III — Debugging and engineering judgment

## 11. Debugging workflow — Covered in practice; continue practicing

1. **Reproduce:** Get a reliable failing input or test.
2. **Observe:** Read the traceback and inspect actual values.
3. **Localize:** Find where actual behavior diverges from expected behavior.
4. **Hypothesize:** Explain a likely cause before changing code.
5. **Fix narrowly:** Change the smallest relevant behavior.
6. **Verify:** Rerun the failure and nearby regression tests.

**Examples from Task Manager:** Invalid numeric input, missing JSON file, empty titles, missing task IDs, and integer keys after JSON loading.

**Interview check:** Explain how you would investigate a task that appears to save correctly but disappears after restart.

## 12. Known limitations in the current Task Manager — Review, not immediate rewrite

- Malformed JSON currently isn't handled by the loader.
- After deleting the highest task ID and restarting, `max(existing_ids) + 1` can reuse a previously issued ID. Whether that matters depends on the identifier requirements.
- A single JSON file is unsuitable for simultaneous multi-user updates without additional coordination.
- Keep the interactive CLI behind `main()` and an `if __name__ == "__main__":` guard so importing `main.py` does not start the menu.

**Engineering principle:** Not every limitation deserves an immediate fix. Prioritize by requirements, risk, and learning value.

---

# Part IV — Interview retrieval checks

Answer aloud, then implement a tiny example when relevant:

1. What is the difference between `return` and `print`?
2. What happens when a function mutates a dictionary argument?
3. How is reassignment different from mutation?
4. When would you choose a dictionary over a list?
5. What are the average time complexities of dictionary lookup and insertion?
6. What is CRUD? Give an example of each operation.
7. Why does JSON loading change integer dictionary keys into strings?
8. What does `with open(...)` accomplish?
9. What should happen when a user enters a nonnumeric task ID?
10. Why are databases often preferable to JSON files for production services?
11. What is refactoring, and how do tests reduce its risk?
12. How do you reproduce, isolate, fix, and verify a bug?

**Practical challenge (15–20 minutes, no AI):** Write `complete_task(tasks, task_id)` that marks an existing task completed and reports whether it succeeded. Test an existing ID, a missing ID, and a task already completed. Explain whether your function mutates its input.

---

# Part V — Automated testing with pytest (completed)

## 13. Why tests exist — Covered

An automated test executes code and checks whether its **actual behavior** matches an **expected result**. Running the same tests after changes is **regression testing**: it helps detect previously working behavior that has broken. A passing test proves only the conditions that test actually checks; it does not prove the entire program is correct.

**Remember:** Test the behavior and important state changes, not incidental implementation details. Prefer meaningful cases over chasing a raw test count.

**Interview check:** Why is manual testing alone insufficient after repeated code changes?

## 14. Arrange → Act → Assert — Covered

Most tests follow three steps:

```python
def test_complete_task():
    # Arrange: create known initial state
    tasks = {1: {"id": 1, "title": "Study", "status": "pending"}}

    # Act: execute the behavior
    result = complete_task(tasks, 1)

    # Assert: verify outcome AND state
    assert result is True
    assert tasks[1]["status"] == "completed"
```

`assert` raises `AssertionError` if its condition is false. Pytest discovers functions whose names start with `test_` in appropriately named test files.

**Common mistake:** Asserting only that a function returned `True` while forgetting to verify that the task actually changed.

**Interview check:** Write a test for deleting a task that checks both the return value and dictionary contents.

## 15. Unit, integration, end-to-end, and acceptance testing — Covered conceptually

| Level | What it checks | Task Manager example |
|---|---|---|
| Unit | One small behavior in isolation | `create_task`, `complete_task`, `delete_task` operating on in-memory dictionaries |
| Integration | Interaction between components or external resources | `save_tasks` followed by `load_tasks` against a real temporary JSON file |
| End-to-end (E2E) | Full workflow from user entry point | Launch CLI, enter menu choices, exit, restart, and inspect saved tasks |
| Acceptance | Whether a requirement is satisfied | User can create, complete, and delete tasks; may be tested at multiple levels |

**Important nuance:** Test classification is partly contextual. A test touching the real filesystem is commonly called an integration test, even if it exercises a small storage module. We manually checked the CLI workflow; we did **not** write an automated E2E test.

**Interview check:** Why not test every behavior only through E2E tests? They tend to be slower, more brittle, and less precise at locating a failure.

## 16. Happy paths, negative paths, and edge cases — Covered

- **Happy path:** Existing task is completed successfully.
- **Negative path:** Completing or deleting ID `99` when no such task exists returns `False` without modifying other tasks.
- **Edge case:** Empty dictionary, blank title, missing JSON file, repeated completion, or malformed JSON (some remain untested/unhandled).

A robust test often checks **what must not happen** as well as what must happen.

```python
def test_complete_nonexistent_task():
    tasks = {1: {"id": 1, "title": "Study", "status": "pending"}}
    result = complete_task(tasks, 99)
    assert result is False
    assert tasks[1]["status"] == "pending"
```

**Interview check:** List three negative cases for an API endpoint that updates a task.

## 17. Fixtures and filesystem isolation — Covered

A **pytest fixture** provides setup/resources for a test. Pytest injects fixtures by matching function parameter names.

- `tmp_path` provides a fresh temporary directory as a `pathlib.Path`.
- `monkeypatch` temporarily modifies environment or process state and restores it after the test.
- `monkeypatch.chdir(tmp_path)` makes relative file paths resolve inside the temporary directory during that test.

```python
from storage import save_tasks, load_tasks


def test_save_and_load_tasks(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    tasks = {1: {"id": 1, "title": "Study", "status": "pending"}}

    save_tasks(tasks)
    loaded = load_tasks()

    assert (tmp_path / "tasks.json").exists()
    assert loaded == tasks


def test_load_tasks_missing_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert load_tasks() == {}
```

**Why it matters:** Tests must not overwrite your real `tasks.json`, depend on a previous test, or leave behind unexpected data.

**Common mistake:** Testing file-writing functions against the actual user data file.

**Interview check:** Explain why an isolated temporary directory is better than writing into a shared project file.

## 18. Your seven completed tests — Reported passing

| Test | Type | Main assertion |
|---|---|---|
| `test_create_task` | Unit | Correct record created and inserted |
| `test_complete_task` | Unit | Existing task changes to completed |
| `test_delete_task` | Unit | Existing task removed |
| `test_complete_nonexistent_task` | Unit | `False`, no unintended change |
| `test_delete_nonexistent_task` | Unit | `False`, existing tasks retained |
| `test_save_and_load_tasks` | Filesystem integration | Round-trip data preserved |
| `test_load_tasks_missing_file` | Filesystem integration | Missing file produces `{}` |

From the project root, with your test folder named `test`:

```bash
python -m pytest test/ -v
```

**Terminal lesson:** Relative paths depend on the current working directory (`pwd`). Running a command from the parent folder can make an otherwise valid test path appear missing. Use `python -m pytest` to run pytest with the selected Python interpreter.

## 19. Final Task Manager architecture — Covered

```text
task_manager_rebuild/
├── main.py             # menu, user input/output, orchestration
├── task_service.py     # create/complete/delete task logic
├── storage.py          # JSON save/load
├── tasks.json          # persisted task data
└── test/
    ├── test_task_service.py
    └── test_storage.py
```

**Call flow:** CLI gathers and validates input → task service changes in-memory data → CLI calls storage to persist successful changes. The storage module converts JSON's string object keys back to integer task IDs when loading.

**Python module pattern:**

```python
from task_service import create_task


def main():
    # interactive CLI logic
    pass


if __name__ == "__main__":
    main()
```

The `__main__` guard means running `python main.py` starts the CLI, but importing `main` does not start the menu. **Design lesson from this project:** Establish the smallest appropriate architecture, data flow, and testing strategy before implementation; avoid predictable rewrites and overengineering.

**Interview check:** What belongs in `main.py`, `task_service.py`, and `storage.py`, and why?

## 20. Further practice and honest gaps

- **Covered with guided implementation:** Python CRUD, JSON persistence, module imports, basic tests, failure tests, filesystem isolation.
- **Needs independent proof:** Design a new small application from requirements, implement functions without copying, debug unfamiliar code, write tests without provided solutions.
- **Known app limitations:** Task ID reuse after restart, malformed JSON errors, and service-level title validation. They are documented rather than endlessly polished.

### Testing review questions

1. Explain Arrange–Act–Assert using a task operation.
2. What is the difference between unit and integration tests?
3. Which of your tests touches the real filesystem?
4. Why use `tmp_path` and `monkeypatch.chdir`?
5. What is a regression test?
6. Why do we test missing IDs, not just valid IDs?
7. What does seven passing tests **not** prove?
8. How does the `__main__` guard help testability?

### Independent mastery check (based on covered material)

Write a `test_complete_task_already_completed` test. Choose the expected behavior, assert the returned result and final state, and explain why you chose that expectation. Then run the full suite.

---

# Part VI — What you must be able to implement independently

Use this as a self-check, **not** as a claim that these skills have all been independently demonstrated. Each task below uses only concepts encountered in Task Manager.

## Python and task logic

- [ ] Write a function accepting parameters and returning a result; explain `return` versus `print`.
- [ ] Create, look up, update, iterate through, and delete entries in a dictionary.
- [ ] Explain mutation versus reassignment by predicting the caller's dictionary after a function call.
- [ ] Implement `create_task(tasks, task_id, title)` using the established task record format.
- [ ] Implement `complete_task(tasks, task_id)` and `delete_task(tasks, task_id)` with a clear success/failure result.
- [ ] Reject empty or whitespace-only task titles in the CLI and handle invalid numeric input without crashing.

## Persistence and modules

- [ ] Save a dictionary as JSON with `with open(...)` and `json.dump(...)`.
- [ ] Load JSON, handle a missing file, and convert serialized string task keys back to integers.
- [ ] Explain what belongs in `main.py`, `task_service.py`, and `storage.py`.
- [ ] Explain what happens when a Python file is imported versus executed as a script.
- [ ] Diagnose a failure caused by running a command from the wrong working directory.

## Testing and debugging

- [ ] Write a pytest test with Arrange → Act → Assert, without copying a template.
- [ ] Test both a successful task operation and a missing-ID operation.
- [ ] Verify the returned value **and** the resulting dictionary state.
- [ ] Write a save/load test using `tmp_path` and `monkeypatch.chdir` without touching the real `tasks.json`.
- [ ] Explain the distinction between unit tests, filesystem integration tests, and a manual end-to-end check.
- [ ] Reproduce a bug, identify its cause, make a focused fix, and rerun relevant tests.

## Review standard

**Understand:** Explain the concept and when to use it.  
**Implement:** Write a working version without copying supplied code.  
**Verify:** Run the program or tests and inspect the actual output.  

Seven passing tests confirm the tested behaviors in the user's reported environment; they do not independently establish mastery of every checklist item.
