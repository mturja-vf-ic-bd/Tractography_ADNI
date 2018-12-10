#include <string.h>
#include <string>
#include <iostream>
#include <map>
#include <iterator>

#include <vtkSmartPointer.h>
#include <vtkCellData.h>
#include <vtkMath.h>
#include <vtkIntArray.h>
#include <vtkStringArray.h>
#include <vtkPoints.h>
#include <vtkPolyData.h>
#include <vtkPointData.h>
#include <vtkFieldData.h>
#include <vtkSphereSource.h>
#include <vtkPolyDataReader.h>
#include <vtkPolyDataWriter.h>
#include <vtkDelimitedTextReader.h>
#include <vtkTable.h>
#include <vtkAppendPolyData.h>

int main(int argc, char *argv[])
{
    std::string inputFilenames[2] = {strdup(argv[1]), strdup(argv[2])}; //lh_white_matter.vtk, rh_white_matter.vtk
    std::string outputFilename = strdup(argv[3]); //combinedvtk
    int debug = std::stoi(strdup(argv[4]));
    std::string mapFiles[] = {"EditLabel/map_lh.txt", "EditLabel/map_rh.txt"}; //map files
    std::map<int, int> m;
    std::map<int, int> m_flag;
    vtkSmartPointer<vtkPolyData> polyData[2];

    
    for (int i = 0; i < 2; i++) {
        const char *mapFile = mapFiles[i].c_str();
        const char *inputFilename = inputFilenames[i].c_str();

        // Read file
        vtkSmartPointer<vtkPolyDataReader> polyIn = vtkSmartPointer<vtkPolyDataReader>::New();
        polyIn->SetFileName(inputFilename); 
        polyIn->Update();
        vtkSmartPointer<vtkPolyData> polydata = polyIn->GetOutput();
        unsigned int nPoints = polydata->GetNumberOfPoints();
        unsigned int numberOfArrays = polydata-> GetPointData()->GetNumberOfArrays();
        
        // Reading the label to AAL_ID map
        vtkSmartPointer<vtkDelimitedTextReader> reader =
        vtkSmartPointer<vtkDelimitedTextReader>::New();
        
        reader->SetFileName(mapFile);
        reader->DetectNumericColumnsOn();
        reader->SetFieldDelimiterCharacters(",");
        reader->Update();

        vtkTable* table = reader->GetOutput();
        for(vtkIdType i = 0; i < table->GetNumberOfRows(); i++) {
            int key = table->GetValue(i, 0).ToInt();
            int value = table->GetValue(i, 1).ToInt();
            m[key] = value;
            m_flag[key] = 0;
        }

        // Update label values with AAL_ID
        int count = 0;
        int id = 0;
        for (int i = 0; i < numberOfArrays; i++) {
            const char *label = polydata->GetPointData()->GetArrayName(i);
            vtkIntArray *data = vtkIntArray::SafeDownCast(polydata->GetPointData()->GetArray(label));
            if (debug) printf("Number of element in %s is %ld\n", label, data->GetDataSize());
            
            
            for (int j = 0; j < nPoints; j++) {
                int k = data->GetComponent(j, 0);
                int updateVal;
                m_flag[k] = 1;
                if(m.find(k) != m.end()) {
                    updateVal = m[k];
                    data->SetComponent(j, 0, updateVal);
                    count++;
                }
            }
        }
        
        polyData[i] = polydata; // Storing the polydata for later merging event

        if (debug) {
            cout << "Number of Arrays " << numberOfArrays << endl;
            cout << "Number of Points " << nPoints << endl;
            cout << "Number of match " << count << endl;
            cout << "Number of label in vtk " << m_flag.size() << endl;

            cout << "Missing : ";
            for (std::map<int, int>::iterator it = m_flag.begin(); it != m_flag.end(); ++it) {
                if (it -> second == 0) {
                    cout << it -> first << " ";
                }
            }

            cout << endl;
        }
    }
    
    // Merge two polydatas into one
    vtkSmartPointer<vtkAppendPolyData> appendFilter = vtkSmartPointer<vtkAppendPolyData>::New();
    appendFilter->AddInputData(polyData[0]);
    appendFilter->AddInputData(polyData[1]);
    appendFilter->Update();

    // Write the combined polydata into outputfile
    vtkSmartPointer<vtkPolyDataWriter> SurfaceWriter = vtkSmartPointer<vtkPolyDataWriter>::New();
    SurfaceWriter->SetInputData(appendFilter->GetOutput());
    SurfaceWriter->SetFileName(outputFilename.c_str());
    //SurfaceWriter->SetFileTypeToBinary();
    SurfaceWriter->Update();
    
    return EXIT_SUCCESS;
}