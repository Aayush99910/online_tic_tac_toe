cmake_minimum_required(VERSION 3.15)
project(GameLogic LANGUAGES CXX)

# Enable modern Python detection
set(PYBIND11_FINDPYTHON ON)

# Find pybind11 package
find_package(pybind11 REQUIRED)

# Create the Python extension module
pybind11_add_module(gamelogic GameLogic.cpp)

# Install the generated module
install(TARGETS gamelogic DESTINATION .)

