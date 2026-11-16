cmake_minimum_required(VERSION 3.20)
project(BustAMove2JPRecomp LANGUAGES C CXX)
set(PSXRECOMP_ROOT "${CMAKE_CURRENT_SOURCE_DIR}/psxrecomp" CACHE PATH "Framework")
set(PSX_RECOMP_UI OFF CACHE BOOL "External assistant" FORCE)
set(PSX_SETUP_WIZARD OFF CACHE BOOL "External assistant" FORCE)
set(PSX_NETPLAY OFF CACHE BOOL "Local play" FORCE)
set(PSX_DEBUG_TOOLS OFF CACHE BOOL "Release" FORCE)
set(PSXRECOMP_REQUIRE_GAME_C ON CACHE BOOL "Generate from personal disc first" FORCE)
include("${PSXRECOMP_ROOT}/runtime/runtime.cmake")
psxrecomp_add_game_runtime(psx-runtime
    PRELOADED_MODS_DIR "NONE"
    WINDOW_TITLE "BustAMove2JP Recompiled"
    EXE_NAME "BustAMove2JP_Pessoal"
    DEFAULT_GAME_CONFIG_PATH "game.toml"
    MAX_PLAYERS 2
    GEN_MARKER "generated/SLPM_862.19_dispatch.c"
    GEN_FULL_GLOB "generated/SLPM_862.19_full_*.c"
)
add_custom_command(TARGET psx-runtime POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy_if_different
        "${CMAKE_CURRENT_SOURCE_DIR}/game.toml" "$<TARGET_FILE_DIR:psx-runtime>/game.toml")
