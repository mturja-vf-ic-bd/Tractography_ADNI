#include <iostream>
#include <map>
#include <fstream>
#include "rapidjson/filereadstream.h"   // FileReadStream
#include "rapidjson/encodedstream.h"    // EncodedInputStream
#include "rapidjson/document.h"
#include "rapidjson/writer.h"
#include "rapidjson/stringbuffer.h"
#include <string>

struct label
{
    int labelNumber;
    std::string labelTextName;
};

std::map <std::string , label> ReadLabelTranslationTable ( std::string labelTranslationTable )
{

    // 1. Parse a JSON string into DOM.
    FILE* fp = fopen(labelTranslationTable.c_str(), "r"); // non-Windows use "r"
    char readBuffer[65536];
    //Output Map containing all info about labels
    std::map <std::string , label> labelTranslationMap ;
    std::string name ;
    int AAL_ID ;
    std::string labelValue ;

    if(fp == NULL)
    {
        std::cout << "Cannot open the json translation table file " << std::endl ;
        return labelTranslationMap;
    }
    rapidjson::FileReadStream is(fp, readBuffer, sizeof(readBuffer));
    rapidjson::Document document;
    document.ParseStream(is);
    fclose(fp);

    assert(document.IsArray());
    std::cout << "Size : " << document.Size() << std::endl;

    for (rapidjson::SizeType i = 0; i < document.Size(); i++)
    {
        assert(document[i].HasMember("name"));
        assert(document[i]["name"].IsString());

        assert(document[i].HasMember("AAL_ID"));
        assert(document[i]["AAL_ID"].IsInt());

        assert(document[i].HasMember("labelValue"));
        assert(document[i]["labelValue"].IsString());

        assert(document[i].HasMember("VisuHierarchy"));
        assert(document[i]["VisuHierarchy"].IsString());

        assert(document[i].HasMember("VisuOrder"));
        assert(document[i]["VisuOrder"].IsInt());

        assert(document[i].HasMember("MatrixRow"));
        assert(document[i]["MatrixRow"].IsInt());

        labelValue=document[i]["labelValue"].GetString();
        AAL_ID = document[i]["AAL_ID"].GetInt();
        name = document[i]["name"].GetString();

        labelTranslationMap[labelValue].labelNumber = AAL_ID ;
        labelTranslationMap[labelValue].labelTextName = name ;

      }

    return labelTranslationMap ;
}

int main() {
    std::map <std::string , label> labelTranslationMap = ReadLabelTranslationTable ( "/home/turja/Desktop/sub/S100790/parcellationTable.json" );
    //Read Map
    std::map <std::string , label>::const_iterator itS, endS ;
    for( itS = labelTranslationMap.begin() , endS = labelTranslationMap.end() ; itS != endS ; ++itS )
    {
        std::cout<< itS->first << " , " << itS->second.labelNumber << " , " << itS->second.labelTextName << std::endl ;
    }

    std::cout << "Size : " << labelTranslationMap.size() << std::endl;
    return 0;
}