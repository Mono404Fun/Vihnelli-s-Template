function(optimize TARGET)
    if(MSVC)
        target_compile_options(${TARGET} PRIVATE
            $<$<CONFIG:Release>:
                /O2
                /Oi
                /Ot
                /GL
                /Gy
                /Gw
                /fp:fast
                /arch:AVX2
                /Oy
                /Zc:inline
            >

            $<$<CONFIG:RelWithDebInfo>:
                /O2
                /Oi
                /Ot
                /GL
                /Gy
                /Gw
                /fp:fast
                /arch:AVX2
                /Oy
                /Zc:inline
            >

            $<$<CONFIG:MinSizeRel>:
                /O1
                /GL
                /Gy
                /Gw
            >
        )

        target_link_options(${TARGET} PRIVATE
            $<$<CONFIG:Release>:
                /LTCG
                /OPT:REF
                /OPT:ICF
                /INCREMENTAL:NO
            >

            $<$<CONFIG:RelWithDebInfo>:
                /LTCG
                /OPT:REF
                /OPT:ICF
                /INCREMENTAL:NO
            >

            $<$<CONFIG:MinSizeRel>:
                /LTCG
                /OPT:REF
                /OPT:ICF
            >
        )

    elseif(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")

        target_compile_options(${TARGET} PRIVATE
            $<$<CONFIG:Release>:
                -O3
                -march=native
                -mtune=native
                -ffast-math
                -funroll-loops
                -flto
                -fomit-frame-pointer
                -fdata-sections
                -ffunction-sections
                -pipe
            >
        )

        target_link_options(${TARGET} PRIVATE
            $<$<CONFIG:Release>:
                -flto
                -Wl,--gc-sections
                -Wl,-O2
            >
        )
    endif()
endfunction()