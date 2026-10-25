// SPDX-License-Identifier: Apache-2.0
#pragma once
#include <stdexcept>
#include <string_view>
namespace brother {
enum class Media { A4, Letter };
enum class Color { Color, Monochrome };
enum class Quality { Draft = 3, Normal = 4, Fine = 5 };
struct JobTicket {
    Media media = Media::A4;
    Color color = Color::Color;
    Quality quality = Quality::Normal;
};
inline Media parse_media(std::string_view value) {
    if (value == "iso_a4_210x297mm") return Media::A4;
    if (value == "na_letter_8.5x11in") return Media::Letter;
    throw std::invalid_argument("Unsupported media");
}
inline Color parse_color(std::string_view value) {
    if (value == "color") return Color::Color;
    if (value == "monochrome") return Color::Monochrome;
    throw std::invalid_argument("Unsupported print-color-mode");
}
inline Quality parse_quality(std::string_view value) {
    if (value == "3" || value == "draft") return Quality::Draft;
    if (value == "4" || value == "normal") return Quality::Normal;
    if (value == "5" || value == "high") return Quality::Fine;
    throw std::invalid_argument("Unsupported print-quality");
}
} // namespace brother
