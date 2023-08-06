def _cmake_to_bool(s):
    return s.upper() not in ['', '0','FALSE','OFF','N','NO','IGNORE','NOTFOUND']

is_python_package    = _cmake_to_bool("TRUE")

BUILD_STUB_FILES     = _cmake_to_bool("OFF")
BUILD_UMFPACK        = _cmake_to_bool("")
ENABLE_UNIT_TESTS    = _cmake_to_bool("OFF")
INSTALL_DEPENDENCIES = _cmake_to_bool("OFF")
USE_CCACHE           = _cmake_to_bool("ON")
USE_HYPRE            = _cmake_to_bool("OFF")
USE_LAPACK           = _cmake_to_bool("ON")
USE_MKL              = _cmake_to_bool("ON")
USE_MKL              = _cmake_to_bool("ON")
USE_MUMPS            = _cmake_to_bool("OFF")
USE_PARDISO          = _cmake_to_bool("OFF")
USE_UMFPACK          = _cmake_to_bool("OFF")

NETGEN_DIR = "C:/gitlabci/tools/builds/3zsqG5ns/0/ngsolve/venv_ngs/Lib/site-packages"

NGSOLVE_COMPILE_DEFINITIONS         = "HAVE_NETGEN_SOURCES;USE_TIMEOFDAY;TCL;USE_PARDISO;LAPACK;NGS_PYTHON"
NGSOLVE_COMPILE_DEFINITIONS_PRIVATE = "USE_MKL"
NGSOLVE_COMPILE_INCLUDE_DIRS        = ""
NGSOLVE_COMPILE_OPTIONS             = "/std:c++17;-DMAX_SYS_DIM=3"

NGSOLVE_VERSION = "6.2.2304"
NGSOLVE_VERSION_GIT = "v6.2.2304-0-g5d68379e1"
NGSOLVE_VERSION_PYTHON = "6.2.2304"

NGSOLVE_VERSION_MAJOR = "6"
NGSOLVE_VERSION_MINOR = "2"
NGSOLVE_VERSION_TWEAK = "0"
NGSOLVE_VERSION_PATCH = "2304"
NGSOLVE_VERSION_HASH = "g5d68379e1"

version = NGSOLVE_VERSION_GIT
