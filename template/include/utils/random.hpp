#pragma once

struct Range {
    long start, end;
};

auto randInt(Range range) -> long;