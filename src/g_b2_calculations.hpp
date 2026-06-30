#pragma once

#include <iostream>
#include "g_a_values.hpp"

namespace MWE::Tests::Routine {
    class B2 {
        public:
            B2(MWE::Tests::Values* values){
                m_values = values;
            };

            void Run() {
                std::cout << "Running Test B2" << "\n";
                std::cout << "UUID b21: a1-a2 = " << m_values->b21 << "\n";
std::cout << "UUID b22: a2-a5 = " << m_values->b22 << "\n";
std::cout << "UUID b23: a1-a3 = " << m_values->b23 << "\n";
std::cout << "UUID b24: a4-a3 = " << m_values->b24 << "\n";

                std::cout << "\n\n";
            }

        private:
            MWE::Tests::Values* m_values;
    };
}