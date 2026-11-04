# Task Forge — Master Engineering Notes & Decision Journal

> Foundational Python apprenticeship · Final retrospective · 3 November 2026

Foundational Python apprenticeship | Final retrospective | 3 November 2026

A study guide covering the decisions, code patterns, mistakes, tradeoffs, and engineering habits demonstrated during the Task Forge build.

Evidence boundary: This guide is grounded in the Task Forge conversation and the repository structure/code previously reviewed. It covers documented decisions and representative implementation; it does not claim a full audit of every historical commit or all possible edge cases.


## How to use this guide

- First pass: read the decisions and explain the “why” out loud without looking at the explanations.
- Second pass: reproduce the core functions from a blank editor; do not copy the reference implementation.
- Third pass: use the retrieval questions and mini-labs at the end to prove understanding.
- When you struggle, identify the missing mental model, not merely the missing line of syntax.

## 1. Executive engineering assessment

Task Forge is a deliberately small Python CLI task manager. It uses a dictionary keyed by integer task IDs, a service module for task operations, a storage module for JSON persistence, and a CLI module for user interaction. By the final reported run, 13 pytest tests passed and the project was pushed to GitHub.

The most important learning outcome was not the number of features. It was repeated exposure to the boundary between knowing what a feature should do and constructing a correct implementation independently.

| Demonstrated or practiced | Evidence | Next standard |
| --- | --- | --- |
| Feature integration | Added filtering, search, and editing to an existing CLI | Implement a comparable feature from requirements with less guidance |
| Debugging | Resolved `task` versus `tasks` UnboundLocalError | Diagnose unfamiliar tracebacks independently |
| Testing | Ran pytest and added targeted checks | Specify meaningful expected behavior before delegating tests |
| Reliability | Handled corrupted JSON and invalid task IDs | Understand more failure modes and data contracts |
| Git hygiene | Removed tracked caches/local data, documented project | Recognize tracked vs ignored files immediately |


## 2. Architecture and core data model


```text
task_forge_rebuild/
    main.py              # CLI: input, menu, presentation
    task_service.py      # business operations on task data
    storage.py           # JSON file read/write
    test/
        test_task_service.py
        test_storage.py
```


```python
tasks = {
    1: {"id": 1, "title": "Study Python", "status": "pending"},
    2: {"id": 2, "title": "Build API", "status": "completed"},
}
```


### D01 — Use a dictionary keyed by task ID

Decision: Store tasks as `dict[int, dict]`.

Why: Individual lookup, update, and delete by ID are natural operations. `tasks[task_id]` expresses the intent directly.

Tradeoff / alternative: A list would make ordered display simple but generally requires scanning to find a particular ID. The dictionary adds a key-versus-value iteration trap.

Engineering takeaway: Choose a data structure based on the dominant operations, then understand how iteration behaves.


### D02 — Separate CLI, service, and storage

Decision: Keep input/output in `main.py`, task operations in `task_service.py`, and JSON in `storage.py`.

Why: Each module has one primary reason to change. Service logic can be tested without simulating a menu. Storage can be tested with temporary files.

Tradeoff / alternative: One large file would initially be shorter but would mix UI, business rules, and persistence. A heavier layered framework would be overengineering.

Engineering takeaway: A boundary is useful when it makes code easier to reason about or verify—not because architecture diagrams look impressive.


### D03 — Use JSON file persistence

Decision: Serialize the task dictionary to `tasks.json` with `json.dump`; read with `json.load`.

Why: Standard library only; sufficient for a single-user foundational exercise. It teaches serialization and persistence without introducing a database.

Tradeoff / alternative: JSON is not transactional, offers no concurrency control, and can be corrupted by interrupted writes. PostgreSQL belongs in the next phase.

Engineering takeaway: Use the simplest persistence that satisfies actual requirements, but name its limits.


### D04 — Convert JSON keys back to integers

Decision: During load, use `int(key)` for each serialized key.

Why: JSON object keys are strings, even when Python dictionary keys were integers. The CLI and service expect integer IDs.

Tradeoff / alternative: Leaving keys as strings would make integer lookups fail unexpectedly. Converting can fail on malformed IDs and therefore needs validation.

