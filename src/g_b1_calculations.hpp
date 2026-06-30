#pragma once

#include <iostream>
#include "g_a_values.hpp"

namespace MWE::Tests::Routine {
    class B1 {
        public:
            B1(MWE::Tests::Values* values){
                m_values = values;
            };

            void Run() {
                std::cout << "Running Test B1" << "\n";
                std::cout << "UUID b11: a1+a2 = " << m_values->b11 << "\n";
std::cout << "UUID b12: a2+a5 = " << m_values->b12 << "\n";
std::cout << "UUID b13: a1+a3 = " << m_values->b13 << "\n";
std::cout << "UUID b14: a4+a3 = " << m_values->b14 << "\n";

                std::cout << "\n\n";
            }

        private:
            MWE::Tests::Values* m_values;
    };
}