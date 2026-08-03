# 🦁 Vihnelli's Template

<p align="center">
  <b>A modern, reusable C++ project template with an automated CMake workflow.</b>
  <br>
  Build faster. Structure better. Focus on your code.
</p>

<p align="center">

![Language](https://img.shields.io/badge/language-C%2B%2B-blue)
![Build](https://img.shields.io/badge/build-CMake-green)
![Python](https://img.shields.io/badge/tooling-Python%203.9%2B-yellow)
![License](https://img.shields.io/badge/license-MIT-purple)

</p>

---

> ⚠ Note: After cloning the template, replace this file with your project's README.md file.

## 📌 Overview

**Vihnelli's Template** is a complete C++ project foundation designed for developers who want a clean, scalable, and automated workflow.

Instead of manually creating:

- CMake configurations
- Build scripts
- Output folders
- Packaging logic
- Compiler setups

Vihnelli's Template provides everything in one reusable structure.

Configure your project once using `project.toml`, then use the built-in CLI to handle the workflow.

```text
New Project
     |
     v
Edit project.toml
     |
     v
python project.py build
     |
     v
Start developing 🚀
```

---

# ✨ Features

| Category | Features |
|---|---|
| 🏗️ Build System | Modern CMake workflow, multiple generators, compiler detection |
| ⚙️ Configuration | Fully customizable `project.toml` configuration |
| 🖥️ Toolchains | MSVC, GCC, Clang support |
| 🔨 Building | Parallel builds, automatic configuration checks |
| ▶️ Running | Multiple executable management |
| 🧹 Maintenance | Clean, rebuild, environment diagnostics |
| 📦 Packaging | Release archive generation |
| 🗜️ Compression | UPX executable compression (Other compressors available tho) |
| 📁 Structure | Organized source, output, and dependency layout |

---

# 🛠 Requirements

## Required

| Tool | Version |
|---|---|
| Python | 3.9+ |
| CMake | 3.20+ |

---

## Supported Compilers

### Windows

| Compiler | Status |
|---|---|
| Microsoft Visual C++ (MSVC) | ✅ Supported |
| LLVM Clang | ✅ Supported |
| MinGW GCC | ✅ Supported |

### Linux

| Compiler | Status |
|---|---|
| GCC | ✅ Supported |
| Clang | ✅ Supported |

---

# 📂 Project Structure

A generated project follows this layout:

```text
📦 Vihnelli's Template
├── 📄 CMakeLists.txt                 # main cmake entry point
├── 📄 CMakePresets.json              # ready-to-use build presets
├── 📄 CMakeUserPresets.json          # your local build settings
├── 📄 README.md                      # getting started guide
├── 📄 LICENSE                        # license information
├── 🐍 project.py                     # build and project manager
├── 📄 project.toml                   # project configuration
│
├── 📁 assets/                        # project resources
│   ├── 📁 fonts/                     # custom fonts
│   ├── 📁 icons/                     # application icons
│   ├── 📁 images/                    # images and textures
│   ├── 📁 music/                     # background music
│   └── 📁 sound/                     # sound effects
│
├── 📁 cmake/                         # shared cmake files
│   ├── 📄 build_options.cmake        # build options
│   ├── 📄 compiler_options.cmake     # compiler settings
│   ├── 📄 config.cmake               # global configuration
│   ├── 📄 dirs.cmake                 # output directories
│   ├── 📄 project_options.cmake      # project options
│   ├── 📄 utils.cmake                # helper functions
│   └── 📄 warns.cmake                # warning levels
│
├── 📁 config/                        # application configuration
│   └── 📄 default.conf               # default settings
│
├── 📁 data/                          # generated application data
│   ├── 📁 config/                    # saved settings
│   ├── 📁 logs/                      # log files
│   └── 📁 saves/                     # save files
│
├── 📁 docs/                          # documentation
├── 📁 examples/                      # example projects
│
├── 📁 include/                       # public header files
│   ├── 📁 app/                       # application api
│   ├── 📁 core/                      # core components
│   ├── 📁 general_/                  # shared code
│   ├── 📁 logger/                    # logging system
│   ├── 📁 platform/                  # platform-specific code
│   └── 📁 utils/                     # utility helpers
│
├── 📁 src/                           # source files
│   ├── 📄 CMakeLists.txt             # source configuration
│   ├── 📁 exe/                       # executable targets
│   │   ├── 📄 CMakeLists.txt
│   │   └── 📁 my_project/
│   │       ├── 📄 CMakeLists.txt
│   │       └── 📄 main.cpp           # application entry point
│   └── 📁 lib/                       # library implementations
│       ├── 📄 CMakeLists.txt
│       ├── 📁 app/
│       ├── 📁 core/
│       ├── 📁 general_/
│       ├── 📁 logger/
│       ├── 📁 platform/
│       └── 📁 utils/
│
├── 📁 tests/                         # unit tests
│   ├── 📄 CMakeLists.txt
│   └── 📁 unit/
│       ├── 📄 CMakeLists.txt
│       └── 📁 core/
│           └── 📄 test.cpp
│
├── 📁 tools/                         # external development tools
└── 📁 screenshots/                   # images used in the README
```

---

# ⚙️ Configuration

All project settings are controlled through:

```text
project.toml
```

Example:

```toml
[project]

name = "My Application"
version = "1.0.0"
type = "exe"
description = "My C++ application"


[build]

generator = "auto"
toolchain = "auto"
config = "Release"
jobs = 0
defines = []


[main]

create = true
name = "auto"


[run.executables.main]

args = []
show_console = true
wait = false
enabled = true
```

---

# ⌨️ CLI Commands

All commands follow:

```bash
python project.py <command>
```

| Command | Description |
|---|---|
| `configure` | Configure the CMake project |
| `build` | Build the project |
| `run` | Run configured executables |
| `build-run` | Build then run |
| `clean` | Remove generated files |
| `rebuild` | Clean and rebuild |
| `test` | Run tests |
| `doctor` | Show environment information |
| `compress` | Compress binaries |
| `package` | Create release package |

---

# 🔧 Configure

Generate the CMake build environment:

```bash
python project.py configure
```

Performs:

- Compiler detection
- Generator selection
- CMake configuration
- Build directory preparation

---

# 🔨 Build

Compile the project:

```bash
python project.py build
```

Example:

```text
==> Building (Release)

[100%] Built target MyProject
```

---

# ▶️ Run

Launch configured applications:

```bash
python project.py run
```

Executables are configured inside:

```toml
[run.executables.main]
```

Example:

```toml
[run.executables.main]

args = [
    "--debug"
]

enabled = true
show_console = true
wait = false
```

Multiple executables can be added:

```toml
[run.executables.editor]

enabled = true
args = []
```

---

# ⚡ Build & Run

Build and launch immediately:

```bash
python project.py build-run
```

Equivalent:

```text
build → run
```

---

# 🧹 Clean

Remove generated files:

```bash
python project.py clean
```

Deletes:

```text
build/
output/
dist/
temp/
```

---

# 🔄 Rebuild

Perform a clean rebuild:

```bash
python project.py rebuild
```

Equivalent:

```text
clean
 ↓
configure
 ↓
build
```

---

# 🧪 Testing

Run tests:

```bash
python project.py test
```

Enable:

```toml
[test]

enabled = true
```

Testing is powered by CTest through CMake.

---

# 🩺 Doctor

Check your development environment:

```bash
python project.py doctor
```

Example:

```text
Generator : Ninja
Compiler  : msvc
Build type: Release
Jobs      : 8
```

Useful for diagnosing toolchain problems.

---

# 🗜 Compression

Vihnelli's Template supports binary compression using tools like UPX.

Configuration:

```toml
[compress]

enabled = true
tool = "upx"

args = [
    "--best",
    "--lzma"
]

targets = [
    "main",
    "output/bin/**/*.dll"
]

keep_original = true
```

Run:

```bash
python project.py compress
```

Output:

```text
Compressed: MyProject.exe
```

With backups enabled:

```text
MyProject.exe
MyProject.exe.bak
```

---

# 📦 Packaging

Create a distributable release:

```bash
python project.py package
```

Example:

```text
dist/

└── MyProject-1.0.0-windows-x86_64-Release.zip
```

Package contents:

```text
bin/
 └── MyProject.exe

assets/

data/

README.md

LICENSE
```

Executables and libraries are automatically placed inside `bin/`.

---

# 🧰 Compiler Selection

## Automatic

Recommended:

```toml
toolchain = "auto"
```

Automatically detects:

- MSVC
- GCC
- Clang

(Selects available one)

---

## Manual

### MSVC

```toml
toolchain = "msvc"
```

Requires:

```text
cl.exe
```

Through using `Visual Studio Developer Propmpt`.

---

### LLVM

```toml
toolchain = "llvm"
```

Requires:

```text
clang
clang++
```

---

### GNU

```toml
toolchain = "gnu"
```

Requires:

```text
gcc
g++
```

---

# 🏗 Build Generators

## Automatic

```toml
generator = "auto"
```

---

## Ninja

```toml
generator = "Ninja"
```

---

## Visual Studio

```toml
generator = "Visual Studio 17 2022"
```

---

## Unix Makefiles

```toml
generator = "Unix Makefiles"
```

---

# 🧠 Smart Configuration Detection

Vihnelli's Template avoids unnecessary CMake configuration.

Tracked files:

```text
CMakeLists.txt
*.cmake
project.toml
```

No changes:

```text
Config manager: No work to do.
```

Changes detected:

```text
CMake change detected!
```

The project is automatically reconfigured.

---

# 🎯 Design Philosophy

Vihnelli's Template follows three main ideas:

### Simple

One configuration file:

```text
project.toml
```

One command:

```bash
python project.py build
```

---

### Reusable

Create a project once, reuse the structure forever.

---

### Automated

Let the tools handle:

- Configuration
- Building
- Packaging
- Releasing

while you focus on development.

---


# 📜 License

Licensed under the MIT License.

See:

```text
LICENSE
```

for details.

---

> ⚠️ **Current Limitations**
>
> The `project.py` testing command is available, but full project testing support is not implemented yet.
>
> Currently:
>
> - `python project.py test` exists and integrates with the workflow.
> - Real test discovery, test configuration, and complete testing infrastructure are **not fully supported yet**.
>
> Testing support is planned to be improved in future releases.
>
> Library projects are also **not fully supported yet**. Setting:
>
> ```toml
> [project]
> type = "lib"
> ```
>
> may result in configuration or build errors.
>
> For now, Vihnelli's Template is designed primarily for executable projects:
>
> ```toml
> [project]
> type = "exe"
> ```

<p align="center">
  Made with ❤️ by Vihnelli, for C++ developers
</p>
