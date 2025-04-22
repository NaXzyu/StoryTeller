# StoryTeller Implementation Plan

This document outlines the development tasks, grouped into logical phases, required to implement the StoryTeller application based on the `Specification.md`.  
**Check off each task as you complete it!**

---

## Phase 1: Project Setup & Core Infrastructure

**Goal:** Establish project structure, dependencies, configuration, and logging.

| # | Task | Details/Instructions | Component(s) |
|:-:|:-----|:---------------------|:-------------|
| 1 | [ ] Initialize git repository and Python project (`uv init`) | Create repo, set up `.gitignore`, initialize with `uv` | Project Root |
| 2 | [ ] Create `pyproject.toml` with all dependencies | Add all dependencies from Specification, including dev tools | Project Root |
| 3 | [ ] Create directory structure (`src/`, `tests/`, `docs/`, etc.) | Follow the detailed structure in the Specification's Appendix | All |
| 4 | [ ] Add `main.py` entry point | Should initialize logging, config, and launch GUI | Root |
| 5 | [ ] Implement logging utility (`utils/logger.py`) | Centralized logging, supports file and console output | Utils |
| 6 | [ ] Implement config loader (`config/config_loader.py`) | Loads user/project config, supports overrides, uses `platformdirs` | Config |
| 7 | [ ] Define default config values (`config/defaults.py`) | Store all default settings, including model, theme, etc. | Config |
| 8 | [ ] Create core data models (`data/models.py`) | Use Pydantic/dataclasses for Character, Relationship, Context, Dialogue, Project | Data |
| 9 | [ ] Add initial README and SPEC documentation | Copy from Specification, add project badges, usage, etc. | Docs |
| 10 | [ ] Set up pre-commit hooks and linting | Use `black`, `isort`, `flake8` | Project Root |

---

## Phase 2: Data Management & Persistence

**Goal:** Implement Data Store, serialization, and character/relationship management.

| # | Task | Details/Instructions | Component(s) |
|:-:|:-----|:---------------------|:-------------|
| 1 | [ ] Implement DataStore (`core/data_store.py`) | Centralized access to all DataFrames, in-memory and persistent | Core, Data |
| 2 | [ ] Implement data serialization (`data/serializer.py`) | Read/write CSV, Parquet, JSON; handle schema migrations | Data |
| 3 | [ ] Implement data validation (`data/validator.py`) | Validate data on load/save, enforce schema, handle errors | Data |
| 4 | [ ] Implement Character Engine (`core/character_engine.py`) | CRUD for characters/relationships, enforce referential integrity | Core, DataStore |
| 5 | [ ] Implement Character CRUD operations | Add, edit, delete, list; ensure unique IDs | Character Engine |
| 6 | [ ] Implement Relationship CRUD operations | Add, edit, delete, list; validate character existence | Character Engine |
| 7 | [ ] Implement Project Load/Save logic | Save/load all project data, support new project templates | DataStore |
| 8 | [ ] Integrate config and data paths with `platformdirs` | Ensure all user/project data is stored in correct locations | Utils, Config |
| 9 | [ ] Add unit tests for data models, serialization, validation | Use `tests/` | Tests, Data |

---

## Phase 3: Basic GUI Implementation

**Goal:** Create main window, project management, and character viewing.

| # | Task | Details/Instructions | Component(s) |
|:-:|:-----|:---------------------|:-------------|
| 1 | [X] Set up main application entry (`main.py`) | Launch PyQt6 app, handle exceptions, show splash screen | Root, GUI |
| 2 | [X] Implement Main Window (`gui/main_window.py`) | Dockable panels, theme support, window state persistence | GUI |
| 3 | [ ] Implement Menu Bar (New/Open/Save Project) | Connect to DataStore, show recent projects, handle errors | GUI |
| 4 | [ ] Implement Status Bar | Show current project, model, and status messages | GUI |
| 5 | [ ] Implement Project Open/Save dialogs | Use native file dialogs, validate structure, show errors | GUI, DataStore |
| 6 | [ ] Implement Character List View (`gui/views/character_editor_view.py`) | List all characters, support selection, search/filter | GUI, Character Engine |
| 7 | [ ] Implement Character Detail View (read-only) | Show all character fields, relationships, and history | GUI, Character Engine |
| 8 | [ ] Add unit tests for GUI models and logic | Use `tests/` | Tests, GUI |

---

## Phase 4: Core Dialogue Logic & AI Integration

**Goal:** Implement dialogue pipeline and integrate with Ollama.