Engineering takeaway: Serialization boundaries can change data types; never assume a round trip preserves every Python type.


### D05 — Generate next ID using max existing key + 1

Decision: Initialize `next_task_id = max(tasks.keys(), default=0) + 1`.

Why: Works with an empty dictionary and generally avoids collisions with currently present IDs during one run.

Tradeoff / alternative: Deleted highest IDs can be reused after a restart; this is not a durable monotonic ID generator. A database sequence would be stronger.

Engineering takeaway: Identify what an ID-generation strategy guarantees—and what it does not.


## 3. CRUD: operations, mutation, and return contracts


```python
def create_task(tasks, task_id, title):
    task = {"id": task_id, "title": title, "status": "pending"}
    tasks[task_id] = task
    return task
```


```python
def complete_task(tasks, task_id):
    if task_id not in tasks:
        return False
    tasks[task_id]["status"] = "completed"
    return True
```


```python
def delete_task(tasks, task_id):
    if task_id not in tasks:
        return False
    del tasks[task_id]
    return True
```


### D06 — Mutate the task dictionary in service operations

Decision: Create, complete, delete, and edit modify the passed-in dictionary.

Why: The CLI retains one shared in-memory state, and subsequent saves serialize the updated state.

Tradeoff / alternative: Pure functions could return a new dictionary, but would require callers to replace state consistently. Mutation is acceptable if explicit and tested.

Engineering takeaway: Ask on every function: does it mutate inputs, return new data, or both?


### D07 — Use boolean success for some commands

Decision: Complete/delete/edit return `True` on success and `False` when no update occurs.

Why: The CLI can display a success/failure message without parsing exceptions for expected user mistakes.

Tradeoff / alternative: A boolean cannot distinguish missing ID from invalid title; typed result objects or exceptions become useful as requirements grow.

Engineering takeaway: A return type is part of the function contract; pick one that communicates enough information for callers.


### D08 — Validate title before mutation

Decision: Reject empty or whitespace-only edits; trim valid titles.

Why: Prevents an invalid update from partially changing state.

Tradeoff / alternative: Validation only in the CLI would allow direct service callers to bypass it. For create-task, service-level validation remained limited.

Engineering takeaway: Validate at the boundary where the invariant must hold, not only where input happens to arrive.


```python
def update_task_title(tasks, task_id, new_title):
    if not new_title.strip():
        return False
    if task_id not in tasks:
        return False
    tasks[task_id]["title"] = new_title.strip()
    return True
```


## 4. The highest-priority skill gap: requirements → code

The filtering exercise exposed a repeatable issue: the intent was correct (loop, compare status, return result), but the implementation omitted the accumulation pattern and misunderstood dictionary iteration. This is a construction gap, not a lack of intelligence or a reason to restart all Python fundamentals.


# The actual first attempt


```python
def filter_tasks_by_status(tasks, status):
    for task in tasks:
        if task["status"] == status:
            return task[]
    else:
        return []
```

| Problem | Why it fails | Repair |
| --- | --- | --- |
| `for task in tasks` | Iterates keys (integers), not task dictionaries | Use `tasks.values()` |
| `return task[]` | Invalid syntax; no valid index supplied | Append the task to a results list |
| Return inside loop | Exits after first match | Return after the loop finishes |
| No result collection | Cannot return multiple matches | Initialize `results = []` first |
| Loop `else` | Not needed for “no matches” | An untouched results list is already `[]` |


# The reusable algorithm


```python
def filter_tasks_by_status(tasks, status):
    results = []
    for task in tasks.values():
        if task["status"] == status:
            results.append(task)
    return results
```

Memorize the mental sequence, not only this function: INITIALIZE → ITERATE → CHECK → ACCUMULATE → RETURN. The same pattern appears in logs, API responses, report generation, database result processing, and ETL pipelines.


# Critical micro-concepts

