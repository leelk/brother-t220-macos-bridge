// SPDX-License-Identifier: Apache-2.0
#pragma once
#include <algorithm>
#include <cstdint>
#include <istream>
#include <stdexcept>
#include <string>
#include <vector>
namespace brother {
struct RasterInfo { std::uint32_t width, height; };
// Deliberately restricted to our generated P6/255/LF single-image fixtures.
inline std::string header_line(std::istream &input) {
    std::string line;
    for (unsigned n = 0; n < 64; ++n) {
        const int c = input.get();
        if (c == '\n') return line;
        if (c == std::char_traits<char>::eof()) break;
        line.push_back(static_cast<char>(c));
    }
    throw std::runtime_error("Invalid or oversized PPM header");
}
inline std::uint32_t dimension(const std::string &text) {
    if (text.empty() || text.size() > 5) throw std::runtime_error("Invalid dimension");
    std::uint32_t value = 0;
    for (const char c : text) {
        if (c < '0' || c > '9') throw std::runtime_error("Invalid dimension");
        value = value * 10 + static_cast<unsigned>(c - '0');
    }
    if (value == 0 || value > 10000) throw std::runtime_error("Dimension out of bounds");
    return value;
}
template<class Consumer>
RasterInfo read_ppm(std::istream &input, Consumer consume) {
    if (header_line(input) != "P6") throw std::runtime_error("Expected P6 LF header");
    const auto size = header_line(input);
    const auto space = size.find(' ');
    if (space == std::string::npos) throw std::runtime_error("Expected width height");
    const RasterInfo info{dimension(size.substr(0, space)), dimension(size.substr(space + 1))};
    if (header_line(input) != "255") throw std::runtime_error("Expected 8-bit RGB samples");
    const std::uint64_t total = std::uint64_t(info.width) * info.height * 3;
    if (total > 128ULL * 1024 * 1024) throw std::runtime_error("Raster exceeds 128 MiB limit");
    constexpr std::uint32_t band_rows = 128;
    const std::size_t stride = static_cast<std::size_t>(info.width) * 3;
    std::vector<unsigned char> band(stride * std::min(band_rows, info.height));
    for (std::uint32_t y = 0; y < info.height; y += band_rows) {
        const auto rows = std::min(band_rows, info.height - y);
        const auto bytes = stride * rows;
        input.read(reinterpret_cast<char *>(band.data()), static_cast<std::streamsize>(bytes));
        if (input.gcount() != static_cast<std::streamsize>(bytes) || input.bad())
            throw std::runtime_error("Truncated or unreadable raster");
        // Consumer must finish using these bytes before returning; buffer is reused.
        consume(info, y, rows, band.data(), bytes);
    }
    if (input.peek() != std::char_traits<char>::eof() || input.bad())
        throw std::runtime_error("Trailing image/data or input failure");
    return info;
}
} // namespace brother
