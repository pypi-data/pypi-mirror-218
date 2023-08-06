from os.path import join, dirname, realpath
from platform import architecture, machine
from ctypes import CDLL
import cffi
import logging
import logging.handlers
import platform
import os

logger = logging.getLogger()  # 不加名称设置 (Get root logger without specifying name)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

# 使用FileHandler输出到文件 (Output to file using FileHandler)
log_path = ""
if platform.system().lower() == "windows":
    program_data_path = os.getenv("LOCALAPPDATA")
    log_path = os.path.join(program_data_path, "Pnd")
elif platform.system().lower() == "linux":
    log_path = "/tmp/log/Pnd"
elif platform.system().lower() == "darwin":
    log_path = os.path.join(os.path.dirname(__file__), "log")

if not os.path.exists(log_path):
    os.makedirs(log_path)
fh = logging.handlers.RotatingFileHandler(
    os.path.join(log_path, "fourier_server_log.txt"), maxBytes=4 * 1024 * 1024, backupCount=5
)
fh.setFormatter(formatter)

# 使用StreamHandler输出到屏幕 (Output to terminal using StreamHandler)
ch = logging.StreamHandler()
ch.setFormatter(formatter)

log_level = logging.DEBUG
# log_level_str = configuration.get_config().get("log_level", "INFO")
# if log_level_str == "DEBUG":
#     log_level = logging.DEBUG
# elif log_level_str == "INFO":
#     log_level = logging.INFO
# elif log_level_str == "WARNING":
#     log_level = logging.WARNING
# elif log_level_str == "ERROR":
#     log_level = logging.ERROR

logger.setLevel(log_level)
fh.setLevel(log_level)
ch.setLevel(log_level)

# 添加两个Handler (Add two instances of Handler)
logger.addHandler(ch)
logger.addHandler(fh)

ffi = cffi.FFI()


class SharedLibraryLoader(object):
    def __init__(self, library: str):
        self._candidates: "list[str]" = list()
        self._library = library

    def add_candidate(self, loc: str):
        self._candidates.append(loc)

    @property
    def candidates(self):
        return self._candidates

    def try_load_library(self):
        """Goes through all candidate libraries in priority order.

        :return: a tuple (pair): `ctypes` object representing the library, along with the file path of the library
        """
        candidates = self.candidates
        candidate_count = len(candidates)
        logging.debug(f"Loading library {self._library}.")
        logging.debug(f"Loader(library={self._library}): {candidate_count} candidate binaries:")
        logging.debug(f"Loader(library={self._library}): Candidate binaries, in order of priority:")

        # Loop twice so all candidate libraries can be printed to debug stream in case of debugging enabled
        for i, candidate in enumerate(candidates):
            logging.debug("Candidate {}: {}".format(i + 1, candidate))

        from ctypes import cdll

        for candidate in candidates:
            try:
                lib = cdll.LoadLibrary(candidate)
                logging.debug("Successfully loaded library at {}".format(candidate))
                return lib, candidate
            except Exception as e:
                logging.debug("Attempting to load library {} raised exception:\n{}".format(candidate, e))

        logging.warning("Unable to load (library={}).\nCandidate libraries attempted (in order):".format(self._library))
        for i, candidate in enumerate(candidates):
            logging.warning("Candidate {}: {}".format(i + 1, candidate))
        return None, None

    def try_load_library_(self):
        candidates = self.candidates
        candidate_count = len(candidates)
        logging.debug(f"Loading library {self._library}.")
        logging.debug(f"Loader(library={self._library}): {candidate_count} candidate binaries:")
        logging.debug(f"Loader(library={self._library}): Candidate binaries, in order of priority:")

        # Loop twice so all candidate libraries can be printed to debug stream in case of debugging enabled
        for i, candidate in enumerate(candidates):
            logging.debug("Candidate {}: {}".format(i + 1, candidate))

        from ctypes import cdll

        for candidate in candidates:
            try:
                ffi.cdef(
                    """
                    int pndGetLibraryVersion(int32_t *major, int32_t *minor, int32_t *revision);
                """
                )
                # 加载共享对象
                lib = ffi.dlopen(candidate)
                logging.debug("Successfully loaded library at {}".format(candidate))
                return lib, candidate
            except Exception as e:
                logging.debug("Attempting to load library {} raised exception:\n{}".format(candidate, e))

        logging.warning("Unable to load (library={}).\nCandidate libraries attempted (in order):".format(self._library))
        for i, candidate in enumerate(candidates):
            logging.warning("Candidate {}: {}".format(i + 1, candidate))
        return None, None

    def try_load_library__(self):
        candidates = self.candidates
        candidate_count = len(candidates)
        logging.debug(f"Loading library {self._library}.")
        logging.debug(f"Loader(library={self._library}): {candidate_count} candidate binaries:")
        logging.debug(f"Loader(library={self._library}): Candidate binaries, in order of priority:")

        # Loop twice so all candidate libraries can be printed to debug stream in case of debugging enabled
        for i, candidate in enumerate(candidates):
            logging.debug("Candidate {}: {}".format(i + 1, candidate))

        from ctypes import cdll

        for candidate in candidates:
            try:
                ffi.cdef(
                    """
                    int pndGetLibraryVersion(int32_t *major, int32_t *minor, int32_t *revision);
                """
                )
                # 加载共享对象
                lib = ffi.dlopen(candidate)
                logging.debug("Successfully loaded library at {}".format(candidate))
                return lib, candidate
            except Exception as e:
                logging.debug("Attempting to load library {} raised exception:\n{}".format(candidate, e))

        logging.warning("Unable to load (library={}).\nCandidate libraries attempted (in order):".format(self._library))
        for i, candidate in enumerate(candidates):
            logging.warning("Candidate {}: {}".format(i + 1, candidate))
        return None, None


