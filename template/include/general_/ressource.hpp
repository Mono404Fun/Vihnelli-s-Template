#include <iostream>

class Animal {
    public:
    virtual Animal& speak();
};

class Dog: public Animal {
    public:
    Dog& speak() override;
};