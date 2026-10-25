// SPDX-License-Identifier: Apache-2.0
// Development fixture bridge only, not installed or used by the runtime.
#include "ppm_reader.hpp"
#include <cups/raster.h>
#include <fstream>
#include <cstring>
#include <iostream>
#include <stdexcept>
#include <unistd.h>
int main(int argc,char **argv) {
    if(argc!=3)return 2;
    cups_raster_t *out=nullptr;
    try {
        std::ifstream input(argv[1],std::ios::binary);
        if(!input)throw std::runtime_error("Cannot read fixture");
        const std::string media(argv[2]);
        if(media!="A4" && media!="Letter")throw std::runtime_error("Unsupported media");
        out=cupsRasterOpen(STDOUT_FILENO,CUPS_RASTER_WRITE);
        if(!out)throw std::runtime_error("Cannot open test raster");
        bool started=false;
        brother::read_ppm(input,[&](brother::RasterInfo info,std::uint32_t,std::uint32_t,const unsigned char *bytes,size_t count){
            if(!started){
                cups_page_header2_t h{};h.HWResolution[0]=h.HWResolution[1]=300;
                h.PageSize[0]=media=="A4"?595:612;h.PageSize[1]=media=="A4"?842:792;
                h.cupsWidth=info.width;h.cupsHeight=info.height;h.cupsBitsPerColor=8;
                h.cupsBitsPerPixel=24;h.cupsBytesPerLine=info.width*3;h.cupsNumColors=3;
                h.cupsColorOrder=CUPS_ORDER_CHUNKED;h.cupsColorSpace=CUPS_CSPACE_SRGB;
                if(!cupsRasterWriteHeader2(out,&h))throw std::runtime_error("Cannot write test header");started=true;
            }
            if(cupsRasterWritePixels(out,const_cast<unsigned char*>(bytes),static_cast<unsigned>(count))!=count)
                throw std::runtime_error("Cannot write test pixels");
        });
        cupsRasterClose(out);return 0;
    }catch(const std::exception &e){if(out)cupsRasterClose(out);std::cerr<<e.what()<<"\n";return 2;}
}
