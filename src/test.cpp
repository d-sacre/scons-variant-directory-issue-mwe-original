#include <iostream>

#include "g_a_values.hpp"
#include "g_b1_calculations.hpp"
#include "g_b2_calculations.hpp"

int main(){
    // DESCRIPTION: Initialize all data and functionality
    auto values = MWE::Tests::Values();
    auto routineB1 = MWE::Tests::Routine::B1(&values);
    auto routineB2 = MWE::Tests::Routine::B2(&values);

    // DESCRIPTION: Code execution
    std::cout << "\nStarting Test Sequence\n" << "\n";
    routineB1.Run();
    routineB2.Run();
}
