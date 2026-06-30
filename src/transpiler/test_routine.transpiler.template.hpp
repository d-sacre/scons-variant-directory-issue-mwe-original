#pragma once

#include <iostream>

namespace MWE::Tests::Routine {
    template <typename T>
    class <TEST_ROUTINE_ID> {
        public:
            <TEST_ROUTINE_ID>(T values){
                m_values = values;
            };

            void Run() {
                std::cout << "Running Test <TEST_ROUTINE_ID>" << "\n";
                <RUN>
                std::cout << "\n\n";
            }

        private:
            T m_values;
    };
}