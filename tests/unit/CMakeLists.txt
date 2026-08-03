add_executable(
    unit_tests
    core/test.cpp
)

target_link_libraries(
    unit_tests

    PRIVATE
    GTest::gtest_main
)

add_custom_command(TARGET unit_tests POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy_if_different
        $<TARGET_FILE:utils>  # duplicate and replace "utils" with lib name to add more
        $<TARGET_FILE:gtest>
        $<TARGET_FILE:gtest_main>
        $<TARGET_FILE_DIR:unit_tests>
)

include(GoogleTest)

gtest_discover_tests(unit_tests)