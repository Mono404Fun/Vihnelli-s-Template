#include "ressource.hpp"

auto Animal::speak() -> Animal& {
    std::cout << "Animal!\n";
    return *this;
}

auto Dog::speak() -> Dog& {
    std::cout << "Dog!";
    return *this;
}