- `for x in some_dict` iterates keys. `some_dict.values()` iterates values. `some_dict.items()` yields `(key, value)` pairs.
- `return` ends the entire function immediately. `continue` skips to the next loop iteration. `break` exits the loop.
- `list.append(item)` mutates the list and returns `None`. Do not write `results = results.append(item)`.
- Nested assignment: `tasks[2]["status"] = "completed"` changes one field of one nested record.
- A new list containing original task dictionaries is a new collection, but its elements still refer to the original dictionaries. Changing an element can still mutate source data.

## 5. Filtering and searching: design decisions


### D09 — Filtering returns a list rather than mutating the task store

Decision: `filter_tasks_by_status(tasks, status)` returns matching task records.

Why: Viewing a subset should not delete or change tasks. A list is easy for the CLI to display.

Tradeoff / alternative: Returning a dictionary keyed by IDs would also work and preserve fast lookup; list output is simpler for display.

Engineering takeaway: Separate read-only queries from state-changing commands.


### D10 — Search with case-insensitive substring matching

Decision: Compare `query.lower() in task["title"].lower()`.

Why: Small, understandable behavior; users need not match capitalization or the whole title.

Tradeoff / alternative: No fuzzy matching, tokenization, or indexing. A blank query matches every title in Python.

Engineering takeaway: Understand the exact semantics of string operators, including edge cases.


```python
def search_tasks(tasks, query):
    results = []
    for task in tasks.values():
        if query.lower() in task["title"].lower():
            results.append(task)
    return results
```


### D11 — Reject empty search in the CLI

Decision: Use `.strip()` and refuse an empty search query before calling the service.

Why: Avoids unintentionally displaying every task because `"" in any_string` is true.

Tradeoff / alternative: This is a CLI-only guard; a direct call to `search_tasks(tasks, "")` still returns all tasks. A stronger service contract could reject it too.

Engineering takeaway: Distinguish an input-validation fix from a system-wide invariant.


### D12 — Reuse one display loop for all view modes

Decision: Each filter branch sets `selected_tasks`; one loop prints the selected records.

Why: Prevents four copies of the same formatting logic.

Tradeoff / alternative: The menu block remains long; splitting it further was not worth the complexity in this small CLI.

Engineering takeaway: Normalize branches to a common data shape, then reuse the downstream logic.


```python
if filter_choice == "1":
    selected_tasks = list(tasks.values())
elif filter_choice == "2":
    selected_tasks = filter_tasks_by_status(tasks, "pending")
elif filter_choice == "3":
    selected_tasks = filter_tasks_by_status(tasks, "completed")
```


## 6. Debugging: the `task` vs `tasks` failure

During CLI integration, the app raised `UnboundLocalError` at `selected_tasks = list(task.values())`. The intended variable was `tasks` (plural). Because `task` was also assigned later in a loop, Python treated it as a local variable, but it had not been assigned at that point.


```python
# Incorrect
selected_tasks = list(task.values())
# Correct
selected_tasks = list(tasks.values())
```


# A repeatable debugging procedure

- 1. Read the last line of the traceback: exception type and message.
- 2. Find the first frame in your own application that points to the failure.
- 3. Inspect the exact expression, variable names, and values in scope.
- 4. Form one small hypothesis; change the smallest relevant line.
- 5. Re-run the same failing action, then regression-check nearby behavior.
Why this matters: Debugging is not guessing what “might be wrong.” It is a disciplined search using evidence. This is one of the most transferable skills when reviewing AI-generated code.


## 7. Persistence and failure safety


### D13 — Missing file is normal; corrupted file is not

Decision: Return `{}` on `FileNotFoundError`, but stop startup on `json.JSONDecodeError`.

Why: First launch may have no data yet. A corrupted existing file is evidence of a problem, not permission to reset user data.

Tradeoff / alternative: Returning `{}` for both cases could cause the next save to overwrite the corrupted file and destroy recoverable data.

Engineering takeaway: Distinguish “nothing exists yet” from “something exists but cannot be trusted.”


### D14 — Convert JSON parsing failures to a clear application error

Decision: Raise `ValueError("Cannot load tasks: ...") from error`.

Why: Preserves the original cause for debugging while giving the CLI a readable failure message.

Tradeoff / alternative: Catching every exception and continuing would hide defects. `from error` may still show a chained traceback to developers, which is useful.

