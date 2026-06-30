#pragma once

#include <iostream>
#include "g_a_values.hpp"

namespace MWE::Tests::Routine {
    class <TEST_ROUTINE_ID> {
        public:
            <TEST_ROUTINE_ID>(MWE::Tests::Values* values){
                m_values = values;
            };

            void Run() {
                std::cout << "Running Test <TEST_ROUTINE_ID>" << "\n";
                <RUN>
                std::cout << "\n\n";
            }

        private:
            MWE::Tests::Values* m_values;
    };
}