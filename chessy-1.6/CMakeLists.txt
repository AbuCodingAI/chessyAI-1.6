cmake_minimum_required(VERSION 3.16)
project(Chessy-1.6 CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find required packages
find_package(Eigen3 REQUIRED)
find_package(nlohmann_json REQUIRED)
find_package(Boost REQUIRED)

# Include directories
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/src)

# Source files
set(SOURCES
    src/main.cpp
    src/chess/board.cpp
    src/chess/moves.cpp
    src/chess/rules.cpp
    src/chess/position.cpp
    src/engine/evaluator.cpp
    src/engine/search.cpp
    src/engine/transposition.cpp
    src/training/trainer.cpp
    src/training/stockfish_interface.cpp
    src/training/blunder_injector.cpp
    src/neural/network.cpp
    src/neural/weights.cpp
)

# Create executable
add_executable(chessy-1.6 ${SOURCES})

# Link libraries
target_link_libraries(chessy-1.6 
    Eigen3::Eigen
    nlohmann_json::nlohmann_json
)

# Compiler flags
if(MSVC)
    target_compile_options(chessy-1.6 PRIVATE /W4 /O2)
else()
    target_compile_options(chessy-1.6 PRIVATE -Wall -Wextra -O3)
endif()

# Output directory
set_target_properties(chessy-1.6 PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin"
)
