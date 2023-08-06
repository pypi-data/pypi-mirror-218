/* 
 * PDF Estimator:  A non-parametric probability density estimation tool based on maximum entropy
 * File:   OutputControl.cpp
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


#include "OutputControl.h"



OutputControl::OutputControl() {
    debug = false;
}

OutputControl::OutputControl(const OutputControl& orig) {
    debug = false;
}

OutputControl::~OutputControl() {
}


//#ifdef outputCommandLine

void OutputControl::print(string output) {
    if (debug) {
        cout << output << "\n";
    }
}

void OutputControl::print(string output, int value) {
    if (debug) {
        cout << output << ": " << value << "\n";
    }
}

void OutputControl::print(string output, double value) {
    if (debug) {
        cout << output << ": " << value << "\n";
    }
}

void OutputControl::error(string output) {
    cout << output << "\n";
}

void OutputControl::error(string output, int value) {
   cout << output << ": " << value << "\n";
}

void OutputControl::error(string output, double value) {
    cout << output << ": " << value << "\n";
}

//#endif
    
   