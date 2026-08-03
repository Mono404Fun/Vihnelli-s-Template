#include <gtest/gtest.h>

// Example function you might have in your project:
// #include "utils/math.hpp"

TEST(BasicTest, ExpectTrue) {
    EXPECT_TRUE(true);
}

TEST(BasicTest, AdditionWorks) {
    int result = 2 + 3;

    EXPECT_EQ(result, 5);
}

TEST(BasicTest, StringsMatch) {
    std::string hello = "Hello";

    EXPECT_EQ(hello, "Hello");
}