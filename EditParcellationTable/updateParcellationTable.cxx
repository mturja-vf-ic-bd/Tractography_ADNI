#include <string.h>
#include <string>
#include <iostream>
#include <fstream>
#include <iterator>
#include <map>

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
    // Input
    // Verify input arguments
    if ( argc != 4 )
    {
        std::cout << "Usage: " << argv[0]
                  << " updateParcellationTable.cxx" << std::endl;
        return EXIT_FAILURE;
    }

    std::string surface = strdup(argv[1]);              // vtk file of the surface
    std::string target = strdup(argv[2]);
    std::string targetFile = target + strdup("/coord_map");
    int debug = std::stoi(strdup(argv[3]));

    // Read file
    vtkSmartPointer<vtkPolyDataReader> polyIn = vtkSmartPointer<vtkPolyDataReader>::New();
    polyIn->SetFileName(surface.c_str()); 
    polyIn->Update();
    vtkSmartPointer<vtkPolyData> polydata = polyIn->GetOutput();
    unsigned int nPoints = polydata->GetNumberOfPoints();
    unsigned int numberOfArrays = polydata->GetPointData()->GetNumberOfArrays();
    const char *label = polydata->GetPointData()->GetArrayName(0);
    vtkIntArray *data = vtkIntArray::SafeDownCast(polydata->GetPointData()->GetArray(label));
    if (debug) printf("Number of element in %s is %ld\n", label, data->GetDataSize());

    double x[3];
    std::map<int, double*> m;
    std::map<int, double*> :: iterator itr;
    
    for (vtkIdType id = 0; id < nPoints; id++) {
        polydata->GetPoint(id, x);
        int k = data->GetComponent(id, 0);

        if (m[k] == NULL) {
            double *t = new double[4];
            for (int j = 0; j < 3; j++){
                t[j] = x[j];
            }
            t[3] = 0;
            m[k] = t;
        } else {
            double *t = m[k];
            for (int j = 0; j < 3; j++){
                t[j] += x[j];
            }

            t[3]++;
        }
    }

    ofstream coord_map;
    coord_map.open(targetFile.c_str());
    double avg_left[3] = {0, 0, 0};
    double avg_right[3] = {0, 0, 0};
    int c_m = 0;
    for (itr = m.begin(); itr != m.end(); ++itr) {
        double *t = itr->second;
        for (int j = 0; j < 3; j++){
            t[j] /= t[3];
            if (c_m < m.size()/2) {
                avg_left[j] += t[j];
            } else {
                avg_right[j] += t[j];
            }
        }
        c_m++;
    }

    for (int j = 0; j < 3; j++) {
        avg_left[j] /= (m.size()/2);
        avg_right[j]/= (m.size()/2);
    }


    c_m = 0;

    for (itr = m.begin(); itr != m.end(); ++itr) {
        double *t = itr->second;

        coord_map << itr->first << " , ";
        for (int j = 0; j < 3; j++) {
            if (c_m < m.size()/2) {
                t[j] -= avg_left[j];
            } else {
                t[j] -= avg_right[j];
            }
            coord_map << t[j];
            if ( j < 2 ) coord_map << " ,  ";

            if (debug) {
                cout << t[j];
                if (j < 2) cout << " , ";
            }
        }

        coord_map << endl;
        if (debug) cout << endl;
        c_m++;
    }
    return EXIT_SUCCESS;
}