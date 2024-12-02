//
// Created by alexa on 11/29/2024.
//

#include <iostream>
#include <string>
#include <chrono>
#include <thread>

#include "std_lib.h"

void print(std::string message) {
    std::cout << message << std::endl;
}

std::string input(std::string message) {
    std::string value;
    std::cout << message;
    std::getline(std::cin, value);
    return value;
}

void wait(int milliseconds_) {
    std::this_thread::sleep_for(std::chrono::milliseconds(milliseconds_));
}

int scasti(std::string value) {
    return std::stoi(value);
}

std::string icasts(int value) {
    return std::to_string(value);
}