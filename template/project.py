from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
import textwrap
import re
import zipfile
import threading

from pathlib import Path
from datetime import datetime
from textwrap import dedent

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

ROOT = Path(__file__).resolve().parent
CONFIG_FILE = ROOT / "project.toml"

DEFAULT_CONFIG = {
    "project": {
        "name": "C++ Project",
        "version": "1.0.0",
        "type": "exe",
        "description": "My C++ project",
    },

    "main": {
        "main_executable": True,
        "name": "auto",
    },

    "build": {
        "generator": "auto",
        "toolchain": "auto",
        "config": "Release",
        "jobs": 0,
        "build_docs": "false",
        "build_examples": "false",
        "build_deps": "true",
        "shared_libs": "false",
        "defines": [],
        "flags": {}
    },

    "test": {
      "enabled": "true"
    },

    "run": {
        "executables": {},
        "multi_threaded": True,
    },

    "paths": {
        "build_dir": "build",
        "output_dir": "output",
        "output_bin": "output/bin",
        "output_lib": "output/lib",
        "dist_dir": "dist",
        "temp_dir": "temp",
        "assets_dir": "assets",
        "data_dir": "data",
        "tools_dir": "tools",
        "compressors_dir": "tools/compressors",
    },

    "package": {
        "formats": ["zip"],
        "include": [
            "assets",
            "config",
            "data",
            "README.md",
            "LICENSE",
        ],
        "name_template": "{name}-{version}-{platform}-{arch}-{config}",
    },

    "compress": {
        "enabled": True,
        "tool": "upx",
        "args": [
            "--best",
            "--lzma",
        ],
        "targets": [
            "output/bin/**/*.exe",
            "output/bin/**/*.dll",
        ],
        "keep_original": True,
    },

    "toolkit": {
        "color": True,
        "verbose": False,
    },
}

