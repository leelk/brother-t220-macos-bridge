// SPDX-License-Identifier: Apache-2.0
#include "ppm_reader.hpp"
#include <fstream>
#include <iostream>
int main(int argc, char **argv) {
    if (argc != 2) { std::cerr << "Usage: raster-check input.ppm\n"; return 2; }
    try {
        std::ifstream input(argv[1], std::ios::binary);
        if (!input) throw std::runtime_error("Cannot open raster");
        std::uint64_t hash = 14695981039346656037ULL, bytes = 0;
        std::size_t bands = 0, peak = 0;
        const auto info = brother::read_ppm(input,
            [&](brother::RasterInfo, std::uint32_t, std::uint32_t,
                const unsigned char *data, std::size_t count) {
                for (std::size_t i = 0; i < count; ++i) { hash ^= data[i]; hash *= 1099511628211ULL; }
                bytes += count; ++bands; peak = std::max(peak, count);
            });
        std::cout << "{\"width\":" << info.width << ",\"height\":" << info.height
                  << ",\"payload_bytes\":" << bytes << ",\"bands\":" << bands
                  << ",\"max_band_bytes\":" << peak << ",\"fnv1a64\":" << hash << "}\n";
        return 0;
    } catch (const std::exception &error) {
        std::cerr << "Error: " << error.what() << "\n"; return 2;
    }
}