| # | Task | Details/Instructions | Component(s) |
|:-:|:-----|:---------------------|:-------------|
| 1 | [ ] Implement Ollama Integration (`ai/ollama_integration.py`) | Async API calls, error handling, model listing | AI |
| 2 | [ ] Implement Prompt Template management (`ai/prompts.py`) | Support for default and user-defined templates | AI |
| 3 | [ ] Implement basic Dialogue Manager (`core/dialogue_manager.py`) | Orchestrate pipeline, manage session state | Core |
| 4 | [ ] Implement Context Tracker (`core/context_tracker.py`) | Aggregate context (spatial, temporal, narrative, etc.) | Core |
| 5 | [ ] Implement Dialogue Generator logic | Build prompts, select parameters, call Ollama | Dialogue Manager, AI |
| 6 | [ ] Implement Dialogue Post-processor (`ai/postprocessor.py`) | Clean/format LLM output, extract metadata | AI |
| 7 | [ ] Implement Dialogue Quality Control (`ai/quality_control.py`) | Check for length, tone, context, safety | AI |
| 8 | [ ] Integrate all pipeline stages in Dialogue Manager | Ensure correct order, error handling, retries | Dialogue Manager |
| 9 | [ ] Add dialogue history logging to DataStore | Store all requests, responses, QA results | Dialogue Manager, DataStore |
| 10 | [ ] Add unit tests for dialogue pipeline | Use `tests/` | Tests, Core, AI |

---

## Phase 5: GUI Enhancements & Dialogue Testing

**Goal:** Build GUI for character/context editing and dialogue testing.

| # | Task | Details/Instructions | Component(s) |
|:-:|:-----|:---------------------|:-------------|
| 1 | [ ] Implement Character Editor View (`gui/views/character_editor_view.py`) | Editable fields, validation, undo/redo | GUI, Character Engine |
| 2 | [ ] Implement Relationship Editor (in Char Editor) | Visual graph, add/remove/edit relationships | GUI, Character Engine |
| 3 | [ ] Implement Dialogue Tester View (`gui/views/dialogue_tester_view.py`) | Select speaker/listener/context, show output, regenerate | GUI, Dialogue Manager |
| 4 | [ ] Implement Context Editor View (`gui/views/context_editor_view.py`) | Timeline, event editing, context presets | GUI, Context Tracker |
| 5 | [ ] Implement Model/Parameter Configuration UI | Select model, adjust parameters, save/load presets | GUI, Config |
| 6 | [ ] Implement Dialogue History View (`gui/views/dialogue_history_view.py`) | List/search previous generations, show metadata | GUI, DataStore |
| 7 | [ ] Implement Project Settings dialog (`gui/views/settings_view.py`) | Edit project name, description, settings | GUI, Config |
| 8 | [ ] Add unit tests for GUI enhancements | Use `tests/` | Tests, GUI |

---

## Phase 6: Query Engine & Advanced Features

**Goal:** Integrate natural language query engine and visualization.

| # | Task | Details/Instructions | Component(s) |
|:-:|:-----|:---------------------|:-------------|
| 1 | [ ] Implement Query Engine wrapper (`ai/query_engine.py`) | Wrap LlamaIndex, support caching, error handling | AI, LlamaIndex |
| 2 | [ ] Integrate Query Engine into Character Engine | Use for advanced character/relationship queries | Character Engine, AI |
| 3 | [ ] Integrate Query Engine into Context Tracker | Use for context/event queries | Context Tracker, AI |
| 4 | [ ] Implement Relationship Visualization (`gui/views/visualization_view.py`) | Interactive graph, filter by type/strength | GUI, Character Engine |
| 5 | [ ] Implement Timeline Visualization (optional) | Show events, context changes, dialogue history | GUI, Context Tracker |
| 6 | [ ] Implement Data Import/Export features | Support CSV/JSON, batch import/export, validation | GUI, DataStore, Serializer |
| 7 | [ ] Add support for user-defined prompt templates | GUI for editing, validation, save to project | AI, GUI |
| 8 | [ ] Add unit tests for query engine and visualizations | Use `tests/` | Tests, AI, GUI |

---

## Phase 7: Testing, Packaging & Documentation

**Goal:** Ensure stability, create distributables, and finalize documentation.

| # | Task | Details/Instructions | Component(s) |
|:-:|:-----|:---------------------|:-------------|
| 1 | [/] Write unit tests for all modules | Cover all logic, edge cases, error handling (Started for main.py) | Tests, All |
| 2 | [ ] Write integration tests for key workflows | Simulate end-to-end scenarios | Tests |
| 3 | [ ] Refine GUI usability and appearance | Polish UI, accessibility, keyboard shortcuts | GUI |
| 4 | [X] Configure PyInstaller spec file | Integrate build logic into `main.py` via `storyteller build` command, spec file in `build/` | Project Root, Main |
| 5 | [ ] Build and test executables for all target OSs | Windows, macOS, Linux | PyInstaller |
| 6 | [ ] Finalize `README.md` and user documentation | Usage, troubleshooting, FAQ, diagrams | Docs |
| 7 | [ ] Code cleanup, review, and polish | Lint, format, remove dead code, final review | All |
| 8 | [ ] Tag release and update changelog | Prepare for distribution | Project Root |

---
