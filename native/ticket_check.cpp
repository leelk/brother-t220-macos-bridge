// SPDX-License-Identifier: Apache-2.0
#include "job_ticket.hpp"
#include <iostream>
#include <set>
#include <string>
int main(int argc, char **argv) {
    brother::JobTicket ticket;
    std::set<std::string_view> seen;
    try {
        for (int i = 1; i < argc; i += 2) {
            const std::string_view option(argv[i]);
            if (i + 1 >= argc) throw std::invalid_argument("Missing option value");
            if (!seen.insert(option).second) throw std::invalid_argument("Duplicate option");
            const std::string_view value(argv[i + 1]);
            if (option == "--media") ticket.media = brother::parse_media(value);
            else if (option == "--color-mode") ticket.color = brother::parse_color(value);
            else if (option == "--quality") ticket.quality = brother::parse_quality(value);
            else throw std::invalid_argument("Unknown option");
        }
        std::cout << "{\"media\":\""
                  << (ticket.media == brother::Media::A4 ? "iso_a4_210x297mm" : "na_letter_8.5x11in")
                  << "\",\"color_mode\":\""
                  << (ticket.color == brother::Color::Color ? "color" : "monochrome")
                  << "\",\"print_quality\":" << static_cast<int>(ticket.quality)
                  << ",\"device_quality\":\""
                  << (ticket.quality == brother::Quality::Draft ? "Draft" :
                      ticket.quality == brother::Quality::Normal ? "Normal" : "Fine")
                  << "\"}\n";
        return 0;
    } catch (const std::invalid_argument &error) {
        std::cerr << "Error: " << error.what() << "\n";
        return 2;
    }
}
