// SPDX-License-Identifier: Apache-2.0
#include "job_ticket.hpp"
#include <cups/cups.h>
#include <cups/raster.h>
#include <algorithm>
#include <cerrno>
#include <csignal>
#include <cmath>
#include <cstdio>
#include <cstring>
#include <fcntl.h>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <string>
#include <unistd.h>
#include <vector>
namespace {
volatile sig_atomic_t cancelled = 0;
void cancel(int) { cancelled = 1; }
void check_cancel() { if (cancelled) throw std::runtime_error("Job cancelled"); }
struct File {
    FILE *p = nullptr;
    explicit File(FILE *value) : p(value) {}
    ~File() { if (p) std::fclose(p); }
    File(const File &) = delete;
    File &operator=(const File &) = delete;
};
struct Raster {
    cups_raster_t *p;
    explicit Raster(cups_raster_t *value) : p(value) {
        if (!p) throw std::runtime_error("Cannot open raster stream");
    }
    ~Raster() { cupsRasterClose(p); }
    Raster(const Raster &) = delete;
    Raster &operator=(const Raster &) = delete;
};
ssize_t file_write(void *ctx, unsigned char *data, size_t bytes) {
    if (cancelled) return -1;
    const auto position = std::ftell(static_cast<FILE *>(ctx));
    if (position < 0 || bytes > 512ULL*1024*1024 || static_cast<unsigned long long>(position)+bytes > 512ULL*1024*1024) return -1;
    const size_t n = std::fwrite(data, 1, bytes, static_cast<FILE *>(ctx));
    return n == bytes ? static_cast<ssize_t>(n) : -1;
}
void text(FILE *file, const std::string &value) {
    const auto position = std::ftell(file);
    if (position < 0 || static_cast<unsigned long long>(position)+value.size() > 512ULL*1024*1024)
        throw std::runtime_error("Spool limit exceeded");
    if (std::fwrite(value.data(), 1, value.size(), file) != value.size())
        throw std::runtime_error("Cannot stage printer stream");
}
const char *option(int count, cups_option_t *options, const char *name) {
    return cupsGetOption(name, count, options);
}
brother::Quality quality(int count, cups_option_t *options, const cups_page_header2_t &h) {
    if (const char *v = option(count,options,"print-quality")) return brother::parse_quality(v);
    if (const char *v = option(count,options,"PrintQuality")) {
        if (!std::strcmp(v,"Draft")) return brother::Quality::Draft;
        if (!std::strcmp(v,"Normal")) return brother::Quality::Normal;
        if (!std::strcmp(v,"Fine")) return brother::Quality::Fine;
        throw std::invalid_argument("Unsupported PrintQuality");
    }
    const unsigned value = h.cupsInteger[CUPS_RASTER_PWG_PrintQuality];
    if (value == 0) return brother::Quality::Normal;
    return brother::parse_quality(std::to_string(value));
}
bool monochrome(int count, cups_option_t *options, const cups_page_header2_t &h) {
    if (const char *v = option(count,options,"print-color-mode"))
        return brother::parse_color(v) == brother::Color::Monochrome;
    if (const char *v = option(count,options,"ColorModel")) {
        if (!std::strcmp(v,"Gray")) return true;
        if (!std::strcmp(v,"RGB")) return false;
        throw std::invalid_argument("Unsupported ColorModel");
    }
    return h.cupsNumColors == 1;
}
struct Media { const char *name; unsigned width,height,points_x,points_y; };
Media media(const cups_page_header2_t &h) {
    // Physical sizes distinguish paper, independent of raster crop/margins.
    const double w = h.cupsPageSize[0] ? h.cupsPageSize[0] : h.PageSize[0];
    const double v = h.cupsPageSize[1] ? h.cupsPageSize[1] : h.PageSize[1];
    if (w >= 594 && w <= 596 && v >= 840 && v <= 843) return {"A4",2480,3507,595,842};
    if (w >= 611 && w <= 613 && v >= 791 && v <= 793) return {"LETTER",2550,3300,612,792};
    throw std::runtime_error("Unsupported page size; only portrait A4/Letter raster geometry accepted");
}
void encode_page(cups_raster_t *input, const cups_page_header2_t &h,
                 int count, cups_option_t *options, FILE *output) {
    check_cancel();
    const auto m = media(h);
    const bool gray = monochrome(count,options,h);
    const auto q = quality(count,options,h);
    if (h.HWResolution[0] != 300 || h.HWResolution[1] != 300 || h.cupsBitsPerColor != 8 ||
        h.cupsColorOrder != CUPS_ORDER_CHUNKED ||
        !((h.cupsNumColors == 3 && h.cupsBitsPerPixel == 24 && h.cupsColorSpace == CUPS_CSPACE_SRGB) ||
          (h.cupsNumColors == 1 && h.cupsBitsPerPixel == 8 && h.cupsColorSpace == CUPS_CSPACE_SW)))
        throw std::runtime_error("Expected 300 dpi 8-bit chunked sRGB/sGray raster");
    // macOS renders the imageable rectangle only. Restore its position on a
    // full white page from floating-point image bounds, without rescaling.
    const double page_height = h.cupsPageSize[1] ? h.cupsPageSize[1] : h.PageSize[1];
    const bool full = h.cupsWidth == m.width && h.cupsHeight >= m.height && h.cupsHeight <= m.height+1;
    const double left_points = full ? 0.0 : h.cupsImagingBBox[0];
    const double top_points = full ? 0.0 : page_height - h.cupsImagingBBox[3];
    if (!std::isfinite(left_points) || !std::isfinite(top_points) || left_points < 0 || top_points < 0 ||
        left_points > 72 || top_points > 72)
        throw std::runtime_error("Invalid raster image bounds");
    const unsigned left = static_cast<unsigned>(std::lround(left_points*300/72));
    const unsigned top = static_cast<unsigned>(std::lround(top_points*300/72));
    if (!h.cupsWidth || !h.cupsHeight || h.cupsWidth > m.width || h.cupsHeight > m.height+1 ||
        left+h.cupsWidth > m.width || top+h.cupsHeight > m.height+1 ||
        h.cupsBytesPerLine != h.cupsWidth * h.cupsNumColors ||
        (!full && (!h.cupsImagingBBox[2] || !h.cupsImagingBBox[3])))
        throw std::runtime_error("Unexpected raster geometry; refusing to stretch content");
    const char *qname = q == brother::Quality::Draft ? "DRAFT" : q == brother::Quality::Fine ? "HIGH" : "NORMAL";
    text(output, std::string("\x1b%-12345X@PJL \n@PJL SET PAPER=") + m.name +
        "\n@PJL SET BORDERLESS=OFF\n@PJL SET JTTOPMARGIN=300\n@PJL SET JTBOTMARGIN=300\n"
        "@PJL SET JTLEFTMARGIN=300\n@PJL SET JTRIGHTMARGIN=300\n@PJL SET RENDERMODE=" +
        (gray ? "GRAYSCALE" : "COLOR") + "\n@PJL SET PRINTQUALITY=" + qname +
        "\n@PJL SET DUPLEX=OFF\n@PJL SET MEDIATYPE=REGULAR\n@PJL SET SOURCETRAY=AUTO\n"
        "@PJL SET FIDELITY=TRUE\n@PJL ENTER LANGUAGE=PWGRASTER\n");
    {
        Raster target(cupsRasterOpenIO(file_write, output, CUPS_RASTER_WRITE_PWG));
        cups_page_header2_t out{};
        std::strcpy(out.MediaClass,"PwgRaster");
        std::strcpy(out.MediaType,"auto");
        out.HWResolution[0] = out.HWResolution[1] = 300;
        out.PageSize[0] = m.points_x; out.PageSize[1] = m.points_y;
        out.cupsWidth = m.width; out.cupsHeight = m.height;
        out.cupsBitsPerColor = 8; out.cupsNumColors = gray ? 1 : 3;
        out.cupsBitsPerPixel = out.cupsNumColors * 8;
        out.cupsBytesPerLine = m.width * out.cupsNumColors;
        out.cupsColorOrder = CUPS_ORDER_CHUNKED;
        out.cupsColorSpace = gray ? CUPS_CSPACE_SW : CUPS_CSPACE_SRGB;
        if (!cupsRasterWriteHeader2(target.p,&out)) throw std::runtime_error("Cannot encode PWG header");
        std::vector<unsigned char> row(h.cupsBytesPerLine), result(out.cupsBytesPerLine,255);
        unsigned read_rows = 0;
        for (unsigned y = 0; y < m.height; ++y) {
            check_cancel();
            std::fill(result.begin(),result.end(),255);
            if (y >= top && y-top < h.cupsHeight) {
                if (cupsRasterReadPixels(input,row.data(),h.cupsBytesPerLine) != h.cupsBytesPerLine)
                    throw std::runtime_error("Truncated raster page");
                ++read_rows;
                if (h.cupsNumColors == out.cupsNumColors)
                    std::copy(row.begin(),row.end(),result.begin()+left*out.cupsNumColors);
                else for (unsigned x = 0; x < h.cupsWidth; ++x) {
                    if (gray) result[left+x] = static_cast<unsigned char>((30U*row[3*x]+59U*row[3*x+1]+11U*row[3*x+2])/100U);
                    else result[3*(left+x)] = result[3*(left+x)+1] = result[3*(left+x)+2] = row[x];
                }
            }
            if (cupsRasterWritePixels(target.p,result.data(),out.cupsBytesPerLine) != out.cupsBytesPerLine)
                throw std::runtime_error("Cannot encode PWG row");
        }
        // Only the at-most-one rounding row below the paper edge may be discarded.
        while (read_rows < h.cupsHeight) {
            check_cancel();
            if (cupsRasterReadPixels(input,row.data(),h.cupsBytesPerLine) != h.cupsBytesPerLine)
                throw std::runtime_error("Truncated final raster row");
            ++read_rows;
        }
    }
    text(output,"\x1b%-12345X\x1b%-12345X");
}
}
int main(int argc,char **argv) {
    if (argc != 6 && argc != 7) { std::cerr << "ERROR: Expected CUPS filter arguments\n"; return 1; }
    std::signal(SIGTERM,cancel); std::signal(SIGINT,cancel); std::signal(SIGPIPE,SIG_IGN);
    cups_option_t *options = nullptr;
    const int count = cupsParseOptions(argv[5],0,&options);
    int fd = -1;
    try {
        const std::string copies_text(argv[4]);
        if (copies_text.empty() || copies_text.size() > 2 ||
            copies_text.find_first_not_of("0123456789") != std::string::npos)
            throw std::runtime_error("Invalid copy count");
        const unsigned copies = static_cast<unsigned>(std::stoul(copies_text));
        if (!copies || copies > 99) throw std::runtime_error("Copy count must be 1 to 99");
        if (const char *sides = option(count,options,"sides"))
            if (std::strcmp(sides,"one-sided")) throw std::runtime_error("Duplex is unsupported");
        for (const char *name : {"PageSize", "PageRegion", "media"}) {
            if (const char *value = option(count,options,name)) {
                const std::string v(value);
                if (v != "A4" && v != "Letter" && v != "iso_a4_210x297mm" && v != "na_letter_8.5x11in")
                    throw std::runtime_error("Unsupported media selection");
            }
        }
        // Validate explicit selections even when the input contains no valid page.
        if (const char *v = option(count,options,"print-color-mode")) (void)brother::parse_color(v);
        if (const char *v = option(count,options,"print-quality")) (void)brother::parse_quality(v);
        fd = argc == 7 ? open(argv[6],O_RDONLY | O_CLOEXEC) : dup(STDIN_FILENO);
        if (fd < 0) throw std::runtime_error("Cannot open input raster");
        File staged(std::tmpfile());
        if (!staged.p) throw std::runtime_error("Cannot create private temporary stream");
        Raster input(cupsRasterOpen(fd,CUPS_RASTER_READ));
        cups_page_header2_t h{};
        unsigned pages = 0;
        while (cupsRasterReadHeader2(input.p,&h)) {
            if (++pages > 1000) throw std::runtime_error("Page limit exceeded");
            encode_page(input.p,h,count,options,staged.p);
            if (std::ftell(staged.p) > 512L*1024*1024) throw std::runtime_error("Spool limit exceeded");
        }
        if (!pages || (cupsRasterErrorString() && *cupsRasterErrorString()))
            throw std::runtime_error("Invalid or incomplete raster job");
        if (std::fflush(staged.p)) throw std::runtime_error("Cannot flush staged stream");
        const auto staged_size = std::ftell(staged.p);
        if (staged_size < 0 || static_cast<unsigned long long>(staged_size)*copies > 512ULL*1024*1024)
            throw std::runtime_error("Copies exceed job byte limit");
        // Commit to backend only after all pages validate. A transport failure
        // during this final copy is uncertain; configure the queue to abort,
        // never automatically retry a possibly partially transmitted job.
        unsigned char buffer[65536];
        for (unsigned copy = 0; copy < copies; ++copy) {
            if (std::fseek(staged.p,0,SEEK_SET)) throw std::runtime_error("Cannot rewind staged stream");
            size_t n;
            while ((n = std::fread(buffer,1,sizeof(buffer),staged.p))) {
                check_cancel();
                if (std::fwrite(buffer,1,n,stdout) != n) throw std::runtime_error("Backend write failed");
            }
            if (std::ferror(staged.p)) throw std::runtime_error("Cannot read staged stream");
        }
        if (std::fflush(stdout)) throw std::runtime_error("Backend write failed");
        std::cerr << "INFO: Native raster conversion complete; physical completion unverified\n";
        cupsFreeOptions(count,options); close(fd); return 0;
    } catch (const std::exception &error) {
        std::cerr << "ERROR: " << error.what() << "\n";
        cupsFreeOptions(count,options); if (fd >= 0) close(fd); return 1;
    }
}
