include(FetchContent)

set(FETCHCONTENT_BASE_DIR
    "${PROJECT_SOURCE_DIR}/deps/fetch/content"
    CACHE PATH "" FORCE
)

include(gtest.cmake)