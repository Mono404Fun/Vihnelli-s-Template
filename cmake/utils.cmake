function(create_library LIB_NAME LIB_TYPE)

    string(TOUPPER "${LIB_TYPE}" LIB_TYPE_U)

    if(NOT LIB_TYPE_U MATCHES "^(STATIC|SHARED|INTERFACE)$")
        message(FATAL_ERROR
            "create_library(${LIB_NAME}): Invalid library type '${LIB_TYPE}'. "
            "Expected STATIC, SHARED, or INTERFACE."
        )
    endif()

    if(LIB_TYPE_U STREQUAL "INTERFACE")
        add_library(${LIB_NAME} INTERFACE)

        target_include_directories(${LIB_NAME}
            INTERFACE
                ${PROJECT_SOURCE_DIR}/include
    )

    else()

        file(GLOB_RECURSE SOURCES CONFIGURE_DEPENDS
            "${PROJECT_SOURCE_DIR}/src/lib/${LIB_NAME}/*.cpp"
            "${PROJECT_SOURCE_DIR}/src/lib/${LIB_NAME}/*.c"
            "${PROJECT_SOURCE_DIR}/src/lib/${LIB_NAME}/*.cc"
            "${PROJECT_SOURCE_DIR}/src/lib/${LIB_NAME}/*.cxx"
        )

        add_library(${LIB_NAME} ${LIB_TYPE_U}
            ${SOURCES}
        )

        target_include_directories(${LIB_NAME}
            PUBLIC
                ${PROJECT_SOURCE_DIR}/include/${LIB_NAME}
        )

        set_target_properties(${LIB_NAME}
            PROPERTIES WINDOWS_EXPORT_ALL_SYMBOLS ON
        )

    endif()

    add_library(${PROJECT_NAME}::${LIB_NAME} ALIAS ${LIB_NAME})

    set(_visibility "")
    foreach(arg IN LISTS ARGN)

        string(TOUPPER "${arg}" ARG_U)

        if(ARG_U MATCHES "^(PUBLIC|PRIVATE|INTERFACE)$")
            set(_visibility "${ARG_U}")
        else()
            if(NOT _visibility)
                message(FATAL_ERROR
                    "Library '${arg}' has no preceding PUBLIC, PRIVATE or INTERFACE."
                )
            endif()

            target_link_libraries(${LIB_NAME}
                ${_visibility}
                ${arg}
            )
        endif()

    endforeach()

endfunction()

function(create_executable EXE_NAME)

    file(GLOB_RECURSE SOURCES CONFIGURE_DEPENDS
        "${PROJECT_SOURCE_DIR}/src/exe/${EXE_NAME}/*.cpp"
        "${PROJECT_SOURCE_DIR}/src/exe/${EXE_NAME}/*.c"
        "${PROJECT_SOURCE_DIR}/src/exe/${EXE_NAME}/*.cc"
        "${PROJECT_SOURCE_DIR}/src/exe/${EXE_NAME}/*.cxx"
    )

    add_executable(${EXE_NAME}
        ${SOURCES}
    )

    add_executable(${PROJECT_NAME}::${EXE_NAME} ALIAS ${EXE_NAME})

    set(_visibility "")
    foreach(arg IN LISTS ARGN)

        string(TOUPPER "${arg}" ARG_U)

        if(ARG_U MATCHES "^(PUBLIC|PRIVATE|INTERFACE)$")
            set(_visibility "${ARG_U}")
        else()
            if(NOT _visibility)
                message(FATAL_ERROR
                    "Library '${arg}' has no preceding PUBLIC, PRIVATE or INTERFACE."
                )
            endif()

            target_link_libraries(${EXE_NAME}
                ${_visibility}
                ${arg}
            )
        endif()

    endforeach()

endfunction()

string(TOLOWER "${PROJECT_NAME}" TMP_TARGET_NAME)
string(REPLACE " " "_" TMP_TARGET_NAME "${TMP_TARGET_NAME}")

set(TARGET_NAME "${TMP_TARGET_NAME}" CACHE INTERNAL "Exectuable target name (lowered)")