def _get_library_load_candidates(library: str, readable_name: str, env_var: "str | None" = None):
    ret: "list[str]" = list()
    from os import environ
    import sys

    # Top priority: environment variables (if set)
    if env_var is not None:
        environ_val = environ.get(env_var)
        if environ_val is not None:
            logging.debug(
                "{} library candidate '{}' from {} environment variable".format(readable_name, environ_val, env_var)
            )
            ret.append(environ_val)

    # Lower priority: load from installed package
    lib_base_path = join(join(dirname(realpath(__file__)), "..", "pnd"), "lib")

    if sys.platform.startswith("linux"):
        _find_linux_candidates(ret, lib_base_path, library)
    elif sys.platform == "darwin":
        _find_mac_candidates(ret, lib_base_path, library)
    elif sys.platform == "win32":
        _find_win_candidates(ret, lib_base_path, library)

    return ret


def _load_shared_library(name: str, readable_name: str, env_var: "str | None" = None):
    loader = SharedLibraryLoader(name)

    for entry in _get_library_load_candidates(name, readable_name, env_var):
        loader.add_candidate(entry)

    loaded_c_lib, loaded_loc = loader.try_load_library_()
    if loaded_c_lib is None:
        raise RuntimeError("{} library not found".format(readable_name))

    assert loaded_loc is not None
    return loaded_c_lib, loaded_loc


def _load_core_shared_library():
    return _load_shared_library("pnd", "PND Core", "PND_C_LIB")


def _find_linux_candidates(output: "list[str]", lib_base_path: str, library: str):
    import re

    cpu = machine()
    py_exec_arch = architecture()[0]
    lib_str = "lib{}.so".format(library)

    if cpu == "x86_64" and ("64" in py_exec_arch):
        # 64 bit x86 CPU with 64 bit python
        lib_path = join(lib_base_path, "linux_x86_64", lib_str)

    elif (re.match("i[3-6]86", cpu) is not None) or (cpu == "x86_64") and ("32" in py_exec_arch):
        raise RuntimeError(
            "i686 is no longer supported. If you are on a 64 bit kernel, install and run an x86_64 instance of Python."
        )

    elif (re.match("arm.*", cpu) is not None) and ("32" in py_exec_arch):
        # 32 bit armhf with 32 bit python
        lib_path = join(lib_base_path, "linux_armhf", lib_str)

    elif (re.match("arm.*", cpu) is not None) or "aarch64" in cpu and ("64" in py_exec_arch):
        lib_path = join(lib_base_path, "linux_aarch64", lib_str)
    else:
        raise RuntimeError("Unknown architecture {0}".format(cpu))

    output.append(f"{lib_path}")
    output.append(lib_path)


def _find_mac_candidates(output: "list[str]", lib_base_path: str, library: str):
    cpu = machine()
    if cpu == "arm64":
        output.append(join(lib_base_path, "darwin_arm64", f"lib{library}.dylib"))
    else:  # if cpu == 'amd64' or cpu == 'x86' ?
        output.append(join(lib_base_path, "darwin_x86_64", f"lib{library}.dylib"))


def _find_win_candidates(output: "list[str]", lib_base_path: str, library: str):
    cpu = machine()
    py_exec_arch = architecture()[0]

    if cpu == "AMD64" or cpu == "x86":
        # Windows doesn't like to make it easy to detect which architecture the process is running in (x86 vs x64)
        # You can use `ctypes` to detect this, but this is a more terse way.
        output.append(join(lib_base_path, "win_x64", "{}.dll".format(library)))
        output.append(join(lib_base_path, "win_x86", "{}.dll".format(library)))
    elif cpu == "ARM":
        # XXX Not yet supported :(
        # 32 bit ARM on Windows
        raise RuntimeError("ARM is not yet supported on Windows")
    elif cpu == "ARM64":
        # XXX Not yet supported :(
        # 64 bit ARM on Windows
        raise RuntimeError("ARM64 is not yet supported on Windows")
    else:
        raise RuntimeError("Unknown architecture {}".format(cpu))


def _init_libraries():
    from lvhao_lib._pnd import ffi, lib

    major = ffi.new("int32_t *")
    minor = ffi.new("int32_t *")
    revision = ffi.new("int32_t *")
    ret = lib.pndGetLibraryVersion(major, minor, revision)
    print(f"{ret} major: {major[0]}, minor: {minor[0]}, revision: {revision[0]}")

    # core_lib, core_loc = _load_core_shared_library()
    # print(core_lib)
    # major = ffi.new("int32_t *")
    # minor = ffi.new("int32_t *")
    # revision = ffi.new("int32_t *")
    # ret = core_lib.pndGetLibraryVersion(major, minor, revision)
    # print(f"{ret} major: {major[0]}, minor: {minor[0]}, revision: {revision[0]}")


#   return HEBICoreLibrary(core_lib, core_loc)


# Load library on import
_handle = _init_libraries()