Engineering takeaway: Translate low-level errors at boundaries without hiding the root cause.


### D15 — Fail startup safely

Decision: Wrap `load_tasks()` in `main()` with `try/except ValueError`, print a message, and return.

Why: The app cannot safely operate on unknown data. Stopping prevents accidental saves over a bad file.

Tradeoff / alternative: A future app could offer backup/recovery, but that is outside this exercise.

Engineering takeaway: Fail closed when continuing could corrupt or overwrite state.


### D16 — Validate parsed data shape and task ID keys

Decision: Require top-level `dict` and integer-convertible keys.

Why: Valid JSON is not necessarily valid task data. E.g., `{"abc": ...}` parses but violates the ID contract.

Tradeoff / alternative: Current checks do not fully validate every nested task record or ensure the internal `id` equals its outer key.

Engineering takeaway: Parsing answers “can I read it?”; validation answers “is it allowed?”


```python
try:
    with open("tasks.json", "r") as file:
        data = json.load(file)
    if not isinstance(data, dict):
        raise ValueError("Invalid task data: expected a dictionary.")
    tasks = {}
    for key, value in data.items():
        try:
            task_id = int(key)
        except ValueError as error:
            raise ValueError(f"Invalid task data: task ID '{key}' is not an integer.") from error
        tasks[task_id] = value
    return tasks
except FileNotFoundError:
    return {}
except json.JSONDecodeError as error:
    raise ValueError("Cannot load tasks: tasks.json contains invalid JSON.") from error
```

Known caveat: if `data` is a dictionary but contains values of the wrong type, some operations may still fail later. This was explicitly deferred rather than pretending the validation was complete.


## 8. Testing decisions: what tests actually prove


### D17 — Use pytest and focused tests

Decision: Use basic asserts for service functions and `tmp_path`/`monkeypatch.chdir` for file tests.

Why: Low ceremony, fast feedback, and filesystem isolation. The final reported suite had 13 passing tests.

Tradeoff / alternative: Passing tests are evidence only for scenarios actually asserted; they do not prove the entire application correct.

Engineering takeaway: Think in terms of behavior and failure modes, not test counts.


### D18 — Verify both return value and state

Decision: For title editing, assert `True`, changed title, unchanged ID, and unchanged status.

Why: A function might report success but change the wrong field, or mutate state and report failure.

Tradeoff / alternative: Checking only `result is True` would miss such defects.

Engineering takeaway: Tests should verify observable contracts and important invariants.


### D19 — Verify corrupted files remain unchanged

Decision: Use temporary `tasks.json`, assert the exception, then assert the original bytes/text are intact.

Why: Protects against the most serious failure mode: silent data loss.

Tradeoff / alternative: Testing only the exception would not catch accidental file rewriting.

Engineering takeaway: Test non-events when preservation is a requirement.


```python
def test_update_task_title():
    tasks = {1: {"id": 1, "title": "Study Python", "status": "pending"}}
    result = update_task_title(tasks, 1, "Practice Python")
    assert result is True
    assert tasks[1]["title"] == "Practice Python"
    assert tasks[1]["status"] == "pending"
    assert tasks[1]["id"] == 1
```

The test suite initially failed when the new update tests were added; after checking the import/function and rerunning, the user reported success. The specific failure cause was not confirmed in the visible record, so it should not be treated as a proven root cause.


# Testing mental model

- Arrange: create inputs and initial state.
- Act: call the behavior under test.
- Assert: check return values, state changes, and important non-changes.
- Include happy path, nonexistent record, invalid input, and file corruption when relevant.
- AI may write test boilerplate; you must judge whether the assertions match the requirement.

## 9. CLI design, integration, and deliberate non-refactors


### D20 — Keep input conversion in the CLI

Decision: Convert typed task IDs with `int(input(...))`, catch `ValueError`, and show a user-friendly message.

Why: Text input is a UI concern. Service functions can assume integer IDs under the current contract.

Tradeoff / alternative: Repeated `try/except` blocks could be extracted, but that refactor offered little learning value at this scale.

Engineering takeaway: A little duplication is sometimes preferable to a premature abstraction.