class Color:
    RESET = "\033[0m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    CYAN = "\033[36m"
    MAGENTA = "\033[35m"
    BOLD = "\033[1m"

class Log:
    color = True
    verbose = False

    @classmethod
    def _fmt(cls, c, txt):
        if not cls.color:
            return txt

        return f"{c}{txt}{Color.RESET}"

    @classmethod
    def info(cls, txt):
        print(cls._fmt(Color.BLUE, f"[info] {txt}"))

    @classmethod
    def ok(cls, txt):
        print(cls._fmt(Color.GREEN, f"[ ok ] {txt}"))

    @classmethod
    def warn(cls, txt):
        print(cls._fmt(Color.YELLOW, f"[warn] {txt}"))

    @classmethod
    def fail(cls, txt):
        print(cls._fmt(Color.RED + Color.BOLD, f"[fail] {txt}"))
        sys.exit(1)

    @classmethod
    def step(cls, txt):
        print()
        print(cls._fmt(Color.CYAN + Color.BOLD, f"==> {txt}"))

    @classmethod
    def cmd(cls, args):
        print(cls._fmt(Color.MAGENTA, "$ " + " ".join(map(str, args))))

    @classmethod
    def debug(cls, txt):
        if cls.verbose:
            print(cls._fmt(Color.YELLOW, f"[debug] {txt}"))

class Platform:
    @staticmethod
    def is_windows():
        return platform.system() == "Windows"

    @staticmethod
    def is_linux():
        return platform.system() == "Linux"

    @staticmethod
    def is_macos():
        return platform.system() == "Darwin"

    @staticmethod
    def exe_ext():
        return  ".exe" if Platform.is_windows() else ""

class Utils:
    @staticmethod
    def which(name: str):
        return shutil.which(name)
    
    @staticmethod
    def cpu_count():
        return os.cpu_count() or 4
    
    @staticmethod 
    def mkdir(path: Path):
        path.mkdir(parents=True, exist_ok=True)
    
    @staticmethod
    def remove(path: Path):
        if path.exists():
            shutil.rmtree(path)
    
    @staticmethod
    def run(cmd, cwd=None, env=None, check=True):
        Log.cmd(cmd)

        final_env = os.environ.copy()

        if env:
            final_env.update(env)

        result = subprocess.run(
            cmd,
            cwd=cwd,
            env=final_env,
        )

        if check and result.returncode:
            Log.fail(f"Command failed ({result.returncode})")

        return result
    
    @staticmethod
    def merge(base, user):
        out = dict(base)

        for k, v in user.items():
            if isinstance(v, dict):
                out[k] = Utils.merge(base.get(k, {}), v)
            else:
                out[k] = v

        return out

    def clear_terminal():
        subprocess.run(
            "cls" if os.name == "nt" else "clear",
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    def enable_windows_ansi():
        if not Platform.is_windows():
            return

        try:
            import ctypes

            kernel = ctypes.windll.kernel32
            handle = kernel.GetStdHandle(-11)
            mode = ctypes.c_uint()
            kernel.GetConsoleMode(handle, ctypes.byref(mode))
            kernel.SetConsoleMode(handle, mode.value | 4)
        except Exception:
            pass

class Config:
    def __init__(self):
        if CONFIG_FILE.exists():
            with CONFIG_FILE.open("rb") as f:
                user = tomllib.load(f)

        else:
            user = {}

        self.data = Utils.merge(DEFAULT_CONFIG, user)
        Log.color = self.get("toolkit.color")
        Log.verbose = self.get("toolkit.verbose")

    def get(self, key, required=True):
        value = self.data

        for part in key.split("."):
            if part not in value:
                if required:
                    Log.fail(f"Missing key {key}")
                return None

            value = value[part]

        if required and value is None:
            Log.fail(f"Key {key} cannot be empty!")

        return value

    @property
    def output_dir(self):
        return ROOT / self.get("paths.output_dir")
    
    @property
    def build_dir(self):
        return ROOT / self.get("paths.build_dir")

    @property
    def output_bin(self):
        return ROOT / self.get("paths.output_bin")

    @property
    def output_lib(self):
        return ROOT / self.get("paths.output_lib")

    @property
    def dist_dir(self):
        return ROOT / self.get("paths.dist_dir")

    @property
    def temp_dir(self):
        return ROOT / self.get("paths.temp_dir")

    @property
    def compressors_dir(self):
        return ROOT / self.get("paths.compressors_dir")

class Compiler:
    """
    Represents a C/C++ toolchain.
    """

    def __init__(self, name, cc, cxx, linker=None, env=None):
        self.name =name
        self.cc = cc
        self.cxx = cxx
        self.linker = linker
        self.env = env or {}

    @property
    def cmake_args(self):
        args = [
            f"-DCMAKE_C_COMPILER={self.cc}",
            f"-DCMAKE_CXX_COMPILER={self.cxx}"
        ]

        if self.linker:
            args.append(
                f"-DCMAKE_LINKER={self.linker}"
            )

        return args

class Toolchain:
    @staticmethod
    def detect_generator():
        if Utils.which("ninja"):
            return "Ninja"
        if Platform.is_windows():
            return "Visual Studio 17 2022"

        return "Unix Makefiles"

    @staticmethod
    def detect_compiler(requested="auto"):
        requested = requested.lower()

        if requested == "auto":
            if Utils.which("cl"):      return Toolchain.detect_msvc()
            if Utils.which("g++"):     return Compiler("gcc", "gcc", "g++")
            if Utils.which("clang++"): return Compiler("clang", "clang", "clang++")
            Log.fail("No supported compiler was found.")

        if requested == "gnu":
            if not Utils.which("g++") or not Utils.which("gcc"):
                Log.fail("GNU was requested but g++/gcc was not found.")

            return Compiler("gcc", "gcc", "g++", "ld")

        if requested == "llvm":
            if not Utils.which("clang++") or not Utils.which("clang"):
                Log.fail("LLVM was requested but clang++/clang was not found.")

            return Compiler("clang", "clang", "clang++", "ld")

        if requested == "msvc":
            return Toolchain.detect_msvc()

        Log.fail(f"Unknown toolchain '{requested}'.")
        
    @staticmethod
    def detect_msvc():
        if Utils.which("cl"): return Compiler("msvc", "cl", "cl", linker="link")

        Log.fail(
            "MSVC was requested but cl.exe was not found.\n"
            "Opening Visual Studio Developer Prompt may fix the problem."
        )

class Builder:
    def __init__(self, cfg):
        self.cfg = cfg
        self.generator = cfg.get("build.generator")
        self.toolchain = cfg.get("build.toolchain")
        self.config = cfg.get("build.config")
        self.jobs = cfg.get("build.jobs")

        if self.generator == "auto":
            self.generator = Toolchain.detect_generator()

        self.compiler = Toolchain.detect_compiler(self.toolchain)

        if self.jobs == 0:
            self.jobs = Utils.cpu_count()

    @property
    def is_multi_config(self):
        return ("Visual Studio" in self.generator or self.generator == "Xcode")

    def compute_hash(self):
        hasher = hashlib.sha256()
        files = [str(CONFIG_FILE)]
        
        root_str = os.fspath(ROOT)
        allowed_dirs = {
            os.path.join(root_str, d) 
            for d in ("src", "include", "external", "tests", "docs", "cmake")
        }

        with os.scandir(root_str) as entries:
            for entry in entries:
                if entry.is_file():
                    if entry.name == "CMakeLists.txt" or entry.name.endswith(".cmake"):
                        files.append(entry.path)

                elif entry.is_dir() and entry.path in allowed_dirs:
                    for root_dir, _, filenames in os.walk(entry.path):
                        for filename in filenames:
                            if filename == "CMakeLists.txt" or filename.endswith(".cmake"):
                                files.append(os.path.join(root_dir, filename))

        files.sort()

        for full_path in files:
            relative = os.path.relpath(full_path, root_str).replace(os.sep, "/")
            
            hasher.update(relative.encode("utf-8"))
            hasher.update(b"\0")

            with open(full_path, "rb") as f:
                while chunk := f.read(8192):
                    hasher.update(chunk)

            hasher.update(b"\0")

        return hasher.hexdigest()

    def cmake_modified(self):
        Utils.mkdir(self.cfg.build_dir)

        current = self.compute_hash()
        cache = self.cfg.build_dir / ".project.cache"

        if cache.exists() and cache.stat().st_size > 0:
            previous = cache.read_text().strip()

            if current == previous:
                return False

        cache.write_text(current)
        return True

    def update_project_metadata(self):
        cmake = ROOT / "CMakeLists.txt"
        text = cmake.read_text(encoding="utf-8")

        project_block = f"""project(
        {"_".join(self.cfg.get("project.name").split())}
        VERSION {self.cfg.get("project.version")}
        DESCRIPTION "{self.cfg.get("project.description")}"
        LANGUAGES C CXX
        )"""

        text = re.sub(
            r"project\s*\(.*?\)",
            project_block,
            text,
            flags=re.DOTALL
        )

        cmake.write_text(text, encoding="utf-8")

    def target_name(self):
        name = self.cfg.get("main.name", False)
        return "_".join(
            (self.cfg.get("project.name") if (name == "auto" or not name) else name).lower().split()
        )

    def current_project_name(self) -> str:
        cmake = ROOT / "CMakeLists.txt"
        text = cmake.read_text(encoding="utf-8")

        match = re.search(r'project\s*\(\s*([A-Za-z0-9_.+-]+)', text, re.IGNORECASE)

        if match is None:
            raise RuntimeError("Couldn't locate project() in CMakeLists.txt.")

        return match.group(1)

    def ensure_main_target(self):
        project_type = self.cfg.get("project.type")

        old_name = "_".join(self.current_project_name().lower().split())
        new_name = self.target_name()
        src_dir  =  ROOT / "src" / project_type

        old_path = src_dir / old_name
        new_path = src_dir / new_name

        old_exists = old_path.exists()
        new_exists = new_path.exists()

        is_just_case_change = (
            old_exists
            and old_path.name.lower() == new_path.name.lower()
            and old_path.name != new_path.name
        )

        if old_exists and old_name != new_name:
            Log.info(f"Renaming target folder: {old_name} -> {new_name}")

            if new_exists:
                raise ProjectError(
                    f"Target folder already exists:\n{new_path}"
                )

            if is_just_case_change:
                temp = src_dir / f"{new_name}_temp"
                old_path.rename(temp)
                temp.rename(new_path)
            else:
                old_path.rename(new_path)

        elif not old_exists and not new_exists:
            Log.info(f"Creating target folder: {new_name}")
            new_path.mkdir(parents=True)

        main_cpp = new_path / "main.cpp"

        if not main_cpp.exists():
            main_cpp.write_text(
                dedent("""\
                    #include <iostream>

                    auto main(int argc, const char** argv) -> int {
                        std::cout << "Hello world!\\n";

                        return 0;
                    }
                """),
                encoding="utf-8",
            )

        main_cmake = new_path / "CMakeLists.txt"

        if not main_cmake.exists():
            command = ("create_executable" if project_type == "exe" else "create_library")
            main_cmake.write_text(f"{command}(${{TARGET_NAME}} PRIVATE utils)\n", encoding="utf-8")
            
        src_cmake = src_dir / "CMakeLists.txt"
        if not src_cmake.exists():
            src_cmake.write_text("", encoding="utf-8")

        text = src_cmake.read_text(encoding="utf-8")
        line = "add_subdirectory(${TARGET_NAME})"

        if line not in text:
            if text and not text.endswith("\n"):
                text += "\n"

            text += line + "\n"
            src_cmake.write_text(text, encoding="utf-8")

    def remove_main_target(self):
        project_type = self.cfg.get("project.type")
        src_dir  =  ROOT / "src" / project_type
        target =  "_".join(self.current_project_name().lower().split())
        src_cmake = src_dir / "CMakeLists.txt"

        Utils.remove(src_dir / target)

        if not src_cmake.exists():
            return

        line = "add_subdirectory(${TARGET_NAME})"

        text = src_cmake.read_text(encoding="utf-8").replace(line, "")
        src_cmake.write_text(text, encoding="utf-8")

        Utils.remove((ROOT / "output/bin" / self.cfg.get("build.config") / target))

    def set_metadata(self):
        if self.cfg.get("main.create"):
            self.ensure_main_target()
        else:
            Log.info("Disabled!")
            self.remove_main_target()

        self.update_project_metadata()

    def ensure_configured(self):
        if not self.cfg.build_dir.exists():
            self.configure()
            return

        if self.cmake_modified():
            Log.info("CMake change detected!")
            self.configure() 
            return

        Log.info("Config manager: No work to do.")

    def configure(self):
        cmd = ["cmake", "-S", str(ROOT), "-B", str(self.cfg.build_dir), "-G", self.generator, f"-DTARGET_NAME={self.target_name()}"]
        Log.step("Configuring project")
        Utils.mkdir(self.cfg.build_dir)

        if not self.is_multi_config:
            cmd.append(f"-DCMAKE_BUILD_TYPE={self.config}")

        for target in ("docs", "examples", "deps"):
            name = "build_" + target
            cmd.append(f"-D{name.upper()}={"ON" if self.cfg.get("build." + name) else "OFF"}")

        cmd.append(f"-DBUILD_TESTS={"ON" if self.cfg.get("test.enabled") else "OFF"}")
        cmd.append(f"-DBUILD_SHARED_LIBS={"ON" if self.cfg.get("build.shared_libs") else "OFF"}")
        cmd.extend(self.compiler.cmake_args)

        for define in self.cfg.get("build.defines"):
            cmd.append(f"-D{define}=ON")

        for key, value in self.cfg.get("build.flags").items():
            if isinstance(value, bool):
                value = "ON" if value else "OFF"
            elif isinstance(value, str):
                value = f"\"{value}\""
            cmd.append(f"-D{key}={value}")

        Utils.run(cmd, env=self.compiler.env)
        Log.ok("Configuration finished.")

    def build(self):
        self.set_metadata()
        self.ensure_configured()

        Log.step(f"Building ({self.config})")
        cmd = ["cmake", "--build", str(self.cfg.build_dir)]

        if self.is_multi_config:
            cmd.extend(["--config", self.config])

        cmd.extend(["--parallel", str(self.jobs)])
        Utils.run(cmd, env=self.compiler.env)

        Log.ok("Build completed.")

    def rebuild(self):
        self.clean()
        self.configure()
        self.build()

    def test(self):
        if not self.cfg.get("test.enabled"):
            Log.warn("Tests are disabled.")
            return

        self.build()
        Log.step("Running tests")
        cmd = ["ctest", "--test-dir",str(self.cfg.build_dir)]

        if self.is_multi_config:
            cmd.extend(["-C", self.config])

        cmd.append("--output-on-failure")
        Utils.run(cmd)
        Log.ok("All tests passed.")

    def clean(self):
        Log.step("Cleaning project")

        for directory in (self.cfg.build_dir, self.cfg.output_dir, self.cfg.dist_dir, self.cfg.temp_dir):
            if directory.exists():
                Utils.remove(directory)
                Log.info(f"Removed {directory.name}")

        Log.ok("Project cleaned.")

    def doctor(self):
        Log.step("Environment")
        print("\nGenerator :", self.generator)
        print("Compiler  :", self.compiler.name)
        print("Build type:", self.config)
        print("Jobs      :", self.jobs)

class Runner:
    def __init__(self, builder):
        self.builder = builder
        self.cfg = builder.cfg

    def executable(self, name):
        return (self.cfg.output_bin / self.builder.config / (
                name + Platform.exe_ext()))

    def run(self):
        executables = self.cfg.get("run.executables")

        for name, options in executables.items():
            if name == "none" or not options.get("enabled"):
                continue

            exe = (self.executable(self.builder.target_name()) if name == "main" else self.executable(name))
            cmd = [str(exe), *options.get("args", [])]
            wait = options.get("wait", False)
            creationflags = (subprocess.CREATE_NEW_CONSOLE if options.get("show_console", False) else 0)

            if not exe.exists():
                Log.fail(f"Executable not found:\n{exe}")
            Log.step(f"Running: {exe.name}")

            if wait:
                subprocess.Popen(cmd, cwd=ROOT, creationflags=creationflags)
                continue

            proc = subprocess.Popen(cmd, cwd=ROOT, creationflags=creationflags)

            if creationflags:
                proc.wait()
                continue

            try:
                proc.wait()
            except KeyboardInterrupt:
                Log.info("Executable interrupted, next...")
                continue
                
    def build_run(self):
        self.builder.build()
        self.run()

    def rebuild_run(self):
        self.builder.clean()
        self.build_run()

class Compressor:
    def __init__(self, builder):
        self.cfg = builder.cfg
        self.tool = self.cfg.compressors_dir / self.cfg.get("compress.tool")

    def find_tool(self):
        path = Utils.which(self.tool)

        if path:
            return Path(path)

        local = self.cfg.compressors_dir / (
            self.tool + (".exe" if Platform.is_windows() else "")
        )

        if local.exists():
            return local

        Log.fail(
            f"Compression tool '{tool}' was not found.\n"
            f"Searched PATH and:\n{self.cfg.compressors_dir}"
        )

    def find_targets(self):
        files = []

        for target in self.cfg.get("compress.targets"):
            if target == "main":
                path = self.runner.executable(self.builder.target_name())

            elif "*" not in target and "?" not in target and "/" not in target and "\\" not in target:
                path = self.runner.executable(target)

            else:
                files.extend(ROOT.glob(target))
                continue

            if path.exists():
                files.append(path)
            else:
                Log.warn(f"Target not found: {path}")

            files.extend(ROOT.glob(target))

        files = sorted(set(files))

        return [f for f in files if f.is_file()]

    def backup_file(self, file_):
        if not self.cfg.get("compress.keep_original"):
            return

        backup = file_.with_suffix(file_.suffix + ".bak")
        shutil.copy2(file_, backup)

        Log.info(f"File backup created: {backup.name}")

    def compress_file(self, file_):
        self.backup_file(file_)

        cmd = [
            str(self.tool),
            *self.cfg.get("compress.args"),
            str(file_)
        ]

        Utils.run(cmd)

        Log.ok(f"Compressed: {file_.name}")

    def compress(self):
        if not self.cfg.get("compress.enabled"):
            Log.warn("Compression is disabled.")
            return

        Log.step("Compressing binaries")

        tool = self.find_tool()
        targets = self.find_targets()

        if not targets:
            Log.warn("No files matched the compression targets.")
            return

        Log.info(f"Using: {tool.name}")

        for file_ in targets:
            self.compress_file(file_)

        Log.ok(f"Compressed {len(targets)} file(s).")

class Packager:
    def __init__(self, builder):
        self.builder = builder
        self.cfg = self.builder.cfg

    @property
    def archive_name(self):
        template = self.cfg.get("package.name_template")

        values = {
            "name": self.cfg.get("project.name"),
            "version": self.cfg.get("project.version"),
            "platform": platform.system().lower(),
            "arch": platform.machine().lower(),
            "config": self.builder.config,
            "date": datetime.now().strftime("%Y%m%d"),
        }

        for key, value in values.items():
            template = template.replace(f"{{{key}}}", value)

        return template

    def collect_files(self):
        files = []

        binary_dir = self.cfg.output_bin / self.builder.config

        if binary_dir.exists():
            for file_ in binary_dir.iterdir():
                if file_.is_file() and file_.suffix.lower() in (".exe", ".dll"):
                    files.append(file_)

        for item in self.cfg.get("package.include"):
            path = ROOT / item

            if path.exists():
                files.append(path)

        return files

    def create_zip(self, archive):
        files = self.collect_files()

        with zipfile.ZipFile(
            archive,
            "w",
            compression=zipfile.ZIP_DEFLATED,
            compresslevel=9
        ) as zipf:
            for path in files:
                if path.is_file():
                    if path.suffix.lower() in {".exe", ".dll"}:
                        arcname = Path("bin") / path.name
                    else:
                        arcname = path.relative_to(ROOT)

                    zipf.write(path, arcname=arcname)
                    continue

                for file in path.rglob("*"):
                    if not file.is_file():
                        continue

                    if file.suffix.lower() in {".exe", ".dll"}:
                        arcname = Path("bin") / file.name
                    else:
                        arcname = file.relative_to(ROOT)

                    zipf.write(file, arcname=arcname)

    def package(self):
        Log.step("Packaging")

        Utils.mkdir(self.cfg.dist_dir)

        formats = self.cfg.get("package.formats")

        if "zip" not in formats:
            Log.fail("Only ZIP packaging is currently supported.")

        archive = self.cfg.dist_dir / f"{self.archive_name}.zip"

        if archive.exists():
            archive.unlink()

        self.create_zip(archive)

        Log.ok(f"Created: {archive.name}")
        

def main():

    Utils.enable_windows_ansi()

    parser = argparse.ArgumentParser(prog="project")

    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("configure")
    sub.add_parser("build")
    sub.add_parser("run")
    sub.add_parser("build-run")
    sub.add_parser("clean")
    sub.add_parser("rebuild")
    sub.add_parser("rebuild-run")
    sub.add_parser("test")
    sub.add_parser("doctor")
    sub.add_parser("compress")
    sub.add_parser("package")

    args = parser.parse_args()
    cfg = Config()
    builder = Builder(cfg)
    runner = Runner(builder)
    compressor = Compressor(builder)
    packager = Packager(builder)

    match args.command:
        case "configure":
            builder.configure()
        case "build":
            builder.build()
        case "run":
            runner.run()
        case "build-run":
            runner.build_run()
        case "clean":
            builder.clean()
        case "rebuild":
            builder.rebuild()
        case "rebuild-run":
            runner.rebuild_run()
        case "test":
            builder.test()
        case "doctor":
            builder.doctor()
        case "compress":
            compressor.compress()
        case "package":
            packager.package()

if __name__ == "__main__":
    Utils.clear_terminal()

    main()