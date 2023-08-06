/* 
 * PDF Estimator:  A non-parametric probability density estimation tool based on maximum entropy
 * File:   InputParameters.cpp
 * Copyright (C) 2018
 * Jenny Farmer jfarmer6@uncc.edu
 * Donald Jacobs djacobs1@uncc.edu
 * 
 * This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published 
 * by the Free Software Foundation, either version 3 of the License, or (at your option) any later version. This program is distributed in 
 * the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR 
 * PURPOSE.  See the GNU General Public License for more details. You should have received a copy of the GNU General Public License along with 
 * this program.  If not, see <http://www.gnu.org/licenses/>.
 */

#include "InputParameters.h"

InputParameters::InputParameters() {  
    
    debug = false;
   
    inputPath = "";
    inputFile = ".txt";
    outputPath = "";
    writeFile = true;
    writeHeader = true;
    writeQQ = false;
    writeSQR = false;
    writeFailed = true;
    qqFile = "";
    sqrFile = "";
    adaptive = true;
    
    lowerBoundSpecified = false;
    upperBoundSpecified = false;
    
    scoreType = "QZ";
    SURDMinimum = 5;
    SURDTarget  = 70;
    SURDMaximum = 100;
    initPartitionSize = 1025;
    startSolutionNumber = 0;
    integrationPoints = -1;
    maxLagrange = 200;//2 for power
    minLagrange = 1;
    nLagrangeAdd = 5;
    outlierCutoff = 7.0;
    smooth = true;
    
    fractionLagrangeAdd = 0.1;
    initSigma = 0.1;
    finalSigma =0.001;
    decayFactor = sqrt(2.0);
    loopMax = 100;                  // updated from 30; September 2020
    
    estimatePoints = false;
    
 }

//InputParameters::InputParameters(const InputParameters& orig) {
//}

InputParameters::~InputParameters() {
}


void InputParameters::setEstimationPoints(vector<double> x) {
    estimatedPoints.resize(x.size());
    estimatedPoints =  x;
    estimatePoints = true;
}


void InputParameters::printUsage() {
    out.print("Usage:");
    out.print("getpdf -f <filename> [-option <argument>]");
    
    out.print("Options:");
    out.print(" -f    input filename (REQUIRED)");
    out.print(" -o    main output filename");
    out.print( " -w    write main output file [on/off]");
    out.print( " -h    include header info in main output file [on/off]");
    out.print( " -q    QQ filename");
    out.print( " -r    SQR filename");
    out.print( " -l    lower bound");
    out.print( " -u    upper bound");
    out.print( " -s    score threshold percentage [1-100]");
    out.print( " -p    minimum number of integration points");
    out.print( " -n    maximum number of Lagrange multipliers");
    out.print( " -m    minimum number of Lagrange multipliers");
    out.print( " -y    penalty flag [on/off]");
    out.print( " -g    debug [on/off]");
}