### D21 — Save only after successful state-changing operations

Decision: Call `save_tasks(tasks)` after create, complete, delete, or successful edit.

Why: Avoids unnecessary writes on invalid commands and makes the persistence boundary explicit.

Tradeoff / alternative: There is no atomic write, rollback, or crash-safe transaction. A failed write can still leave inconsistent persistence.

Engineering takeaway: Understand when state changes become durable and what happens when saving fails.


### D22 — Fix menu correctness without redesigning the CLI

Decision: Put Edit at option 5, Exit at option 6, update handlers and invalid-option text.

Why: The displayed interface must agree with the control flow.

Tradeoff / alternative: Only changing printed labels would produce a real bug; the mapping must be changed consistently.

Engineering takeaway: Small UX edits can be functional changes; verify both display and behavior.


### D23 — Do not split `main()` just to make it shorter

Decision: Keep the CLI loop as one function for this project.

Why: The current program is small and readable enough. More helpers would create indirection without clear payoff.

Tradeoff / alternative: A larger CLI with repeated commands would justify command handlers or a parser framework.

Engineering takeaway: Refactor when there is a concrete maintenance cost, not simply because code is longer than ideal.


## 10. Git, environment, and delivery


### D24 — Use a Python virtual environment

Decision: Create `.venv` and install pytest there.

Why: On macOS, `python` was initially unavailable and the global Python 3.14 environment lacked pytest. A venv makes dependencies project-specific.

Tradeoff / alternative: A pinned requirements file would improve reproducibility; the project used a minimal setup instead.

Engineering takeaway: Know which interpreter runs your code and where its packages are installed.


### D25 — Ignore generated files and local data

Decision: Add `.gitignore` for `__pycache__/`, `.pyc`, `.venv/`, `.pytest_cache/`, `tasks.json`, and `.DS_Store`.

Why: Generated caches and local user data should not clutter source control or expose private state.

Tradeoff / alternative: `.gitignore` does not untrack already committed files.

Engineering takeaway: Git tracks its index, not your intentions. Ignore rules affect future additions.


### D26 — Remove tracked generated files without deleting local copies

Decision: Use `git rm -r --cached` for tracked cache folders and `tasks.json`.

Why: Cleans repository history going forward while preserving local working files.

Tradeoff / alternative: `git rm` without `--cached` removes working-tree files too.

Engineering takeaway: Understand staged deletions versus local file deletion before running Git commands.


### D27 — Document setup, structure, features, and limitations

Decision: Write a README that explains how to run and test the app and what it does not support.

Why: A teammate or reviewer should not need the original chat to understand the project.

Tradeoff / alternative: Documentation does not replace code clarity or automated verification.

Engineering takeaway: A handoff is complete when someone else can orient, run, and evaluate the software.


### D28 — Stop adding features and close the learning project

Decision: Finish after cleanup, tests, and GitHub push.

Why: The next learning bottleneck is APIs, SQL, and production backend systems—not a larger CLI task manager.

Tradeoff / alternative: Additional features could be useful for a product, but not necessarily for this apprenticeship.

Engineering takeaway: Scope discipline is an engineering skill. Know when a project has served its purpose.


## 11. What you struggled with: targeted remediation

| Skill gap | Evidence from work | Independent proof exercise |
| --- | --- | --- |
| Dictionary traversal | Tried `for task in tasks` and indexed integer keys | Given nested dict, produce values, keys, and `(key, value)` pairs |
| Accumulation | No result list in initial filter | Build a list of all records meeting two conditions |
| Control flow | Returned from inside loop | Explain and fix early return in a multi-match search |
| Nested mutation | Needed explanation for `tasks[1]["title"]` | Update one field while preserving all others |
| Reading tracebacks | `task` vs `tasks` caused crash | Diagnose a fresh variable/scope error without solution |
| Testing confidence | Asked whether manual tests matter with AI | Define 3 meaningful assertions for a feature |
| System integration | Needed guided CLI modifications | Add a service call to an existing menu with correct persistence |


# The 10-minute daily construction drill

