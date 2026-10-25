// SPDX-License-Identifier: Apache-2.0
// Test-only inspector for our synthetic fixtures; never a printer transport.
#include <cups/raster.h>
#include <algorithm>
#include <cstdint>
#include <cstring>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>
struct Memory { const unsigned char *p; size_t count; };
ssize_t read_memory(void *ctx,unsigned char *out,size_t count) {
    auto &m=*static_cast<Memory *>(ctx); const auto n=std::min(count,m.count);
    std::memcpy(out,m.p,n);m.p+=n;m.count-=n;return static_cast<ssize_t>(n);
}
int main(int argc,char **argv) {
    if(argc!=2)return 2;
    try {
        std::ifstream file(argv[1],std::ios::binary);
        if(!file)throw std::runtime_error("Missing file");
        file.seekg(0,std::ios::end);const auto length=file.tellg();
        if(length<0 || length>16*1024*1024)throw std::runtime_error("Test file size limit");
        file.seekg(0);std::string data(static_cast<size_t>(length),'\0');
        file.read(data.data(),length);if(!file)throw std::runtime_error("Read failure");
        const std::string begin="\x1b%-12345X@PJL \n", middle="@PJL ENTER LANGUAGE=PWGRASTER\n", end="\x1b%-12345X\x1b%-12345X";
        size_t pos=0;unsigned pages=0;std::cout<<"[";
        while(pos<data.size()) {
            if(data.compare(pos,begin.size(),begin))throw std::runtime_error("Bad framing");
            const auto start=data.find(middle,pos);if(start==std::string::npos)throw std::runtime_error("Missing PJL end");
            const auto payload=start+middle.size(), last=data.find(end,payload);
            if(last==std::string::npos)throw std::runtime_error("Missing trailer");
            Memory memory{reinterpret_cast<const unsigned char*>(data.data()+payload),last-payload};
            cups_raster_t *r=cupsRasterOpenIO(read_memory,&memory,CUPS_RASTER_READ);
            if(!r)throw std::runtime_error("No raster");
            cups_page_header2_t h{};
            if(!cupsRasterReadHeader2(r,&h) || h.cupsWidth>3000 || h.cupsHeight>4000 ||
               (h.cupsNumColors!=1 && h.cupsNumColors!=3) || h.cupsBytesPerLine!=h.cupsWidth*h.cupsNumColors) {
                cupsRasterClose(r);throw std::runtime_error("Bad raster header");
            }
            std::vector<unsigned char> row(h.cupsBytesPerLine);
            std::uint64_t hash=14695981039346656037ULL;bool chromatic=false,white_edge=true;
            for(unsigned y=0;y<h.cupsHeight;++y) {
                if(cupsRasterReadPixels(r,row.data(),h.cupsBytesPerLine)!=h.cupsBytesPerLine){cupsRasterClose(r);throw std::runtime_error("Truncated pixels");}
                for(unsigned char v:row){hash^=v;hash*=1099511628211ULL;}
                for(unsigned x=0;x<h.cupsWidth;++x) {
                    if(h.cupsNumColors==3 && (row[x*3]!=row[x*3+1] || row[x*3]!=row[x*3+2]))chromatic=true;
                    if(y==0 || y+1==h.cupsHeight || x==0 || x+1==h.cupsWidth)
                        for(unsigned c=0;c<h.cupsNumColors;++c) if(row[x*h.cupsNumColors+c]!=255)white_edge=false;
                }
            }
            cupsRasterClose(r);
            if(pages++)std::cout<<",";
            std::cout<<"{\"width\":"<<h.cupsWidth<<",\"height\":"<<h.cupsHeight<<",\"channels\":"<<h.cupsNumColors
                     <<",\"dpi\":"<<h.HWResolution[0]<<",\"fnv1a64\":"<<hash
                     <<",\"chromatic\":"<<(chromatic?"true":"false")<<",\"white_edge\":"<<(white_edge?"true":"false")<<"}";
            pos=last+end.size();
        }
        std::cout<<"]\n";return pages?0:2;
    }catch(const std::exception &e){std::cerr<<e.what()<<"\n";return 2;}
}
