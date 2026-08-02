#include <random>
#include "random.hpp"

auto randInt(Range range) -> long {
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> rng(range.start, range.end);
    return rng(gen);
}