Use a small input, write the contract, outline the algorithm in English, implement without AI, run three examples, and explain one edge case. Stop at 10–15 minutes. This is more useful for your current gap than memorizing more syntax without building.


```python
# Drill template (not a solution)
# Input type:
# Output type:
# Mutates input? yes/no
# Edge cases:
# Algorithm:
## 1. Initialize ...
## 2. Iterate ...
## 3. Check ...
## 4. Accumulate / update ...
## 5. Return ...
```


## 12. Retrieval practice — answer without looking

1. Why was a dictionary better suited than a list for Task Forge’s ID-based operations?

2. What does `for task in tasks` produce, and why did the first filter fail?

3. Why must the filter return occur after the loop?

4. What is the difference between `append` and `return`?

5. Explain `tasks[2]["status"] = "completed"` one lookup at a time.

6. Does `list(tasks.values())` deep-copy each task? What mutation risk remains?

7. Why does `"" in "Study Python"` evaluate to `True`?

8. Why is missing `tasks.json` different from corrupted `tasks.json`?

9. How can valid JSON still be invalid task data?

10. Why did JSON keys need conversion back to integers?

11. What does `raise ... from error` contribute?

12. Why does a passing test not establish complete correctness?

13. What does `--cached` change in `git rm`?

14. Why did we choose not to extract every repeated CLI block?

15. What could go wrong if the app modifies memory and `save_tasks` then fails?


## 13. Three independent mini-labs


## Lab A — Filtering with two criteria

Given a dictionary of tasks, write `find_pending_with_word(tasks, word)` that returns all pending tasks whose titles contain the word, case-insensitively. Do not mutate the input. Prove behavior for zero, one, and multiple matches.


## Lab B — Safe nested update

Write `rename_if_pending(tasks, task_id, new_title)` that updates only pending tasks, rejects blank titles, and returns a boolean. Explain whether the function mutates input and show that completed tasks remain unchanged.


## Lab C — Debug an unfamiliar failure


```python
def titles_for_status(tasks, wanted):
    matches = []
    for task in tasks:
        if task["status"] == wanted:
            matches.append(task["title"])
            return matches
    return matches
```

Without executing it, identify both independent defects, explain their symptoms, then fix them. Write a test case that would reveal each defect.


# 14. Engineering interview translation

| Interview prompt | Task Forge story to tell |
| --- | --- |
| Tell me about a bug you debugged | UnboundLocalError caused by `task` vs `tasks`; traceback-first diagnosis |
| How do you structure a small app? | CLI/service/storage boundaries; tradeoff against one-file design |
| How do you handle bad data? | Missing vs malformed JSON; preserve file and fail startup |
| What does good testing mean? | Assert both success and invariants; test data preservation |
| Describe a design tradeoff | Dictionary for ID lookup, list for filter results |
| When do you refactor? | Only when a concrete correctness or maintenance issue justifies it |
| How do you work with AI? | Delegate routine generation while owning contracts, review, debugging, and verification |


# 15. Final competency checklist

☐ I can explain keys, values, and items without looking them up.

☐ I can independently write a collect/filter function from requirements.

☐ I can place return statements correctly and explain early exit.

☐ I can update a nested dictionary field without replacing the entire record.

☐ I can identify whether a function mutates its inputs.

☐ I can read a traceback and find the failing expression.

☐ I can distinguish JSON parsing from application validation.

☐ I can name the main failure risks of file-based persistence.

☐ I can write or critically review a basic test that checks behavior and invariants.

☐ I can explain why Task Forge has three modules and why we stopped extending it.

Do not mark an item complete because you remember reading the answer. Mark it complete after you can explain it and demonstrate it on a new example.


# 16. What comes next

Close Task Forge as a completed foundational exercise. Continue short independent Python construction drills while moving into HTTP, FastAPI, PostgreSQL, SQLAlchemy, transactions, API design, debugging, and production workflows in Economic Intelligence. AI can accelerate implementation; independent comprehension and verification remain non-negotiable.

Source note: Decisions D01–D28 summarize explicit or directly evidenced choices from the Task Forge conversations. The remediation drills, interview framing, and competency checklist are instructional recommendations added for review; they are not claims about additional completed work.

